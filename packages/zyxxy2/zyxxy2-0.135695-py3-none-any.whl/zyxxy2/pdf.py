import datetime
from pathlib import Path
from functools import partial

from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages

from .shape_class import get_cf, get_ca, set_current_lone_figure
from .canvas import place_axes
from .word_bubbles import draw_a_speech_bubble, place_text
from .utils import random_integer_number, random_element # get_random_int
from .shape_functions import draw_a_rectangle

class paper_size:
  inch = 1
  cm = inch / 2.54

  _W, _H = (21*cm, 29.7*cm)

  A6 = (_W*.5, _H*.5)
  A5 = (_H*.5, _W)
  A4 = (_W, _H)
  A3 = (_H, _W*2)
  A2 = (_W*2, _H*2)
  A1 = (_H*2, _W*4)
  A0 = (_W*4, _H*4)

  LETTER = (8.5*inch, 11*inch)
  LEGAL = (8.5*inch, 14*inch)
  ELEVENSEVENTEEN = (11*inch, 17*inch)
  # lower case is deprecated as of 12/2001, but here
  # for compatability
  letter=LETTER
  legal=LEGAL
  elevenSeventeen = ELEVENSEVENTEEN

  _BW, _BH = (25*cm, 35.3*cm)
  B6 = (_BW*.5, _BH*.5)
  B5 = (_BH*.5, _BW)
  B4 = (_BW, _BH)
  B3 = (_BH*2, _BW)
  B2 = (_BW*2, _BH*2)
  B1 = (_BH*4, _BW*2)
  B0 = (_BW*4, _BH*4)

  @staticmethod
  def get_figsize(init_figsize):
    if isinstance(init_figsize, str) and \
           ((init_figsize not in ('cm', 'inch')) and (init_figsize[0] != '_')): 
      if hasattr(paper_size, init_figsize):
        result = getattr(paper_size, init_figsize)
        return result
      if hasattr(paper_size, init_figsize[:-1].upper()):
        result = getattr(paper_size, init_figsize[:-1].upper())
        if init_figsize[-1].lower() == 'l':
          result = [max(result), min(result)]
          return result
        if init_figsize[-1].lower() == 'p':
          result = [min(result), max(result)]
          return result
    return init_figsize

##########################################################################################



##########################################################################################
def _read(filename):
  inspirations = []
  p = Path(__file__).with_name(filename)
  with p.open('r') as handle:
    for l in handle:
      inspirations.append(l.strip())
  return inspirations

inspirations = {filename:_read(filename) for filename in ['inspirations.txt', 'nameless_inspirations.txt']}

def get_random_inspiration(name=None):
  insp = random_element(inspirations[('' if name else 'nameless_')+'inspirations.txt'])
  if name:
    if insp.startswith("You're") and random_integer_number(0, 1):
      insp = "You a"+ insp[4:]
    if random_integer_number(0, 1):
      if insp.startswith("You"):
        insp = f"{name}, y" + insp[1:]
      else:
        insp = insp[:-1] + f", {name}!"
  return insp

##########################################################################################
def place_watermarks(generator, 
                     max_per_line=20, fontsize=8, copyright=None,
                     layer_nb=-5, line_gap=1., color='lightgrey'):  

  t = get_ca().get_ylim()[1]
  i = 0
  while t > 0:
    wm_array = [generator() for _ in range(max_per_line)] \
          if ((i%2) or (not copyright)) \
          else ['© '+ copyright + ' ' for _ in range(max_per_line)] 
    wm_array[0] = wm_array[0][random_integer_number(1, len(wm_array[0])//2):].strip()
    new_wm = ' '.join(wm_array)
    wm_text = draw_a_speech_bubble(text=new_wm, x=0, y=t, fontsize=fontsize, position='lt', 
                                   color=color, layer_nb=layer_nb, wrap=False, background_color='none')
    t = wm_text.bottom * (1 + line_gap) - line_gap * wm_text.top
    i += 1

##########################################################################################
def create_a_page(page_size, dpi, bg_color=None, wms=None, header=None, header_fontsize=20, margin=.05, header_top_margin=.02, **wm_kwargs):
  
  figsize = paper_size.get_figsize(init_figsize=page_size) 

  set_current_lone_figure(figsize=figsize, dpi=dpi)
  place_axes(axes_bbox=[[margin, margin], [1-margin, 1-margin]], canvas_width=(1-2*margin)*figsize[0], canvas_height=(1-2*margin)*figsize[1], gap_x=0, gap_y=0)
  if bg_color:
    draw_a_rectangle(left=margin*figsize[0], bottom=margin*figsize[1], 
                     width=(1-2*margin)*figsize[0], 
                     height=(1-2*margin)*figsize[1], color=bg_color, layer_nb=-6)
  if wms is not None:
    wm_generator = partial(get_random_inspiration, wms if isinstance(wms, str) else None)
    _wm_kwargs = {key[3:]:value for key, value in wm_kwargs.items()}
    place_watermarks(generator=wm_generator, **_wm_kwargs)

  if header:
    title = place_text(text=header, x=.5, y=1-header_top_margin, position='ct', fontsize=header_fontsize)
  else:
    title = None
    
  return title
  
##########################################################################################
_infodoc_keys = ['Title', 'Author', 'Subject', 'Keywords', 'CreationDate', 'ModDate', 'Producer']

def _singleton_fig_yielder():
  yield get_cf()
  
def create_a_pdf(filename, page_yielder=_singleton_fig_yielder, pdf_info={}):
  assert not {k for k in pdf_info if k not in _infodoc_keys}
  
  with PdfPages(filename if filename.endswith('.pdf') else (filename+'.pdf')) as pdf:
    for page in page_yielder():
      if False:
        plt.show(block=False)
        input('Press Enter to continue...')
      pdf.savefig(page)

    infodict_ref = pdf.infodict()
    infodict_ref = {**infodict_ref, 'Author' : "", 'Producer' : "", 'ModDate' : datetime.datetime.today(), 
                                      'CreationDate' : datetime.datetime.today(), **pdf_info}
    return pdf
  