import sys

import pygame
from pygame.locals import *
import random
import menu
import Pipe
import Bird
import pymysql
from tkinter import *

pygame.mixer.init()
pygame.init()
clock = pygame.time.Clock()
fps = 60

genislik = 600
uzunluk = 500

ekran_boyut = pygame.display.set_mode((genislik, uzunluk))
pygame.display.set_caption('Flappy Bird')


#yazı tipini tanımla
font = pygame.font.SysFont('Bauhaus 93', 60)

#oyun değişkenlerini tanımla
white = (255, 255, 255)



borular_mesafe = 1000 #millisaniye

score = 0
boru_say = False



#resimleri yükle
arkaplan = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\cizim1.1.png")
arkaplan2 = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\arkapllan2.png")
taban = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\taban.png")
button_img = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\start1.png")
start_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\baslat.png")
options_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\start1.png")
exit_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\kapat.png")
gameover_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\gameover2.png")
harita_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\harita.png")
skor_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\skor.png")
siralama_button = pygame.image.load(r"C:\Users\MONSTER\PycharmProjects\flappybird\img\SIRALAMA.png")
current_background = arkaplan
son_boru = pygame.time.get_ticks() - borular_mesafe




def draw_text(text, font, text_col, x, y):
	img = font.render(text, True, text_col)
	ekran_boyut.blit(img, (x, y))


def reset_game():
	boru_group.empty()
	flappy.rect.x = 100
	flappy.rect.y = int(uzunluk / 3)
	score = 0
	return score


def save_score(score):
	try:
		# Veritabanına bağlan
		connection = pymysql.connect(host='localhost',
									 user='root',
									 password='Tedarik25',
									 db='deneme',
									 charset='utf8mb4')



				# Yeni skor verisini kaydet
		with connection.cursor() as cursor:
			sql = "INSERT INTO skortablosu1 (score) VALUES (%s)"
			cursor.execute(sql, (score,))
			connection.commit()


				# Bağlantıyı kapat
		connection.close()
		print("Skor başarıyla kaydedildi!")
	except pymysql.Error as e:
		print("Skor kaydedilirken bir hata oluştu:", str(e))




host = 'localhost'
user = 'root'
password = 'Tedarik25'
database = 'deneme'


def button_clicked():
    # Veritabanına bağlan
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    # Tablodan en büyük ilk 5 skoru sorgula
    query = "SELECT score FROM skortablosu1 ORDER BY score DESC LIMIT 20"
    cursor.execute(query)
    result = cursor.fetchall()

    # Skorları bir liste içinde sakla
    scores = sorted([row[0] for row in result], reverse=True)



    # Sonuçları projede göster
    # Örneğin, bir label üzerine yazdırabilirsiniz
    result_label.configure(text="\n".join(map(str, scores)))

    # Bağlantıyı kapat
    cursor.close()
    conn.close()




bird_group = pygame.sprite.Group()
boru_group = pygame.sprite.Group()

flappy = Bird.Bird(100, int(uzunluk / 2))

bird_group.add(flappy)

# yeniden başlatma düğmesi örneği oluştur
tekrarla_button = menu.Button(235, 200, button_img, 1.0)
start_button = menu.Button(235 , 200 , start_button, 1.0)
exit_button = menu.Button(235 ,350 , exit_button,1.0)
gameover_button = menu.Button(110 , 100, gameover_button, 2.0)

siralama_button = menu.Button(320,250, siralama_button ,1.0)
skor_button = menu.Button(150,250, skor_button ,1.0)
button_rect = harita_button.get_rect()
button_rect.center = (295, 320)





bird_sound= pygame.mixer.Sound(r"C:\Users\MONSTER\PycharmProjects\flappybird\img1\kanat.aiff")
game_over_sound= pygame.mixer.Sound(r"C:\Users\MONSTER\PycharmProjects\flappybird\img1\gameover2.wav")
game_over_sound.set_volume(0.1)


