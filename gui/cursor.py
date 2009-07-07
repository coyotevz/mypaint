# This file is part of MyPaint.
# Copyright (C) 2009 by Martin Renold <martinxyz@gmx.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import gtk
gdk = gtk.gdk

# caching only the last cursor
last_cursor_info = None
last_cursor = None

def get_brush_cursor(radius, is_eraser):
    global last_cursor, last_cursor_info
    # OPTIMIZE: looks like big cursors can be a major slowdown with X11

    d = int(radius)*2
    if d < 6: d = 6
    if is_eraser and d < 8: d = 8
    if d > 500: d = 500 # hm, better ask display for max cursor size? also, 500 is pretty slow
    cursor_info = (d, is_eraser)
    if cursor_info != last_cursor_info:
        last_cursor_info = cursor_info

        cursor = gdk.Pixmap(None, d+1, d+1,1)
        mask   = gdk.Pixmap(None, d+1, d+1,1)
        colormap = gdk.colormap_get_system()
        black = colormap.alloc_color('black')
        white = colormap.alloc_color('white')

        bgc = cursor.new_gc(foreground=black)
        wgc = cursor.new_gc(foreground=white)
        cursor.draw_rectangle(wgc, True, 0, 0, d+1, d+1)
        cursor.draw_arc(bgc,False, 0, 0, d, d, 0, 360*64)

        bgc = mask.new_gc(foreground=black)
        wgc = mask.new_gc(foreground=white)
        mask.draw_rectangle(bgc, True, 0, 0, d+1, d+1)
        mask.draw_arc(wgc, False, 0, 0, d, d, 0, 360*64)
        mask.draw_arc(wgc, False, 1, 1, d-2, d-2, 0, 360*64)

        if is_eraser:
            thickness = d/8
            mask.draw_rectangle(bgc, True, d/2-thickness, 0, 2*thickness+1, d+1)
            mask.draw_rectangle(bgc, True, 0, d/2-thickness, d+1, 2*thickness+1)

        last_cursor = gdk.Cursor(cursor,mask,gdk.color_parse('black'), gdk.color_parse('white'),(d+1)/2,(d+1)/2)

    return last_cursor
