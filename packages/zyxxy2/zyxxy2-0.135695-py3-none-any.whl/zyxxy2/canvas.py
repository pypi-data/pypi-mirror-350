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

import inspect
import ntpath
import numpy as np
import os
from io import BytesIO
import base64
from functools import partial
from math import floor
from matplotlib import animation
from matplotlib.text import Text
import matplotlib.pyplot as plt
from collections.abc import Iterable

from .shape_style import set_default_diamond_size_factor, set_trace_color, set_trace_diamond_color, \
  find_color_code, reset_default_color_etc_settings, set_default_diamond_color, \
  set_default_color_etc_settings, get_default_color_etc_settings
from .shape_class import Shape, get_ca, get_cf, is_create_image_only, set_current_lone_figure, get_current_lone_figure
from .word_bubbles import WordBubble
from .files import filename_to_image, show_image
from .utils import equal_or_almost
from .settings import default_font_sizes, default_display_params, default_image_params, default_animation_params, default_images_folder

USE_PLT_SHOW = True
IMAGES_FOLDER = default_images_folder
SLIDE_OR_FRAME_NUMBER = None
INSIDE_ANIMATION = False
WOULD_BE_AXES_LIMITS = None

########################################################################

if not os.path.exists(IMAGES_FOLDER):
  os.makedirs(IMAGES_FOLDER)

########################################################################

__is_running_tests = False


def _is_running_tests(val=None):
  global __is_running_tests
  if val is not None:
    __is_running_tests = val
  return __is_running_tests


def start_animation():
  global INSIDE_ANIMATION
  INSIDE_ANIMATION = True


########################################################################
def _find_relative_bbox(in_bbox, out_bbox):
  result = {
    'width': in_bbox['width'] / out_bbox['width'],
    'height': in_bbox['height'] / out_bbox['height'],
    'x0': (in_bbox['x0'] - out_bbox['x0']) / out_bbox['width'],
    'y0': (in_bbox['y0'] - out_bbox['y0']) / out_bbox['height']
  }
  return result


########################################################################
def _find_absolute_bbox(in_bbox, out_bbox):
  result = {
    'width': in_bbox['width'] * out_bbox['width'],
    'height': in_bbox['height'] * out_bbox['height'],
    'x0': out_bbox['x0'] + in_bbox['x0'] * out_bbox['width'],
    'y0': out_bbox['y0'] + in_bbox['y0'] * out_bbox['height']
  }
  return result

########################################################################
def get_axes_limits(ax=None):
  if ax is None:
    ax = get_ca()
  result = ax.get_xlim(), ax.get_ylim()
  return result

########################################################################
def place_axes_on_axes(ax_parent, ax_parent_absolute, new_coords):
  # ax_parent_absolute should be get_window_extent(), but correct value is not available on the run
  parent_coords = {
    'x0': ax_parent.get_xlim()[0],
    'y0': ax_parent.get_ylim()[0],
    'width': (ax_parent.get_xlim()[1] - ax_parent.get_xlim()[0]),
    'height': (ax_parent.get_ylim()[1] - ax_parent.get_ylim()[0])
  }

  new_box_relative = _find_relative_bbox(in_bbox=new_coords,
                                         out_bbox=parent_coords)
  new_box_absol = _find_absolute_bbox(in_bbox=new_box_relative,
                                      out_bbox=ax_parent_absolute)
  ax_new = get_cf().axes([
    new_box_absol['x0'], new_box_absol['y0'], new_box_absol['width'],
    new_box_absol['height']
  ])

  get_cf().sca(ax_parent)

  return ax_new


########################################################################
def _get_axes_limits(canvas_width, canvas_height, make_symmetric,
                     bottom_left_coords):

  # preparing parameters for axes
  assert make_symmetric in ['x', 'y', True, False]
  assert bottom_left_coords is None or (make_symmetric == False)
  if bottom_left_coords is None:
    bottom_left_coords = [0., 0.]

  if make_symmetric in ['x', True]:
    left_x, right_x = -canvas_width / 2, canvas_width / 2
  else:
    left_x, right_x = bottom_left_coords[
      0], canvas_width + bottom_left_coords[0]
  if make_symmetric in ['y', True]:
    bottom_y, top_y = -canvas_height / 2, canvas_height / 2
  else:
    bottom_y, top_y = bottom_left_coords[
      1], canvas_height + bottom_left_coords[1]

  return left_x, right_x, bottom_y, top_y


