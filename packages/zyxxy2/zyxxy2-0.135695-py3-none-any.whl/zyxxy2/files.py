import matplotlib.image as mlp_image
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import PIL #cv2
import os
import numpy as np
import urllib.request
import os.path
import gc, time, types, functools, importlib.machinery

from .utils import fix_random_seed
from .shape_class import get_ca

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }

##################################################################
def filename_to_image(filename):
    # download the image, convert it to a NumPy array, and then read it
    if os.path.isfile(filename): # cbook.get_sample_data(filename_with_path) as file:
      image = mlp_image.imread(filename) # cv2.imread(filename)
    else:
      assert filename.startswith("http")
      url = filename
      request = urllib.request.Request(url, headers=headers)
      image_PIL = PIL.Image.open(urllib.request.urlopen(request))
      image = np.asarray(image_PIL)
      
    # return the image
    return image

##################################################################
def mirror_image(img):
    return img[:,::-1,:]

##################################################################
def write_file(filename_, contents_func):
  contents = contents_func()
  with open(filename_, "w") as writer:
    writer.write("\n".join(contents))

##################################################################
def execute_module(filemane_):
  loader = importlib.machinery.SourceFileLoader(filemane_[:-3], filemane_)
  mod = types.ModuleType(loader.name)
  loader.exec_module(mod)

##################################################################
def _clear_memory():
  plt.figure().clear()
  plt.close()
  plt.cla()
  plt.clf()
  plt.close('all')

##################################################################
def execute_example_or_module(module_or_function):
  start = time.perf_counter() 
  fix_random_seed()
  name_of_what_was_executed = None
  if isinstance(module_or_function, (types.FunctionType, functools.partial)):
    module_or_function()
    if isinstance(module_or_function, types.FunctionType):
      name_of_what_was_executed = module_or_function.__name__
    else:
      name_of_what_was_executed = module_or_function.func.__name__
  elif isinstance(module_or_function, str): #
    execute_module(filemane_=module_or_function)
    name_of_what_was_executed = module_or_function[:-3]
  else:
    raise Exception(str(module_or_function), "is neither a function or an executable module")

  end = time.perf_counter() 
  print( f'{end - start:.2f}' + " seconds", name_of_what_was_executed)
  _clear_memory()

  return (end - start)

##################################################################
def show_image(prepared_image, origin=None, ax=None, zorder=0, opacity=1, scaling_factor=1, LB_position=[0, 0]):
    if ax is None:
      ax = get_ca()
    if origin is None:
      origin = [ax.get_xlim()[0], ax.get_xlim()[1]]

    extent = np.array([0, prepared_image.shape[1]*scaling_factor, 0, prepared_image.shape[0]*scaling_factor])
    extent[0:2] += origin[0] + LB_position[0]
    extent[2:4] += origin[1] + LB_position[1]

    result = ax.imshow(prepared_image, extent=extent, zorder=zorder, alpha=opacity)
    return result

##################################################################
def compare_images(image_to_test_filename, image_benchmark_filename):

  print('comparing', image_to_test_filename, 'and', image_benchmark_filename)

  image_benchmark = plt.imread(image_benchmark_filename)
  image_to_test = plt.imread(image_to_test_filename)

  if image_to_test.shape != image_benchmark.shape:
    print("IMAGE SIZES ARE DIFFERERENT:", image_to_test.shape, image_benchmark.shape)
    return -1
  
  diff_black_white = np.linalg.norm(image_benchmark - image_to_test, axis=2) > 0 
  diff_black_white = diff_black_white.astype(int)

  dist = np.linalg.norm(image_to_test - image_benchmark) / image_to_test.size
  
  if np.sum(np.sum(diff_black_white)) > 0:
    print("IMAGES ARE DIFFERERENT! THE DIFFERENCE IS (% OF ALL PIXELS)", dist * 100)
    plt.imsave(image_to_test_filename+'_DIFF.png', 255 * (1 - diff_black_white), cmap=cm.gray)

  del image_benchmark
  del image_to_test
  del diff_black_white
  
  gc.collect()

  return dist