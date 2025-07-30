from .yandex.mqtt import MQTTClient
from .yandex.device import YandexIoTDevice
from .yandex.database import YandexDB
from .yandex.tools import YandexIoTDeviceSerializer
from .yandex.iam import get_user_id

"""
Этот модуль реализует класс Engine для обработки событий устройств Yandex IoT.
Он управляет регистрацией устройств, обработкой событий и выполнением возможностей.
"""
class Engine:
  def __init__(self):
    self.__devices = dict() 

    self.__yandex_db = YandexDB()
    self.__mqtt_client = MQTTClient()
    
    self.__mqtt_client.connect()
    self.__mqtt_client.publish('/yandex-iot-core/engine/logs', "engine-created")   

  """
  Метод handle обрабатывает события от Yandex Alice.
  """
  def handle(self, event, context):
    request_type = event.get('request_type', None)
    if request_type is None:
      print('request_type cannot be None')
      return {'statusCode': 400, 'body': 'request_type cannot be None'}    

    match request_type:
      case "discovery":
        return self.__handle_discovery(event, context)
      case "action":
        return self.__handle_action(event, context)
      case "query":
        return self.__handle_query(event, context)
      case _:
        print(f'Unknown request type: {request_type}')
        return {'statusCode': 400, 'body': f'Unknown request type: {request_type}'}
      
  """
  Регистрация устройства в системе.
  Если устройство уже зарегистрировано, оно не будет добавлено повторно.
  """
  def register_device(self, device: YandexIoTDevice):
    if device.id in self.__devices:
      print(f'Device {device.id} already registered')
      return False

    self.__devices[device.id] = device
    return True
      
  """
  Discovery - обработка события обнаружения устройств.
  Этот метод вызывается, когда Yandex Alice запрашивает список доступных пользователю устройств. 
  """
  def __handle_discovery(self, event, context):
    devices = list()
    for device_id in self.__devices:
      devices.append(YandexIoTDeviceSerializer.serialize(self.__devices[device_id]))

    print(devices)

    return {
      'request_id': self.__get_request_id(event),
      'payload': {
        'user_id': "f475df023c0e408d8cc84bc79be90017",
        'devices': devices
      }
    } 
    

  """
  Action - обработка события действия устройства.
  Этот метод вызывается, когда Yandex Alice запрашивает выполнение действия на устройстве.
  Например, включение или выключение устройства.
  """  
  def __handle_action(self, event, context):
    user_id = get_user_id(event)    
    devices = list()
    for event_device in self.__get_payload_devices(event):
      if event_device['id'] in self.__devices:
        print(event_device)

        device = self.__devices[event_device['id']]
        
        capabilities = list()        
        for event_capability in self.__get_payload_devices_capabilities(event_device):
          capability = YandexIoTDeviceSerializer.get_capability(device, event_capability['type']) 
          state = event_capability['state']

          success, result = self.__execute_capability(device, capability, state)     
          if success:
            capability_key = self.__get_capability_key(device, capability) 
            # Сохраняем состояние в YandexDB

            print("save state", user_id, capability_key, device.id, state)
            print("user_id type:", type(user_id))
            self.__yandex_db.set_capability_state(
              int(user_id), 
              capability_key,
              device.id,
              state
            )

          capabilities.append(result)

        devices.append({
          'id': device.id,
          'capabilities': capabilities
        })
        
    return {                
      'request_id': self.__get_request_id(event),
      'payload': {
        'devices': devices
      }
    }
  

  """
  Query - обработка события запроса состояния устройства.
  Этот метод вызывается, когда Yandex Alice запрашивает текущее состояние устройства.
  Например, узнать, включено ли устройство или нет.
  """
  def __handle_query(self, event, context):
    devices = list()
    for event_device in self.__get_payload_devices(event):
      if event_device['id'] in self.__devices:
        device = self.__devices[event_device['id']]
        capabilities = self.__get_devices_state(device)
        devices.append({
          'id': device.id,
          'capabilities': capabilities
        })   
        
    return {                
      'request_id': self.__get_request_id(event),
      'payload': {
        'devices': devices
      }
    }
    

  """
  Получение идентификатора запроса из события.
  """
  def __get_request_id(self, event):
    return event['headers']['request_id']
  
  """
  Получение списка устройств из события.
  """
  def __get_payload_devices(self, event):
    return event['payload']['devices']

  """
  Получение списка действий устройств из события.
  """
  def __get_payload_devices_capabilities(self, event_device):
    return event_device['capabilities']
  

  """
  Получение состояния устройств.
  """  
  def __get_devices_state(self, device):
    return list(
      map(
        lambda x: {
          'type': x.type, 
          'state': self.__load_state(device, x)
        }, 
        YandexIoTDeviceSerializer.get_capabilities(device)
      ))

  """
  Получение состояния устройства из YandexDB.
  Если состояние не найдено, возвращается значение по умолчанию для данной возможности.
  """  
  def __load_state(self, user_id, device, capability):
    capability_key = self.__get_capability_key(device, capability)
    result = self.__yandex_db.get_capability_state(user_id, capability_key)
    return result if result is not None else capability.get_default()


  """
  Выполнение действия устройства.
  Этот метод вызывается, когда Yandex Alice запрашивает выполнение действия на устройстве.
  """
  def __execute_capability(self, device, capability, state):
    message = capability.execute(device, state)
    success = self.__mqtt_client.publish(device.get_topic(), message)

    return success,  {
      'type': capability.get_type(),
      'state': {
        'instance': state['instance'],
        'action_result': {
          'status': "DONE" if success else "ERROR"
        }
      }
    }
  

  """
  Генерация ключа для возможности устройства.
  Этот ключ используется для идентификации состояния возможности в базе данных.
  """
  def __get_capability_key(self, device, capability):
    return f"cp_{device.id}_{capability.get_capability_name()}"
  
