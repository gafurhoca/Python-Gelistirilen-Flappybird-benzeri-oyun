import pygame

zemin_kaydirma = 0
boru_bosluk = 200
kaydirma_hizi = 3

class Pipe(pygame.sprite.Sprite):
	def __init__(self, x, y, position):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(r"C:\Users\MONSTER\Desktop\img\kolon2.png")
		self.rect = self.image.get_rect()

		if position == 1:
			self.image = pygame.transform.flip(self.image, False, True)
			self.rect.bottomleft = [x, y - int(boru_bosluk / 2)]
		if position == -1:
			self.rect.topleft = [x, y + int(boru_bosluk / 2)]

	def update(self):
		self.rect.x -= kaydirma_hizi
		if self.rect.right < 0:
			self.kill()