
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_triangle, draw_a_star, draw_a_circle, draw_a_crescent, draw_an_ellipse, draw_a_segment, draw_a_sector
from zyxxy2 import set_default_patch_color, set_default_linewidth
from zyxxy2 import new_layer_outline_behind
from zyxxy2 import tan, asin, sin, cos, atan

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 80,
                       canvas_height = 80,
                       make_symmetric = True,
                       # tick_step = 2,
                       title = "Green And Blue Mandala",
                       model = 'https://i.pinimg.com/564x/24/be/7a/24be7a90f25924c924733e51660b5cfe.jpg',
                       model_zoom = 1.3 * 1.5 + 0.1,
                       model_shift = [27.5, 4.3],
                       background_color='white')

#######################################################
# Now let's draw the shapes!                         ##

distance_crescents = 38
distance_circles = 30
distance_triangles = 27
triangle_height = 8
crescents_qty = 40
arc_distance = 16
arc_width = 1.05
init_radius_arc = 6.4
assert sin(12/16) * arc_distance < init_radius_arc
distance_triangles_2 = 13
triangle_height_2 = 7

outline_linewidth = 1.5

set_default_linewidth(2*outline_linewidth) # because outline is usually behind

layers_1 = new_layer_outline_behind()
crescent_colors = ['deepskyblue', 'royalblue']
for i in range(crescents_qty):
  crsc = draw_a_crescent(center_x=0, center_y=distance_crescents, width=2*tan(12/(2*crescents_qty))*distance_crescents, depth_1=1.2, depth_2=2, color=crescent_colors[i%2], stretch_coeff=3, stretch_direction='y')
  crsc.turn(turn=12/crescents_qty*i, diamond_override=[0,0])

layers_2 = new_layer_outline_behind()

for i in range(crescents_qty):
  circle = draw_a_circle(center_x=0, center_y=distance_circles, radius=1, color='palegreen')
  circle.turn(turn=12/crescents_qty*(i+0.5), diamond_override=[0,0])

layers_3 = new_layer_outline_behind()
set_default_patch_color("yellow")

for i in range(8):
  triangles = [draw_a_triangle(tip_x=0, tip_y=distance_triangles, height=triangle_height, width=3.5, turn=6) for _ in range(4)]
  for t, angle in enumerate([-0.19, -0.1, 0.1, 0.19]):
    triangles[t].turn(turn=angle, diamond_override=[0,0])

  big_triangles = [draw_a_triangle(tip_x=0, tip_y=distance_triangles, height=triangle_height, width=13, turn=6) for _ in range(2)]
  for t, lr in enumerate([-1, 1]):
    big_triangles[t].turn(turn=-lr*.1, diamond_override=[0, distance_triangles-triangle_height])
    big_triangles[t].turn(turn=lr*.5, diamond_override=[0,0])

  for trngl in triangles + big_triangles:
    trngl.turn(turn=12/8*i, diamond_override=[0,0])

layers_4 = new_layer_outline_behind()
angle_one_arc = asin(sin(12/16) * arc_distance / init_radius_arc)
arc_colors = ['royalblue', 'powderblue']
center_arc_y = arc_distance * cos(12/16) - init_radius_arc * cos(angle_one_arc)
for r in [1, 0]:
  for i in range(8):
    draw_a_segment(start_x=0, start_y=0, turn=12/8*i, length=center_arc_y+init_radius_arc)
    sectors = [draw_a_sector(angle_start=-angle_one_arc, 
                             angle_end=angle_one_arc, 
                             radius=init_radius_arc + r * arc_width, 
                             radius_2=init_radius_arc + (r+1) * arc_width, 
                             center_x=0, 
                             center_y=center_arc_y,
                             color=arc_colors[r])]
    for s in sectors:
      s.turn(turn=12/8*i, diamond_override=[0,0])

layers_5 = new_layer_outline_behind()
width_2 = (distance_triangles_2 - triangle_height_2) * atan(12/(24*2))
print(width_2)
for i in range(24):
  trngl = draw_a_triangle(tip_x=0, tip_y=distance_triangles_2, height=triangle_height_2, width=width_2, turn=6, color='deepskyblue') 
  trngl.turn(turn=12/24*i, diamond_override=[0,0])

  if i%3 == 0:
    continue

  for color, radius in [['royalblue', 1.4], ['white', .5]]:
    circle = draw_a_circle(center_x=0, center_y=distance_triangles_2+1.4, radius=radius, color=color)
    circle.set_style(
      outline_layer_nb=layers_5[0], outline_linewidth=outline_linewidth)
    circle.turn(turn=12/24*i, diamond_override=[0,0])

layers_6 = new_layer_outline_behind()
for i in range(8):
  pass # ellipse = draw_an_ellipse()


show_and_save()