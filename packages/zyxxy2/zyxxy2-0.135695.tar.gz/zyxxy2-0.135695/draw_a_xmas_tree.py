# adding libraries that will help up
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_triangle, draw_a_star, draw_a_circle

create_canvas_and_axes(canvas_width=18,
                       canvas_height=18,
                       make_symmetric=True,
                       tick_step=1)

# draw triangles for the tree
# possible to use a for loop, but need to change parameters
# e.g. if the tops of the triangles need to be on the same vertical line, what can we say about x coordinates of these tops?
# parameters like "3*t+0.5" are functions just to show what you can do, you can use other functions, e.g. 0.5 * t * t + 6

# t will take value 0, then 1, then 2, then 3, then 4, stop at 5
# thus we will draw 5 triangles in this loop
for t in range(0, 5):
  draw_a_triangle(tip_x=t,
                  tip_y=t + 2,
                  height=3 * t + 0.5,
                  width=0.4 * t + 2,
                  color='forestgreen')

# or you can draw triangles one by one
draw_a_triangle(tip_x=-0.5,
                tip_y=-2,
                height=3,
                width=5,
                color='limegreen')

# adding decorations
# polygon with 60 vertices looks like a bubble
draw_a_circle(center_x=-2,
              center_y=-5,
              radius=0.8,
              color='superPink')
# polygon with 4 vertices, looks like a romboid
draw_a_star(center_x=-2,
              center_y=-8,
              radius_1=1,
              radius_2=0.5,
              ends_qty=4,
              color='superViolet')
# a star with 5 points
draw_a_star(center_x=-1,
            center_y=-3,
            radius_1=1,
            radius_2=0.5,
            ends_qty=5,
            color='superGold')

# the technical part, to display the result
show_and_save()
