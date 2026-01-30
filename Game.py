import pygame
import sys
import Entities
from entity_assets_loader import load_images
import json

class tile_class(pygame.sprite.Sprite):
	def __init__(self,game,img, x, y, g_isPressed = False, tile_size = 16):
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pygame.image.load(img)
		self.image.set_colorkey((0, 0,0))
		self.img_w = self.image.get_width()
		self.img_h = self.image.get_height()
		self.rect = pygame.Rect(x*tile_size, y*tile_size, self.img_w, self.img_h)
		

	def update(self, scroll = [0, 0]):
		self.rect.x -= scroll[0]
		self.rect.y += scroll[1]

class Game(pygame.sprite.Sprite):
	def __init__(self,game):
		pygame.sprite.Sprite.__init__(self)
		self.game =game
		self.screen = self.game.screen
		self.display = pygame.Surface((400, 304))
		self.runGame = False
		self.FPS = self.game.FPS
		self.clock = pygame.time.Clock()
		self.able_to_jump = True
		self.player_pos = [0, 0]
		self.enemy_positions = []
		self.dash = False
		self.player = ''
		self.enemy = ''
		self.scroll_direction = [0,0]
		self.rect_scroll = [0, 0]
		self.tiles_with_collision = pygame.sprite.Group()
		self.enemyGroup = pygame.sprite.Group()
		self.tiles_without_collision = pygame.sprite.Group()
		self.bullet_group = pygame.sprite.Group()
		self.Physics_tilesArr = {}
		self.selected_lvl = ''
		self.data = ''
		self.bg = pygame.transform.scale(pygame.image.load('assets/background.png'), (400, 304))
		#self.particles_dict = {'particle/dash': load_images('assets/particles/particle')}



	def add_rect_to_tiles(self, file):
		self.tiles_ongrid= file[0]
		self.Physics_tilesArr.clear()
		for tile in self.tiles_ongrid:
			tile = self.tiles_ongrid[tile]


	def load_map(self, file):
		self.tiles_ongrid= file[0]
		self.tiles_offgrid = file[1]

		self.tiles_without_collision.empty()
		self.tiles_with_collision.empty()
		self.enemy_positions = []
		self.enemyGroup.empty()

		for tile in self.tiles_ongrid:
			tile = self.tiles_ongrid[tile]
			if tile['group']== 'decor':
				t = tile_class(self,tile['img'], tile['pos'][0]*16, tile['pos'][1]*16, True, 1)
				self.tiles_without_collision.add(t)

			if tile['group']=='spawners':
				if tile['img_name'] == '0.png':
					self.player_pos = [tile['pos'][0]*16,tile['pos'][1]*16]
				elif tile['img_name'] == '1.png':
					self.enemy_positions.append([tile['pos'][0]*16,tile['pos'][1]*16])

			else:
				t = tile_class(self,tile['img'], tile['pos'][0], tile['pos'][1])

			if tile['group'] == 'spawners'or tile['group']=='decor':
				pass
			else:
				self.Physics_tilesArr[str(tile['pos'][0]+self.rect_scroll[0])+';'+str(tile['pos'][1]+self.rect_scroll[1])] = self.tiles_ongrid[str(tile['pos'][0]+self.rect_scroll[0])+';'+str(tile['pos'][1]+self.rect_scroll[1])]
				self.tiles_with_collision.add(t)

			
		for tile in self.tiles_offgrid:
			t = tile_class(self,tile['img'], tile['pos'][0], tile['pos'][1], True, 1)
			self.tiles_without_collision.add(t)


	def game_loop(self, file):
		self.selected_lvl = file
		f = open(self.selected_lvl)
		self.data = json.load(f)
		self.load_map(self.data)
		f.close()
		self.player =Entities.player_entity(self,self.player_pos[0], self.player_pos[1],"C:\\Users\\nhlek\\OneDrive\\Documents\\python projects\\platfrormer\\data\\images\\entities\\player.png")	


		for enemyPos in self.enemy_positions:
			enemy = Entities.Enemy(self, enemyPos[0], enemyPos[1], 'assets/tiles/spawners/1.png', self.player.rect)
			self.enemyGroup.add(enemy)



		while self.runGame:
			self.display.fill((100, 149, 237))
			self.display.blit(self.bg, (0, 0))
			self.f = self.data[0]
			self.tiles_without_collision.draw(self.display)
			self.tiles_with_collision.draw(self.display)

			for tile in self.f:
				tile = self.f[tile]
				

			self.tiles_with_collision.update(self.scroll_direction)


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

					
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE and self.able_to_jump == True:
						self.player.jump = True
						self.able_to_jump = False


					if event.key== pygame.K_ESCAPE:
						self.game.selected_lvl = ''
						self.runGame = False
						self.game.runGUI = True


					if event.key == pygame.K_x:
						if self.dash == False:
							self.player.dash()
						self.dash = True


				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						self.player.jump = False

					if event.key == pygame.K_x:
						self.dash = False



			self.bullet_group.update()
			self.player.draw(self.display)
			self.player.move(self.display)
			self.bullet_group.draw(self.display)

			self.enemyGroup.draw(self.display)

			self.screen.blit(pygame.transform.scale(self.display, (800, 608)), (0, 0))
			pygame.display.flip()
			self.clock.tick(self.FPS)



