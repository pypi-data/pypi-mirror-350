import numpy as np
from math import floor
from .canvas import show_and_save

    #all_shapes = Shape._get_all_shapes_in_layers()
    #total_init_frames = qty_frames_for_each_visualization * len(all_shapes) + qty_frames_for_move + qty_frames_wait_at_the_end
    #shape_diamond_coords = [as_.get_diamond_coords() for as_ in all_shapes]
    #shift_diamond = [random_point_on_axes() - as_.diamond_coords for as_ in all_shapes]

###################################################################################################
def anim_putting_together_one_by_one(i, all_shapes, shifted_diamonds, init_diamonds, 
                           qty_frames_for_each_visualization=0, 
                           qty_frames_for_move=0, 
                           qty_frames_wait_at_the_end=0):

  total_init_frames = qty_frames_for_each_visualization * len(all_shapes) + qty_frames_for_move + qty_frames_wait_at_the_end

  if i == 0:
    # initialization for standard animation
    if qty_frames_for_each_visualization:
      for as_ in all_shapes:
        as_.set_visible(False)
    if qty_frames_for_move:
      for n in range(len(all_shapes)):
        all_shapes[n].shift_to(shifted_diamonds[n])  
    return total_init_frames, all_shapes

  i -= 1
  if 0 <= i < qty_frames_for_each_visualization * len(all_shapes): # show_shapes
    if i % qty_frames_for_each_visualization == 0:
      all_shapes[int(i / qty_frames_for_each_visualization)].set_visible(True)
      return total_init_frames, all_shapes
  else:
    j = total_init_frames - qty_frames_wait_at_the_end - 1 - i
    if j >= 0:
      for n in range(len(all_shapes)):
        all_shapes[n].shift_to(init_diamonds[n] * (1 - j / qty_frames_for_move) + shifted_diamonds[n] * j / qty_frames_for_move)
      return total_init_frames, all_shapes

  return total_init_frames, None

###################################################################################################
def anim_show_put_together_by_groups(i, all_shapes, correct_diamonds, other_diamonds, group_sizes, qty_frames_for_each_visualization, qty_frames_for_move, bubbble=None, message=None):
  
  total_init_frames = 1 + len(group_sizes) * (qty_frames_for_each_visualization + qty_frames_for_move)

  if i >= total_init_frames:
    return total_init_frames, []
    
  group_sizes_cumsum = np.hstack(([0],np.cumsum(group_sizes)))
  assert group_sizes_cumsum[-1] == len(all_shapes)

  if i == 0:
    for as_ in all_shapes:
      as_.make_invisible()
    return total_init_frames, all_shapes

  i -= 1
  gr_num = floor(i / (qty_frames_for_each_visualization + qty_frames_for_move))
  move_i =  i % (qty_frames_for_each_visualization + qty_frames_for_move)

  for s in range(group_sizes_cumsum[gr_num],  group_sizes_cumsum[gr_num+1]):
    if move_i == 0:
      all_shapes[s].shift_to(other_diamonds[s])
      all_shapes[s].make_visible()
      if bubbble is not None:
        bubbble.set_text(message[gr_num])

    if move_i >= qty_frames_for_each_visualization:
      j = move_i - qty_frames_for_each_visualization + 1
      all_shapes[s].shift_to(other_diamonds[s] + (correct_diamonds[s] - other_diamonds[s]) * j / qty_frames_for_move)

  return total_init_frames, [all_shapes[s] for s in range(group_sizes_cumsum[gr_num],  group_sizes_cumsum[gr_num+1])]

###################################################################################################
def show_and_save_basic_animation(qty_frames_for_each_visualization, qty_frames_for_move, qty_frames_wait_at_the_end, **qwargs):

  frames_qty, animation_func = anim_putting_together_one_by_one(
                           qty_frames_for_each_visualization=qty_frames_for_each_visualization, 
                           qty_frames_for_move=qty_frames_for_move, 
                           qty_frames_wait_at_the_end=qty_frames_wait_at_the_end)
  show_and_save(animation_func=animation_func, frames_qty=frames_qty, **qwargs)
