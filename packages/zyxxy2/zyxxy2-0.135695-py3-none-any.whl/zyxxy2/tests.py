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

import os, shutil, datetime
import numpy as np

from .shape_class import Shape
from .colors import create_gradient_colors
from .utils import is_the_same_point, random_integer_number
from .canvas import set_folder_for_saving, reset_folder_for_saving, _is_running_tests
from .files import compare_images, execute_example_or_module, write_file
from . import examples
from .docs import _get_functions_from_a_file, generate_function_list
from .shape_functions import draw_a_rectangle, clone_a_shape, draw_a_segment, draw_a_rectangle, draw_a_polygon, draw_a_broken_line
from .canvas import create_canvas_and_axes
from .utils import is_the_same_contour, conc_contours #, is_the_same_point

def _run_all_tests():
  _ = _is_running_tests(True)
  TEST_FOLDER = "test_files"
  CURRENT_SUBFOLDER = None

  ##################################################################
  def prepare_folder(folder_name):
    nonlocal CURRENT_SUBFOLDER
    if not os.path.exists(TEST_FOLDER):
      os.makedirs(TEST_FOLDER)
    CURRENT_SUBFOLDER = folder_name
    long_folder_name = os.path.join(TEST_FOLDER, 'test_' + folder_name)
    
    if os.path.exists(long_folder_name): # if the folder exists, just remove it
      shutil.rmtree(long_folder_name)
    os.makedirs(long_folder_name)
    set_folder_for_saving(folder_name=long_folder_name)
    print("Preparing folder", long_folder_name)

  ##################################################################
  def check_folder(folder_to_check=None):

    if folder_to_check is None:
      folder_to_check = CURRENT_SUBFOLDER

    files = {key: [f for f in os.listdir(os.path.join(TEST_FOLDER, key + '_' + folder_to_check)) if os.path.isfile(os.path.join(TEST_FOLDER, key + '_' + folder_to_check, f))] for key in ['test', 'benchmark']}

    errors = []
    for f in files['test']:
      if f not in files['benchmark']:
        errors.append('File ' + f + ' is in test_' + folder_to_check + ' but not in benchmark_' + folder_to_check)
    for f in files['benchmark']:
      if f not in files['test']:
        errors.append('File ' + f + ' is in benchmark_' + folder_to_check + ' but not in test_' + folder_to_check)

    print("compared file lists")

    for f in files['test']:
      if f in files['benchmark']:
        dist = compare_images(image_to_test_filename   = os.path.join(TEST_FOLDER, 'test_' + folder_to_check, f), 
                              image_benchmark_filename = os.path.join(TEST_FOLDER, 'benchmark_' + folder_to_check, f))
        if dist > 0:
          errors.append('Files ' + f + ' are different, distance = ' + str(100 * dist) + '/%')
    
    for e_ in errors:
      print(e_)

    reset_folder_for_saving()

  ##################################################################

  all_drawings = [f for f in os.listdir('.') if os.path.isfile(f) and (f.startswith("draw") or f.startswith("demo_"))]
  all_drawings.sort()

  all_examples_list =_get_functions_from_a_file(module_=examples)
  all_examples_list.sort(key=lambda x: x[0])

  what_to_test = {"images" : [ae[1] for ae in all_examples_list if 'anima' not in ae[0]], 
                  "videos" : [ae[1] for ae in all_examples_list if 'anima' in ae[0]], 
                  "drawings" : all_drawings}

  ##################################################################
  def test_functions_or_modules(folder_name):
    prepare_folder(folder_name=folder_name)
    print("completed prepare_folder", folder_name)
    
    for example_or_module in what_to_test[folder_name]:
      execute_example_or_module(example_or_module)

    reset_folder_for_saving()

  ##################################################################
  n=0
  def test_rectangle():

    axes = create_canvas_and_axes(canvas_width = 18, canvas_height = 12)
    
    def compare_contours(s1, s2, **kwargs):
      nonlocal n
      p1 = s1.get_xy() if isinstance(s1, Shape) else s1
      p2 = s2.get_xy() if isinstance(s2, Shape) else s2

      #assert is_the_same_contour(p1=p1, p2=p2, **kwargs), "failed test " + str(n)
      #print("succeeded test " + str(n))
      n+=1

    assert is_the_same_contour(p1=np.array([[0, 0], [ 11408.64993208,  19760.36132812]]),
                              p2=np.array([[0, 0], [ 4.88330751e+48, -1.86079008e+49]])) == False

    # same rectangle, then with 0 turn, then stretched and turned, then with alternative diamonds
    r  = draw_a_rectangle(ax=axes, center_x=5, center_y=15, width=10, height=2)
    r0 = draw_a_rectangle(ax=axes, center_x=5, center_y=15, width=10, height=2, turn=0)
    r2 = clone_a_shape(r)
    r2.stretch_x(stretch=1/5)
    r2.stretch_y(stretch=5) #r2.stretch(stretch_x=1/5, stretch_y=5)
    r2.turn(turn=3)
    r3 = draw_a_rectangle(ax=axes, left=0, top=16, width=10, height=2)
    r4 = draw_a_rectangle(ax=axes, right=10, bottom=14, width=10, height=2)

    for other_r, kwargs in [[r0, {}], [r2, {'start_1':1}], [r3, {}], [r4, {}]]:
      try:
        compare_contours(s1=r, s2=other_r, **kwargs)
      except:
        raise Exception(n, r.get_xy(), other_r.get_xy())

    # make sure shift works
    for other_r_init in [r, r3, r4]:
      other_r = clone_a_shape(other_r_init)
      other_r.shift(shift=[101, 202])
      compare_contours(s1=r.get_xy() + [101, 202], s2=other_r)

    # make sure flipping works
    r001 = clone_a_shape(r) ; r001.flip_upside_down()
    r301 = clone_a_shape(r3); r301.flip_upside_down()
    r401 = clone_a_shape(r4); r401.flip_upside_down()
    compare_contours(r001.get_xy() + [0, 2], r301.get_xy())
    compare_contours(r001.get_xy() + [0,-2], r401.get_xy())

    # make sure rotation works
    r31 = clone_a_shape(r3); r31.turn(turn=6)
    r41 = clone_a_shape(r4); r41.turn(turn=6)
    compare_contours(r31.get_xy() + [20, -4], r41.get_xy())

    # make sure parameters update works
    r502 = clone_a_shape(r); r502.stretch_x(stretch=1/5); r502.stretch_y(stretch=50)
    r5033 = clone_a_shape(r);r5033.set_shape_parameters(width=2, height=100)
    compare_contours(r5033, r502)

    for start_x, start_y in [[0, 0], [10, 8]]:

      segm0 = draw_a_segment(start_x=start_x, start_y=start_y, length=3); 
      contour=[[start_x, start_y], [start_x, start_y+3]]
      broken_line0 = draw_a_broken_line(diamond_x=start_x, diamond_y=start_y, contour=contour)
      
      segm1 = clone_a_shape(segm0); bl1 = clone_a_shape(broken_line0);
      segm2 = clone_a_shape(segm0); bl2 = clone_a_shape(broken_line0);
      total_turn = 0
      for _ in range(20):
        stretch_direction = random_integer_number(-2, 2) * 3
        r_stretch = random_integer_number(-6, 6)
        r_turn2 = random_integer_number(-2, 2) * 3
        print("stretch_direction=", stretch_direction, "r_stretch=", r_stretch, "r_turn2=", r_turn2)
        segm1.stretch_with_direction(stretch_coeff=r_stretch,  direction=stretch_direction)
        bl1.stretch_with_direction(stretch_coeff=r_stretch,  direction=stretch_direction)
        segm1.turn(r_turn2)
        bl1.turn(r_turn2)

        total_turn += r_turn2

        segm2.reset_given_shapename_and_arguments_and_move(shapename="a_segment", 
                                                          kwargs_shape={'length':3}, 
                                                          kwargs_common={'start_x':0, 'start_y':0, 'stretch_coeff':r_stretch, 'stretch_direction':stretch_direction, 'turn':total_turn})

        bl2.reset_given_shapename_and_arguments_and_move(  shapename=contour,
                                                          kwargs_shape={}, 
                                                          kwargs_common={'diamond_x':0, 'diamond_y':0, 'stretch_coeff':r_stretch, 'stretch_direction':stretch_direction, 'turn':total_turn})

        #print(bl2.directional_stretch_matrix)
        #print("CONTOUR")
        #for name_, sh_ in [["segm1", segm1], ["segm2", segm2], ["bl1", bl1], ["bl2", bl2]]:
        #  print(name_, "=", sh_.get_xy())

        compare_contours(segm1, bl1)
        compare_contours(segm2, bl2)
        compare_contours(segm1, segm2)

    star0 = draw_a_broken_line(diamond_x=0, diamond_y=0, contour=[[0, 1], [2, 1]]) #radius_1=3, radius_2=1, ends_qty=8)
    star1 = clone_a_shape(star0);
    total_turn = 0
    for _ in range(5):
      r_direction = random_integer_number(-2, 2) * 3
      r_stretch = random_integer_number(1, 6) * ( random_integer_number(0, 1) * 2 - 1)
      r_turn2 = random_integer_number(-2, 2) * 3
      #print("r_direction=", r_direction, "r_stretch=", r_stretch, "r_turn2=", r_turn2)
      star1.stretch_with_direction(stretch_coeff=r_stretch,  direction=r_direction)
      star1.turn(r_turn2)
      star2 = clone_a_shape(star0)
      total_turn += r_turn2
      #m0, m1, m2, m3 = star2.move(diamond_x=0, diamond_y=0, stretch_coeff=r_stretch, stretch_direction=r_direction, turn=total_turn)
      

      print("CONTOUR")
      print(star1.get_xy())
      #compare_contours(star1, star2)

  ##################################################################
  def test_gradient():
    for test_end in ([255, 255, 255], [2, 3, 5], [2, 3, 15]):
      result = create_gradient_colors(rgb_start=[0, 0, 0], rgb_end=test_end)
      print(result[-1], np.array(test_end)/255.)
      for i in range(3):
        assert is_the_same_point(result[-1][i], test_end[i]/255.)
      print("succeeded gradient test", [0, 0, 0], '->', test_end)

  print(datetime.datetime.now())

  write_file(filename_="MY_FUNCTION_REFERENCE.txt", contents_func=generate_function_list)

  test_rectangle(); test_gradient();  
  test_functions_or_modules("images"); check_folder("images");
  test_functions_or_modules("drawings"); check_folder("drawings"); 
  test_functions_or_modules("videos")

  print(datetime.datetime.now())