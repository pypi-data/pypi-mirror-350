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
from . import examples, shape_style, coordinates, shape_class

##################################################################
def _get_functions_from_a_file(module_):
  def linenumber_of_member(m):
    return m[1].__code__.co_firstlineno

  all_functions_list = inspect.getmembers(module_, inspect.isfunction)
  all_functions_list = [f for f in all_functions_list if inspect.getmodule(f[1]) == module_ and not(f[0].startswith('_'))]
  
  all_functions_list.sort(key=linenumber_of_member)
  return all_functions_list

##################################################################
def _get_members_of_a_class(class_):
  def linenumber_of_member(m):
    return m[1].__code__.co_firstlineno

  all_functions_list = inspect.getmembers(class_, inspect.isfunction)
  all_functions_list = [f for f in all_functions_list if not(f[0].startswith('_'))]
  
  all_functions_list.sort(key=linenumber_of_member)
  return all_functions_list

##################################################################
def _get_function_comment(f_object):
  comments = inspect.getcomments(f_object)
  if comments is None:
    return []
  while comments.count("  "):
    comments = comments.replace("  ", " ")
  comments = comments.split("\n")
  comments = [c_line for c_line in comments if len([s for s in c_line if s not in ['#', ' ']]) != 0]
  if len(comments):
    comments = [""] + comments
  return comments

##################################################################
def _function_with_comments_and_arguments(f_name, f_object, class_name=None):

  func_args_object = inspect.getfullargspec(f_object)
  func_args_line = [a for a in func_args_object.args if a != 'self'] if func_args_object.args is not None else []
  if func_args_object.defaults is not None:
    for i, d in enumerate(reversed(func_args_object.defaults)):
      func_args_line[len(func_args_line)-1-i] += '='+str(d)

  result = f_name + '(' + ', '.join(func_args_line) + ')'
  if class_name is not None:
    result = "<an instance of " + class_name + ">."+result
  comments = _get_function_comment(f_object=f_object)

  result = comments + [result]

  return result

##################################################################
def get_shape_creating_functions(shapetype):

    if shapetype is None:
      return ["clone_a_shape(init_shape)"]

    result = []
    for shapename, params in coordinates.shape_names_params_dicts_definition.items():
      if (shapename in coordinates.line_shapes) != (shapetype == "line"):
        continue
      if shapename not in coordinates.bespoke_diamonds:
        ds = "center_x, center_y"
      elif isinstance(coordinates.bespoke_diamonds[shapename], str):
        d = coordinates.bespoke_diamonds[shapename]
        ds = d + "_x, " + d + "_y"
      else:
        ds =  ", ".join([str(d) for d in coordinates.bespoke_diamonds[shapename]])
      result += ["draw_" + shapename + "(" + ds + ', ' + ", ".join([k for k in params.keys()]) + ')']

    result += ["draw_" + ("a_broken_line" if shapetype == "line" else "a_polygon" ) + "(diamond_x, diamond_y, contour)"]
    result += ["", "Admissible Style Arguments:"] + ['  ' + ', '.join(shape_style.get_admissible_style_arguments(shapetype))]
    result += ["", "Admissible Movement Arguments:"] + ['  ' + ', '.join(["turn", "stretch", "stretch_direction (optional)"])]

    return result

def get_functions_subsection(title, module, func_list_function_override=None, import_needed=True):
    result = ["", "##############################################################################", "", title]
    if import_needed:
      result += ["from " + module.__name__ + " import"]
    else:
      result += ["(no import required)"]
    result += [""]
    if func_list_function_override is not None:
      result += func_list_function_override()
    else:
      _functions = _get_functions_from_a_file(module_=module)
      for uf, uf_object in _functions:
        result += _function_with_comments_and_arguments(f_name=uf, f_object=uf_object)
    return result

def get_Shape_members():
    result = []
    shape_methods = _get_members_of_a_class(shape_class.Shape)
    for sf, sf_obj in shape_methods:
      result += _function_with_comments_and_arguments(f_name=sf, f_object=sf_obj, class_name="Shape")
    return result

def get_style_functions():
    result = []
    for shapetype in ["line", "patch"]:
      asa = shape_style.get_admissible_style_arguments(shapetype)
      result += ["set_default_" + shapetype + '_style(' + ', '.join(asa) + ')']
    result += ['set_default_outline_style(' + ', '.join(shape_style.line_arg_types) + ')', ""]

    style_functions = _get_functions_from_a_file(module_=shape_style)
    style_functions = [sf for sf in style_functions if sf[0].startswith("set_default_") and not sf[0].endswith('_style')]
    for sf in style_functions:
      if 'layer_nb' in sf[0]:
        result += _function_with_comments_and_arguments(f_name=sf[0], f_object=sf[1])
      else:
        result += _get_function_comment(f_object=sf[1]) + [sf[0]+"(<just enter parameter value, no name is needed>)"] 
    return result

def generate_function_list():
  from . import utils, colors, layers, shape_functions
  from functools import partial

  func_ref_cont = []
  for shapetype in ["patch", "line", None]:
    if shapetype is None:
      title = "Another Function That Can Create A Shape"
    else: 
      title="Functions That Create " + ("Lines" if shapetype == "line" else "Patches")
    func_ref_cont += get_functions_subsection(title=title,
                                              module=shape_functions,
                                              func_list_function_override=partial(get_shape_creating_functions, shapetype=shapetype))
  func_ref_cont  += ( get_functions_subsection(title="Layer-Related Functions", module=layers)
                    + get_functions_subsection(title="Default Shape Style-Related Functions", 
                                               module=shape_style,
                                               func_list_function_override=get_style_functions)
                    + get_functions_subsection(title="Utility Functions", module=utils)
                    + get_functions_subsection(title="Default Shape Style-Related Functions", 
                                               module=shape_class, import_needed=False,
                                               func_list_function_override=get_Shape_members)
                    + get_functions_subsection(title="color-Related Functions", module=colors))

  func_ref_cont += get_functions_subsection(title="Functions That Create Examples",
                                              module=examples)
  return func_ref_cont
