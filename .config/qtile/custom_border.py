import xcffib
import functools
from libqtile.backend.x11 import xcbq

def _enable(style):
    xcbq.Window.paint_borders = style

def set_bar_border():

    def _style(self, position, width, color):
        core = self.conn.conn.core
        pixmap = self.conn.conn.generate_id()
        core.CreatePixmap(self.conn.default_screen.root_depth, pixmap, self.wid, 0, width)
        gc = self.conn.conn.generate_id()
        core.CreateGC(gc, pixmap, xcffib.xproto.GC.Foreground, color)
        rect = xcffib.xproto.RECTANGLE.synthetic(width, width)
        core.PolyFillRectangle(pixmap, gc, 1, [rect])
        core.FreePixmap(pixmap)
        core.FreeGC(gc)

    _enable(_style)
