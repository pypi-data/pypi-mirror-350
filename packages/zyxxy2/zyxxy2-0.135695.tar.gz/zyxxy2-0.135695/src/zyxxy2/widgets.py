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

from matplotlib.widgets import Slider, RadioButtons, CheckButtons, Button
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection

from .settings import widget_params
from .utils import is_the_same_point
from .shape_class import get_cf

##########################################################################################
default_widget_sizes = {
  'width' : widget_params['width'], 'height' : widget_params['height'], 'gap' : widget_params['gap']
}

##########################################################################################
def set_default_widget_width(val):
  default_widget_sizes['width'] = val

def get_default_widget_width():
  return default_widget_sizes['width']
 
##########################################################################################
def get_axes_for_widget(w_left, w_bottom, w_width=None, w_height=None):
  w_width  =  w_width if  w_width is not None else default_widget_sizes['width']
  w_height = w_height if w_height is not None else default_widget_sizes['height']
  wax = plt.axes([w_left, w_bottom, w_width, w_height]) 
  new_bottom = w_height + w_bottom + default_widget_sizes['gap']
  return new_bottom, wax

##########################################################################################
def add_a_button(w_left, w_bottom, w_caption, w_width=None, w_height=None, on_click_or_change=None):
  w_width  =  w_width if  w_width is not None else default_widget_sizes['width']
  w_height = w_height if w_height is not None else default_widget_sizes['height']
  new_bottom, b_axes = get_axes_for_widget(w_bottom=w_bottom, w_left=w_left, w_width=w_width, w_height=w_height)
  result = Button(ax=b_axes, label=w_caption)
  if on_click_or_change is not None:
    result.on_clicked(on_click_or_change)
  return new_bottom, result, None

##########################################################################################
def add_vertical_radio_buttons(w_left, w_bottom, w_caption, rb_options, active_option=0, on_click_or_change=None):
  
  new_bottom, rax = get_axes_for_widget(w_left=w_left, 
                                        w_bottom=w_bottom, 
                                        w_height=default_widget_sizes['height']*len(rb_options))

  active = rb_options.index(active_option) if active_option in rb_options else active_option
  result = RadioButtons(rax, rb_options, active=active, activecolor='black')

  added_text = get_cf().text(w_left, new_bottom, w_caption)
  new_bottom += default_widget_sizes['height'] + default_widget_sizes['gap']

  #for circle in result.circles: # adjust radius here. The default is 0.05
    #pass # circle.set_radius(widget_params['height']/2.)

  if on_click_or_change is not None:
    result.on_clicked(on_click_or_change)

  return new_bottom, result, added_text

##########################################################################################
def add_a_slider(w_left, w_bottom, w_caption, s_vals, w_width=None, caption_in_the_same_line=True, on_click_or_change=None, **slider_qwargs):
  _, sax = get_axes_for_widget(w_left=w_left, w_bottom=w_bottom, w_width=w_width)
  label = w_caption if caption_in_the_same_line else ""
  result = Slider(ax=sax, label=label, valmin=s_vals[0], valmax=s_vals[1], valinit=s_vals[2], valstep=s_vals[3], color='black', **slider_qwargs)

  new_bottom = sax.get_position().ymax + default_widget_sizes['gap']
  if caption_in_the_same_line:
    added_text = None
  else:
    added_text = get_cf().text(sax.get_position().xmin, new_bottom, w_caption)
    new_bottom += default_widget_sizes['height'] + default_widget_sizes['gap']

  initline_linewidth = widget_params['slider_initline_linewidth']
  if is_the_same_point(s_vals[0], s_vals[2]) or is_the_same_point(s_vals[1], s_vals[2]):
    initline_linewidth *= 2
  result.vline.set_linewidth(initline_linewidth)
  if on_click_or_change is not None:
    result.on_changed(on_click_or_change)

  return new_bottom, result, added_text

##########################################################################################
def add_a_check_button(w_left, w_bottom, w_caption, on_click_or_change=None):

  def resize_1_checkbox(a_checkbox, left, bottom, width, height):
    r = a_checkbox.rectangles[0]
    r.set_x(left)
    r.set_y(bottom)
    r.set_width(width)
    r.set_height(height)
    l = a_checkbox.lines[0]
    l[0].set_data([left, left+width], [bottom+height, bottom])
    l[1].set_data([left, left+width], [bottom, bottom+height])

  new_bottom, w_axes = get_axes_for_widget(w_bottom=w_bottom, w_left=w_left)
  result = CheckButtons(w_axes, (w_caption, ), (False, ))
  resize_1_checkbox(a_checkbox=result, left=0.05, bottom=0.15, width=0.05, height=0.7)

  if on_click_or_change is not None:
    result.on_clicked(on_click_or_change)

  return new_bottom, result, None

##########################################################################################
def set_slider_values(slider, val, valmin, valmax, valinit, valstep, label):
  slider.set_val(val)
  slider.valstep = valstep
  slider.valinit = valinit
  slider.valmax = valmax
  slider.valmin = valmin
  slider.label.set_text(label)
  slider.ax.set_xlim(valmin, valmax)
  slider.vline.set_data([valinit, valinit], slider.ax.get_ylim())

  initline_linewidth = widget_params['slider_initline_linewidth']
  if is_the_same_point(valmin, valinit) or is_the_same_point(valmax, valinit):
    initline_linewidth *= 2
  slider.vline.set_linewidth(initline_linewidth)

##########################################################################################
def get_widget_value(a_widget):
  if isinstance(a_widget, Slider):
    return a_widget.val
  if isinstance(a_widget, CheckButtons):
    return a_widget.get_status()[0]
  if isinstance(a_widget, RadioButtons):
    return a_widget.value_selected
  raise Exception(type(a_widget), "is not handled")

##########################################################################################
def reset_widget(a_widget):
  if isinstance(a_widget, Slider):
    a_widget.reset()
  elif isinstance(a_widget, CheckButtons):
    if a_widget.get_status()[0]:
      a_widget.set_active(index=0)
  else:
    raise Exception(type(a_widget), "type not recognized")
  
##########################################################################################
def set_widget_visible(a_widget, val):
  a_widget.ax.set_visible(val)
  if isinstance(a_widget, RadioButtons):
    pcs = [ch for ch in a_widget.ax.get_children()  if isinstance(ch, PathCollection) ]
    for pc in pcs:
      pc.set_visible(val)
