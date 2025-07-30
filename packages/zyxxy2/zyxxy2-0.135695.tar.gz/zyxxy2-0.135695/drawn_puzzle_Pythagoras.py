from zyxxy2 import create_canvas_and_axes, wait_for_enter
from zyxxy2 import atan, random_integer_number, calc_Pythagoras
from zyxxy2 import draw_a_square, clone_a_shape, draw_a_polygon
import matplotlib.pyplot as plt
from zyxxy2.settings import default_font_sizes

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 20,
                              canvas_height = 23,
                              tick_step = 1,
                              make_symmetric = True,
                              title = "Pythagoras Puzzle",
                              diamond_color = "black")

header_txts = [plt.text(x=plt.gca().get_xlim()[0]+1.5, y=plt.gca().get_ylim()[1]-i*1.53, s="", fontdict={'size': default_font_sizes['title']/2}) for i in range(1, 4)]

#######################################################

a = 6 # random_integer_number(max=8, min=3.)
b = 8 # random_integer_number(max=8, min=3.)
c = calc_Pythagoras(a=a, b=b)

print("a = ", a, ", b = ", b, ", c = ", c)

a_square = draw_a_square(side=c, center_x=0, center_y=0, color='crimson')
triangle_1 = draw_a_polygon(contour=[[0, a], [0, 0], [b, 0]], color='dodgerblue')
triangle_1.shift(shift=[-10, -10])

triangle_2 = clone_a_shape(triangle_1)
triangle_2.shift(shift=[0, 15])
triangle_2.set_color("royalblue")

triangle_3 = clone_a_shape(triangle_1)
triangle_3.shift(shift=[15, 15])
triangle_3.turn(turn=1)
triangle_3.set_color("mediumturquoise")

triangle_4 = clone_a_shape(triangle_1)
triangle_4.shift(shift=[15, 0])
triangle_4.turn(turn=11)
triangle_4.set_color("aqua")

#######################################################
# Kian's code  that puts all triangles together into a blue rectangle goes here ...
# Kian can use methods "shift" and "turn", as above, to move TRIANGLES
# Hint: it only takes rotation by angles with integer values between 0 and 12
# Full angle = 12, like on the clock
#######################################################

header_txts[0].set_text("PART I: All Triangles Together -> A Rectangle")
header_txts[1].set_text("Area Of Blue Rectangle = " + str("???"))
header_txts[2].set_text("Area Of Red Square = " + str("???"))

wait_for_enter()

#######################################################
#######################################################

# turn the square by a magic angle, to make it easy to put together a big square
a_square.turn(turn = atan(a/b))

#######################################################
# Kian's code that puts [all triangles] + [a square] => [a bigger square] goes here ...
# Kian can use methods "shift" and "turn", as above, to move TRIANGLES
# Hint: it only takes rotation by angles with integer values between 0 and 12
# Full angle = 12, like on the clock
#######################################################

#a_square.set_color=("violet")
header_txts[0].set_text("PART II: A Square + 4 Triangles Together")
header_txts[1].set_text(" -> A Bigger Square")
header_txts[2].set_text("Area Of The Big Mixed color Square = " + str("???"))

wait_for_enter()