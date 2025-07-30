# rmind.yandex.smart.home

Библиотека для упрощения реализации умного дома с Алисой в Yandex Cloud Function.

### Необходимая облачная инфраструктура
#### Managed Service for YDB
хранение состояния устройств

| Переменные окружения | Значение | По умолчанию | Обязательный |
|----------------------|----------|--------------|--------------|
| YDB_ENDPOINT | grpcs | grpcs://ydb.serverless.yandexcloud.net:2135 | Нет |
| YDB_DATABASE | адресс БД  |- | Да |

#### IoT Core/Брокер
общение с устройствами пользователя через MQTT протокол

| Переменные окружения | Значение      | По умолчанию          | Обязательный |
|----------------------|---------------|-----------------------|--------------|
| MQTT_URL             | адрес брокера | mqtt.cloud.yandex.net | Нет          |
| MQTT_PORT            | порт брокера  | 8883                  | Нет          |
| MQTT_USER            | пользователь  | -                     | Да           |
| MQTT_PASS            | пароль        | -                     | Да           |


### Пример устройства 

```python
from rmind_yandex_smart_home import YandexIoTDevice
from rmind_yandex_smart_home.yandex import on_off

class MyDevice(YandexIoTDevice):
  def __init__(self, id, type):
    super().__init__(id, "MyDeviceName", type) 


  @on_off()
  def on_off(self, params):    
    value = params['value']    
    return 'on:1' if value else 'on:0'
```

Метод класса, помеченный атрибутом Capability (в данном случае @on_off), 
должен вернуть текст сообщения устройству, которое Engine отправит в MQTT очередь
```py 
f"/yandex-iot-core/{self.id}/commands"
```
Дальнейшая обработка сообщения проходит на IoT устройстве.

Так как IoT устройства обычно строятся на микроконтроллерах типа Arduino, esp32 и т.д., рекомендуется сложные преобразования делать в cloud function

```python
# обработка rgb сообщения от yandex alice
# значение приходит в формате int
# для значения value:14210514 получим '216;213;210;'

def get_rgb_message(value):
  h = hex(value)[2:]
  if len(h) == 5:
    h = '0' + h

  r,g,b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
  return f"{r};{g};{b}"
```


### Использование в **Cloud Function**

```python
import rmind_yandex_smart_home as rmind

engine = rmind.Engine()
engine.register_device(MyDevice(
  "my-device-unique-id",
  "devices.types.light"
))

def handler(event, context):
  return engine.handle(event, context)
```

## Входящие параметры **Capability** 

### on_off
Включение и выключение устройства

**объявление**
```python
@on_off()
def on_off(self, params):
  pass
```

**params**
 ```python
{
  "instance": "on",
  "value": False
}
``` 

### color_setting

Параметры цвета.В текущей реализации по умолчанию схема RGB. Параметры `temperature_k` и `scenes` необязательные.

**объявление**
```python
@color_setting(temperature_k = [2700, 5100], scenes = ["party"])
def color_setting(self, params):
  pass
```

возможные варианты **params**
```python
// цвет RGB
{
  "instance": "rgb",
  "value": 14210514
}

// цветовая температура
{
  "instance": "temperature_k",
  "value": 5100
}

// Сцена
{
  "instance": "scene",
  "value": "party"
}
```

### brightness
Яркость. Значение от 0 до 100

**объявление**
```python
@brightness()
def brightness(self, params):
  pass
```

**params**
 ```python
{
  "instance": "brightness",
  "value": 50
}
``` 

## Собственная реализация **Capability** 
В следующих версиях я буду добавлять умения, но если Вам необходима что то конкретное, то в библиотеке можно реализовать свои кастомные умения. 

Описание параметров и возможностей, с которыми работает алиса брать в 
[документации Yandex](https://yandex.ru/dev/dialogs/smart-home/doc/ru/concepts/capability-types)

### Пример реализации program
[список режимов](https://yandex.ru/dev/dialogs/smart-home/doc/ru/concepts/mode-instance-modes)
```python
from rmind_yandex_smart_home.yandex import Capability

class program(Capability):
  def __init__(self, **kwargs):
    super().__init__("devices.capabilities.mode", **kwargs)

    self.parameters = {
      'instance': "program"
    }

    modes = kwargs.get('modes')
    if modes is not None:
      self.parameters['modes'] = [{'value': x} for x in modes]

  def get_default(self):
    return  {
      'instance': "program",
      'value': "auto"
    }
```

### Пример использования

```python
from rmind_yandex_smart_home import YandexIoTDevice
...

class MyDevice(YandexIoTDevice):
  def __init__(self, id, type):
    super().__init__(id, "MyDeviceName", type) 

  @program(modes=["auto", "one", "two"])
  def program(self, params):    
    value = params['value']
    return '1' if value == "auto" else '0'
```