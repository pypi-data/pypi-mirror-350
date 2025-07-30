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

import numpy as np
from matplotlib.transforms import Bbox
import matplotlib as mpl

mpl.rcParams['svg.fonttype'] = 'none'    # keep text as <text>
mpl.rcParams['font.family']    = 'monospace'
mpl.rcParams['font.monospace'] = ['Courier',
                                  'Courier New',
                                  'monospace']   # last resort

from .shape_style import get_default_text_bubble_params
from .utils import calc_angle, calc_Pythagoras
from .shape_functions import draw_a_triangle
from .colors import find_color_code
from .bbox import ObjPosition
from .shape_class import _get_axes, get_ca, get_linewidth_factor, _get_renderer

##################################################################
## TEXT                                                         ## 
##################################################################

class WordBubble:

  for s in ['left', 'right', 'bottom', 'top', 'center_x', 'center_y']:
    locals()[s] = ObjPosition(name=s)

  text_boxes = []
  all_objects = []

  ################################################################# 
  def get_all():
    return WordBubble.text_boxes

  ########################################################################
  def get_all_in_layers(layer_nbs=[], ax=None):
    ax = _get_axes(ax=ax)
    _tbs_in_layers = [as_ for as_ in WordBubble.all_objects if as_.get_axes() == ax]
    if len(layer_nbs) != 0:
      _tbs_in_layers = [sh for sh in _tbs_in_layers if sh.get_layer_nb() in layer_nbs]
    return _tbs_in_layers

  ################################################################# 
  def _create_params_subdictionary(param_names_dictionary, kwargs):
    result = {}
    used_argnames = []
    for dict_entry in param_names_dictionary:
      if isinstance(dict_entry, str):
        result[dict_entry] = kwargs[dict_entry] if dict_entry in kwargs else get_default_text_bubble_params(dict_entry)
        if dict_entry in kwargs:
          used_argnames += [dict_entry]
      else:
        result[dict_entry[0]] = kwargs[dict_entry[1]] if dict_entry[1] in kwargs else get_default_text_bubble_params(dict_entry[1])
        if dict_entry[1] in kwargs:
          used_argnames += [dict_entry[1]]
    return result, used_argnames

  ################################################################## 
  def __init__(self, text, x, y, ax=None, start=None, connection=None, **kwargs):

    WordBubble.all_objects.append(self)

    ax = _get_axes(ax=ax)
    self.position = 'lb'
    props, used_argnames = WordBubble._create_params_subdictionary([['facecolor', 'background_color'],                                                                
    ['alpha', 'opacity'], 'pad', # 'rounding_size', 
    ['edgecolor', 'linecolor'], 'linewidth', ['zorder', 'layer_nb']], kwargs)
    props['boxstyle'] = 'round'
    if 'opacity' in props:
      opacity = props['opacity']
      props['opacity'] = 1.
    else:
      opacity = None
    
    text_dict, used_argnames2 = WordBubble._create_params_subdictionary(['fontsize', 
    'verticalalignment', 'horizontalalignment', 'multialignment', 
    'wrap', ['zorder', 'layer_nb'], 'clip_on',
    'fontfamily', 'fontstyle', 'fontvariant', 'fontweight', 'color'], kwargs)
    used_argnames += used_argnames2

    _triangle = draw_a_triangle(tip=[0, 0], height=0, width=0, turn=0, color=props['facecolor'], 
                                outline_linewidth=props['linewidth']*get_linewidth_factor(), 
                                outline_color=props['edgecolor'],
                                layer_nb=props['zorder']+1/4, outline_layer_nb=props['zorder'])
    
    _triangle.set_visible(False)

    for dict_ in [props, text_dict]:
      for k in dict_.keys():
        if 'color' in k:
          dict_[k] = find_color_code(dict_[k])

    # place a text box in upper left in axes coords
    self.text_boxes = [ax.text(s=text, x=x, y=y, transform=ax.transData, **text_dict, bbox=props)]

    props['zorder'] += 1/2
    text_dict['zorder'] += 1/2
    props['edgecolor'] = 'none'
    #props['facecolor'] = 'none'

    self.text_boxes.append(ax.text(s=text, x=x, y=y, transform=ax.transData, **text_dict, bbox=props))
    WordBubble.text_boxes += self.text_boxes

    if start is not None:
      connection = 'triangle'
    self.connection = connection
    self.start = np.array(start)
    if start is None:
      self.connector = None
    else:
      assert connection in ['bubble', 'triangle']
      if  self.connection == 'triangle':
        self.connector = _triangle
        self.connector.shift_to(start)
        self.connector.width = kwargs['triangle_width'] if 'triangle_width' in kwargs else get_default_text_bubble_params('triangle_width')
        self.connector.set_visible(True)
      else:
        raise Exception("not implemented")
      self.set_text(text) # to adjust the size of the connector
    
    WordBubble.text_boxes.append(self)

  def get_axes(self):
    result = self.text_boxes[0].axes
    return result
  
  def set_outline_color(self, color):
    self.text_boxes[0].get_bbox_patch().set_ec(color)
    if self.connector:
      self.connector.outline_color = color

  def get_layer_nb(self):
    result = self.text_boxes[0].get_zorder()
    return result

  def _get_what_to_move(self):
    result = self.connector._get_what_to_move() if self.connector else []
    result += self.text_boxes
    return result
  
