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
import matplotlib.pyplot as plt

from .settings import default_color_etc_settings as default_color_etc_settings_, \
                      default_text_bubble_params as default_text_bubble_params_, \
                      default_diamond_size, default_outlines_width, default_extreme_layer_nb, screen_zoom
from .colors import find_color_code

########################################################################

line_arg_types = ["color", "layer_nb", "linewidth", "joinstyle", "capstyle"]
patch_arg_types = ["color", "layer_nb", "opacity"]

format_arg_dict = {
  "line": line_arg_types,
  "patch": patch_arg_types,
  "outline": line_arg_types,
  "diamond": patch_arg_types
}

########################################################################

__diamond_size_factor = 1.


#default value for the diamond_size_factor is 1.0
def set_default_diamond_size_factor(value=1.):
  global __diamond_size_factor
  __diamond_size_factor = float(value)


default_color_etc_settings = copy.deepcopy(default_color_etc_settings_)
default_text_bubble_params = copy.deepcopy(default_text_bubble_params_)

def get_default_text_bubble_params(name):
  return default_text_bubble_params[name]

def scale_default_fontsize(mult):
  global default_text_bubble_params
  default_text_bubble_params['fontsize'] *= mult

def reset_default_color_etc_settings(diamond_size_factor_override=1):
  global default_color_etc_settings, default_text_bubble_params, __diamond_size_factor
  default_color_etc_settings = copy.deepcopy(default_color_etc_settings)
  default_text_bubble_params = copy.deepcopy(default_text_bubble_params)
  __diamond_size_factor = diamond_size_factor_override


def set_default_color_etc_settings(saved_settings):
  global default_color_etc_settings, default_text_bubble_params, __diamond_size_factor
  default_color_etc_settings = copy.deepcopy(
    saved_settings['color_etc_settings'])
  default_text_bubble_params = copy.deepcopy(
    saved_settings['text_bubble_params'])
  __diamond_size_factor = saved_settings['diamond_size_factor']


def get_default_color_etc_settings():
  saved_settings = {
    'color_etc_settings': copy.deepcopy(default_color_etc_settings),
    'text_bubble_params': copy.deepcopy(default_text_bubble_params),
    'diamond_size_factor': __diamond_size_factor
  }
  return saved_settings

########################################################################

def raise_Exception_if_not_processed(kwarg_keys, allowed_keys):
  not_processed = [
    arg_name for arg_name in kwarg_keys if arg_name not in allowed_keys
  ]
  if len(not_processed) > 0:
    raise Exception("Arguments", ', '.join(not_processed),
                    " are not recognised, allowed keys:", allowed_keys)


########################################################################

OUTLINES_color = None
OUTLINES_diamond_color = None


def set_trace_color(val):
  global OUTLINES_color
  OUTLINES_color = None if val is None else find_color_code(val)


def get_trace_color():
  global OUTLINES_color
  return OUTLINES_color


def set_trace_diamond_color(val):
  global OUTLINES_diamond_color
  OUTLINES_diamond_color = None if val is None else find_color_code(val)


def get_trace_diamond_color():
  global OUTLINES_diamond_color
  return OUTLINES_diamond_color


########################################################################


def get_admissible_style_arguments(shapetype):
  d_args = ["diamond_color"]
  if shapetype == "line":
    return line_arg_types + d_args
  if shapetype == "patch":
    return patch_arg_types + ["outline_" + a for a in line_arg_types] + d_args
  raise Exception(shapetype, "not recognised")


########################################################################
# as defined by matplotlib
# in https://matplotlib.org/stable/gallery/lines_bars_and_markers/joinstyle.html

__joinstyle_dict = {
  'rounded': 'round',
  'straight': 'miter',
  'cut off': 'bevel'
}
__capstyle_disc = {
  'rounded': 'round',
  'straight': 'projecting',
  'cut off': 'butt'
}


def __to_joinstyle(a_corner_style):
  if a_corner_style in __joinstyle_dict:
    return __joinstyle_dict[a_corner_style]
  raise Exception(
    f"{a_corner_style} is invalid, the only valid corner_styles are {', '.join([k for k in __joinstyle_dict.keys()])}"
  )


def __to_capstyle(an_ending_style):
  if an_ending_style in __capstyle_disc:
    return __capstyle_disc[an_ending_style]
  raise Exception(
    f"{an_ending_style} is invalid, the only valid ending_styles are {', '.join([k for k in __capstyle_disc.keys()])}"
  )


def __from_joinstyle(a_joinstyle):
  for _corner_style, _joinstyle in __joinstyle_dict.items():
    if a_joinstyle == _joinstyle:
      return _corner_style
  raise Exception(
    f"{a_joinstyle} is invalid, the only valid joinstyles are {', '.join([k for k in __joinstyle_dict.values()])}"
  )


