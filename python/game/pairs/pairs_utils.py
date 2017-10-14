import math
import os
import pygame

#Lerp between two rgb 3-tuples
# 0 <= t <= 1 
def color_lerp(color1, color2, t):
    r1 = color1[0]
    g1 = color1[1]
    b1 = color1[2]

    r2 = color2[0]
    g2 = color2[1]
    b2 = color2[2]

    return (r1 + (r2 - r1) * t, g1 + (g2 - g1) * t, b1 + (b2 - b1) * t)

def load_image(name):
   fullname = os.path.join('data/', name)
   image = pygame.image.load(fullname)
   image = image.convert()
   return image, image.get_rect()

