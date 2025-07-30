class attribute:
  attributes_member_name = "__attributes__"
  def __init__(self):
    self.func = None
  
  def __call__(self, func):
    self.func = func

    if (func.__dict__.__contains__(attribute.attributes_member_name)):
      func.__dict__[attribute.attributes_member_name].append(self)
    else:
      func.__setattr__(attribute.attributes_member_name, [self])

    return func

"""
Базовый класс для всех возможностей устройства
"""
class Capability(attribute): 
  def __init__(self, type, **kwargs):
    super().__init__()
    self.type = type
    self.retrievable = True
    self.reportable = False
    self.parameters = { 'split': False }

  def get_type(self):
    return self.type

  def execute(self, device, state):
    return self.func(device, state)  
  
  def get_capability_name(self):
    return "__" + self.type.replace(".", "_")

  def get_default(self):
    return  {
      'instance': "on",
      'value': False
    }
  

"""Включение/выключение устройства"""
class on_off(Capability):
  def __init__(self, **kwargs):
    super().__init__("devices.capabilities.on_off", **kwargs) 

# color
class color_setting(Capability):
  def __init__(self, **kwargs):
    super().__init__("devices.capabilities.color_setting", **kwargs)

    self.parameters = {
      'color_model': "rgb"
    }

    temperature_k = kwargs.get('temperature_k')
    if temperature_k is not None:
      self.parameters['temperature_k'] = {
        'min': temperature_k[0],
        'max': temperature_k[1]
      } 

    scenes = kwargs.get('scenes')
    if scenes is not None:
      self.parameters['color_scene'] = {
        'scenes': [{'id': x} for x in scenes]
      } 

  def get_default(self):
    return  {
      'instance': "rgb",
      'value': 14210514
    } 


class brightness(Capability):
  def __init__(self, **kwargs):
    super().__init__("devices.capabilities.range", **kwargs)

    self.parameters = {
      'instance': "brightness",
      'unit': "unit.percent",
      'range': {
        'min': 0,
        'max': 100
      }
    }

  def get_default(self):
    return {
      'instance': "brightness",
      'value': 100
    }

class mode(Capability):
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