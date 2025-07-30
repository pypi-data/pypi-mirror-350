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

from .shape_style import set_default_layer_nb, get_top_layer_nb
from .shape_class import Shape
from .word_bubbles import WordBubble

########################################################################
# adding new layers
########################################################################
def new_layer():
  new_layer_nb = 1 + get_top_layer_nb()
  for fa in ["line", "patch", "outline", "text"]: 
    set_default_layer_nb(what=fa, layer_nb=new_layer_nb)
  return new_layer_nb

def new_layer_outline_behind():
  new_layer_nb = 1 + get_top_layer_nb()
  set_default_layer_nb(what='outline', layer_nb=new_layer_nb)
  for fa in ["line", "patch", "text"]: 
    set_default_layer_nb(what=fa, layer_nb=new_layer_nb+1)
  return new_layer_nb+1, new_layer_nb

########################################################################
# handling shapes per layers
########################################################################
def shift_layers(shift, layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.shift(shift=shift)

########################################################################
def turn_layers(turn, diamond, layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.turn(turn=turn, diamond_override=diamond)

########################################################################
def stretch_layers(diamond, stretch, layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.stretch(diamond_override=diamond, stretch=stretch)

########################################################################
def make_layers_visible(layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.make_visible()

########################################################################
def make_layers_invisible(layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.make_invisible()

########################################################################
def stretch_layers_with_direction(diamond, stretch_coeff, stretch_direction, layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.stretch_with_direction(diamond_override=diamond, stretch_coeff=stretch_coeff, direction=stretch_direction)

##################################################################
def remove_layers(layer_nbs=[]):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.remove()

##################################################################
def restyle_layers(layer_nbs=[], **style_kwargs):
  _shapes = Shape._get_all_shapes_in_layers(layer_nbs) + WordBubble.get_all_in_layers(layer_nbs)
  for shape in _shapes:
    shape.set_style(**style_kwargs)
