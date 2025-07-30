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

import copy
import numpy as np

from matplotlib.pyplot import Polygon, gca, gcf
from matplotlib.transforms import Bbox
from matplotlib.figure import Figure

from . import coordinates
from .utils import is_the_same_contour, move_by_matrix, get_rotation_matrix, sin, cos, is_a_number, random_number
from .shape_style import set_polygon_style, format_arg_dict, line_arg_types, get_default_color_etc_settings, \
                              raise_Exception_if_not_processed, patch_arg_types, get_polygon_style, get_trace_color
from .bbox import ObjPosition

from .settings import create_image_only as create_image_only_ 
from .settings import default_diamond_size, screen_zoom

########################################################################
create_image_only = create_image_only_
current_lone_figure = None
def set_create_image_only(val):
  global create_image_only
  create_image_only = val

def is_create_image_only():
  return create_image_only

def get_cf():
  if create_image_only:
    return current_lone_figure
  return gcf()

def get_ca():
  if create_image_only:
    return current_lone_figure.gca() if current_lone_figure else None
  return gca()

def set_current_lone_figure(*args, **kwargs):
  global current_lone_figure
  current_lone_figure = Figure(*args, **kwargs)
  return current_lone_figure

def get_current_lone_figure():
  return current_lone_figure

##################################################################
## CANVAS HELPERS                                               ##
##################################################################
def _get_renderer(fig=None):
  if fig is None:
    fig = get_cf()
  try:
    rend = fig.canvas.get_renderer()
  except:
    rend = None
  return rend

def _get_axes(ax):
  if ax is None:
    ax = get_ca()
  return ax

def get_canvas_width(ax=None):
  ax = _get_axes(ax=ax)
  xlims = ax.get_xlim()
  return (xlims[1] - xlims[0])


def get_canvas_height(ax=None):
  ax = _get_axes(ax=ax)
  ylims = ax.get_ylim()
  return (ylims[1] - ylims[0])

def get_canvas_left(ax=None):
  ax = _get_axes(ax=ax)
  xlims = ax.get_xlim()
  return xlims[0]

def get_canvas_bottom(ax=None):
  ax = _get_axes(ax=ax)
  ylims = ax.get_ylim()
  return ylims[0]

def get_diamond_size(ax=None):
  ax = _get_axes(ax=ax)

  return get_canvas_width(ax=ax) * default_diamond_size * get_default_color_etc_settings()['diamond_size_factor']

def get_linewidth_factor():
  return get_cf().dpi / 100 / screen_zoom

def random_point_on_axes(ax=None, x_min=None, x_max=None, y_min=None, y_max=None):
  if ax is None:
    ax = get_ca()

  random_x = random_number(limit_1 = x_min if x_min is not None else ax.get_xlim()[0],
                           limit_2 = x_max if x_max is not None else ax.get_xlim()[1])
  random_y = random_number(limit_1 = y_min if y_min is not None else ax.get_ylim()[0],
                           limit_2 = y_max if y_max is not None else ax.get_ylim()[1])

  result = np.array([random_x, random_y])
  
  return result

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
      instance.set_shape_parameters(**{self.name : val})
    else:
      raise Exception(f'Could not find {self.name}. Available keys: {", ".join(instance.shape_kwargs.keys())}')

########################################################################################
########################################################################################
class ShapeStyleAttribute:

  def __get_polygon(self, instance):
    if self.prefix is not None:
      assert instance.outline is not None, 'This object has no outline'
      return 'outline', instance.outline
    if instance.line is not None:
      return 'line', instance.line
    else:
      assert self.name in patch_arg_types, f'{self.name} not in {patch_arg_types}'
      return 'patch', instance.patch
  
  def __init__(self, name, prefix):
    self.name = name
    self.prefix = prefix

  def __get__(self, instance, owner=None):
    if instance is None:
      return None # needed for the docs
    _p_name, _polygon = self.__get_polygon(instance)
    return get_polygon_style(parent=instance, attr_name=_p_name, style_name=self.name)

  def __set__(self, instance, val):
    _p_name, _polygon = self.__get_polygon(instance)
    linewidth_factor = get_linewidth_factor()
    set_polygon_style(something=_polygon, linewidth_factor=linewidth_factor,
                       attr_name=_p_name, kwargs={self.name : val})

