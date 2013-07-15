#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Plug-in:      Scale Layer to Image Size
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

def python_tiltshift(image, drawable, startx=20, endx=50, starty=20, endy=50,
                     degree=45, radius=20, lightness=0, saturation=0, blur=30, channel=None):

    image.disable_undo()


    width = drawable.width
    height = drawable.height

    background = image.active_layer
    image.add_layer(background.copy())
    toplayer = image.layers[0]
    pdb.plug_in_gauss_rle(image, toplayer, blur, 1, 1)

    gradient_mask = pdb.gimp_layer_create_mask(toplayer, 0)

    gr = pdb.gimp_gradient_new("tiltshift")
    #TODO: define gradient

    if not channel is None:
        #TODO: open png channel file, copy Red||Green||Blue channel instead
        selection_mask = pdb.gimp_layer_create_mask(toplayer,0)
        mychannel = ""
        for ch in image.channels:
            if ch.name == channel:
                mychannel = ch
        mymask = pdb.gimp_layer_create_mask(toplayer, 0)
        pdb.gimp_channel_combine_masks(gradient_mask, mychannel, 1, 0, 0)


    pdb.gimp_layer_add_mask(toplayer, gradient_mask)



    image.flatten()
    image.enable_undo()


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
        (PF_SLIDER, "lightness", "Lightness:", 0, (-100, 100, 1)),
        (PF_SLIDER, "saturation", "Saturation:", 0, (-100, 100, 1)),
        (PF_INT, "blur", "Blur", 30)
    ],
    [],
    python_tiltshift, menu="<Image>/Layer/"
    )

main()