run = True
while run:


	clock.tick(fps)

	#arka plan çiz
	ekran_boyut.blit(current_background, (0, 0))
	bird_group.draw(ekran_boyut)
	bird_group.update()
	boru_group.draw(ekran_boyut)

	#zemini çiz
	ekran_boyut.blit(taban, (Pipe.zemin_kaydirma, 400))

	#skoru kontrol et
	if len(boru_group) > 0:
		if bird_group.sprites()[0].rect.left > boru_group.sprites()[0].rect.left\
			and bird_group.sprites()[0].rect.right < boru_group.sprites()[0].rect.right\
			and boru_say == False:
			boru_say = True
		if boru_say == True:
			if bird_group.sprites()[0].rect.left > boru_group.sprites()[0].rect.right:
				score += 1
				bird_sound.play()
				 # Skoru kaydet
				boru_say = False
				#save_score(score)



	draw_text(str(score), font, white, 270, 20)

	#çarpışma ara
	if pygame.sprite.groupcollide(bird_group, boru_group, False, False) or flappy.rect.top < 0:
		Bird.game_over = True
		game_over_sound.play()


	#kuşun yere çarpıp çarpmadığını kontrol et
	if flappy.rect.bottom >= 400:
		game_over_sound.play()
		Bird.game_over = True
		Bird.flying = False


	if Bird.game_over == False and Bird.flying == True:


		#yeni borular oluştur
		time_now = pygame.time.get_ticks()
		if time_now - son_boru > borular_mesafe:
			boru_genislik = random.randint(-50, 50)
			alt_boru = Pipe.Pipe(genislik, int(uzunluk / 2) + boru_genislik, -1)
			ust_boru = Pipe.Pipe(genislik, int(uzunluk / 2) + boru_genislik, 1)
			boru_group.add(alt_boru)
			boru_group.add(ust_boru)
			son_boru = time_now


		#zemini çiz ve kaydır
		Pipe.zemin_kaydirma -= Pipe.kaydirma_hizi
		if abs(Pipe.zemin_kaydirma) > 35:
			Pipe.zemin_kaydirma = 0

		boru_group.update()

	if Bird.flying == False:
		if start_button.draw(ekran_boyut) == True:
			Bird.game_over = False


	if Bird.game_over == True:
		if exit_button.draw(ekran_boyut) == True:
			pygame.quit()
			sys.exit()
	if Bird.game_over == True:
		if skor_button.draw(ekran_boyut) == True:
			save_score(score)
	if Bird.game_over == True:
		ekran_boyut.blit(harita_button, button_rect)

	if Bird.game_over == True:
		if harita_button == True:
			ekran_boyut.blit(harita_button, button_rect)
			ekran_boyut.blit(current_background, (0, 0))

	if Bird.game_over == True:
		if siralama_button.draw(ekran_boyut) == True:
			# Pencere oluştur
			window = Tk()

			# Butonu oluştur
			button = Button(window, text="Skorları Göster", command=button_clicked)
			button.pack()

			# Sonuçların gösterileceği bir label oluştur
			result_label = Label(window, text="")
			result_label.pack()

			# Pencereyi çalıştır
			window.mainloop()

	if Bird.game_over == True:
		if gameover_button.draw(ekran_boyut) == True:
			QUIT


	if Bird.game_over == True:
		if tekrarla_button.draw(ekran_boyut) == True:

			Bird.game_over = False
			score = reset_game()
			pygame.mixer.stop()


	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			run = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_pos = pygame.mouse.get_pos()
			if button_rect.collidepoint(mouse_pos):
				# Butona tıklandığında fotoğrafı değiştir
				if current_background == arkaplan:
					current_background = arkaplan2
				else:
					current_background = arkaplan







		if event.type == pygame.MOUSEBUTTONDOWN   and Bird.flying == False and Bird.game_over == False:



			Bird.flying = True


	pygame.display.update()

pygame.quit()