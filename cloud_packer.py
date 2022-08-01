# Window Cloud Packer
# Packing a list of tuples (id, w, h)
# Returning a list of tuples (id, x, y)
import math

class CloudPacker():
   # TODO: assign a weight to each window according to their area, width, height.
   #       These will be used to determine the order in which the windows are placed,
   #       in accordance with the aspect ratio of the root window.
   def organic_sort(self, block):
      return (block[1] * block[2])

   def fit(self, blocks, view_width, view_height, margin=0, sorting="organic"):
      self.view_width = view_width
      self.view_height = view_height
      self.aspect_ratio = view_width / view_height
      self.margin = margin # TODO: implement margin

      blocks.sort(key=self.organic_sort, reverse=True)

      placements = []
      spiral = self.spiral_generator(20, 1.5)

      for position, block in enumerate(blocks):
         window, w, h = block
         px, py = next(spiral)
         dx, dy = self.find_window_center_coordinates([window, px - margin, py - margin, w + margin, h + margin])

         block = [window, dx - margin, dy - margin, w + margin, h + margin]

         while(position and self.is_window_intersect_view(block, placements)):
            px, py = next(spiral)
            dx, dy = self.find_window_center_coordinates([window, px - margin, py - margin, w + margin, h + margin])
            block = [window, dx - margin, dy - margin, w + margin, h + margin]

         placements.append([window, dx, dy, w, h])

      return placements

   def spiral_generator(self, step=10, radius=1.0):
      h = (self.view_width / 2)
      k = (self.view_height / 2)
      theta = 0
      r = 0

      while True:
         x = h + (r * self.aspect_ratio) * math.cos(theta)
         y = k + (r * 1 / self.aspect_ratio) * math.sin(theta)

         yield (round(x), round(y))

         theta += step
         r += radius

         if (theta > 360):
            theta = 0

   def is_window_intersect_view(self, window, windows):
      for w in windows:
         if (window[0] != w[0] and self.is_window_intersect(window, w)):
            return True
      return False

   def is_window_intersect(self, window1, window2):
      _, x1, y1, w1, h1 = window1
      _, x2, y2, w2, h2 = window2
      return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)

   def find_window_center_coordinates(self, window):
      _, x, y, w, h = window
      return (x - (w / 2), y - (h / 2))
