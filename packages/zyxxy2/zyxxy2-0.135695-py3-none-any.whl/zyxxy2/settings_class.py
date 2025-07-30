import settings

print(getattr(settings, 'my_color_palette'))

########################################################################################
class ShapeFormAttribute:
  
  def __init__(self, name):
    self.name = name

  def __get__(self, instance, owner=None):
    if instance is None:
      return None # needed for the docs
    if self.name in instance.shape_kwargs:
      return instance.shape_kwargs[self.name]
    raise Exception(f'Could not find {self.name}. Available keys: {", ".join(instance.shape_kwargs.keys())}')

  def __set__(self, instance, val):
    if self.name in instance.shape_kwargs:
      instance.shape_kwargs[self.name] = val
      instance.set_shape_parameters(**{self.name : val})
    else:
      raise Exception(f'Could not find {self.name}. Available keys: {", ".join(instance.shape_kwargs.keys())}')


########################################################################################
class OneTypeOfSettings_OneValue:
  
  def __init__(self, name):
    self.name = name

  def __get__(self, instance, owner=None):
    if instance is None:
      return None # needed for the docs
    if self.name in instance.settings_dict:
      return instance.settings_dict[self.name]
    raise Exception(f'Could not find {self.name}. Available keys: {", ".join(instance.settings_dict.keys())}')

  def __set__(self, instance, val):
    if self.name in instance.settings_dict:
      instance.settings_dict[self.name] = val
    else:
      raise Exception(f'Could not find {self.name}. Available keys: {", ".join(instance.settings_dict.keys())}')

########################################################################################
class OneTypeOfSettings:
  
  def __init__(self, name):
    self.name = name

  def __get__(self, instance, owner=None):
    if instance is None:
      return None # needed for the docs
    if self.name in instance.settings_dict:
      return instance.settings_dict[self.name]
    raise Exception(f'Could not find {self.name}. Available keys: {", ".join(instance.settings_dict.keys())}')
  
########################################################################################
class Settings:
  for s in ['screen_zoom']:
    locals()[s] = OneTypeOfSettings(name=s)

  def __init__(self):
    pass


settings = Settings()
