import pygame
import os


def load_image(path):
	img = pygame.image.load("assets/"+path).convert()
	img.set_colorkey((0 , 0, 0))
	return img

def load_images(path):
	images = []
	for img_name in os.listdir('assets/'+path):
		images.append(load_image(path+'/'+img_name))
	return images
