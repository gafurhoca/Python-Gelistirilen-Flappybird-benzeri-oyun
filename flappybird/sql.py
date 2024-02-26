import pygame

# Ekran boyutları
WIDTH = 800
HEIGHT = 600

# Renkler
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Oyunun başlatılması
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Arka plan fotoğrafları
background1 = pygame.image.load(r"C:\Users\MONSTER\Desktop\cizim1.1.png")
background2 = pygame.image.load(r"C:\Users\MONSTER\Desktop\img\arkapllan2.png")

# Aktif arka plan fotoğrafı
current_background = background1

# Harita butonu
button_img = pygame.image.load(r"C:\Users\MONSTER\Desktop\img\harita.png")
button_rect = button_img.get_rect()
button_rect.center = (WIDTH // 2, HEIGHT // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button_rect.collidepoint(mouse_pos):
                # Butona tıklandığında fotoğrafı değiştir
                if current_background == background1:
                    current_background = background2
                else:
                    current_background = background1

    # Arka planı temizle
    screen.fill(BLACK)

    # Arka plan fotoğrafını çiz
    screen.blit(current_background, (0, 0))

    # Harita butonunu çiz
    screen.blit(button_img, button_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

