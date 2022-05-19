from multiprocessing.dummy import current_process
import pygame
from sprite import *


pygame.init()



SCREEN_WIDTH = 8*64
SCREEN_HEIGHT = 8*64

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
TILESIZE = 64

FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Tracking System")

sheet = SpriteSheet('./images/sprites.png')

sprites = pygame.sprite.Group()

board = [
	[-5,-4,-3,-2,-1,-3,-4,-5],
	[-6,-6,-6,-6,-6,-6,-6,-6],
	[ 0, 0, 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0, 0, 0],
	[ 0, 0, 0, 0, 0, 0, 0, 0],
	[ 6, 6, 6, 6, 6, 6, 6, 6],
	[ 5, 4, 3, 2, 1, 3, 4, 5]
]


			

def draw_board(screen):
	for i in range(8):
		for j in range(8):
			color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
			pygame.draw.rect(screen, color, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))


# rectangle = Sprite(sheet.get_image(0, 0, 200, 200))
# sprites.add(rectangle)

pieces = []

def load_position():
	k = 0
	for i in range(8):
		for j in range(8):
			n = board[j][i]
			if n == 0: continue

			src_x = abs(n) - 1
			src_y = 0 if n > 0 else 1

			pieces.append(Sprite(sheet.get_image(src_x * 200, src_y * 200, 200, 200)))
			pieces[k].rect.x = i * TILESIZE
			pieces[k].rect.y = j * TILESIZE
			sprites.add(pieces[k])

			k += 1


draging = False

clock = pygame.time.Clock()


load_position()

running = True

cp = 0 # current piece moving
while running:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				for i in range(32):
					if pieces[i].rect.collidepoint(event.pos):
						cp = i
						draging = True
						mouse_x = event.pos[0]
						mouse_y = event.pos[1]
						offset_x = pieces[i].rect.x - mouse_x
						offset_y = pieces[i].rect.y - mouse_y

		elif event.type == pygame.MOUSEBUTTONUP:
			if event.button == 1:            
				draging = False
				
				# centered x and y positions
				i = mouse_x // TILESIZE
				j = mouse_y // TILESIZE

				pieces[cp].rect.x = i * TILESIZE
				pieces[cp].rect.y = j * TILESIZE
				

		elif event.type == pygame.MOUSEMOTION:
			if draging:
				mouse_x, mouse_y = event.pos
				pieces[cp].rect.x = mouse_x + offset_x
				pieces[cp].rect.y = mouse_y + offset_y

	screen.fill(WHITE)

	draw_board(screen)
	sprites.draw(screen)

	pygame.display.flip()


	clock.tick(FPS)


pygame.quit()