##################################################################
## SHAPE                                                        ## 
##################################################################

class Shape:

##################################################################
  for k in coordinates._get_all_param_names():
    locals()[k] = ShapeFormAttribute(name=k)

  for s in ['left', 'right', 'bottom', 'top', 'center_x', 'center_y']:
    locals()[s] = ObjPosition(name=s)

##################################################################
  for prefix in [None, 'outline']:
    for k in line_arg_types + [patch_arg_types[-1]]:
      if k == 'ending_style' and prefix == 'outline':
        continue
      full_name = k if prefix is None else prefix + '_' + k
      locals()[full_name] = ShapeStyleAttribute(name=k, prefix=prefix)

  all_shapes = []

  

##################################################################

  # def __getattr__(self, attrName: str) -> Any:
  #   print(self.)
  #   print(self.patch.__dict__)
  #   print(self.__dict__)
  #   if attrName not in self.__dict__:
  #     value = self.fetchAttr(attrName)    # computes the value
  #     self.__dict__[attrName] = value
  #   return self.__dict__[attrName]


########################################################################
  def get_shape(shape_nb):
    return Shape.all_shapes[shape_nb]

########################################################################
# just list the numbers of the layers that you need. 
# If you pass no arguments, all shapes will be returned
########################################################################
  def _get_all_shapes_in_layers(layer_nbs=[], ax=None):
    if ax is None:
      ax = get_ca()
    _shapes_in_layers = [as_ for as_ in Shape.all_shapes if as_.get_axes() == ax]
    if len(layer_nbs) != 0:
      _shapes_in_layers = [sh for sh in _shapes_in_layers if sh.get_layer_nb() in layer_nbs]
    return _shapes_in_layers

##################################################################
  def _get_xy(something):
    if isinstance(something, np.ndarray):
      return something
    elif isinstance(something, list):
      return np.array(something)
    elif isinstance(something, Polygon):
      return something.get_xy()
    raise Exception("Data type ", type(something), " is not handled")

  def _set_xy(something, xy):
    if isinstance(something, np.ndarray):
      something = xy
    elif isinstance(something, Polygon):
      something.set_xy(xy)
    else:
      raise Exception("Data type ", type(something), " is not handled")
    return something

  ##################################################################
  def _x_y_to_direction(direction):
    if direction in ['x', 'X']:
      return 3
    if direction in ['y', 'Y']:
      return 0
    return direction

 ################################################################## 
  def __init__(self, **kwargs):

    Shape.all_shapes.append(self)

    dummy_xy = np.array([[0,0], [0,1], [1,1]])

    # clone constructor
    if len(kwargs) == 1:
      init_shape = kwargs['init_shape']
      assert isinstance(init_shape, Shape)

      def clone_patch(init_patch):
        if init_patch is None:
          return None
        else:
          result = Polygon(xy=dummy_xy, closed=init_patch.get_closed())
          result.update_from(other=init_patch)
          result.set_zorder(init_patch.get_zorder())
          result.set_xy(np.copy(init_patch.get_xy()))
          init_patch.axes.add_patch(result)

          assert is_the_same_contour(p1=result.get_xy(), p2=init_patch.get_xy())
          return result

      self.patch = clone_patch(init_patch=init_shape.patch)
      self.outline = clone_patch(init_patch=init_shape.outline)
      self.line = clone_patch(init_patch=init_shape.line)
      self.diamond = clone_patch(init_patch=init_shape.diamond)

      self.shapename = init_shape.shapename
      self.clip_patches = copy.deepcopy(init_shape.clip_patches)
      self.move_matrix = init_shape.move_matrix.copy()
      self.shape_kwargs = copy.deepcopy(init_shape.shape_kwargs)
      self.diamond_coords = init_shape.diamond_coords.copy()
      self.total_turn = init_shape.total_turn
      self.directional_stretch_matrix = init_shape.directional_stretch_matrix.copy()

    # from-scratch constructor
    elif len(kwargs) == 2:
      ax = kwargs['ax']
      if ax is None:
        ax = get_ca()
      shapetype = kwargs['shapetype']
      assert shapetype in ["patch", "line"]

      self.diamond_coords = np.array([0, 0])
      diamond_size = get_diamond_size(ax)
      diamond_contour = np.array([[1, 0], [0, -1], [-1, 0], [0, 1]]) * diamond_size if diamond_size is not None else None 

      self.patch   = Polygon(xy=dummy_xy, fill=True,  closed=True)  if shapetype == "patch" else None
      self.outline = Polygon(xy=dummy_xy, fill=False, closed=True)  if shapetype == "patch" else None
      self.line    = Polygon(xy=dummy_xy, fill=False, closed=False) if shapetype == "line"  else None
      self.diamond = Polygon(xy=diamond_contour, fill=True, closed=True) if diamond_size is not None else None

      for what in [self.patch, self.outline, self.line, self.diamond]:
        if what is not None:
          ax.add_patch(what)

      self.set_style()    

      self.clip_patches = []
      self.move_matrix = np.array([[1, 0],
                                   [0, 1]])
      self.shape_kwargs = {}
      self.total_turn = 0
      self.directional_stretch_matrix = np.array([[1, 0],
                                                  [0, 1]])
      self.shapename = None
    else:
      raise Exception("Constructor arguments are invalid")

