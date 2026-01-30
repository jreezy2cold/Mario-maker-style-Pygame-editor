import pygame
import sys
import os
from Game import Game


class Levels:
	def __init__(self, game):
		self.game = game
		self.screen = self.game.screen
		self.display = pygame.Surface((400, 304)).convert()
		self.runGUI = False
		self.FPS = 60
		self.clock = pygame.time.Clock()
		self.levesArr = []
		self.index= 0
		self.Game = Game(self)
		self.selected_lvl = ''
		self.font_BIG = pygame.font.SysFont('Lucida Sans', 20)



	def draw_text(self,text,font, color, x, y):
		img = font.render(text,True, color)
		self.display.blit(img, (x, y))


	def click(self, lst, dictionary):
		
		mouse_clicked = pygame.mouse.get_pressed()[0]
		mouse= [pygame.mouse.get_pos()[0]//2, pygame.mouse.get_pos()[1]//2]

		for i in range(len(lst)):
			if dictionary[i].collidepoint(mouse[0], mouse[1]):
				if mouse_clicked:
					self.selected_lvl = lst[i]
					self.runGUI =False
					self.Game.runGame = True
					self.Game.game_loop(self.selected_lvl)
					
	def run(self):
		for file in os.listdir('LEVELS'):
			if file != 'Custom LEVELS':
				self.levesArr.append(str('LEVELS/'+str(file)))

		while self.runGUI:
			levels_linked_to_jsonArr = []
			self.display.fill((0,0, 0))
			

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.runGUI = False
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.runGUI=False
						self.selected_lvl= ''
					
			level_count = 0
			for y in range(4):
				for x in range(4):
					level_count += 1
					pygame.draw.rect(self.display, (255, 0, 0), ((x*100)+33, (y*76)+20, 40, 40))
					self.draw_text(str(level_count), self.font_BIG, (255, 255, 255), (x*100)+43, (y*76)+24)

					levels_linked_to_jsonArr.append(pygame.Rect((x*100)+33, (y*76)+20, 40, 40))

			self.click(self.levesArr, levels_linked_to_jsonArr)

			self.screen.blit(pygame.transform.scale(self.display, (800, 608)), (0, 0))
			pygame.display.update()
			self.clock.tick(self.FPS)