def __from_capstyle(a_capstyle):
  for _ending_style, _capstyle in __capstyle_disc.items():
    if a_capstyle == _capstyle:
      return _ending_style
  raise Exception(
    f"{a_capstyle} is invalid, the only valid capstyles are {', '.join([k for k in __capstyle_disc.values()])}"
  )


################################################################################################################################################
style_params_howto = [["layer_nb", 'zorder', "patch|line|outline", None, None],
                      ["opacity", 'alpha', "patch|line|outline", None, None],
                      ["color", 'fc', "patch", find_color_code, None],
                      ["color", 'ec', "line|outline", find_color_code, None],
                      ["linestyle", 'linestyle', "line|outline", None, None],
                      ["linewidth", 'lw', "line|outline", None, None],
                      [
                        "corner_style", 'joinstyle', "line|outline",
                        __to_joinstyle, __from_joinstyle
                      ],
                      [
                        "ending_style", 'capstyle', "line|outline",
                        __to_capstyle, __from_capstyle
                      ]]


################################################################################################################################################
def get_polygon_style(attr_name, style_name, parent, attr_override=None):
  something = attr_override if attr_override else getattr(
    parent, attr_name)
  assert something is not None
  polys = []
  for zyxxy_name, mpl_name, poly_str, _, tranf_m_z in style_params_howto:
    if zyxxy_name == style_name:
      polys = poly_str.split('|')
      if attr_name in polys:
        result = getattr(something, f'get_{mpl_name}')()
        if zyxxy_name == "linewidth":
          result = tranf_m_z(result, parent=parent)
        elif tranf_m_z is not None:
          result = tranf_m_z(result)
        return result
  if not (polys):
    raise Exception(f'Style {style_name} does not exist')
  else:
    raise Exception(f'Can only get {style_name} for {", ".join(polys)}')


########################################################################

def set_polygon_style(something, linewidth_factor, attr_name, kwargs=None):

  if kwargs is None or (not kwargs):
    kwargs = default_color_etc_settings[attr_name]

  if OUTLINES_color is not None:
    something.set_fc('none')
    something.set_ec(OUTLINES_color)
    something.set_lw(default_outlines_width / linewidth_factor)
    something.set_linestyle('--')
    something.set_zorder(default_extreme_layer_nb)
  else:
    if "line" in attr_name:
      something.set_fc('none')
      something.set_linestyle('solid')
      if "color" in kwargs:
        something.set_ec(find_color_code(kwargs['color']))
      if "linewidth" in kwargs:
        something.set_lw(kwargs['linewidth'] / linewidth_factor)
      if "layer_nb" in kwargs:
        something.set_zorder(kwargs['layer_nb'])
    else:
      something.set_ec('none')
      if "color" in kwargs:
        something.set_fc(find_color_code(kwargs['color']))
      if "layer_nb" in kwargs:
        something.set_zorder(kwargs['layer_nb'])
      if "opacity" in kwargs:
        something.set_alpha(kwargs['opacity'])

  if OUTLINES_color is not None or "line" in attr_name:
    if "joinstyle" in kwargs:
      something.set_joinstyle(__to_joinstyle(kwargs['joinstyle']))
    if 'capstyle' in kwargs:
      something.set_capstyle(__to_capstyle(kwargs['capstyle']))


########################################################################


def _set_default_style(what, **kwargs):
  if what == 'text':
    global default_text_bubble_params
    raise_Exception_if_not_processed(
      kwarg_keys=kwargs.keys(),
      allowed_keys=default_text_bubble_params.keys())
    for ua in kwargs.keys():
      default_text_bubble_params[ua] = kwargs[ua]
  else:
    global default_color_etc_settings
    raise_Exception_if_not_processed(
      kwarg_keys=kwargs.keys(),
      allowed_keys=default_color_etc_settings[what].keys())
    for ua in kwargs.keys():
      default_color_etc_settings[what][ua] = kwargs[ua]


def set_default_line_style(**kwargs):
  _set_default_style(what='line', **kwargs)


def set_default_patch_style(**kwargs):
  _set_default_style(what='patch', **kwargs)


def set_default_outline_style(**kwargs):
  _set_default_style(what='outline', **kwargs)


def set_default_diamond_style(**kwargs):
  _set_default_style(what='diamond', **kwargs)

def set_default_text_style(**kwargs):
  _set_default_style(what='text', **kwargs)


def set_default_patch_color(color):
  set_default_patch_style(color=color)


def set_default_line_color(color):
  set_default_line_style(color=color)


def set_default_diamond_color(color):
  set_default_diamond_style(color=color)


def set_default_linewidth(linewidth):
  set_default_line_style(linewidth=linewidth)
  set_default_outline_style(linewidth=linewidth)


##################################################################


def get_top_layer_nb():
  top_layer_nb = max([
    default_color_etc_settings[fa]['layer_nb']
    for fa in format_arg_dict.keys() if fa != 'diamond'
  ])
  return top_layer_nb


def set_default_layer_nb(what, layer_nb):
  _set_default_style(what=what, layer_nb=layer_nb)
