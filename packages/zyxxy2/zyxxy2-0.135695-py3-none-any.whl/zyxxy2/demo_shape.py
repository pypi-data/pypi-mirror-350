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

import matplotlib.pyplot as plt
import numpy as np
import functools

from .utils import equal_or_almost
from .canvas import create_canvas_and_axes, show_demo, _find_scale_place_axes
from .shape_class import Shape
from .coordinates import shape_names_params_dicts_definition, get_type_given_shapename, _get_common_keys_for_shape, common_params_dict_definition
from .widgets import get_widget_value, set_slider_values, set_default_widget_width, add_a_button, add_a_slider, add_vertical_radio_buttons, reset_widget, get_default_widget_width, set_widget_visible
from .files import write_file
from .colors import find_color_code
from .settings import default_color_etc_settings, default_extreme_layer_nb
from .settings import demo_figure_params as figure_params, demo_style_widgets_value_ranges, demo_shapes, demo_style
from .settings import widget_params, canvas_width, canvas_height, slider_range

# variables that will be populated later
sides = ['left', 'right']
shape_types = ["patch", "line"]

def try_shapes(font_scaling=2):
  plt.rcParams.update({'font.size': font_scaling*figure_params['font_size']})
  active_shapename = {side: None for side in sides}
  shapes_by_side_by_shapetype = {
    side: {st: None
          for st in shape_types}
    for side in sides
  }
  common_widgets_by_side = {side: {} for side in sides}
  specific_widgets_by_side = {side: [] for side in sides}  # slider objects
  specific_widgets_values_by_side_by_shapename = {side: {}
                                                  for side in sides
                                                  }  # current values
  specific_inputs_values_by_shapename = {}  # min, max etc. params

  style_widgets_side_by_shapetype = {
    side: {st: {
      'text': []
    }
          for st in shape_types + ['']}
    for side in sides
  }
  shape_switchers = {side: None for side in sides}
  reset_button = {side: None for side in sides}
  stretch_button = {side: None for side in sides}

  TURN_OFF_XY_UPDATE = False


  ##########################################################################################
  def fill_in_specific_inputs_values_by_shapename_widgets_values_by_side_by_shapename(
  ):
    nonlocal specific_inputs_values_by_shapename
    nonlocal specific_widgets_values_by_side_by_shapename
    # specific sliders # todo
    for shapename, shape_params in shape_names_params_dicts_definition.items():
      specific_inputs_values_by_shapename[shapename] = {}
      for side in sides:
        specific_widgets_values_by_side_by_shapename[side][shapename] = {}
      for param_name, param_name_range in shape_params.items():

        if isinstance(param_name_range, str):
          param_params = np.copy(slider_range[param_name_range])
        else:
          param_params = np.copy(slider_range[param_name_range[0]])
          param_params[2] = param_name_range[1]

        specific_inputs_values_by_shapename[shapename][param_name] = {
          'valmin': param_params[0],
          'valmax': param_params[1],
          'valinit': param_params[2],
          'valstep': param_params[3]
        }
        for side in sides:
          specific_widgets_values_by_side_by_shapename[side][shapename][
            param_name] = param_params[2]


  fill_in_specific_inputs_values_by_shapename_widgets_values_by_side_by_shapename(
  )

  ##########################################################################################
  # create the figure
  fig = plt.figure(figsize=figure_params['figsize'], dpi=figure_params['dpi'])




  def get_max_specific_sliders():
    max_specific_sliders = 0
    for spec_param_dict in shape_names_params_dicts_definition.values():
      max_specific_sliders = max(max_specific_sliders, len(spec_param_dict))
    return max_specific_sliders


  def get_demo_rax_bottom():
    max_widget_qty = get_max_specific_sliders() + len(
      common_params_dict_definition) + 1
    demo_rax_bottom = max_widget_qty * (widget_params['height'] +
                                        widget_params['gap'])
    demo_rax_bottom += figure_params['plot_bottom_gap']
    return demo_rax_bottom


  x0 = 0.5 - figure_params['left_right_gap']
  background_rectangle = {
    side: plt.Rectangle(xy=(left, 0),
                        width=x0,
                        height=1,
                        color=find_color_code(demo_style[side][""]["color"]),
                        alpha=figure_params['left_right_opacity'],
                        zorder=-default_extreme_layer_nb,
                        fill=True,
                        transform=fig.transFigure,
                        figure=fig)
    for side, left in [['left', 0], ['right', 1 - x0]]
  }

  plot_ax_left = 2 * (widget_params['radio_side_margin'] +
                      widget_params['radio_width']) + figure_params['plot_gap']
  plot_ax_bottom = get_demo_rax_bottom() + figure_params['plot_bottom_gap']

  white_rectangle = plt.Rectangle(
    xy=(plot_ax_left - figure_params['add_width_to_axes_background'],
        plot_ax_bottom - figure_params['add_height_to_axes_background']),
    width=1 - 2 * (plot_ax_left - figure_params['add_width_to_axes_background']),
    height=1 - plot_ax_bottom + figure_params['add_height_to_axes_background'],
    color="white",
    alpha=1,
    zorder=-default_extreme_layer_nb + 1,
    fill=True,
    transform=fig.transFigure,
    figure=fig)

  fig.patches.extend([background_rectangle[side]
                      for side in sides] + [white_rectangle])

  x1 = widget_params['radio_side_margin'] * 1.5 + widget_params['radio_width']
  y1 = figure_params['plot_bottom_gap'] + (
    len(common_params_dict_definition) -
    1) * (widget_params['height'] +
          widget_params['gap']) - 0.5 * widget_params['gap']
  hatched_polygon_xy = {
    'left': np.array([[x0, 0], [0, 0], [0, 1], [x1, 1], [x1, y1], [x0, y1]])
  }
  hatched_polygon_xy['right'] = hatched_polygon_xy['left'].copy()
  hatched_polygon_xy['right'][:, 0] = 1 - hatched_polygon_xy['right'][:, 0]
  hatched_polygon = {
    side: plt.Polygon(xy=hatched_polygon_xy[side],
                      closed=True,
                      fill=False,
                      hatch='***',
                      lw=0,
                      color='white',
                      zorder=-default_extreme_layer_nb + 2,
                      transform=fig.transFigure,
                      figure=fig)
    for side in sides
  }

  fig.patches.extend(hatched_polygon.values())

  ##########################################################################################
  # Creating the canvas!
  ##########################################################################################

  main_ax = _find_scale_place_axes(
    max_width=1 - 2 *
    (plot_ax_left - figure_params['add_width_to_axes_background']),
    max_height=1 - plot_ax_bottom +
    figure_params['add_height_to_axes_background'] -
    (widget_params['height'] + 10 * widget_params['gap']),
    canvas_width=canvas_width,
    canvas_height=canvas_height,
    min_margin=0,
    font_size={
      l: figure_params['font_size']
      for l in ['axes_label', 'axes_tick']
    },
    title_pad=0,
    xlabel=figure_params['x_axis_label'],
    ylabel=figure_params['y_axis_label'],
    tick_step_x=figure_params['tick_step'], tick_step_y=figure_params['tick_step'],
    xy=(plot_ax_left,# - figure_params['add_width_to_axes_background'],
        plot_ax_bottom + 3 * figure_params['add_height_to_axes_background']
        ))

  canvas_parameters = {
    'canvas_width': canvas_width,
    'canvas_height': canvas_height,
    'tick_step': figure_params['tick_step'],
    'axes_label_font_size': figure_params['font_size'],
    'axes_tick_font_size': figure_params['font_size']
  }
  create_canvas_and_axes(**canvas_parameters, axes=main_ax)


  ##########################################################################################
  def dump_py_file():
    active_shapename_draw_function = {
      side: "draw_" + active_shapename[side]
      for side in sides if active_shapename[side] is not None
    }

    def param_dict_to_str(param_dict_):
      result = [
        key + '=' + (str(value) if not isinstance(value, str) else '"' + value + '"')
          for key, value in param_dict_.items()
      ]
      return result

    removable_values = {
      'turn': 0,
      'stretch': 1,
      'color': 'none',
      'diamond_color': 'cyan',
      'outline_linewidth': 0.,
      'outline_color': 'black',
      'opacity': 1.,
      'outline_joinstyle': 'straight',
      'joinstyle': 'straight',
      'linewidth': 2.,
      'capstyle': 'straight'
    }

    file_contents = [
      "# This file is regenerated every time you press 'Dump Python File' button",
      "# Rename it if you want to keep the contents", "",
      "from zyxxy2 import create_canvas_and_axes, show_and_save",
      "from zyxxy2 import " +
      ", ".join(active_shapename_draw_function.values()), "",
      "create_canvas_and_axes(" + ', '.join(
        param_dict_to_str(
          {k: v
          for k, v in canvas_parameters.items() if 'font' not in k})) + ")", ""
    ]

    kwargs_shape, kwargs_common, kwarg_style_widgets, kwargs_style_widgets_shapetype, layer_nbs = {}, {}, {}, {}, {}
    for side in sides:
      kwargs_shape[side], kwargs_common[side] = get_shape_kwargs(side=side)
      style_widgets_side = style_widgets_side_by_shapetype[side][""]
      style_widgets_shapetype_side = style_widgets_side_by_shapetype[side][
        get_active_shapetype(side)]
      for dict_ in [style_widgets_side, style_widgets_shapetype_side]:
        if 'text' in dict_:
          del dict_['text']
      kwarg_style_widgets[side] = {
        key: get_widget_value(value)
        for key, value in style_widgets_side.items()
      }
      kwargs_style_widgets_shapetype[side] = {
        key: get_widget_value(value)
        for key, value in style_widgets_shapetype_side.items()
      }

      for dict_ in [
          kwargs_shape, kwargs_common, kwarg_style_widgets,
          kwargs_style_widgets_shapetype
      ]:
        keys_to_remove = []
        for r_key, r_value in removable_values.items():
          if r_key in dict_[side]:
            if equal_or_almost(dict_[side][r_key], r_value):
              keys_to_remove += [r_key]
        for key_ in keys_to_remove:
          del dict_[side][key_]

      layer_nbs[side] = {
        key: value
        for key, value in kwargs_style_widgets_shapetype[side].items()
        if 'layer_nb' in key
      }
      layer_nbs[side]['layer_nb'] = kwarg_style_widgets[side]['layer_nb']

    remove_layer_nb = equal_or_almost(layer_nbs['left']['layer_nb'],
                                      layer_nbs['right']['layer_nb'])
    if 'outline_layer_nb' in layer_nbs['left']:
      remove_layer_nb = remove_layer_nb and equal_or_almost(
        layer_nbs['left']['outline_layer_nb'], layer_nbs['right']['layer_nb'])
    if 'outline_layer_nb' in layer_nbs['right']:
      remove_layer_nb = remove_layer_nb and equal_or_almost(
        layer_nbs['left']['layer_nb'], layer_nbs['right']['outline_layer_nb'])
    if remove_layer_nb:
      for side in sides:
        del kwarg_style_widgets[side]['layer_nb']
        if 'outline_layer_nb' in kwargs_style_widgets_shapetype[side]:
          del kwargs_style_widgets_shapetype[side]['outline_layer_nb']

    for side in sides:
      parameters = []
      for dict_ in [
          kwargs_shape, kwargs_common, kwarg_style_widgets,
          kwargs_style_widgets_shapetype
      ]:
        parameters += param_dict_to_str(dict_[side])[::-1]
      file_contents += [
        active_shapename_draw_function[side] + '(' + ", ".join(parameters) + ')'
      ]

    file_contents += ["", "show_and_save()"]

    return file_contents


  def write_file_wrapper(event):
    write_file(filename_="my_demo_dump.py", contents_func=dump_py_file)

  _, dump_py_file_button, _ = add_a_button(
    w_left=plot_ax_left + 6 * widget_params['gap'],
    w_bottom=1 - (widget_params['height'] + 3 * widget_params['gap']),
    w_width=get_default_widget_width(),
    w_caption='Dump Python File',
    on_click_or_change=write_file_wrapper)


  ##########################################################################################
  def get_active_shapetype(side):
    shapetype = get_type_given_shapename(shapename=active_shapename[side])
    return shapetype


  def get_active_shape(side):
    _shape = shapes_by_side_by_shapetype[side][get_active_shapetype(side=side)]
    return _shape


  ##########################################################################################
  def get_shape_kwargs(side, stretch_direction_coeff={}):
    kwargs_shape = {
      silder_.label.get_text(): silder_.val
      for silder_ in specific_widgets_by_side[side] if silder_.ax.get_visible()
    }

    _widgets_common = common_widgets_by_side[side]
    common_keys_for_shape = _get_common_keys_for_shape(
      shapename=active_shapename[side])

    kwargs_common = {
      key: value
      for key, value in stretch_direction_coeff.items()
    }
    for key in _widgets_common.keys():
      if key not in ["stretch_direction", "stretch_coeff"]:
        kwargs_common[common_keys_for_shape[key]] = get_widget_value(
          _widgets_common[key])

    return kwargs_shape, kwargs_common


  ##########################################################################################
  def update_shape_form_given_side(_, side, stretch_direction_coeff={}):

    if TURN_OFF_XY_UPDATE:
      return

    kwargs_shape, kwargs_common = get_shape_kwargs(
      side=side, stretch_direction_coeff=stretch_direction_coeff)

    _shape = get_active_shape(side=side)
    _shape.reset_given_shapename_and_arguments_and_move(active_shapename[side],
                                                        kwargs_shape,
                                                        kwargs_common)

    fig.canvas.draw_idle()


  ##################################################################################
  def get_left_adj(param_name):

    left_adj = {
      "stretch_direction": 0.13,
      "stretch_coeff": 0.03,
      'angle_top_middle': 0.033,  #heart
      'height_widest_point': 0.048,  # egg
      'nb_intermediate_points': 0.053,  # power curve
      'nb_segments': 0.01,  #zigzag
      'angle_start': 0.01
    }
    result = left_adj[param_name] if param_name in left_adj else 0
    return result


  ##########################################################################################
  def update_visibility(side, switch_on):

    #shape visibility
    _shape = shapes_by_side_by_shapetype[side][get_active_shapetype(side=side)]
    _shape.set_visible(switch_on)

    spec_param_dict = specific_inputs_values_by_shapename[active_shapename[side]]
    current_slider_nb = 0

    for param_name in spec_param_dict.keys():
      current_slider_nb -= 1
      current_slider = specific_widgets_by_side[side][current_slider_nb]
      set_widget_visible(current_slider, switch_on)
      axes_box = current_slider.ax.get_position().bounds
      axes_height = axes_box[3]
      axes_bottom = axes_box[1]
      current_slider.ax.set_position(pos=[
        figure_params['widget_lefts'][side] +
        get_left_adj(param_name), axes_bottom,
        get_default_widget_width() - get_left_adj(param_name), axes_height
      ])

      if switch_on:
        set_slider_values(slider=current_slider,
                          val=specific_widgets_values_by_side_by_shapename[side][
                            active_shapename[side]][param_name],
                          label=param_name,
                          **spec_param_dict[param_name])
      else:
        if current_slider.label.get_text() == param_name:
          specific_widgets_values_by_side_by_shapename[side][
            active_shapename[side]][param_name] = current_slider.val

    for i in range(get_max_specific_sliders() + current_slider_nb):
      set_widget_visible(specific_widgets_by_side[side][i], False)

    # style widgets visibility
    patch_or_line = get_active_shapetype(side=side)
    for key, sw_or_all_texts in style_widgets_side_by_shapetype[side][
        patch_or_line].items():
      if key == "text":
        for t in sw_or_all_texts:
          t.set_visible(switch_on)
      else:
        set_widget_visible(sw_or_all_texts, switch_on)


  ##########################################################################################
  def switch_active_shapename_given_side(label, side):

    nonlocal TURN_OFF_XY_UPDATE
    TURN_OFF_XY_UPDATE = True

    if active_shapename[side] is not None:
      update_visibility(side=side, switch_on=False)
    else:
      for patch_or_line in shape_types:
        _shape = shapes_by_side_by_shapetype[side][patch_or_line]
        _shape.set_visible(False)
        for key, sw_or_all_texts in style_widgets_side_by_shapetype[side][
            patch_or_line].items():
          if key == "text":
            for t in sw_or_all_texts:
              t.set_visible(False)
          else:
            set_widget_visible(sw_or_all_texts, False)

    active_shapename[side] = label
    update_visibility(side=side, switch_on=True)

    # update diamond labels
    common_keys_for_shape = _get_common_keys_for_shape(
      shapename=active_shapename[side])
    for diam_name in ["diamond_x", "diamond_y"]:
      common_widgets_by_side[side][diam_name].label.set_text(
        common_keys_for_shape[diam_name])

    TURN_OFF_XY_UPDATE = False
    update_shape_form_given_side(None, side=side)

    fig.canvas.draw_idle()


  ##########################################################################################
  def reset(_, side):
    for w in specific_widgets_by_side[side]:
      reset_widget(a_widget=w)
    for w in common_widgets_by_side[side].values():
      reset_widget(a_widget=w)


  ##########################################################################################
  def stretch_with_direction(_, side):
    slider_coeff = common_widgets_by_side[side]["stretch_coeff"]
    slider_direction = common_widgets_by_side[side]["stretch_direction"]
    update_shape_form_given_side(None,
                                side=side,
                                stretch_direction_coeff={
                                  "stretch_direction":
                                  get_widget_value(slider_direction),
                                  "stretch_coeff":
                                  get_widget_value(slider_coeff)
                                })


  ##########################################################################################
  def update_shape_style(_, side, shapetype, argname):
    argvalue = get_widget_value(
      style_widgets_side_by_shapetype[side][shapetype][argname])
    if argname not in ['color', 'diamond_color', 'layer_nb']:
      shapes_by_side_by_shapetype[side][shapetype].set_style(
        **{argname: argvalue})
    else:
      shapes_by_side_by_shapetype[side]['line'].set_style(**{argname: argvalue})
      shapes_by_side_by_shapetype[side]['patch'].set_style(**{argname: argvalue})
      if argname == 'color':
        background_rectangle[side].set_facecolor(find_color_code(argvalue))
        hatched_polygon[side].set_color('lightgrey' if argvalue ==
                                        'none' else 'white')

    fig.canvas.draw_idle()


  #########################################################################################
  # create shapestyle widgets
  def place_style_widgets(side, shapetype, arg_category, w_left, w_bottom):

    captions_init_values = demo_style[side][arg_category]
    if arg_category not in ['diamond', '']:
      for key, value in default_color_etc_settings[arg_category].items():
        if key not in captions_init_values:
          if key not in ['color', 'layer_nb'] or arg_category == "outline":
            captions_init_values[key] = value

    where_to_add = style_widgets_side_by_shapetype[side][shapetype]  # a shortcut
    for argname, init_value in captions_init_values.items():
      w_options = demo_style_widgets_value_ranges[argname]

      if not isinstance(w_options[0], str):
        w_options[2] = init_value
        func_name = functools.partial(add_a_slider,
                                      s_vals=w_options,
                                      caption_in_the_same_line=False)
      else:
        func_name = functools.partial(add_vertical_radio_buttons,
                                      rb_options=w_options,
                                      active_option=init_value)

      prefixed_caption = arg_category + "_" + argname if arg_category in [
        "diamond", "outline"
      ] else argname
      on_click_or_change = functools.partial(update_shape_style,
                                            side=side,
                                            shapetype=shapetype,
                                            argname=prefixed_caption)
      w_bottom, where_to_add[prefixed_caption], added_text = func_name(
        w_left=w_left,
        w_bottom=w_bottom,
        w_caption=prefixed_caption,
        on_click_or_change=on_click_or_change)

      if added_text is not None:
        where_to_add['text'].append(added_text)

    return w_bottom


  ##################################################################################
  def place_shapes_and_widgets(side):
    # placing the shapes_by_side_by_shapetype
    shapes_by_side_by_shapetype[side] = {
      shapetype: Shape(ax=main_ax, shapetype=shapetype)
      for shapetype in shape_types
    }

    # adding style widgets
    set_default_widget_width(widget_params['radio_width'] * .9)
    w_left = widget_params[
      'radio_side_margin'] if side == "left" else 1 - widget_params[
        'radio_width'] - widget_params['radio_side_margin']

    new_bottom = place_style_widgets(side=side,
                                    shapetype='',
                                    arg_category='diamond',
                                    w_left=w_left,
                                    w_bottom=figure_params['plot_bottom_gap'])

    new_bottom = place_style_widgets(side=side,
                                    shapetype='',
                                    arg_category='',
                                    w_left=w_left,
                                    w_bottom=new_bottom)

    _ = place_style_widgets(side=side,
                            shapetype='line',
                            arg_category='line',
                            w_left=w_left,
                            w_bottom=new_bottom)

    new_bottom = place_style_widgets(side=side,
                                    shapetype='patch',
                                    arg_category='patch',
                                    w_left=w_left,
                                    w_bottom=new_bottom)

    _ = place_style_widgets(side=side,
                            shapetype='patch',
                            arg_category='outline',
                            w_left=w_left,
                            w_bottom=new_bottom)

    # adding shapename switchers
    set_default_widget_width(widget_params['radio_width'])
    rax_left = widget_params['radio_side_margin'] * 2 + widget_params[
      'radio_width'] if side == 'left' else 1 - 2 * (
        widget_params['radio_width'] + widget_params['radio_side_margin'])
    _, shape_switchers[side], _ = add_vertical_radio_buttons(
      rb_options=[k for k in shape_names_params_dicts_definition.keys()],
      w_left=rax_left,
      w_bottom=get_demo_rax_bottom(),
      w_caption="shapenames",
      active_option=demo_shapes[side])

    shape_switchers[side].on_clicked(
      functools.partial(switch_active_shapename_given_side, side=side))

    # adding common form parameters sliders
    set_default_widget_width(widget_params['width'])

    new_bottom = figure_params['plot_bottom_gap']
    w_left = figure_params['widget_lefts'][side]

    new_bottom, reset_button[side], _ = add_a_button(
      w_left=w_left,
      w_bottom=new_bottom,
      w_caption='Reset',
      on_click_or_change=functools.partial(reset, side=side))

    upd_shape_given_side = functools.partial(update_shape_form_given_side,
                                            side=side)

    for param_name, slider_range_name in common_params_dict_definition.items():

      current_bottom = new_bottom
      new_bottom, common_widgets_by_side[side][param_name], _ = add_a_slider(
        w_bottom=new_bottom,
        w_left=w_left + get_left_adj(param_name),
        w_width=get_default_widget_width() - get_left_adj(param_name),
        w_caption=param_name if
        (param_name != "stretch_direction") else "direction",
        s_vals=np.copy(slider_range[slider_range_name]),
        on_click_or_change=upd_shape_given_side if
        (param_name not in ["stretch_direction", "stretch_coeff"]) else None)

      if (param_name == "stretch_direction"):
        new_bottom, stretch_button[side], _ = add_a_button(
          w_bottom=current_bottom,
          w_left=w_left - 0.055,
          w_width=get_default_widget_width() * 0.47,
          w_caption="stretch_with_direction",
          on_click_or_change=functools.partial(stretch_with_direction,
                                              side=side))

    # ... and specific sliders
    for s in range(get_max_specific_sliders()):
      new_bottom, s_slider, _ = add_a_slider(
        w_left=figure_params['widget_lefts'][side],
        w_width=get_default_widget_width(),
        w_bottom=new_bottom,
        w_caption="Dummy",  #todo: add dummies
        s_vals=[0, 1, 1 / 2, 1 / 2],
        on_click_or_change=upd_shape_given_side)
      specific_widgets_by_side[side] += [s_slider]

    # ... and style!
    for st in shape_types:
      style_widgets = {}
      for dict_ in [
          style_widgets_side_by_shapetype[side][st],
          style_widgets_side_by_shapetype[side][""]
      ]:
        for key, value in dict_.items():
          style_widgets[key] = value
      kwargs_style = {
        key: get_widget_value(style_widgets[key])
        for key in style_widgets.keys() if key != 'text'
      }
      shapes_by_side_by_shapetype[side][st].set_style(**kwargs_style)

    # ... and  switch on those that need to be active!
    switch_active_shapename_given_side(label=demo_shapes[side],
                                      side=side)


  # placing the shapes and widgets
  for side in sides:
    place_shapes_and_widgets(side=side)

  show_demo()
