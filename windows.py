# Collect X-Window windows information
from Xlib.display import Display, X
from cloud_packer import CloudPacker

DISPLAY=":100"
MARGIN = 10

def listVisibleWindows(root):
   windows = []
   children = root.query_tree().children
   for w in children:
      if (w.get_wm_class() is not None):
         attrs = w.get_attributes()
         if attrs.map_state == X.IsViewable:
            windows.append(w)
      windows += listVisibleWindows(w)

   return windows

def move_window(window, x, y):
   window.configure(x=x, y=y)

display = Display(DISPLAY)
root = display.screen().root
root_width = root.get_geometry().width
root_height = root.get_geometry().height
root_aspect_ratio = root_width / root_height

windows = listVisibleWindows(root)

packer = CloudPacker()

blocks = []
for window in windows:
   blocks.append((window, window.get_geometry().width, window.get_geometry().height))

blocks = packer.fit(blocks, view_width=root_width, view_height=root_height, margin=MARGIN)

for window, x, y, w, h in blocks:
   print(window.get_wm_class(), window.get_wm_name(), window.get_geometry())
   move_window(window, round(x), round(y))

display.sync()
