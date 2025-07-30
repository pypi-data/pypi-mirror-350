
from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import example_us_flag
from zyxxy2 import draw_a_star, draw_a_rectangle

#######################################################
# Creating the canvas!                               ##
create_canvas_and_axes(canvas_width = 19*13*2,
                       canvas_height = 10*13*2,
                       tick_step = 50,
                       title = "Flag Of The U.S.A.",
                       model = example_us_flag,
                       diamond_color = 'cyan',
                       diamond_size = 0.75)

#######################################################
# Now let's draw the shapes!                         ##
for stripe_nb in range(3):
  draw_a_rectangle(left=0, center_y=15+30*stripe_nb, width=19*13*2, height=15, color='red')
    
draw_a_rectangle(left=0, center_y=190, width=90, height=80, color='navy')   

for row in range(7): # there are 9 rows of stars
  # let's define how many stars are in this row
  # and where is the center_x of the first star    
  if row%2==0: # if row number is even
    stars_qty=9
    first_star_center_x = 15 
  else:        # if row number is odd
    stars_qty=8
    first_star_center_x = 33 
  # center_y=260-(row+1)*14 because we are counting star rows from the top
  for column in range(stars_qty):
    draw_a_star(center_x=first_star_center_x+column*40, center_y=260-(row+1)*20, radius_1=18, radius_2=6, ends_qty=5, color='skyblue')               

show_and_save()