##################################################################
## 'get' methods, a.k.a. accessors                                ##
##################################################################
  def get_visible(self):
    result = {}
    for attr_name in format_arg_dict.keys():
      _attr = getattr(self, attr_name)
      if _attr is not None:
        result[attr_name] = _attr.get_visible()
    return result

##################################################################
  def get_xy(self):
    if self.patch is not None:
      return Shape._get_xy(self.patch)
    if self.line is not None:
      return Shape._get_xy(self.line)
    raise Exception("Unable to identify xy")

  def get_bbox(self):
    xy_ = self.get_xy()
    return Bbox.from_extents(min(xy_[:, 0]), min(xy_[:, 1]), max(xy_[:, 0]), max(xy_[:, 1]))

##################################################################
  def get_axes(self):
    if self.patch is not None:
      return self.patch.axes
    if self.line is not None:
      return self.line.axes
    raise Exception("Unable to identify axes")

##################################################################
  def get_layer_nb(self):
    if self.patch is not None:
      return self.patch.zorder
    if self.line is not None:
      return self.line.zorder
    raise Exception("Unable to identify layer_nb")
    
##################################################################
  def get_shape_parameter(self, param_name):
    if param_name in self.shape_kwargs:
      return self.shape_kwargs[param_name]
    raise Exception(param_name, "not found. Available parameters: ", 
                    ', '.join(self.shape_kwargs.keys()))

##################################################################
  def get_diamond_coords(self):
    return self.diamond_coords.copy()

##################################################################
## methods that change the style of the shape                   ##
##################################################################
  def set_visible(self, val):
    for attr_name in format_arg_dict.keys():
      _attr = getattr(self, attr_name)
      if _attr is not None:
        _attr.set_visible(val)

  def make_visible(self):
    self.set_visible(True)

##################################################################
  def make_invisible(self):
    self.set_visible(False)
    
##################################################################
  def set_color(self, color):
    self.set_style(color=color)

##################################################################
  def set_style(self, **kwargs):
    used_args = []
    for attr_name, arg_types in format_arg_dict.items():
      _attr = getattr(self, attr_name)
      if _attr is None:
        continue

      if attr_name == "diamond" and get_trace_color() is not None:
        _attr.set_fc('none')
        _attr.set_ec('none')
        continue

      if attr_name in ["patch", "line"]:
        prefix = ""
      else:
        prefix = attr_name + "_"
      keys_for_kwargs = [prefix + at for at in arg_types]
      _kwargs = {key[len(prefix):] : value for key, value in kwargs.items() if key in keys_for_kwargs}
      used_args += [prefix + k for k in _kwargs.keys()]

      # (not kwargs) is called in constructor
      # _kwargs is called to pass instance-specific style-arguments
      if _kwargs or not kwargs:
        linewidth_factor = get_linewidth_factor()
        set_polygon_style(_attr, linewidth_factor, attr_name, _kwargs)

    raise_Exception_if_not_processed(kwarg_keys=kwargs.keys(), allowed_keys=used_args)

