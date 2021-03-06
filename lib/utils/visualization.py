# --------------------------------------------------------
# Tensorflow Faster R-CNN
# Licensed under The MIT License [see LICENSE for details]
# Written by Xinlei Chen
# --------------------------------------------------------
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np
import PIL.Image as Image
import PIL.ImageColor as ImageColor
import PIL.ImageDraw as ImageDraw
import PIL.ImageFont as ImageFont
from matplotlib import cm
STANDARD_COLORS = [
    'AliceBlue', 'Chartreuse', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque',
    'BlanchedAlmond', 'BlueViolet', 'BurlyWood', 'CadetBlue', 'AntiqueWhite',
    'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan',
    'DarkCyan', 'DarkGoldenRod', 'DarkGrey', 'DarkKhaki', 'DarkOrange',
    'DarkOrchid', 'DarkSalmon', 'DarkSeaGreen', 'DarkTurquoise', 'DarkViolet',
    'DeepPink', 'DeepSkyBlue', 'DodgerBlue', 'FireBrick', 'FloralWhite',
    'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'GoldenRod',
    'Salmon', 'Tan', 'HoneyDew', 'HotPink', 'IndianRed', 'Ivory', 'Khaki',
    'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue',
    'LightCoral', 'LightCyan', 'LightGoldenRodYellow', 'LightGray', 'LightGrey',
    'LightGreen', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue',
    'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime',
    'LimeGreen', 'Linen', 'Magenta', 'MediumAquaMarine', 'MediumOrchid',
    'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen',
    'MediumTurquoise', 'MediumVioletRed', 'MintCream', 'MistyRose', 'Moccasin',
    'NavajoWhite', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed',
    'Orchid', 'PaleGoldenRod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed',
    'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple',
    'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Green', 'SandyBrown',
    'SeaGreen', 'SeaShell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue',
    'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'GreenYellow',
    'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'Wheat', 'White',
    'WhiteSmoke', 'Yellow', 'YellowGreen'
]

NUM_COLORS = len(STANDARD_COLORS)

try:
  FONT = ImageFont.truetype('arial.ttf', 24)
except IOError:
  FONT = ImageFont.load_default()

def _draw_single_box(image, xmin, ymin, xmax, ymax, display_str, font, color='black', thickness=4):
  draw = ImageDraw.Draw(image)
  (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
  draw.line([(left, top), (left, bottom), (right, bottom),
             (right, top), (left, top)], width=thickness, fill=color)
  text_bottom = bottom
  # Reverse list and print from bottom to top.
  text_width, text_height = font.getsize(display_str)
  margin = np.ceil(0.05 * text_height)
  draw.rectangle(
      [(left, text_bottom - text_height - 2 * margin), (left + text_width,
                                                        text_bottom)],
      fill=color)
  draw.text(
      (left + margin, text_bottom - text_height - margin),
      display_str,

      fill='black',
      font=font)

  return image

def draw_bounding_boxes(image, gt_boxes, im_info):
  num_boxes = gt_boxes.shape[0]
  gt_boxes_new = gt_boxes.copy()
  gt_boxes_new[:,:4] = np.round(gt_boxes_new[:,:4].copy() / im_info[2])
  disp_image = Image.fromarray(np.uint8(image[0][:,:,1:4].copy()))

  for i in range(num_boxes):
    this_class = int(gt_boxes_new[i, 4])
    disp_image = _draw_single_box(disp_image, 
                                gt_boxes_new[i, 0],
                                gt_boxes_new[i, 1],
                                gt_boxes_new[i, 2],
                                gt_boxes_new[i, 3],
                                'N%02d-C%02d' % (i, this_class),
                                FONT,
                                color=STANDARD_COLORS[this_class % NUM_COLORS])

  sx,sy,sz = image[0].shape
  bgr_img = np.float32(np.zeros((1,sx,sy,3)))
  bgr_img[0,:] = np.array(disp_image)
  return bgr_img

def draw_bbox_only(image, gt_boxes, im_info,means):
  #print(image.shape)
  num_boxes = gt_boxes.shape[0]
  gt_boxes_new = gt_boxes.copy()
  gt_boxes_new[:,:4] = np.round(gt_boxes_new[:,:4].copy() / im_info[2])

  # resized = tf.image.resize_bilinear(image, tf.to_int32(self._im_info[:2] / self._im_info[2]))

  # if num_boxes < 1:
  #   disp_image = Image.fromarray(np.uint8(image[0][:,:,0:3].copy() + means))
  #   disp_image.show()
    # assert False

  sx,sy,sz = image[0].shape
  # disp_image = Image.fromarray(np.uint8(np.zeros((sx,sy,4))), mode='RGBA')
  disp_image = Image.new('L', (sy,sx))

  for i in range(num_boxes):
    this_class = int(gt_boxes_new[i, 4])
    print("class info", i, this_class)
    disp_image = _draw_single_box_only(disp_image, 
                                gt_boxes_new[i, 0]*im_info[2],
                                gt_boxes_new[i, 1]*im_info[2],
                                gt_boxes_new[i, 2]*im_info[2],
                                gt_boxes_new[i, 3]*im_info[2],
                                'N%02d-C%02d' % (i, this_class),
                                FONT,
                                color=this_class+1)
  assert this_class + 1 < 92, this_class
  # sx,sy,sz = image[0].shape
  # bgr_img = np.float32(np.zeros((1,sx,sy,3)))
  # bgr_img[0,:] = np.array(disp_image)
  # disp_image.show()
  # disp_image.convert('L').show()
  # assert False

  disp_image =  disp_image.convert('L')
  out = np.array(disp_image)
  # Image.fromarray(out).show()
  return out

def _draw_single_box_only(image, xmin, ymin, xmax, ymax, display_str, font, color='black', thickness=4):
  #draw = ImageDraw.Draw(image, 'RGBA')
  draw = ImageDraw.Draw(image)
  (left, right, top, bottom) = (xmin, xmax, ymin, ymax)
  scale = 255/92
  rgba_val = [int(x) for x in np.dot(cm.ocean(int(scale*color)),255)]
  rgba_val[-1] = 50
  # print(rgba_val, "class", color)
  draw.rectangle([(left, top),(right, bottom)], fill=int(scale*color))

  return image
