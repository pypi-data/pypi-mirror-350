########################################################################
## Draw With yyyyy (or yyyyy Drawings, or Drawing With yyyyy)
## (C) 2021 by Yulia Voevodskaya (draw.with.zyxxy@outlook.com)
## 
##  This program is free software: you can redistribute it and/or modify
##  it under the terms of the GNU General Public License as published by
##  the Free Software Foundation, either version 3 of the License, or
##  (at your option) any later version.
##  See <https://www.gnu.org/licenses/> for the specifics.
##  
##  This program is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##  GNU General Public License for more details.
########################################################################

class ObjPosition:

  pos_dic = {'left': 'xmin', 'right': 'xmax', 'bottom': 'ymin', 'top': 'ymax'}
  
  def __init__(self, name):
    self.name = name
    if name in ObjPosition.pos_dic:
      self.box_name = ObjPosition.pos_dic[name]
    elif name in ['center_x', 'center_y']:
      self.box_name = '_'
    else:
      raise Exception(f'{name} is not recognised')

  def __get__(self, instance, owner=None):
    if instance is None:
      return None # needed for the docs
    if self.name == 'center_x':
      return (instance.left + instance.right) / 2.
    if self.name == 'center_y':
      return (instance.bottom + instance.top) / 2.
    if self.box_name in ObjPosition.pos_dic.values():
      result = getattr(instance.get_bbox(), self.box_name)   
    return result

  def __set__(self, instance, val):
    move_by = val - getattr(instance, self.name)
    if self.box_name[0] == 'x' or self.name == 'center_x':
      instance.shift([move_by, 0])
    else:
      instance.shift([0, move_by])
