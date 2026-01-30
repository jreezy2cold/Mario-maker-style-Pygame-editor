import pygame
import sys
from Editor import Editor
from Game import Game
from levels_GUI import Levels

class GUI:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((800, 608))
		self.run = True
		self.clock = pygame.time.Clock()
		self.FPS = 60
		self.font_BIG = pygame.font.SysFont('Lucida Sans', 10)
		self.font_small = pygame.font.SysFont('Lucida Sans', 20)
		self.selected_lvl = ''
		self.editor = Editor(self)
		self.levelsGUI = Levels(self)
		self.display = pygame.Surface((400, 304))
		self.click = False


	def draw_text(self,text,font, color, x, y):
		img = font.render(text,True, color)
		self.display.blit(img, (x, y))

	def runn(self):
		while self.run:
			self.display.fill((0, 0, 0))

			EditorButton = pygame.Rect(150, 90, 100, 20)
			GameButton = pygame.Rect(150, 140, 100, 20)
			
			pygame.draw.rect(self.display, (255, 0, 0), EditorButton)
			pygame.draw.rect(self.display, (255, 0, 0), GameButton)
			mx, my = pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2


			self.draw_text("LEVEL EDITOR", self.font_BIG, (255,255,255), 167, 93)
			self.draw_text("PLAY GAME", self.font_BIG, (255,255,255), 170, 143)

			if EditorButton.collidepoint(int(mx),int(my)):
				if self.click == True:
					self.editor.runEditor = True
					self.editor.run_editor()


			if GameButton.collidepoint(int(mx),int(my)):
				if self.click == True:
					self.levelsGUI.runGUI = True
					self.levelsGUI.run()
	

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					self.run = False
					

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						self.click = True
				else:
					self.click=False

			self.screen.blit(pygame.transform.scale(self.display, (800, 608)), (0, 0))
			pygame.display.update()
			self.clock.tick(self.FPS)
			

GUI().runn()