##################################################################
  def remove(self):
    result = self._get_what_to_move()
    for r in result:
      try:
        r.remove()
      except:
        pass

##################################################################
  def make_visible(self, val=True):
    for t in self._get_what_to_move():
      t.set_visible(val)

  def make_invisible(self):
    self.make_visible(False)

  def get_bbox(self):
    rend = _get_renderer(self.get_axes().figure)
    tbb = self.text_boxes[0].get_window_extent(renderer=rend)
    abb = self.get_axes().get_window_extent(renderer=rend)
    a_xlim, a_ylim = self.get_axes().get_xlim(), self.get_axes().get_ylim()
    relative_width = tbb.width/abb.width * (a_xlim[1] - a_xlim[0])
    relative_height =  tbb.height/abb.height * (a_ylim[1] - a_ylim[0])

    xy = self.text_boxes[0].get_position()
    tbb_it = Bbox.from_extents(xy[0], xy[1], xy[0]+relative_width, xy[1]+relative_height)

    return tbb_it

  def shift_to_position(self, xy, position):
    self.position = position
    for _ in range(2):
      # now adjust the position if needed
      new_xy = [xy[0], xy[1]]
      bbox = self.get_bbox()

      assert(position[0] in ['l', 'c', 'r'])
      if position[0] == 'c':
        new_xy[0] -= bbox.width/2
      elif position[0] == 'r':
        new_xy[0] -= bbox.width
      
      assert(position[1] in ['b', 'c', 't'])
      if position[1] == 'c':
        new_xy[1] -= bbox.height/2
      elif position[1] == 't':
        new_xy[1] -= bbox.height

      for tb in self.text_boxes:
        tb.set_position(new_xy)
      if self.connector:
        pass # self.connector.shift(np.array(new_xy) - old_position)
      self.set_text(text=self.get_text())

  def shift(self, shift):
    for tb in self.text_boxes:
      tb.set_position(np.array(shift) + tb.get_position()) 
    if self.connector:
      self.start += shift
      self.connector.shift(shift)
    self.set_text(text=self.get_text())

  def shift_x(self, shift):
    self.shift((shift, 0))

  def shift_y(self, shift):
    self.shift((0, shift))

  def get_text(self):
    return self.text_boxes[0].get_text()
  
  def set_start(self, start):
    if not self.connector:
      return
    old_start = [self.start[0], self.start[1]]
    self.start = start
    self.connector.shift([start[0] - old_start[0], start[1] - old_start[1]])
    self.set_text(text=self.get_text())

  def set_text(self, text):
    for t in self.text_boxes:
      t.set_text(text)  
    tbb_it = self.get_bbox()
    mid = [0.5*(tbb_it.x1+tbb_it.x0), 0.5*(tbb_it.y1+tbb_it.y0)]

    if self.connection is None:
      pass
    elif  self.connection == 'triangle':

      triangle_height = calc_Pythagoras(self.start[0] - mid[0], self.start[1] - mid[1])
      self.connector.height = triangle_height
      triangle_turn = calc_angle(x=mid[0], y=mid[1], diamond_x=self.start[0], diamond_y=self.start[1])
      self.connector.turn_to(turn=triangle_turn)
    else:
      raise Exception("not implemented")
    
  def stretch(self, diamond_override, stretch):
    orig_x = {'l' : self.left, 'c' : self.center_x, 'r' : self.right}[self.position[0]]
    orig_y = {'b' : self.bottom, 'c' : self.center_y, 't' : self.top}[self.position[1]]
    if self.connector:
      self.connector.stretch(diamond_override=diamond_override, stretch=stretch)
    shift = (np.array([orig_x, orig_y]) - np.array(diamond_override)) * (stretch - 1.)
    self.shift_to_position(xy=shift+np.array([orig_x, orig_y]), position=self.position)
    self.set_text(self.get_text())

  def set_fontsize(self, size):
    for tb in self.text_boxes:
      tb.set_fontsize(size)
    self.set_text(self.get_text())

def draw_a_speech_bubble(text, x, y, position=None, **kwargs):
  wb = WordBubble(text, x, y, **kwargs)
  if position is not None:
    wb.shift_to_position(xy=[x, y], position=position)
  return wb

##########################################################################################
def place_text(text, x, y, **kwargs):
  xlim = get_ca().get_xlim() 
  ylim = get_ca().get_ylim() 
  sb = draw_a_speech_bubble(text=text, x=x*(xlim[1]-xlim[0]), y=y*(ylim[1]-ylim[0]), **kwargs)
  return sb
