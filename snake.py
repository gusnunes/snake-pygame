import time
import pygame
from random import randint

def key_pressed(key):   # define a direcao da cobrinha
    head_direction = snake[0][1]   # controlada pela cabeca
    if key[pygame.K_DOWN] and head_direction != "up":
        snake[0][1] = "down"
    
    elif key[pygame.K_UP] and head_direction != "down":
        snake[0][1] = "up"
    
    elif key[pygame.K_LEFT] and head_direction != "right":
        snake[0][1] = "left"

    elif key[pygame.K_RIGHT] and head_direction != "left":
        snake[0][1] = "right"

def snake_movement():
    for part in snake:
        x, y      = part[0]
        direction = part[1]
        
        if direction == "down":
            y += SNAKE_SIZE
            part[0] = (x,y)
        
        elif direction == "up":
            y -= SNAKE_SIZE
            part[0] = (x,y)
        
        elif direction == "left":
            x -= SNAKE_SIZE
            part[0] = (x,y)
        
        elif direction == "right":
            x += SNAKE_SIZE
            part[0] = (x,y)
        
        pygame.draw.rect(screen, BLUE, [x, y, SNAKE_SIZE, SNAKE_SIZE])

def update_movement():  # a cauda segue a posicao da frente
    for i in range(len(snake)-1, 0, -1):
        snake[i][1] = snake[i-1][1]

def edge_colide():
    x, y = snake[0][0]
    if x == WIDTH or x == -(SNAKE_SIZE):   # borda direita e esquerda
        return True
    
    if y == HEIGH or y == -(SNAKE_SIZE):   # borda abaixo e acima
        return True

def self_colide():
    hx, hy = snake[0][0]   # hx, hy = coordenada x,y da head
    for i in range(1, len(snake)):
        sx, sy = snake[i][0]   # sx, sy = coordenada x,y da snake naquela posicao
        if hx == sx and hy == sy:
            return True            
  
def ate_fruit(): # conferir se colidiu com a fruta
    hx, hy = snake[0][0]
    fx, fy = fruit

    if hx == fx and hy == fy:
        x, y      = snake[-1][0]   # ultima posicao
        direction = snake[-1][1]   # ultima direcao
        
        if direction == "up":
            y += SNAKE_SIZE
        
        elif direction == "down":
            y -= SNAKE_SIZE
        
        elif direction == "right":
            x -= SNAKE_SIZE
        
        elif direction == "left":
            x += SNAKE_SIZE

        snake.append( [(x,y), direction] )   # aumenta a cauda(ocupa a posicao que era da ultima)
        return True

def draw_fruit():
    x, y = fruit

    if ate_fruit():
        colide = True
        while colide:   # a posicao da nova fruta nao pode coincidir com a cobrinha
            
            x = randint(0,31)*SNAKE_SIZE   # (width/snake_size) quadradinho na mesma proporcao do background
            y = randint(0,23)*SNAKE_SIZE   # gerar para heigh (heigh/snake_size)

            for part in snake:
                px, py = part[0]
                if x == px and y == py:
                    break
            else:
                colide = False

    pygame.draw.rect(screen, GREEN, [x, y, SNAKE_SIZE, SNAKE_SIZE])
    return x, y

def draw_lines():   # linhas do background
    for x in range(0, WIDTH, SNAKE_SIZE):   # verticais
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGH))
        
    for y in range(0, HEIGH, SNAKE_SIZE):   # horizontais
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def game_over(string):   # mostrar na tela mensagens de fim de jogo
    over_txt  = string
    score_txt = "Score : " + str(len(snake)-1)
    pygame.font.init()
    fonte        = pygame.font.get_default_font()
    fontesys     = pygame.font.SysFont(fonte, 60)
    txt_screen   = fontesys.render(over_txt, True, WHITE)
    score_screen =  fontesys.render(score_txt, True, WHITE)
    
    screen.fill(BLACK)
    screen.blit(txt_screen,(40,140))
    screen.blit(score_screen,(40,240))
    pygame.display.update()
    time.sleep(2)

# definindo cores
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)
GRAY  = (40,40,40)
WHITE = (255,255,255)

# definindo tamanho da tela
WIDTH = 640
HEIGH = 480

# tamanho do quadradinho que representa a cobrinha
SNAKE_SIZE = 20

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGH))
pygame.display.set_caption("Snake Game")

# cobrinha é uma lista
head  = [(60,240),""]   # cada parte da cobrinha é outra lista: [coord (x,y), direcao]
snake = [head]   

fruit = (320,240)   # posicao da primeira frutinha

clock = pygame.time.Clock()   # controlar os frames

while True:
        clock.tick(8)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                key_pressed(pygame.key.get_pressed())
        
        snake_movement()
        update_movement()
        
        fruit = draw_fruit()
        draw_lines()
        
        if edge_colide():   # cabeca colidiu com as bordas
            game_over("VOCÊ PERDEU!!!!")
            break
        
        if self_colide():   # cabeca colidiu com alguma parte da cauda
            game_over("VOCÊ PERDEU!!!!")
            break
        
        if len(snake) == WIDTH*HEIGH:   # jogador completou todas as posicoes
            game_over("VOCÊ GANHOU!!!!")
            break

        pygame.display.update()
        screen.fill(BLACK)