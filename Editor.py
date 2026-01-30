import pygame
import sys
import os
import math
import tkinter.messagebox
from tkinter import filedialog
import json


class tile_class(pygame.sprite.Sprite):
	def __init__(self,img, x, y, g_isPressed = False, tile_size = 16):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(img)
		self.image.set_colorkey((0, 0,0))
		self.img_w = self.image.get_width()
		self.img_h = self.image.get_height()
		self.rect = pygame.Rect(x*tile_size, y*tile_size, self.img_w, self.img_h)


	def update(self, scroll = (0, 0)):
		self.rect.x += scroll[0]
		self.rect.y += scroll[1]

class Mouse_sprite(pygame.sprite.Sprite):
	def __init__(self,x, y):
		pygame.sprite.Sprite.__init__(self)
		self.rect = pygame.Rect(x, y, 1, 1)

class Editor():
	def __init__(self, game):
		pygame.init()
		self.game = game
		self.screen = self.game.screen
		self.display = pygame.Surface((400, 304)).convert_alpha()
		self.FPS = self.game.FPS
		self.clock = self.game.clock
		self.runEditor = False
		self.tile_folder = ['decor','grass','large_decor','spawners','stone']
		self.tile_folder_index = 0
		self.img_tile_lst = []
		self.img_name_lst = []
		self.tile_selected = ''
		self.name_of_selected_tile = ''
		self.tile_group = pygame.sprite.Group()
		self.selector_group = pygame.sprite.Group()
		self.g_isPressed = False
		self.pos_taken_by_physicsTiles = set()
		self.autoMap = {tuple(sorted([(1, 0),(0, 1)])):'0.png', tuple(sorted([(1,0),(-1,0), (0,1)])):"1.png",tuple(sorted([(-1,0),(0, 1)])):'2.png', tuple(sorted([(-1, 0), (0, 1), (0, -1)])):'3.png', tuple(sorted([(-1, 0),(0,-1)])):"4.png", tuple(sorted([(-1, 0),(1,0), (0, -1)])):'5.png',tuple(sorted([(1, 0),(0,-1)])):"6.png",tuple(sorted([(1,0),(0,-1), (0,1)])):'7.png',tuple(sorted([(1,0),(-1, 0),(0, 1),(0,-1)])):'8.png'}
		self.physics_tiles = {'grass', 'stone'}
		self.tiles_ongrid = {}
		self.tiles_offgrid = []
		self.tile_selected_history = []
		self.constant_point_offDisplay = 0
		self.constant_point_onDisplay = 0
		self.selector_run = False
		self.physics_tiles_counter = 0
		self.scroll = [0, 0]
		self.Selector_collided_tiles = set()
		self.player_spawner_cood = ''#only take 1 set of cood
		self.enemy_spanwer_cood = []#takes all the enemy cood points
		self.save_button_border = (255,100,234)
		self.load_button_border = (255,100,234)
		self.create_new_file_border = (255, 100, 234)
		self.font_small = pygame.font.SysFont('Lucida Sans', 10)
		self.selected_lvl = ''

	def selector(self):
		m_posOffDisplay = (int(pygame.mouse.get_pos()[0]/2), int(pygame.mouse.get_pos()[1]/2))
		m_pos = (int(pygame.mouse.get_pos()[0]/2), int(pygame.mouse.get_pos()[1]/2))
		constant_point = self.constant_point_onDisplay

		GREEN = (0, 200, 0)

		#the selector rect
		#used to delete values on display on grid
		pygame.draw.line(self.display,GREEN ,(constant_point), (m_pos[0], constant_point[1]), 3)
		pygame.draw.line(self.display,GREEN ,(constant_point), (constant_point[0], m_pos[1]), 3)
		pygame.draw.line(self.display,GREEN ,(constant_point[0], m_pos[1]), (m_pos[0], m_pos[1]), 3)
		pygame.draw.line(self.display,GREEN ,(m_pos), (m_pos[0], constant_point[1]), 3)

		#logic
		group = self.tile_group.sprites()

		for tile in group:
			x = tile.rect.x//16
			y = tile.rect.y//16

			if x >= constant_point[0]//16 and y >= constant_point[1]//16 and x< (m_posOffDisplay[0]//16)+1 and y < (m_posOffDisplay[1]//16)+1:
				pygame.draw.rect(self.display, GREEN, (x*16, y*16, 16, 16),1)
				self.Selector_collided_tiles.add(str(x-(self.scroll[0]//16))+";"+str(y-(self.scroll[1]//16)))
				self.pos_taken_by_physicsTiles.add(tile)
				

			if x <= constant_point[0]//16 and y <= constant_point[1]//16 and x> (m_posOffDisplay[0]//16) and y > (m_posOffDisplay[1]//16):
				pygame.draw.rect(self.display, GREEN, (x*16, y*16, 16, 16),1)
				self.Selector_collided_tiles.add(str(x-(self.scroll[0]//16))+";"+str(y-(self.scroll[1]//16)))
				self.pos_taken_by_physicsTiles.add(tile)


			if x <= constant_point[0]//16 and y >= constant_point[1]//16 and x > (m_posOffDisplay[0]//16) and y < (m_posOffDisplay[1]//16):
				pygame.draw.rect(self.display, GREEN, (x*16, y*16, 16, 16),1)
				self.Selector_collided_tiles.add(str(x-(self.scroll[0]//16))+";"+str(y-(self.scroll[1]//16)))
				self.pos_taken_by_physicsTiles.add(tile)


			if x>= constant_point[0]//16 and y <= constant_point[1]//16 and x < (m_posOffDisplay[0]//16) and y > (m_posOffDisplay[1]//16):
				pygame.draw.rect(self.display, GREEN, (x*16, y*16, 16, 16),1)
				self.Selector_collided_tiles.add(str(x-(self.scroll[0]//16))+";"+str(y-(self.scroll[1]//16)))
				self.pos_taken_by_physicsTiles.add(tile)


	def del_from_selecter(self):
		for i in self.pos_taken_by_physicsTiles:
			i.kill()
		
		for i in self.Selector_collided_tiles:
			if len(self.player_spawner_cood)!= 0:
				if i == str(self.player_spawner_cood[0]//16)+';'+str(self.player_spawner_cood[1]//16):
					self.player_spawner_cood.clear()
			try:
				del self.tiles_ongrid[i]
			except KeyError as e:
				continue
		self.Selector_collided_tiles.clear()


	def load_tile(self):
		self.img_tile_lst= []
		self.img_name_lst =[]
		for img in os.listdir('assets/tiles/'+self.tile_folder[self.tile_folder_index]):
			self.img_name_lst.append(img)
			self.img_tile_lst.append('assets/tiles/'+self.tile_folder[self.tile_folder_index]+'/'+img)

	def draw_text(self,text,font, color, x, y):
		img = font.render(text,True, color)
		self.display.blit(img, (x, y))


	def display_load_tile(self):
		#this sets up the widget for the tiles

		pygame.draw.rect(self.display, (255,100,234), (0, 0,32, 304))
		for img in self.img_tile_lst:
			y = self.img_tile_lst.index(img)
			tile = pygame.image.load(img).convert_alpha()
			tile = pygame.transform.scale(tile, (16, 16))
			self.display.blit(tile, (10, 10+y*25))


	def apply_rects_to_tiles(self):
		mouse_key = pygame.mouse.get_pressed()[0]
		tile_selected_history = []
		for i in range(len(self.img_tile_lst)):
			if pygame.Rect(10, 10+i*25, 16,16).collidepoint(int(pygame.mouse.get_pos()[0]/2),int(pygame.mouse.get_pos()[1]/2)):
				pygame.draw.rect(self.display, (255, 255, 255), (10, 10+i*25, 16,16), 2)
				if mouse_key:
					tile_selected_history.append(self.img_tile_lst[i])
					self.tile_selected_history = tile_selected_history
					self.tile_selected = self.img_tile_lst[i]
					self.name_of_selected_tile = self.img_name_lst[i]


	def load_map(self, file):
		self.tiles_ongrid= file[0]
		self.tiles_offgrid = file[1]
		for tile in self.tiles_ongrid:
			tile = self.tiles_ongrid[tile]
			t = tile_class(tile['img'], tile['pos'][0], tile['pos'][1])
			self.tile_group.add(t)

			
		for tile in self.tiles_offgrid:
			t = tile_class(tile['img'], tile['pos'][0], tile['pos'][1], True, 1)
			self.tile_group.add(t)


	def save_and_load_buttons(self):
		mouse = [pygame.mouse.get_pos()[0]/2, pygame.mouse.get_pos()[1]/2]
		click = pygame.mouse.get_pressed()[0]

		pygame.draw.rect(self.display,(255,100,234), (32, 284, 368, 20))


		#save button border
		if pygame.Rect(35, 289, 82, 12).collidepoint(mouse):
			self.save_button_border = (255, 0, 0)
			if click:
				if self.selected_lvl == '':
					f = filedialog.asksaveasfilename(defaultextension = '.json',filetypes = [('Json File', '*.json')])
					if f:
						self.selected_lvl=f
				if self.selected_lvl != '':
					tiles_ongrid = json.dumps([self.tiles_ongrid,self.tiles_offgrid, self.enemy_spanwer_cood], indent =1)
					with open(self.selected_lvl, "w") as openfile:
						openfile.write(tiles_ongrid)

		else:
			self.save_button_border = (255,100,234)

		pygame.draw.rect(self.display, self.save_button_border, (35, 289, 82, 12))
		#save_botton
		pygame.draw.rect(self.display, (255, 255, 255), (36, 290, 80, 10))
		self.draw_text('save file', self.font_small, (0, 0, 0), 40, 288)


		#load button border
		
		if pygame.Rect(140,290, 80, 10).collidepoint(mouse):
			self.load_button_border = (255, 0, 0)
			if click:
				self.tile_group.empty()
				file = filedialog.askopenfilename(filetypes=[('Json Files', '*.json')])
				self.selected_lvl = file
				try:
					f = open(self.selected_lvl)
					self.data = json.load(f)
					self.load_map(self.data)
					f.close()
				except FileNotFoundError:
					pass
		else:
			self.load_button_border = (255, 100, 234)

		pygame.draw.rect(self.display, self.load_button_border, (139, 289, 82, 12))
		#load button
		pygame.draw.rect(self.display, (255, 255, 255), (140,290, 80, 10))
		self.draw_text('Load file', self.font_small, (0, 0, 0), 144, 288)


		if pygame.Rect(254, 290, 80, 10).collidepoint(mouse):
			self.create_new_file_border = (255, 0, 0)
			if click:
				f = filedialog.asksaveasfilename(defaultextension = '.json',filetypes = [('Json File', '*.json')])
				if f:
					self.selected_lvl=f
					self.tile_group.empty()
		else:
			self.create_new_file_border =(255, 100, 234)

		pygame.draw.rect(self.display,self.create_new_file_border, (253, 289, 82, 12))
		pygame.draw.rect(self.display, (255, 255, 255), (254, 290, 80, 10))
		self.draw_text('Create new file', self.font_small, (0, 0, 0), 257, 288)



					
	def add_selected_tile_to_offgrid(self):
		m_pos = pygame.mouse.get_pos()
		m_pos = ((int(m_pos[0]/2)-8),(int(m_pos[1]/2)-8))
		if self.tile_selected != '':
			self.tiles_offgrid.append({'img':self.tile_selected,'group':self.tile_folder[self.tile_folder_index], 'pos':(int(m_pos[0])-self.scroll[0], int(m_pos[1])-self.scroll[1]), "img_name":self.name_of_selected_tile})
			tile = tile_class(self.tile_selected, m_pos[0], m_pos[1], True,1)
			self.tile_group.add(tile)
			

	def add_selected_tile_to_ongrid(self):
		m_pos = pygame.mouse.get_pos()
		m_pos = (int(m_pos[0]/2), int(m_pos[1]/2))

		if self.tile_selected != '':

			if self.tile_folder[self.tile_folder_index] == 'spawners' and self.name_of_selected_tile == '0.png':
				if self.player_spawner_cood != '':
					tkinter.messagebox.showinfo("Player already exists",f"You already have a player spawner at {self.player_spawner_cood},delete that 1 in order to place a new one")
				else:
					self.player_spawner_cood = str(int((m_pos[0]-self.scroll[0])//16))+";"+str(int((m_pos[1]-self.scroll[1])//16))

					self.tiles_ongrid[str(int((m_pos[0]-self.scroll[0])//16))+";"+str(int((m_pos[1]-self.scroll[1])//16))] = {'img':self.tile_selected,'group':self.tile_folder[self.tile_folder_index], 'pos':(int((m_pos[0]-self.scroll[0])//16), int((m_pos[1])-self.scroll[1])//16), 'count':self.physics_tiles_counter, "img_name":self.name_of_selected_tile}
					tile = tile_class(self.tile_selected, int(m_pos[0]//16), int(m_pos[1]//16))
					self.tile_group.add(tile)
					

			else:
				self.tiles_ongrid[str(int((m_pos[0]-self.scroll[0])//16))+";"+str(int((m_pos[1]-self.scroll[1])//16))] = {'img':self.tile_selected,'group':self.tile_folder[self.tile_folder_index], 'pos':(int((m_pos[0]-self.scroll[0])//16), int((m_pos[1])-self.scroll[1])//16), 'count':self.physics_tiles_counter, "img_name":self.name_of_selected_tile}
				tile = tile_class(self.tile_selected, int(m_pos[0]//16), int(m_pos[1]//16))
				self.tile_group.add(tile)
			

	def display_tiles_on_display(self):
		self.tile_group.draw(self.display)

	def del_tile(self):
		m_pos = pygame.mouse.get_pos()
		m_pos2 = (int((m_pos[0]/2)//16), int((m_pos[1]/2)//16))
		mouse_sprite = Mouse_sprite(int(m_pos[0]/2),int(m_pos[1]/2))

		if self.tile_folder[self.tile_folder_index] == 'spawners' and self.name_of_selected_tile == '0.png':
			if self.player_spawner_cood!= '' and self.player_spawner_cood in self.tiles_ongrid:
				del self.tiles_ongrid[self.player_spawner_cood]
				self.player_spawner_cood = ''

		for tile in self.tiles_offgrid:
			img = pygame.image.load(tile['img'])
			tile_r = pygame.Rect(tile['pos'][0],tile['pos'][1],img.get_width(),img.get_height())

			if tile_r.collidepoint(((int(m_pos[0]/2)-8)-self.scroll[0], (int(m_pos[1]/2)-8)-self.scroll[1])):
				self.tiles_offgrid.remove(tile)
				

		for tile in self.tile_group:
			if pygame.sprite.collide_rect(tile, mouse_sprite):
				tile.kill()

		if str(int(((m_pos[0]/2)-self.scroll[0])//16)) +";"+ str(int(((m_pos[1]/2)-self.scroll[1])//16)) in self.tiles_ongrid:
			del self.tiles_ongrid[str(int(((m_pos[0]/2)-self.scroll[0])//16)) +";"+ str(int(((m_pos[1]/2)-self.scroll[1])//16))]
			
	def process_AutoTiles(self,g):
		for i in list(g):
			tileC = tile_class(g[i]['img'],g[i]['pos'][0]+self.scroll[0]//16,g[i]['pos'][1]+self.scroll[1]//16)
			self.tile_group.add(tileC)
		self.Selector_collided_tiles.clear()


	def auto_complete(self):
		g = {}
		for tilex in self.Selector_collided_tiles:
			try:
				tile = self.tiles_ongrid[tilex]
				#print("before:"+str(tile))
				neighbours = set()
				for shift in  [(-1, 0), (1, 0), (0,-1), (0, 1)]:
					check_loc = str(tile['pos'][0]+shift[0])+';'+str(tile['pos'][1]+shift[1])
					if check_loc in self.tiles_ongrid:
						if self.tiles_ongrid[check_loc]['group'] == tile['group']:
							neighbours.add(shift)

				neighbours = tuple(sorted(neighbours))


				if (tile['group'] in self.physics_tiles) and (neighbours in self.autoMap):				
					tile['img'] = "assets/tiles/"+tile['group']+"/"+self.autoMap[neighbours]

					tile = {"img":tile['img'], 'group':self.tile_folder[self.tile_folder_index], 'pos':tile['pos'], 'count':tile['count']}
					g[tilex]=tile


			except KeyError as e:
				continue
		self.process_AutoTiles(g)
		del neighbours


	def know_selected_tile(self, x, y,grid = 16, shift = (0, 0)):
		if self.tile_selected != '':
			tile = pygame.image.load(self.tile_selected).convert_alpha()
			tile.set_colorkey((0, 0, 0))
			tile.set_alpha(125)
			pygame.draw.rect(self.display, (0, 255, 0), ((x-shift[0])*grid, (y-shift[1])*grid, grid, grid), 1)
			self.display.blit(tile, ((x-shift[0])*grid, (y-shift[1])*grid))

	def draw_grid(self):
		for i in  range(int(400/16)):
			pygame.draw.line(self.display, (255, 255, 255), (i*16, 0), (i*16,304),1)
		for z in range(int(304/16)):
			pygame.draw.line(self.display,(255,255,255), (0, z*16), (400, z*16),1)


	def run_editor(self):
		while self.runEditor:
			self.display.fill((0,0,0))
			self.load_tile()
			self.display_tiles_on_display()
			self.display_load_tile()
			self.save_and_load_buttons()
			self.apply_rects_to_tiles()
				
			m_pos = pygame.mouse.get_pos()
			key = pygame.key.get_pressed()
			mouse_key = pygame.mouse.get_pressed()
				
			if self.constant_point_offDisplay != 0 and self.selector_run == True:
				self.selector()
					

			else:
				self.constant_point_offDisplay = 0
				self.selector_run = False
				self.pos_taken_by_physicsTiles.clear()
					

			if self.g_isPressed == False:
				self.know_selected_tile(int((m_pos[0]/2)/16), int((m_pos[1]/2)/16))
			else:
				self.know_selected_tile(int(m_pos[0]/2), int(m_pos[1]/2),1, (8, 8))


			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.runEditor = False
					

				if key[pygame.K_LSHIFT]:
					self.selector_run = True
					self.tile_selected = ''

					if event.type == pygame.MOUSEBUTTONDOWN:
						self.constant_point_offDisplay = (int(m_pos[0]/2)-self.scroll[0], int(m_pos[1]/2)-self.scroll[1])
						self.constant_point_onDisplay = (int(m_pos[0]/2), int(m_pos[1]/2))

					if event.type == pygame.KEYDOWN:
						if  event.key == pygame.K_a:
							self.tile_folder_index= self.tile_folder_index-1%len(self.img_tile_lst)
							
							if self.tile_folder_index <-4:
								self.tile_folder_index =0
								self.load_tile()

						if event.key == pygame.K_d:
							self.tile_folder_index= self.tile_folder_index+1%len(self.img_tile_lst)
								
							if self.tile_folder_index >4:
								self.tile_folder_index =0
								self.load_tile()

						if event.key == pygame.K_t:
							if len(self.pos_taken_by_physicsTiles)>0:
								self.auto_complete()

						if event.key == pygame.K_q:
							if len(self.pos_taken_by_physicsTiles)>0:
								self.del_from_selecter()
								self.pos_taken_by_physicsTiles.clear()
				else:
					self.selector_run = False
					if len(self.tile_selected_history)>0:
							self.tile_selected =  self.tile_selected_history[0]

				if not key[pygame.K_LSHIFT]:
					if key[pygame.K_a]:
						self.scroll[0]-=16
						self.tile_group.update((-16, 0))
					if key[pygame.K_d]:
						self.scroll[0]+=16
						self.tile_group.update((16, 0))
					if key[pygame.K_w]:
						self.scroll[1]+=16
						self.tile_group.update((0, 16))
					if key[pygame.K_s]:
						self.scroll[1]-=16
						self.tile_group.update((0, -16))


					
				m_pos2 = (int((m_pos[0]/2)), int((m_pos[1]/2)))
				if pygame.mouse.get_pos()[0]>64 and pygame.mouse.get_pos()[1]<568:
					if key[pygame.K_g]:
						self.g_isPressed = True
						if event.type == pygame.MOUSEBUTTONDOWN:
							if event.button == 1:
								if self.tile_selected!="":
									self.physics_tiles_counter+=1
									self.add_selected_tile_to_offgrid()
									


					else:
						self.g_isPressed = False
						if mouse_key[0]:
							if str(int((m_pos2[0]-self.scroll[0])//16)) +';'+str(int((m_pos2[1])-self.scroll[1])//16) not in self.tiles_ongrid:
								if self.tile_selected!="":
									self.physics_tiles_counter+=1
									self.add_selected_tile_to_ongrid()

									

				if mouse_key[2]:
					self.del_tile()


			self.screen.blit(pygame.transform.scale(self.display, (800, 608)), (0, 0))
			pygame.display.update()
			self.clock.tick(self.FPS)