########################################################################
def _calc_margins(min_margin, title_pad, tick_step_x, tick_step_y, xlabel, ylabel, title,
                  font_size):
  # 72 is a magic number
  # details here: https://stackoverflow.com/questions/47633546/relationship-between-dpi-and-figure-size
  margin = {side: min_margin for side in ['left', 'right', 'top', 'bottom']}
  if tick_step_x is not None:
    margin['bottom'] += font_size['axes_tick'] / 72
    if xlabel is not None:
      margin['bottom'] += font_size['axes_label'] / 72
  if tick_step_y is not None:
    margin['left'] += font_size['axes_tick'] / 72
    if ylabel is not None:
      margin['left'] += font_size['axes_label'] / 72
  if title is not None:
    margin['top'] += (font_size['title'] + title_pad) / 72

  return margin


########################################################################
# placing in left bottom corner for now
def _find_scale_place_axes(max_width,
                           max_height,
                           canvas_width,
                           canvas_height,
                           min_margin,
                           font_size,
                           title_pad,
                           tick_step_x, tick_step_y,
                           xlabel,
                           ylabel,
                           canvas_aspect=1,
                           title=None,
                           xy=None):
  figure = get_cf()
  figsize = figure.get_size_inches()
  margin = _calc_margins(min_margin,
                         title_pad,
                         tick_step_x, tick_step_y,
                         xlabel,
                         ylabel,
                         title,
                         font_size=font_size)
  scaleV = (max_height * figsize[1] -
            (margin['top'] + margin['bottom'])) / (canvas_height *
                                                   canvas_aspect)
  scaleH = (max_width * figsize[0] -
            (margin['left'] + margin['right'])) / (canvas_width)
  result_scale = min(scaleV, scaleH)

  if xy is None:
    return result_scale

  axes = figure.add_axes([
    xy[0] + margin['left'] / figsize[0], xy[1] + margin['bottom'] / figsize[1],
    canvas_width * result_scale / figsize[0],
    canvas_height * canvas_aspect * result_scale / figsize[1]
  ])
  return axes


########################################################################
def prepare_axes(ax,
                 canvas_width,
                 canvas_height,
                 make_symmetric=False,
                 bottom_left_coords=None,
                 aspect=1,
                 tick_step_x=None,
                 tick_step_y=None,
                 title_font_size=default_font_sizes['title'],
                 axes_label_font_size=default_font_sizes['axes_label'],
                 axes_tick_font_size=default_font_sizes['axes_tick'],
                 title_pad=0,
                 add_border=True,
                 title=None,
                 background_color=None,
                 xlabel=None,
                 ylabel=None):

  left_x, right_x, bottom_y, top_y = _get_axes_limits(canvas_width,
                                                      canvas_height,
                                                      make_symmetric,
                                                      bottom_left_coords)

  if (tick_step_x is not None) and (tick_step_y is not None):
    axis = 'both'
  elif (tick_step_x is not None):
    axis = 'x'
  elif (tick_step_y is not None):
    axis = 'y'
  else:
    axis = None
  args = {'visible' : (axis is not None)}
  if (axis is not None): 
    args['axis'] = axis
    args['linewidth'] = .1
  ax.grid(**args)

  if background_color is not None:
    ax.set_facecolor(find_color_code(background_color))

  if xlabel is not None:
    ax.set_xlabel(xlabel, fontsize=axes_label_font_size)
  if ylabel is not None:
    ax.set_ylabel(ylabel, fontsize=axes_label_font_size)

  ax.tick_params(axis='both', which='major', labelsize=axes_tick_font_size)

  # helper function to make sure the ticks are in the right place
  def get_round_multiple_range(min_, max_, step):
    if step is None:
      return []
    _sign = -1 if min_ < 0 else 1
    min_multiple = _sign * floor(abs(min_ / step)) * abs(step)
    result = np.arange(min_multiple, max_, step)
    return result

  ax.set_xticks(ticks=[] if tick_step_x is None else get_round_multiple_range(
    left_x, right_x, tick_step_x))
  ax.set_yticks(ticks=[] if tick_step_y is None else get_round_multiple_range(
    bottom_y, top_y, tick_step_y))

  # set axis limits
  ax.set_xlim(left=left_x, right=right_x)
  ax.set_ylim(bottom=bottom_y, top=top_y)
  ax.set_aspect(aspect)

  if title is not None:
    ax.set_title(title, fontdict={'size': title_font_size}, pad=title_pad)

  ax.set_frame_on(add_border)