##################################################################
  def get_color(self):
    if self.patch is not None:
      return self.patch.get_facecolor()
    else:
      return self.line.get_edgecolor()

##################################################################
## methods that change the shape of the Shape                   ##
##################################################################

  def _update_the_shape_of_the_Shape(self, contour):
    if self.shapename in ["a_rectangle", "a_square"]:
      extra_shift = coordinates._calc_extra_shift(contour=contour, 
                                                                diamond_names=self.diamond_names)   
      contour += extra_shift
  
    for what in [self.line, self.outline, self.patch]:
      if what is not None:
        Shape._set_xy(what, contour)

    shift = self.diamond_coords # self.shift will restore the value of self.diamond_coords
    self._update_diamond(new_diamond_coords=[0., 0.])

    self._move_by_matrix_around_diamond() # correct for clipping contours

    self.shift(shift=shift)

##################################################################
  def update_contour(self, new_contour):
    assert self.shapename is None
    self._update_the_shape_of_the_Shape(contour=new_contour)

################################################################## 
  def set_shape_parameters(self, **kwargs):
    assert self.shapename is not None

    for key, value in kwargs.items():
      self.shape_kwargs[key] = value
    
    method_to_call = getattr(coordinates, 'build_'+self.shapename)
    contour = method_to_call(**self.shape_kwargs)

    self._update_the_shape_of_the_Shape(contour)

##################################################################
  def increment_shape_parameters(self, **kwargs):
    for key in kwargs.keys():
      kwargs[key] += self.shape_kwargs[key]
    self.set_shape_parameters(**kwargs)

