from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_rectangle
from zyxxy2 import get_canvas_height, get_canvas_width, get_canvas_left, get_canvas_bottom
from zyxxy2 import get_multi_gradient_color
from zyxxy2 import equal_or_almost

def draw_gradient_rectangles(lim1, lim2, colors, how_many=200, color_limits=None, clip_outline=None, is_vertical=True):
  assert not equal_or_almost(lim1, lim2)
  color_limits_normalised = [(cl - lim1) / (lim2 - lim1) for cl in color_limits] if color_limits is not None else None
  result_colors = get_multi_gradient_color(colors=colors, color_limits=color_limits_normalised, how_many=how_many)

  incr = (lim2 - lim1) / how_many 
  if is_vertical:
    left, bottom, width, height = lim1, get_canvas_bottom(), incr, get_canvas_height()
  else:       
    left, bottom, width, height = get_canvas_left(), lim1, get_canvas_width(), incr 
                                                      
  for i, c in enumerate(result_colors):
    draw_a_rectangle(left=left+(i+int(lim1 > lim2))*incr*int(is_vertical), 
                       bottom=bottom+(i+int(lim1 > lim2))*incr*int(not is_vertical), 
                       width=width, height=height, color=c, clip_outline=clip_outline)
#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width=100,
                       canvas_height=100,
                       title="Digital Reproduction",
                       inspiration_addon='"Vanishing Point" by Alexandra Arshanskaya',
                       make_symmetric=True,
                       model='https://moongallery.eu/wp-content/uploads/2018/11/Vanishing-Point-150-25.jpg')

draw_gradient_rectangles(lim1=50, lim2=-50, colors=['#001050', '#0020A0', 'azure', 'white', 
'azure', '#002060', '#001030'], color_limits=[40, 5, 0, -15, -40], is_vertical=False)                       

draw_gradient_rectangles(lim1=-50, lim2=0, colors=['maroon', 'darkred', 'gold', 'lemonchiffon', 'white', 'white'], 
                         color_limits=[-32.5, -32.5, -8, -5], is_vertical=True, 
                         clip_outline=[[0, 0], [-50, 22.5], [-50, -50], [-30, -50]])
draw_gradient_rectangles(lim1=50, lim2=0, colors=['#000030', '#000080', '#002020', '#004040', 'paleturquoise', 'white', 'white'], 
                         color_limits=[18, 18, 7, 6, 5], is_vertical=True,
                         clip_outline= [[0, 0], [50, 27.5], [50, -50], [22.5, -50]])

draw_gradient_rectangles(lim1=50, lim2=0, colors=['lightsteelblue', 'white'],
                         is_vertical=True, clip_outline=[[0, 0], [50, -42], [50, -50], [42, -50]])
draw_gradient_rectangles(lim1=42, lim2=0, colors=['#000020', 'white'],
                         is_vertical=True, clip_outline=[[0, 0], [42, -50], [33, -50]])

draw_gradient_rectangles(lim1=-50, lim2=0, colors=['#282800', 'white'],
                         is_vertical=True, clip_outline=[[0, 0], [-50, -42], [-50, -48]])
draw_gradient_rectangles(lim1=-50, lim2=0, colors=['cornsilk', 'white'],
                         is_vertical=True, clip_outline=[[0, 0], [-50, -42], [-50, -32]])

show_and_save()            
           