##################################################################
## we will check for the presence of this wrapper in the callstack
## when calling create_canvas_and_axes and show_drawing_and_save_if_needed
def draw_and_keep_drawing(func_name,
                          *args,
                          **kwargs):

  current_settings = get_default_color_etc_settings()
  result = func_name(*args, **kwargs)
  set_default_color_etc_settings(current_settings)

  return result

def _is_drawn_and_keep_drawing():
  stack_ = inspect.stack()
  for s_ in stack_:
    if (s_.function == 'draw_and_keep_drawing') and (s_.filename == __file__):
      return True
  return False

def draw_on_another_image(func_name,
                          *args,
                          **kwargs):

  current_settings = get_default_color_etc_settings()
  result = func_name(*args, **kwargs)
  set_default_color_etc_settings(current_settings)

  return result


def _is_drawn_on_another_image():
  stack_ = inspect.stack()
  for s_ in stack_:
    if (s_.function == 'draw_on_another_image') and (s_.filename == __file__):
      return True
  return False


def use_as_a_model(model, *args, **kwargs):
  result = model(*args, **kwargs)
  return result


def _is_used_as_a_model():
  stack_ = inspect.stack()
  for s_ in stack_:
    if (s_.function == 'use_as_a_model') and (s_.filename == __file__):
      return True
  return False


