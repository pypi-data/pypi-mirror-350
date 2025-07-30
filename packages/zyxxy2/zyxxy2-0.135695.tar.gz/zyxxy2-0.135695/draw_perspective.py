from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_polygon, draw_a_broken_line, draw_a_triangle, draw_a_circle
from zyxxy2 import new_layer

#######################################################
# Creating the canvas!                               
ax = create_canvas_and_axes(  canvas_width = 38,
                              canvas_height = 24,                          
                              tick_step = 2,
                              make_symmetric = True,
                              title = "One Point Perspective",
                              diamond_size=0)
new_layer(); new_layer()
chessboard_x = [-18, 10]
how_many_chess_columns = 8
chessboard_bottom = -10
coeff_chessboard = .9
how_many_chess_rows = 18

draw_a_broken_line(diamond_x=0, diamond_y=0, 
                   contour=[[chessboard_x[0], chessboard_bottom], [0, 0], 
                            [chessboard_x[0], -3], [0, 0], [chessboard_x[1], chessboard_bottom]],
                   color='lightgray', linewidth=5, capstyle='rounded', joinstyle='rounded')

for t in range(how_many_chess_rows):
  coeff_this_tree = coeff_chessboard**t
  crown  = draw_a_circle(center=[chessboard_x[0] * coeff_this_tree, -5 * coeff_this_tree], 
                         radius=2*coeff_this_tree, color='green')
  crown.stretch_x(.3)
  draw_a_triangle(tip=[chessboard_x[0]*coeff_this_tree, -3*coeff_this_tree], 
                  width=.5*coeff_this_tree, height=7 * coeff_this_tree, 
                  color='brown', turn=6)

bottom = chessboard_bottom
lr = [(chessboard_x[0] * i + chessboard_x[1] * (how_many_chess_columns - i)) / how_many_chess_columns
           for i in range(how_many_chess_columns+1)]

for r in range(how_many_chess_rows):
  coeff_this_row = coeff_chessboard**r
  top = bottom * coeff_chessboard
  for c in range(how_many_chess_columns):
    draw_a_polygon(diamond_x=0, diamond_y=0, 
                   contour=[[lr[c] * coeff_this_row, bottom], 
                            [lr[c+1] * coeff_this_row, bottom], 
                            [lr[c+1] * coeff_this_row * coeff_chessboard, top], 
                            [lr[c] * coeff_this_row * coeff_chessboard, top]],
                   color='superGold' if (r - c) % 2 else 'superOrange')
  bottom = top

bottom = chessboard_bottom
for r, color in [[0, 'superBlue'], [1, 'superPink'], [2, 'black']]:
  coeff_this_row = coeff_chessboard**r
  c = 3
  draw_a_broken_line(diamond_x=0, diamond_y=0, 
                   contour=[[lr[c] * coeff_this_row, bottom], 
                            [lr[c+1] * coeff_this_row, bottom]],
                   color=color, linewidth=15)
  c = 6
  draw_a_polygon(diamond_x=0, diamond_y=0, 
                   contour=[[lr[c] * coeff_this_row, bottom], 
                            [lr[c+1] * coeff_this_row, bottom], [0, 0]],
                   outline_color=color, outline_linewidth=15-r*6, outline_joinstyle='rounded')
  bottom = bottom * coeff_chessboard

show_and_save()
