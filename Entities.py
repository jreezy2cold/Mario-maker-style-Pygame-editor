import pygame
import random
from entity_assets_loader import load_images, load_image
import math


class player_entity:
	def __init__(self,game, x, y,img):
		self.player_img = pygame.image.load(img)
		self.size = self.player_img.get_size()
		self.game=game
		self.x =x
		self.y = y
		self.rect = pygame.Rect(x, y,self.size[0],self.size[1])
		self.vel_y =0
		self.count = 0
		self.rate = 0
		self.slide_cooldown =0
		self.slide_period = 0
		self.dx, self.dy = 0, 0
		self.animation_timer = 0
		self.slide_vel= 0
		self.able_to_jump = False
		self.state_boolean = 'idle'
		self.is_facing_left = False
		self.player_state_images = {
		'idle':load_images('player/idle'), 
		'jump':load_images('player/jump'),
		'run':load_images('player/run'),
		'slide':load_images('player/slide'),
		'wall_slide':load_images('player/wall_slide'),
		}
		self.dash_v = 0
		self.activate_dash = False


	def set_action(self, action):
		if action != self.state_boolean:
			self.state_boolean = action

	def dash(self):
		if not self.activate_dash:
			if self.is_facing_left:
				self.dash_v = -6
			else:
				self.dash_v = 6


	def move(self, screen):
		dx = 0 
		dy = 0
		slide_cooldown_constant = 10
		slide_period_constant=50
		trying_to_move = False
		tryna_go_down = False
		tiles = self.game.Physics_tilesArr
		
		moveK = pygame.key.get_pressed()


		if moveK[pygame.K_a]:
			self.slide_cooldown+=1
			trying_to_move = True
			dx -=1

		elif moveK[pygame.K_d]:
			self.slide_cooldown+=1
			trying_to_move = True
			dx += 1
		else:
			self.slide_cooldown=0


		if moveK[pygame.K_s]:
			tryna_go_down=True


		if moveK[pygame.K_x]:
			self.dash()
			self.activate_dash = False


		if self.activate_dash==True:
			self.rect.x += self.dash_v
		self.dx = dx + self.slide_vel +(self.dash_v if self.activate_dash else 0)


		if moveK[pygame.K_SPACE] and self.able_to_jump == True:
			self.vel_y = -3
			self.set_action('jump')
			self.able_to_jump = False
		else:
			self.dy = 0
			


#responsible for the window scroll

		if self.rect.top <=250:
			if self.vel_y <0:
				self.dy = 1
			else:
				self.vel_y >=0
				self.dy =0

		if self.rect.bottom >= 155:
			if self.vel_y >0:
				self.dy =-1
			else:
				self.dy = 0



		self.vel_y += min(3, self.rate+0.1)

		dy += self.vel_y

#player collision to tiles
		for tile in self.game.tiles_with_collision:
			if tile.rect.colliderect(self.rect.x + dx +self.slide_vel, self.rect.y, self.size[0], self.size[1]):
				dx = 0
				self.dx = 0

			if tile.rect.colliderect(self.rect.x , self.rect.y + dy, self.size[0], self.size[1]):
		
				if self.vel_y < 0:#up
					dy = tile.rect.bottom - self.rect.top
					self.vel_y = 0

				elif self.vel_y >= 0:#down
					dy = self.rect.bottom - tile.rect.top
					self.vel_y = 0
					

					if self.vel_y == 0:
						self.able_to_jump=True
						



#responsible for plyer flip
		if dx<0:
			self.is_facing_left = True

		if dx>0:
			self.is_facing_left=False

		if dx ==0 and self.able_to_jump:
			self.set_action('idle')