##################################################################
# create the axis, set their sizes,
# add the grid and ticks if needed
def create_canvas_and_axes(
    canvas_width,
    canvas_height,
    make_symmetric=False,
    bottom_left_coords=None,
    background_color=None,
    figure_background_color=None,
    diamond_color=None,
    diamond_size=1.,
    axes=None,
    tick_step=None,
    tick_step_x=None,
    tick_step_y=None,
    add_border=True,
    title=None,
    inspiration_addon=None,
    title_pad=default_display_params['title_pad'],
    xlabel=default_display_params['x_axis_label'],
    ylabel=default_display_params['y_axis_label'],
    title_font_size=default_font_sizes['title'],
    axes_label_font_size=default_font_sizes['axes_label'],
    axes_tick_font_size=default_font_sizes['axes_tick'],
    axes_tick_font_size_factor=1.,
    max_figsize=default_display_params['max_figsize'],
    dpi=default_image_params['dpi'],
    min_margin=default_display_params['min_margin'],
    figure_aspect=None,  # height to width
    model=None,
    model_zoom=1.,
    model_shift=[0., 0.],
    trace_color=None,
    trace_diamond_color=None):

  reset_default_color_etc_settings()

  if _is_drawn_on_another_image():
    global WOULD_BE_AXES_LIMITS
    left_x, right_x, bottom_y, top_y = _get_axes_limits(
      canvas_width, canvas_height, make_symmetric, bottom_left_coords)
    WOULD_BE_AXES_LIMITS = {
      'left': left_x,
      'right': right_x,
      'bottom': bottom_y,
      'top': top_y
    }
    if axes is not None:
      get_cf().sca(axes)
      return axes
    else:
      return get_ca()

  if tick_step is not None:
    assert tick_step_x is None and tick_step_y is None
    tick_step_x, tick_step_y = tick_step, tick_step

  params_for_axes = {
    'canvas_width': canvas_width,
    'canvas_height': canvas_height,
    'make_symmetric': make_symmetric,
    'bottom_left_coords': bottom_left_coords,
    'tick_step_x': tick_step_x,
    'tick_step_y': tick_step_y,
    'axes_label_font_size': axes_label_font_size,
    'axes_tick_font_size': axes_tick_font_size*axes_tick_font_size_factor,
    'title_font_size': title_font_size,
    'background_color': background_color,
    'xlabel': xlabel if tick_step_x is not None else None,
    'ylabel': ylabel if tick_step_y is not None else None,
    'add_border': add_border,
    'title_pad': title_pad
  }

  # only needed for demo and when called inside models
  if _is_used_as_a_model():
    axes = figure.gca()
  if axes is not None:
    figure.sca(axes)
    prepare_axes(ax=axes, **params_for_axes)
    return axes

  font_size = {
    'axes_label': axes_label_font_size,
    'axes_tick': axes_tick_font_size*axes_tick_font_size_factor,
    'title': title_font_size
  }
  margin = _calc_margins(min_margin=min_margin,
                         font_size=font_size,
                         title_pad=title_pad,
                         tick_step_x=tick_step_x, 
                         tick_step_y=tick_step_y,
                         xlabel=xlabel,
                         ylabel=ylabel,
                         title=title)
  sum_margins = [
    margin['left'] + margin['right'], margin['bottom'] + margin['top']
  ]

  if model is not None:
    # decide if the model should be below (vertical) or to the right (horizontal) of the working axes
    scale_if_V_placement = min(
      (max_figsize[0] - sum_margins[0]) / canvas_width,
      (max_figsize[1] * 0.5 - sum_margins[1] * 0.75) / canvas_height)
    scale_if_H_placement = min(
      (max_figsize[0] * 0.5 - sum_margins[0] * 0.75) / canvas_width,
      (max_figsize[1] - sum_margins[1]) / canvas_height)

    scale = max(scale_if_V_placement, scale_if_H_placement)
    figsize = [
      canvas_width * scale + sum_margins[0],
      canvas_height * scale + sum_margins[1]
    ]

    place_model_H_not_V = (scale_if_H_placement > scale_if_V_placement)
    if place_model_H_not_V:
      figsize[0] += figsize[0] - min_margin
    else:
      figsize[1] += figsize[1] - min_margin

    # adjusting the margins
    if figure_aspect is not None:
      if not equal_or_almost(figsize[1] / figsize[0], figure_aspect):
        if figsize[1] < (figsize[0] * figure_aspect):
          what_to_add = 0.5 * (figsize[0] * figure_aspect - figsize[1])
          if not place_model_H_not_V:
            what_to_add *= 0.5
          margin['top'] += what_to_add
          margin['bottom'] += what_to_add
          figsize[1] = (figsize[0] * figure_aspect)
        else:  # figsize[0] < figsize[1] / (aspect)
          what_to_add = 0.5 * (figsize[1] / (figure_aspect) - figsize[0])
          if place_model_H_not_V:
            what_to_add *= 0.5
          margin['left'] += what_to_add
          margin['right'] += what_to_add
          figsize[0] = figsize[1] / (figure_aspect)
  else:
    scale_horizontal = (max_figsize[0] - sum_margins[0]) / canvas_width
    scale_vertical = (max_figsize[1] - sum_margins[1]) / canvas_height
    scale = min(scale_horizontal, scale_vertical)
    figsize = [
      canvas_width * scale + sum_margins[0],
      canvas_height * scale + sum_margins[1]
    ]
    # adjusting the margins
    if figure_aspect is not None:
      if not equal_or_almost(figsize[1] / figsize[0], figure_aspect):
        if figsize[1] < (figsize[0] * figure_aspect):
          what_to_add = 0.5 * (figsize[0] * figure_aspect - figsize[1])
          margin['top'] += what_to_add
          margin['bottom'] += what_to_add
          figsize[1] = (figsize[0] * figure_aspect)
        else:  # figsize[0] < figsize[1] / (aspect)
          what_to_add = 0.5 * (figsize[1] / (figure_aspect) - figsize[0])
          margin['left'] += what_to_add
          margin['right'] += what_to_add
          figsize[0] = figsize[1] / (figure_aspect)

  fig_kwargs = dict(figsize=figsize,
                      dpi=dpi,              
                      facecolor='white' if figure_background_color is None else
                      find_color_code(figure_background_color))
  if is_create_image_only():
    figure = set_current_lone_figure(**fig_kwargs)
  else:
    figure = plt.figure(clear=True, **fig_kwargs)

  axes = figure.add_axes([
    margin['left'] / figsize[0], margin['bottom'] / figsize[1],
    canvas_width * scale / figsize[0], canvas_height * scale / figsize[1]
  ])

  if model is not None:
    axes_model = figure.add_axes([
      margin['left'] / figsize[0] + 0.5 *
      (1 - min_margin / figsize[0]) * place_model_H_not_V,
      margin['bottom'] / figsize[1] + 0.5 * (1 - min_margin / figsize[1]) *
      (1 - place_model_H_not_V), canvas_width * scale / figsize[0],
      canvas_height * scale / figsize[1]
    ])
    if not place_model_H_not_V:
      axes_model, axes = axes, axes_model
    # halve the font size
    for l in ['axes_label', 'axes_tick', 'title']:
      params_for_axes[l + '_font_size'] /= 2
    params_for_axes['background_color'] = None
    # handle the model drawing
    if isinstance(model, str):
      prepare_axes(ax=axes_model, 
                   title="Inspiration" + ("" if inspiration_addon is None else f': {inspiration_addon}'), 
                   **params_for_axes)
      image = filename_to_image(filename=model)
      scaling_factor = model_zoom * min(canvas_width / image.shape[1],
                                        canvas_height / image.shape[0])
      # defining LB_position to center the model image
      LB_position = [
        axes_model.get_xlim()[0] + 0.5 *
        (canvas_width - image.shape[1] * scaling_factor) + model_shift[0],
        axes_model.get_ylim()[0] + 0.5 *
        (canvas_height - image.shape[0] * scaling_factor) + model_shift[1]
      ]
      # placing the image
      show_image(ax=axes_model,
                 prepared_image=image,
                 origin=[0, 0],
                 zorder=0,
                 scaling_factor=scaling_factor,
                 LB_position=LB_position)
    else:
      global USE_PLT_SHOW
      USE_PLT_SHOW = False
      figure.sca(axes_model)
      set_default_diamond_size_factor(0)
      use_as_a_model(model)
      USE_PLT_SHOW = True
      figure.sca(axes)
      if trace_color is not None:
        set_trace_color(trace_color)
        set_trace_diamond_color(trace_diamond_color)
        USE_PLT_SHOW = False
        use_as_a_model(model)
        USE_PLT_SHOW = True
        set_trace_color(None)
        set_trace_diamond_color(None)
      prepare_axes(ax=axes_model, title="Model Drawing", **params_for_axes)

  params_for_axes['background_color'] = background_color
  prepare_axes(ax=axes, title=title, **params_for_axes)
  set_default_diamond_size_factor(diamond_size * (tick_step_x is not None or tick_step_y is not None))
  set_default_diamond_color(diamond_color)

  figure.sca(axes)

  global SLIDE_OR_FRAME_NUMBER
  SLIDE_OR_FRAME_NUMBER = 0

  return axes


