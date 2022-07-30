import math
import random
from PIL import Image, ImageDraw

IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
ASPECT_RATIO = IMAGE_WIDTH / IMAGE_HEIGHT
RECTANGLES = 10
PADDING = 10
RADIUS = 10

def generate_rectangle():
   x = random.randint(0, 800)
   y = random.randint(0, 800)
   w = random.randint(0, 100)
   h = random.randint(0, 100)

   return [(x, y), (x + w, y + h)]

def rectangle_area(rectangle):
   [(x, y), (w, h)] = rectangle

   return ((w - x) * (h - y))

def rectangle_width(rectangle):
   [(x, y), (w, h)] = rectangle

   return (w - x)

def rectangle_height(rectangle):
   [(x, y), (w, h)] = rectangle

   return (h - y)

def find_largest_rectangle(rectangles):
   largest_rectangle = [(0, 0), (0, 0)]

   for rectangle in rectangles:
      if (rectangle_area(rectangle) > rectangle_area(largest_rectangle)):
         largest_rectangle = rectangle

   return largest_rectangle

def find_center_relative_coordinates_rectangle(rectangle):
   [(x1, y1), (x2, y2)] = rectangle

   return ((x2 - x1) / 2, (y2 - y1) / 2)

def find_center_absolute_coordinates_rectangle(rectangle):
   [(x1, y1), (x2, y2)] = rectangle

   return (((x2 - x1) / 2) + x1, ((y2 - y1) / 2) + y1)

def generate_original_image(rectangles):
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
   canvas = ImageDraw.Draw(image)

   for idx, rectangle in enumerate(rectangles):
      # noinspection SpellCheckingInspection
      color = "#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])
      canvas.rectangle(rectangle, fill=color)

      [position, _] = rectangle
      canvas.text(position, f"#{idx}")

   image.save("cloud-original.png", "PNG")

def generate_centered_rectangle(rectangle):
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
   canvas = ImageDraw.Draw(image)

   wx, wy = (IMAGE_WIDTH / 2), (IMAGE_HEIGHT / 2)
   px, py = find_center_relative_coordinates_rectangle(rectangle)

   destination = ((wx - px), (wy - py)), ((wx + px), (wy + py))
   canvas.rectangle(destination, fill="White")

   image.save("cloud-centered-rectangle.png", "PNG")

def generate_aligned_rectangles(rectangles, filename = "cloud-aligned-rectangles.png"):
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
   canvas = ImageDraw.Draw(image)

   step = IMAGE_WIDTH / RECTANGLES

   for idx, rectangle in enumerate(rectangles):
      px, py = find_center_relative_coordinates_rectangle(rectangle)

      destination = ((step * idx), ((IMAGE_HEIGHT / 2) - py)), ((step * idx) + (px * 2), ((IMAGE_HEIGHT / 2) + py))
      canvas.rectangle(destination, fill="White")

   image.save(filename, "PNG")

def move_to_rectangle(rectangle, x, y):
   (x1, y1), (x2, y2) = rectangle
   px, py = (x2 - x1) / 2, (y2 - y1) / 2

   return ((x - px, y - py), (x + px, y + py))

def is_intersect_rectangle(a, b):
   intersect = True
   [(ax, ay), (aw, ah)] = a
   [(bx, by), (bw, bh)] = b

   if ((ax >= bw) or (aw <= bx) or (ah <= by) or (ay >= bh)):
      intersect = False

   return intersect

def is_intersect_rectangles(a, rectangles):
   for b in rectangles:
      if (is_intersect_rectangle(a, b)):
         return True

   return False

def spiral_generator(step = 10, radius = 1.0):
   h = (IMAGE_WIDTH / 2)
   k = (IMAGE_HEIGHT / 2)
   theta = 0
   r = 0

   while True:
      x = h + (r * ASPECT_RATIO) * math.cos(theta)
      y = k + (r * 1 / ASPECT_RATIO) * math.sin(theta)

      yield (round(x), round(y))

      theta += step
      r += radius

      if (theta > 360):
         theta = 0

