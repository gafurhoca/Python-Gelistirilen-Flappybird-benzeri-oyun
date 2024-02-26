import pygame
import menu
flying = False
game_over = False
class Bird(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		self.index = 0 #başlangıç görseli
		self.counter = 0 #animasyon kontrolü
		for num in range(1, 4):
			img = pygame.image.load(f'img1/bird{num}.png')
			self.images.append(img)
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y] #başlangıç pozisyonu
		self.vel = 0 #yerçekimi
		self.clicked = False  #fareye tıklama durumu

	def update(self):

		if flying == True:
			#gravity
			self.vel += 0.5
			if self.vel > 8:
				self.vel = 8
			if self.rect.bottom < 750:
				self.rect.y += int(self.vel)

		if game_over == False:
			#zıpla

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:




				self.clicked = True
				self.vel = -10

			if pygame.mouse.get_pressed()[0] == 0:

				self.clicked = False #sprite a basılmadığı

			#animasyonu yönet
			self.counter += 1 #animasyon için sayaç artırır
			animasyon_hizi = 7

			if self.counter > animasyon_hizi:
				self.counter = 0
				self.index += 1
				if self.index >= len(self.images):
					self.index = 0
			self.image = self.images[self.index]

			#kuşu döndür
			self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
		else:
			self.image = pygame.transform.rotate(self.images[self.index], -90)