##################################################################   
  def reset_given_shapename_and_arguments_and_move(self, shapename, kwargs_shape, kwargs_common):

    if isinstance(shapename, str):
      method_to_call = getattr(coordinates, 'build_'+shapename)
      contour = method_to_call(**kwargs_shape)
      self.shapename = shapename
      self.shape_kwargs = kwargs_shape
    else:
      contour = shapename # assume that it's an array of coordinates
      self.shapename = None 
      self.shape_kwargs = {}

    # updating the elements
    for what in [self.line, self.outline, self.patch]:
      if what is not None:
        Shape._set_xy(what, contour)
    
    # updating the diamond
    self._update_diamond(new_diamond_coords=np.array([0, 0]))

    # update directional_stretch_matrix
    stretch_direction = Shape._x_y_to_direction(kwargs_common['stretch_direction']) if 'stretch_direction' in kwargs_common else None
    stretch_coeff = kwargs_common['stretch_coeff'] if 'stretch_coeff' in kwargs_common else None
    assert (stretch_coeff is None) == (stretch_direction is None)
    if stretch_direction is not None:
      self.directional_stretch_matrix = (
        np.matmul(get_rotation_matrix(turn= -self.total_turn+stretch_direction),
          np.matmul(np.array( [[1,  0], [0, stretch_coeff]] ),
            np.matmul(get_rotation_matrix(turn= self.total_turn-stretch_direction), self.directional_stretch_matrix))))
    
    # apply directional stretch
    self._move_by_matrix_around_diamond(matrix=self.directional_stretch_matrix)

    self.diamond_names = [None, None]
    # apply the shift
    if self.shapename in ["a_rectangle", "a_square"]:
      contour = self.get_xy()
      self.diamond_names = coordinates._get_rect_diamond_names(**kwargs_common)
      extra_shift = coordinates._calc_extra_shift(contour=contour, diamond_names=self.diamond_names)
      new_contour = contour + extra_shift

      # updating the elements
      for what in [self.line, self.outline, self.patch]:
        if what is not None:
          Shape._set_xy(what, new_contour)

    # check the shift and do turning and streching
    common_keys_for_shape = coordinates._get_common_keys_for_shape(
        shapename=self.shapename, 
        available_arguments=kwargs_common)

    shift = [None, None]
    not_recognised = []
    for arg_name, arg_value in kwargs_common.items():
      arg_value_is_used = False
      try:
       if arg_name == common_keys_for_shape['diamond_x']:
        if is_a_number(arg_value):
          shift[0] = arg_value
        else:
          shift[0] = arg_value[0]
        arg_value_is_used = True
       if arg_name == common_keys_for_shape['diamond_y']:  
        if is_a_number(arg_value):
          shift[1] = arg_value
        else:
          shift[1] = arg_value[1]
        arg_value_is_used = True
       if arg_value_is_used:
         continue

       if arg_name == 'turn':  
        self.turn(turn=arg_value)
       elif arg_name == 'stretch':
        self.stretch(stretch=arg_value)        
       elif arg_name not in ['stretch_direction', "stretch_coeff"]:
        not_recognised += [arg_name]
      except:
        raise Exception(arg_name, arg_value, self.shapename, common_keys_for_shape)
    
    error_msg = ""
    if len(not_recognised):
      error_msg = "Parameters " + ', '.join(not_recognised) + " were not recognized. "
    if shift[0] is None:
     try: 
      error_msg +=  "Parameter " + common_keys_for_shape['diamond_x'] + " was not provided. "
     except:
      raise Exception(self.shapename, kwargs_common, common_keys_for_shape)
    if shift[1] is None:
      error_msg +=  "Parameter " + common_keys_for_shape['diamond_y'] + " was not provided. "
    if len(error_msg):
      raise Exception(self.shapename, kwargs_common, common_keys_for_shape, error_msg, shift)

    self.shift(shift=shift)

    if stretch_direction is not None:
      return self.directional_stretch_matrix, get_rotation_matrix(turn= self.total_turn-stretch_direction), np.array([[1,  0], [0, stretch_coeff]]), get_rotation_matrix(turn=-self.total_turn+stretch_direction)

##################################################################
  def clip(self, clip_outline):
    if clip_outline is None:
      return
    for what in [self.patch, self.line, self.outline]:
      if what is None:
        continue
      clip_patch = None
      if isinstance(clip_outline, Shape):
        clip_xy = clip_outline.get_xy()
        for clip_candidate in [clip_outline.patch, clip_outline.line]:
          if clip_candidate is not None:
            if clip_candidate.get_zorder() == what.get_zorder():
              clip_patch = clip_candidate
      else:
        clip_xy = Shape._get_xy(clip_outline)
      if clip_patch is None:
        clip_patch = Polygon(clip_xy, 
                               fc = 'none', 
                               ec = 'none',
                               zorder = what.get_zorder())
        what.axes.add_patch(clip_patch)
        self.clip_patches.append(clip_patch)
        
      what.set_clip_path(clip_patch)

##################################################################
## MOVEMENT METHODS                                             ## 
##################################################################
  def _update_diamond(self, new_diamond_coords):
    diamond_shift = new_diamond_coords - self.diamond_coords
    self.diamond_coords = np.array(new_diamond_coords)
    if self.diamond is not None:                  
      Shape._set_xy(something=self.diamond, 
                    xy=Shape._get_xy(self.diamond)+diamond_shift)

##################################################################
  def _get_what_to_move(self):
    all_candidates = [self.line, self.patch, self.outline] + self.clip_patches
    result = [r for r in all_candidates if r is not None]
    return result
  
##################################################################
  def remove(self):
    result = self._get_what_to_move()
    for r in result:
      r.remove()

##################################################################
  def shift(self, shift):

    what_to_move = self._get_what_to_move()
    for something in what_to_move:
      xy = Shape._get_xy(something=something) + shift
      Shape._set_xy(something=something, xy=xy)

    self._update_diamond(new_diamond_coords = self.diamond_coords + shift)

