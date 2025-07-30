from zyxxy2 import create_canvas_and_axes, show_and_save
from zyxxy2 import draw_a_circle,draw_a_square,draw_a_star
from zyxxy2 import random_number
ball_radius = 0.5
linewidth = 2

create_canvas_and_axes(  canvas_width = 160,
                              canvas_height = 70,
                              bottom_left_coords = [-1, -1],
                              #tick_step = 4,
                              #title = "Random Circles",
                              background_color='lightcyan',
                              diamond_size=0)

all_y = []
def color_mixer(startcolor, endcolor, lion):

  red_in_the_middle = (1-lion) * startcolor[0] + lion * endcolor[0]
  green_in_the_middle = (1-lion) * startcolor[1] + lion * endcolor[1]
  blue_in_the_middle = (1-lion) * startcolor[2] + lion * endcolor[2]

  resulting_color_in_the_middle = [red_in_the_middle,  green_in_the_middle ,  blue_in_the_middle ]
  return resulting_color_in_the_middle
                                                 
def draw_a_gradient_line(startpoint, endpoint, shift_x, shift_y, startcolor = [(6*16+4)/255, 9/16, 1], # [0.76, 0.44, 0.76], 
endcolor =  [(13*16+12)/255, (2*16+6)/255, (7*16+15)/255]): # [0.76, 0.54, 0.34]
  
  our_height = endpoint[1] -  startpoint[1]
  our_width = endpoint[0] -  startpoint[0]

  for _ in range(15):
    lion_position = random_number(0, 1)
    x = lion_position * our_width +  startpoint[0]
    y = lion_position * our_height + startpoint[1]
    lion_color = (y + shift_y - 15) / 45
    draw_a_star(center=[x+shift_x, y+shift_y], layer_nb=0, outline_layer_nb=-1, radius_1=2, radius_2=1, ends_qty=8,
                  color=color_mixer(startcolor=startcolor, endcolor=endcolor, lion=lion_color), #[0.36, 0.71, lion], 
                  outline_linewidth=linewidth)
    
dictionary_letters = {
'K' : [[[2, 3], [2, 18]] , [[15, 3], [2, 10.5]] , [[15, 18], [2, 10.5]]], 
'I' : [[[19, 18], [25, 18]], [[22, 18], [22, 3]], [[25, 3],[19, 3]]], 
'A' : [[[28, 3], [34, 18]] , [[34, 18], [40, 3]] , [[31, 10.5], [37, 10.5]]], 
'N' : [[[44, 3], [44, 18]] , [[44, 18], [54, 3]] , [[54, 3], [54, 18]]], 
'H' : [[[2, 22], [2, 37]],[[2, 30],[12, 30]],[[12, 22],[12, 37]]], 
'P' : [[[14, 22], [14, 37]], [[14, 37],[22, 37]],[[22, 37],[22, 29]], [[22, 29], [14, 29]]],
'Y' : [[[28, 37], [34, 30]], [[34, 30], [34, 22]], [[34, 30], [42, 37]]],
'W' : [[[46, 37], [52, 22]], [[52, 22], [58, 37]], [[58, 37], [64, 22]], [[64, 22], [70, 37]]],
'E' : [[[74, 37], [84, 37]], [[74, 37], [74, 30]], [[74, 30], [84, 30]], [[74, 30], [74, 22]], [[74, 22], [84, 22]]],
'R' : [[[88, 22], [88, 37]], [[88, 37],[96, 37]],[[96, 37],[96, 29]], [[96, 29], [88, 29]], [[88, 29], [96, 22]]],
'O' : [[[69, 35], [61,28]], [[69, 20], [76, 28]], [[61,28], [69,20]], [[76, 28], [69, 35]]],
'U' : [[[84, 35], [84, 20]], [[84,20], [100, 20]], [[96, 20], [96,35]]],
'Z' : [[[104, 35], [120, 35]], [[120, 35], [104, 20]], [[104, 20], [120, 20]]]}

bottom_line_y = 40
target_x = 4

# Kian needs to creare a line like 'HAPPY\nKIAN':
for letter in 'HAPPY NEW\nYEAR': #NOWRUZ':

  if letter == '\n':
    bottom_line_y -= 25
    target_x = 4 + (157 - 70) / 2
  elif letter == ' ':
    target_x += 10
  else:                                                     
    assert letter in dictionary_letters.keys()

    segments_of_the_letter = dictionary_letters[letter]
    # print("the smallest X coordinate is of segments_of_the_letter is",  min([min(s[0][0], s[1][0]) for s in segments_of_the_letter]))
    # print("the greatest X coordinate is of segments_of_the_letter is", max([max(s[0][0], s[1][0]) for s in segments_of_the_letter]))

    min_x = min([min(s[0][0], s[1][0]) for s in segments_of_the_letter])
    max_x = max([max(s[0][0], s[1][0]) for s in segments_of_the_letter])
    length = max_x - min_x 
    
    shift_x =  target_x - min_x
    shift_y = bottom_line_y -min([min(seg[0][1], seg[1][1]) for seg in segments_of_the_letter] ) 
    for startpoint, endpoint in segments_of_the_letter:
      draw_a_gradient_line(startpoint=startpoint, endpoint=endpoint, shift_x=shift_x, shift_y=shift_y)
    target_x += length + 6.3

show_and_save()