#responsibel for the sliding 
		if tryna_go_down and self.able_to_jump:
			if trying_to_move and self.slide_cooldown>slide_cooldown_constant:
				if dx<0:
					self.slide_vel = -5
					

				if dx>0:
					self.slide_vel = 5
				self.slide_period += 1

				self.set_action('slide')
			else:
				self.set_action('idle')
				self.slide_vel=0

		else:
			self.set_action('idle')
			self.slide_vel=0


		if self.slide_period>slide_period_constant:
			self.slide_cooldown=0
			self.slide_period=0
			self.slide_vel=0
			self.set_action('idle')


		if self.able_to_jump == False:
			if trying_to_move and dx ==0:
				self.set_action('wall_slide')

				#allows an extra jump when sliding down a wall
				if moveK[pygame.K_SPACE]:
					self.vel_y = -3

			else:
				self.set_action('jump')


		if trying_to_move and self.able_to_jump:
			self.set_action('run')

		self.rect.y += dy+self.dy
		self.rect.x += dx

		self.game.enemyGroup.update(self.game.display, [self.dx, self.dy])
		self.game.tiles_with_collision.update([self.dx, self.dy])
		self.game.tiles_without_collision.update([self.dx, self.dy])


	def animation_runner(self, screen, boolean):
		count = 0
		animation_timer = 9
		count = len(self.player_state_images[self.state_boolean])
		self.animation_timer+=1
		if self.count < count:
			if self.animation_timer == animation_timer:
				self.count = (self.count + 1)%count
				if self.count == count:
					self.count = 0

				self.animation_timer = 0
		else:
			self.count =0 

		screen.blit(pygame.transform.flip(self.player_state_images[self.state_boolean][self.count],boolean ,False), (self.rect.x-2, self.rect.y-3))

	def draw(self,screen):
		self.animation_runner(screen, self.is_facing_left)

		#bullet group
class bullets(pygame.sprite.Sprite):
	def __init__(self,game ,x, y, px, py, angle, flip, offset = [0, 0]):
		pygame.sprite.Sprite.__init__(self)
		self.game= game
		self.offset = offset
		self.flip = flip
		self.x =x
		self.y = y
		self.image = load_image('projectile.png')
		self.size = self.image.get_size()
		self.angle = math.radians(angle+(-90 if self.flip else 90))
		self.speed = 4
		self.vel_y = math.cos(self.angle)*self.speed
		self.vel_x = math.sin(self.angle)*self.speed
		self.rect = pygame.Rect(x, y, self.size[0], self.size[1])


	def update(self):
		if self.flip:
			self.rect.x += int(self.vel_x) + self.offset[0]
			self.rect.y -= int(self.vel_y) + self.offset[1]
		else:
			self.rect.x += int(self.vel_x)+ self.offset[0]
			self.rect.y += int(self.vel_y) -self.offset[1]

		for bullet in self.game.bullet_group:
			get_hit = pygame.sprite.spritecollideany(bullet, self.game.tiles_with_collision)
			if get_hit:
				bullet.kill()

		for bullet in self.game.bullet_group:
			get_hit = pygame.sprite.spritecollideany(self.game.player, self.game.bullet_group)
			if get_hit:
				bullet.kill()