##################################################################
  def shift_x(self, shift):
    self.shift(shift=(shift, 0))

  def shift_y(self, shift):
    self.shift(shift=(0, shift))

  def shift_with_direction(self, shift, direction):
    direction = Shape._x_y_to_direction(direction)
    self.shift(shift=(shift*sin(direction), shift*cos(direction)))

##################################################################
  def shift_to(self, new_diamond_coords):
    diamond_shift = new_diamond_coords - self.diamond_coords
    self.shift(shift=diamond_shift)

  def shift_x_to(self, new_diamond_x):
    diamond_shift = new_diamond_x - self.diamond_coords[0]
    self.shift(shift=[diamond_shift, 0])

  def shift_y_to(self, new_diamond_y):
    diamond_shift = new_diamond_y - self.diamond_coords[1]
    self.shift(shift=[0, diamond_shift])

##################################################################
  def shift_to_position(self, xy, position):

    # now adjust the position if needed
    bbox = self.get_bbox()
    old_xy = [bbox.xmax, bbox.ymax]
    
    assert(position[0] in ['l', 'c', 'r'])
    if position[0] == 'c':
      old_xy[0] -= bbox.width/2
    elif position[0] == 'l':
      old_xy[0] -= bbox.width
    
    assert(position[1] in ['b', 'c', 't'])
    if position[1] == 'c':
      old_xy[1] -= bbox.height/2
    elif position[1] == 'b':
      old_xy[1] -= bbox.height

    self.shift([xy[0] - old_xy[0], xy[1] - old_xy[1]])
    
##################################################################
  def _move_by_matrix_around_diamond(self, matrix=None, diamond_override=None):
    
    diamond = self.diamond_coords if diamond_override is None else diamond_override

    if matrix is None:
      matrix = self.move_matrix
    else:
      self.move_matrix = np.matmul(matrix, self.move_matrix)

    what_to_move = self._get_what_to_move()
    for something in what_to_move:
      xy = move_by_matrix(contour=Shape._get_xy(something=something), diamond=diamond, matrix=matrix)
      Shape._set_xy(something=something, xy=xy)

    if diamond_override is not None:
      self.diamond_coords = move_by_matrix(contour=self.diamond_coords, 
                                           diamond=diamond_override, 
                                           matrix=matrix)

##################################################################
  def turn(self, turn, diamond_override=None):
    self._move_by_matrix_around_diamond(matrix=get_rotation_matrix(turn=turn), 
                                        diamond_override=diamond_override)
    self.total_turn += turn

##################################################################
  def turn_to(self, turn, diamond_override=None):
    self._move_by_matrix_around_diamond(matrix=get_rotation_matrix(turn=turn-self.total_turn), 
                                        diamond_override=diamond_override)
    self.total_turn = turn

##################################################################
  def flip_upside_down(self, diamond_override=None):
    self.stretch_y(stretch=-1, diamond_override=diamond_override)

##################################################################
  def stretch(self, stretch, diamond_override=None):
      self._move_by_matrix_around_diamond(matrix=np.array([[stretch,  0],
                                                           [0, stretch]]), 
                                        diamond_override=diamond_override)     

##################################################################
  def stretch_with_direction(self, stretch_coeff, direction, diamond_override=None):
    direction = Shape._x_y_to_direction(direction)

    # that's what we do right now
    self.turn(turn=-direction)
    stretch_matrix = np.array([[1,  0], [0, stretch_coeff]])
    self._move_by_matrix_around_diamond(matrix=stretch_matrix, 
                                        diamond_override=diamond_override) 
    self.turn(turn= direction)

##################################################################
  def stretch_x(self, stretch, diamond_override=None):
    self.stretch_with_direction(stretch_coeff=stretch, 
                                direction="x", 
                                diamond_override=diamond_override)

  def stretch_y(self, stretch, diamond_override=None):
    self.stretch_with_direction(stretch_coeff=stretch, 
                                direction="y", 
                                diamond_override=diamond_override)

                         
