import pygame
from sprite import *
from pygame import mixer

pygame.init()



SCREEN_WIDTH = 8*64
SCREEN_HEIGHT = 8*64

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
TILESIZE = 64

FPS = 120

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Chess")

# spritesheet with the chess stuff
sheet = SpriteSheet('./images/sprites.png')

sprites = pygame.sprite.Group()

# the board array
# negative numbers just mean that they will be black
# and positive, they will be white
# check load_position() for details
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


			
# a function for drawining the board to the screen
def draw_board(screen):
	for i in range(8):
		for j in range(8):
			# just a little math i figured out...
			# ...if i + j is odd, render lighter, else render darker
			color = (240, 217, 181) if (i + j) % 2 == 0 else (181, 136, 99)
			pygame.draw.rect(screen, color, (i * TILESIZE, j * TILESIZE, TILESIZE, TILESIZE))

# an array with all pieces sprites
pieces = []

def load_position():
	k = 0
	for i in range(8):
		for j in range(8):
			n = board[j][i]
			if n == 0: continue # skip if there is no piece on current board position

			# figuring out the piece position in the sprites.png image
			src_x = abs(n) - 1
			src_y = 0 if n > 0 else 1 # if negative number pick the blacks
			
			# appending a new sprite and setting its position
			pieces.append(Sprite(sheet.get_image(src_x * 200, src_y * 200, 200, 200)))
			pieces[k].rect.x = i * TILESIZE
			pieces[k].rect.y = j * TILESIZE
			sprites.add(pieces[k])

			k += 1

def move_to(current_piece, x, y):
	# positions that the piece will move next
	new_posx = x * TILESIZE
	new_posy = y * TILESIZE

	# loop through all pieces to check we are over one
	for p in pieces:
		px = p.rect.x
		py = p.rect.y

		# checks if the new position already has a piece
		if new_posx == px and new_posy == py:
			p.rect.x = -1000 # moves it to casa do caralho

	# updates the position of the current piece
	pieces[current_piece].rect.x = new_posx
	pieces[current_piece].rect.y = new_posy


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

				move_to(cp, i, j)
				move_sound = mixer.Sound('sound/move.ogg')
				move_sound.play()
				

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