class Enemy(pygame.sprite.Sprite):
	def __init__(self, game, x, y, img, player_rect):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.playerRect = player_rect
		self.x_coodForm = x//16
		self.dx=0
		self.image = pygame.image.load(img)
		self.image.set_colorkey((0, 0, 0))
		self.size = self.image.get_size()
		self.rect = pygame.Rect(x, y,self.size[0], self.size[1])
		self.vel_y = 0
		self.count = 0
		self.flip = False
		self.idle = False
		self.enemy_state_images = {'idle':load_images('enemy/idle'), 'run':load_images('enemy/run')}
		self.animation_timer = 0
		self.seen = False
		self.end_point = []
		self.gun_vflip = False
		self.gun_hflip = False
		self.gun_img = pygame.transform.scale(load_image('gun.png'), (10, 6))
		self.gun = 0
		self.exclamation_mark = pygame.transform.scale(load_image('exclamationMark.png'), (7, 14))
		self.firing_timer = 0

		#for bullets
		self.bullet_offset = [0, 0]


	def vision_line(self, pos,flip):
		firing_timer_constant = 50
		start_point = [pos[0]+2, pos[1]+2]

		if flip == True:
			self.end_point = [pos[0]-50, pos[1]]
			
		else:
			self.end_point =[pos[0]+50, pos[1]]

		if self.playerRect.clipline(start_point, self.end_point):
			self.seen = True

		if self.seen:
			self.end_point = [self.playerRect.centerx, self.playerRect.centery]
			self.game.display.blit(self.exclamation_mark, (self.rect.centerx, self.rect.centery-20))
			


		for tile in self.game.tiles_with_collision:
			if tile.rect.clipline(start_point, self.end_point):
				self.seen = False

		x =self.rect.centerx
		y =self.rect.centery


		rotation_degree = math.degrees(math.atan2(-(self.end_point[1]-y), (self.end_point[0]-x)))
		sub_degree = math.degrees(math.atan2(-(self.end_point[1]-y), (self.end_point[0]-x)))
		radian_for_cood = math.radians(sub_degree+(360 if rotation_degree<=0 else 0)+90)
		r = 10
			

		if self.flip:
			self.gun_vflip=True
			rotation_degree = math.degrees(math.atan2(-(self.end_point[1]-y), -(self.end_point[0]-x)))
		else:
			self.gun_vflip=False

		if self.seen:
			self.firing_timer+=1
			if self.firing_timer >= firing_timer_constant:
				bullet = bullets(self.game,r*math.sin(radian_for_cood)+self.rect.centerx, r*math.cos(radian_for_cood)+self.rect.centery, self.end_point[0], self.end_point[1], rotation_degree, self.flip, self.bullet_offset)
				self.game.bullet_group.add(bullet)
				self.firing_timer =0
		else:
			self.firing_timer=0

		self.gun = pygame.transform.flip(pygame.transform.rotate(self.gun_img,(rotation_degree)), self.gun_vflip, self.gun_hflip)

		self.game.display.blit(self.gun, (r*math.sin(radian_for_cood)+self.rect.centerx, r*math.cos(radian_for_cood)+self.rect.centery))

	def solid_check(self, pos):
		check_loc = pygame.Rect(pos[0], pos[1], self.size[0], self.size[1])
		for tile in self.game.tiles_with_collision:
			if tile.rect.colliderect(check_loc):
				return tile

	def animation_runner(self, state):
		count = 0
		animation_timer = 10

		count = len(self.enemy_state_images[state])
		self.animation_timer+=1
		if self.count < count:
			if self.animation_timer == animation_timer:
				self.count = (self.count + 1)%count
				self.animation_timer = 0
		else:
			self.count =0 

	def img_flipper(self,boolean,screen, img):
		self.image = pygame.transform.flip(img,boolean ,False)

	def update(self, screen,scroll = [0, 0]):
		dx = 0
		self.vel_y+=1 #gravity
		dy = self.vel_y

		check_x = self.rect.left - 5 if self.flip else self.rect.right + 5
		ground_check_pos = [check_x, self.rect.bottom + 2]

		if self.seen:
			self.idle = True
			if self.playerRect.x < self.rect.x:
				self.flip = True
			elif self.playerRect.x > self.rect.x:
				self.flip= False
		elif random.randint(1, 150) == 1:
			self.idle = not self.idle

		if self.idle == False:
			if self.solid_check(ground_check_pos):
				dx = (-1 if self.flip else 1.5)
			else:
				self.flip = not self.flip

		self.rect.y+= dy
		self.rect.x += dx
		old_y = self.rect.y
		for tile in self.game.tiles_with_collision:
			if self.rect.colliderect(tile.rect):
				if dy > 0:
					self.rect.bottom = tile.rect.top
					self.vel_y = 0
				elif dy < 0:
					self.rect.top = tile.rect.bottom
					self.vel_y = 0

			
			if self.rect.colliderect(tile.rect):
				if dx > 0:
					self.rect.right = tile.rect.left
				elif dx <0:
					self.rect.left = tile.rect.right
				self.flip = not self.flip
				self.vel_y=0


		self.vision_line([self.rect.centerx, self.rect.centery], self.flip)
		if self.idle:
			self.animation_runner('idle')
			self.img_flipper(self.flip, screen, self.enemy_state_images['idle'][self.count])
		else:
			self.animation_runner('run')
			self.img_flipper(self.flip, screen, self.enemy_state_images['run'][self.count])
		
		self.bullet_offset = [scroll[0],scroll[1]]
		
		self.rect.x -= scroll[0]
		
		self.rect.y += dy+scroll[1]

