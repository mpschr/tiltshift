#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plug-in:      Apply tilt shift with an optional mask to avoid blurred (high objects) 
# Version:      0.1
# Date:         01.06.2012
# Copyright:    Michael Schroeder <michael.p.schroeder@gmail.com>
# Tested with:  GIMP 2.8
# ----------------------------------

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#  
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gimpfu import *

def python_tiltshift(image, drawable, startx=50, endx=50, starty=66, endy=80, degree=45, radius=20, blur=30, lightness=0, saturation=0, maskfile=None):

    image.disable_undo()
    width = drawable.width
    height = drawable.height
    startx = startx/100.0*width
    endx = endx/100.0*width
    starty = starty/100.0*height
    endy = endy/100.0*height
    background = image.active_layer
    image.add_layer(background.copy())
    toplayer = image.layers[0]
    toplayername = toplayer.name
    pdb.plug_in_gauss_rle(image, toplayer, blur, 1, 1)
    gradienttype = 1 #bi-linear
    # create blend
    ## create layer
    image.add_layer(toplayer.copy())
    blendlayer = image.layers[0]
    pdb.gimp_edit_blend(blendlayer, CUSTOM_MODE, NORMAL_MODE, gradienttype, 100.0, 1.0, False, False, False, 1, 0.0, False, startx, starty, endx, endy)
    ##TODO: limit blend left and right with same blend:
    ##TODO: save gradient to channel and delete layer
    tilt_shift_mask = pdb.gimp_channel_new_from_component(image,RED_CHANNEL,"tiltshiftmask")
    pdb.gimp_image_add_channel(image,tilt_shift_mask, 0)
    pdb.gimp_image_remove_layer(image,blendlayer)
    if not maskfile is None and maskfile is not "":
        mask_image = pdb.file_png_load(maskfile,0)
        sharp_mask = pdb.gimp_channel_new_from_component(image,RED_CHANNEL,"sharp_mask")
        pdb.gimp_image_add_channel(image,tilt_shift_mask, 0)
        pdb.gimp_image_delete(mask_image)
        pdb.gimp_channel_combine_masks(tilt_shift_mask, sharp_mask, 1, 0, 0)
    gradient_mask = pdb.gimp_layer_create_mask(toplayer, 0)
    pdb.gimp_layer_add_mask(toplayer, gradient_mask)
    pdb.gimp_channel_combine_masks(gradient_mask, tilt_shift_mask, 3, 0, 0)
    image.flatten()
    image.enable_undo()

image = gimp.image_list()[0]
drawable = image.active_layer
python_tiltshift(image, drawable)

register (
    "python-fu-tilt-shift",
    "Scale Layer to Image Size\nVersion 0.1",
    "Scale Layer to Image Size\nVersion 0.1",
    "Michael P Schroeder",
    "Michael P Schroeder <michael.p.schroeder@gmail.com>",
    "01.08.2013",
    "Tilt Shift (Miniature) ...",
    "*",
    [
        (PF_IMAGE, "image", "", None),
        (PF_DRAWABLE, "drawable", "", None),
        (PF_SLIDER, "startx", "Start X (%):", 0, (0, 100, 0.1)),
        (PF_SLIDER, "starty", "Start Y (%):", 0, (0, 100, 0.1)),
        (PF_SLIDER, "endx", "End X (%):", 0, (0, 100, 0.1)),
        (PF_SLIDER, "endy", "End Y (%):", 0, (0, 100, 0.1)),
        (PF_ADJUSTMENT, "degree", "Orientation degree:", 0, (0, 360, 0.1)),
        (PF_SPINNER, "radius", "Radius (%):", 0, (0, 100, 0.1)),
        (PF_INT, "blur", "Blur", 30),
        (PF_SLIDER, "lightness", "Lightness:", 0, (-100, 100, 1)),
        (PF_SLIDER, "saturation", "Saturation:", 0, (-100, 100, 1)),
        (PF_SLIDER, "contrast", "Contrast:", 0, (-100, 100, 1)),
        (PF_FILENAME, "maskfile", "Mask filename", ""),
    ],
    [],
    python_tiltshift, menu="<Image>/Filters/Blur"
    )

main()