##################################################################
def set_folder_for_saving(folder_name):
  global IMAGES_FOLDER
  IMAGES_FOLDER = folder_name


def reset_folder_for_saving():
  global IMAGES_FOLDER
  IMAGES_FOLDER = default_images_folder


##################################################################
def __get_output_filename_and_format(filename=None, image_format=None):
  if not filename:
    frame = inspect.stack()[2]  #1
    module = inspect.getmodule(frame[0])
    if module is not None:
      caller_filename = ntpath.basename(module.__file__)
    else:
      curframe = inspect.currentframe()
      caller_filename = inspect.getouterframes(curframe)[2].filename  #1
    if caller_filename == "all_examples.py":
      filename = frame.function
    else:
      filename = caller_filename
      # remove extension if it exists
      last_dot_position = filename.rfind(".")
      if last_dot_position > 0:
        filename = filename[:last_dot_position]
      # remove prefix if it exists
      for prefix_ in ["draw_", "drawn_"]:
        if filename.startswith(prefix_):
          filename = filename[len(prefix_):]
  else:
    last_dot_position = filename.rfind(".")
    if last_dot_position > 0:
      image_format = filename[last_dot_position + 1:]
      filename = filename[:last_dot_position]

  if image_format is None or image_format == "":
    image_format = default_image_params['format']

  return filename, image_format


##################################################################
def convert_figure_to_image(fig, img_format='png'):
  buf = BytesIO()
  fig.savefig(buf, format=img_format)
  imb_byte = base64.b64encode(buf.getbuffer()).decode('ascii')
  return imb_byte

##################################################################
# this function shows the drawing
# and saves if as a file if requested
# more information in the document below
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.savefig.html#matplotlib.pyplot.savefig
##################################################################