def generate_image_cloud(rectangles):
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
   canvas = ImageDraw.Draw(image)

   centerfold = rectangles[0]
   px, py = find_center_relative_coordinates_rectangle(centerfold)
   rectangle = move_to_rectangle(centerfold, (IMAGE_WIDTH / 2), (IMAGE_HEIGHT / 2))
   canvas.rectangle(rectangle, fill="White")

   h = (IMAGE_WIDTH / 2)
   k = (IMAGE_HEIGHT / 2)
   rx = RADIUS + px
   ry = RADIUS + py

   increment = 360 / len(rectangles)
   for step, rectangle in enumerate(rectangles[1:]):
      print(f"{step}: {rectangle}")
      nx, ny = find_center_relative_coordinates_rectangle(rectangle)

      # TODO: find intersection, loop until false, increase rx and/or ry
      x = h + (rx + nx) * math.cos(step * increment)
      y = k + (ry + ny) * math.sin(step * increment)

      shape = move_to_rectangle(rectangle, x, y)
      # noinspection SpellCheckingInspection
      color = "#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])
      canvas.rectangle(shape, fill=color)

   image.save("cloud-image.png", "PNG")

def generate_image_cloud_experimental(rectangles):
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT), color="White")
   canvas = ImageDraw.Draw(image)

   rectangles.sort(key=rectangle_area, reverse=True)

   spiral = spiral_generator(20, 1.5)

   for step, rectangle in enumerate(rectangles):
      shape = move_to_rectangle(rectangle, *next(spiral))
      print(f"rectangle: {rectangle}, shape: {shape}")
      while (step and is_intersect_rectangles(shape, rectangles)):
         print(f"intersecting: {shape}")
         shape = move_to_rectangle(rectangle, *next(spiral))
      rectangles[step] = shape

      # noinspection SpellCheckingInspection
      color = "#" + ''.join([random.choice('ABCDEF0123456789') for _ in range(6)])
      canvas.rectangle(shape, fill=color)

   image.save("cloud-spiral-experimental.png", "PNG")

# https://www.mathopenref.com/coordcirclealgorithm.html
def draw_circle():
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
   canvas = ImageDraw.Draw(image)

   h = (IMAGE_WIDTH / 2)
   k = (IMAGE_HEIGHT / 2)
   r = 100

   step = 15

   for theta in range(0, 360, step):
      x = h + r * math.cos(theta)
      y = k + r * math.sin(theta)
      canvas.text((x, y), f"{theta}")

   image.save("cloud-circle.png", "PNG")

def draw_spiral():
   image = Image.new("RGB", (IMAGE_WIDTH, IMAGE_HEIGHT))
   canvas = ImageDraw.Draw(image)

   h = (IMAGE_WIDTH / 2)
   k = (IMAGE_HEIGHT / 2)
   rx = ry = 0

   step = 10

   for theta in range(0, 360, step):
      x = h + rx * math.cos(theta)
      y = k + ry * math.sin(theta)
      canvas.text((x, y), f"{theta}")
      rx = rx + 16
      ry = ry + 9

   image.save("cloud-spiral.png", "PNG")

def main():
   rectangles = []

   for n in range(RECTANGLES):
      rectangles.append(generate_rectangle())

   print(rectangles)

   rectangle = find_largest_rectangle(rectangles)
   print(f"The largest rectangle is {rectangle}.")

   rectangles.sort(key=rectangle_area, reverse=True)
   print(rectangles)

   # Display the resulting image
   generate_original_image(rectangles)

   print(f"Image center coordinates: ({IMAGE_WIDTH / 2}, {IMAGE_HEIGHT / 2})")

   print(f"Largest rectangle {rectangles[0]} center coordinates: {find_center_absolute_coordinates_rectangle(rectangles[0])}, relative coordinates: {find_center_relative_coordinates_rectangle(rectangles[0])}")

   generate_centered_rectangle(rectangles[0])
   generate_aligned_rectangles(rectangles)

   draw_circle()

   draw_spiral()

   generate_image_cloud(rectangles)

   rectangles.sort(key=rectangle_width)
   generate_aligned_rectangles(rectangles, "cloud-width-rectangles.png")

   rectangles.sort(key=rectangle_height)
   generate_aligned_rectangles(rectangles, "cloud-width-height.png")

   generate_image_cloud_experimental(rectangles)

if __name__ == '__main__':
   main()