def show_and_save(save=True,
                  filename=None,
                  image_format=None,
                  image_folder=IMAGES_FOLDER,
                  animation_interval=default_animation_params['interval'],
                  animation_blit=default_animation_params['blit'],
                  animation_repeat=default_animation_params['repeat'],
                  animation_FPS=default_animation_params['FPS'],
                  animation_writer=default_animation_params['writer'],
                  animation_format=default_animation_params['format'],
                  animation_func=None,
                  animation_init=None,
                  nb_of_frames=None,
                  block=True):

  if (animation_func is None) != (nb_of_frames is None):
    raise Exception(
      "Either both animation_func and nb_of_frames, or none, should be specified."
    )

  not_an_animation = (animation_func is None)

  if _is_drawn_on_another_image():
    assert (animation_func is None)
    global WOULD_BE_AXES_LIMITS
    WOULD_BE_AXES_LIMITS = None
    return

  if _is_drawn_and_keep_drawing():
    return

  filename, image_format = __get_output_filename_and_format(
    filename=filename, image_format=image_format)

  global INSIDE_ANIMATION

  if not_an_animation:
    if is_create_image_only():
      if not save:
        buf = BytesIO()
        get_current_lone_figure().savefig(buf, format=image_format)
        data = base64.b64encode(buf.getbuffer()).decode('ascii')
        return data
      else:
        fn = [filename + '.' + image_format]
        if image_folder:
          fn = [image_folder] + fn
        get_current_lone_figure().savefig(fname=os.path.join(*fn),
                                          format=image_format)
        return

    elif (save or _is_running_tests()) and USE_PLT_SHOW and not INSIDE_ANIMATION:
      plt.savefig(fname=image_folder + "/" + filename + '.' + image_format,
                  format=image_format)
  else:
    ########################################################################
    def __get_all_polygons(*args):
      result = []
      for arg in args:
        if arg is None:
          return __get_all_polygons(Shape._get_all_shapes_in_layers() +
                                    WordBubble.get_all())
        if isinstance(arg, (Shape, WordBubble)):
          result += arg._get_what_to_move()
        elif isinstance(arg, Iterable):
          for a in arg:
            result += __get_all_polygons(a)
        elif isinstance(arg, Text):
          result += [arg]
        else:
          raise Exception(type(arg), "cannot be processed")
      return result

    def __envelope_init(animation_init):
      # custom init
      if animation_init is not None:
        result = animation_init()
        return __get_all_polygons(result)
      # return the list of the shapes that are moved by animation
      return __get_all_polygons(None)

    def __envelope_animate(i, anim_func):
      # return the list of the shapes that are moved by animation
      result = anim_func(i)
      return __get_all_polygons(result)

    anim = animation.FuncAnimation(fig=get_cf(),
                                   func=partial(__envelope_animate,
                                                anim_func=animation_func),
                                   init_func=partial(
                                     __envelope_init,
                                     animation_init=animation_init),
                                   frames=nb_of_frames,
                                   interval=animation_interval,
                                   blit=animation_blit,
                                   repeat=animation_repeat)

    INSIDE_ANIMATION = False
    if save:
      full_filename = image_folder + "/" + filename + '.' + animation_format
      try:
        writer = animation.writers[animation_writer](fps=animation_FPS)
        anim.save(full_filename, writer=writer)
      except:
        raise Exception(
          "Video cannot be saved. Usually reloading the webpage or restarting the browser solves the problem!"
        )

  if USE_PLT_SHOW and not _is_running_tests() and not INSIDE_ANIMATION:
    plt.show(block=block)

##################################################################

def wait_for_enter(msg="Press ENTER when you are ready ..."):
  if not _is_running_tests():
    plt.show(block=False)
    _input = input(msg)
    return _input
  else:
    global SLIDE_OR_FRAME_NUMBER
    filename, image_format = __get_output_filename_and_format()
    plt.savefig(fname=IMAGES_FOLDER + "/" + filename + '_slide_' +
                str(SLIDE_OR_FRAME_NUMBER) + '.' + image_format,
                format=image_format)
    SLIDE_OR_FRAME_NUMBER += 1


##################################################################
def show_demo():
  if not _is_running_tests():
    plt.show()
  else:
    filename, image_format = __get_output_filename_and_format()
    plt.savefig(fname=IMAGES_FOLDER + "/" + filename + '_screenshot.' +
                image_format,
                format=image_format)


##########################################################################################
def place_axes(axes_bbox, canvas_width, canvas_height, gap_x, gap_y):

  _ax = _find_scale_place_axes(
    max_width=axes_bbox[1][0] - axes_bbox[0][0] - 2 * gap_x,
    max_height=axes_bbox[1][1] - axes_bbox[0][1] - 2 * gap_y,
    canvas_width=canvas_width,
    canvas_height=canvas_height,
    min_margin=0,
    font_size={},
    title_pad=0,
    xlabel="",
    ylabel="",
    tick_step_x=None, tick_step_y=None,
    xy=(axes_bbox[0][0]+gap_x, axes_bbox[0][1]+gap_y))

  canvas_parameters = {
    'canvas_width': canvas_width,
    'canvas_height': canvas_height,
    'tick_step_x': None,
    'tick_step_y': None,
    'add_border': False
  }
  prepare_axes(ax=_ax, **canvas_parameters)
  return _ax