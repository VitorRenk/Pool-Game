import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

TELA_WIDTH = 1200
TELA_HEIGHT = 678
VISOR_PONTUACAO = 50
bola_branca_cacapada = False

tela = pygame.display.set_mode((TELA_WIDTH,TELA_HEIGHT + VISOR_PONTUACAO))
pygame.display.set_caption("JOGO DE SINUCA EM PYGAME")


spaco = pymunk.Space()
statica_body = spaco.static_body
desenha_options = pymunk.pygame_util.DrawOptions(tela)

clock = pygame.time.Clock()
FPS = 120

diametro = 35
forca = 0
forca_maxima = 11000
forca_direcao = 1
forca_taco = False
tacando_taco = True
VIDAS = 3
cacapas_diametro = 66
cacapada_bolas = []

JOGO_RODANDO = True


BLACK = (0, 0, 0)
BG = (0,128,0)
AMARELO = (255, 255, 0)

FONTE = pygame.font.SysFont("arial.ttf", 30)

FONTE_LARGA = pygame.font.SysFont("arial.ttf", 60)

c_taco_image = pygame.image.load("assets/images/taco.png").convert_alpha()
table_img = pygame.image.load("assets/images/mesa.png").convert_alpha()

bolas_images = []
for i in range(1, 17):
    bolas_image = pygame.image.load(f"assets/images/bola_{i}.png").convert_alpha()
    bolas_images.append(bolas_image)

def Desenhar_texto(text, font, text_cor, x, y):
    img = font.render(text, True, text_cor)
    tela.blit(img,(x,y))

def create_ball(radius,pos):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Circle(body,radius)
    shape.mass = 5
    shape.elasticity = 0.9
    pivor = pymunk.PivotJoint(statica_body, body,(0, 0), (0, 0))
    pivor.max_bias = 0
    pivor.max_force = 1000

    spaco.add(body, shape, pivor)
    return shape

bolas = []
rows = 5


for col in range(5):
    for row in range(rows):
        pos = ( 250 + (col * (diametro + 1)), 267 + (row * (diametro + 1)) + (col * diametro / 2))
        nova_bola = create_ball(diametro / 2, pos)
        bolas.append(nova_bola)
    rows -= 1

pos = (888, TELA_HEIGHT / 2)
fila_c_bola = create_ball(diametro / 2, pos)
bolas.append(fila_c_bola)



colisao = [
    [(88, 56), (109, 77), (555, 77), (564, 56)],
    [(621, 56), (630, 77), (1081, 77), (1102, 56)],
    [(88, 621), (110, 600), (556, 600), (564, 621)],
    [(622, 621), (630, 600), (1081, 600), (1102, 621)],
    [(56, 96), (77, 117), (77, 560), (56, 581)],
    [(1143, 96), (1122, 117), (1122, 560), (1143, 581)]
]

cacapas =[
    (55, 63),
    (592, 48),
    (1134, 64),
    (55, 616),
    (592, 629),
    (1134, 616),
]

def create_colisao(poly_dims):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = ((0,0))
    shape = pymunk.Poly(body, poly_dims)

    shape.elasticity = 0.9
    spaco.add(body, shape)

for c in colisao:
    create_colisao(c)

class Ctaco():
    def __init__(self, pos):
        self.original_image = c_taco_image
        self.angulo = 0
        self.image = pygame.transform.rotate(self.original_image, self.angulo)
        self.image = c_taco_image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def Atualizar_angulo(self, angulo):
        self.angulo = angulo

    def TacoDesenhar(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angulo)
        surface.blit(self.image, (self.rect.centerx - self.image.get_width() / 2, self.rect.centery - self.image.get_height() / 2))


ctaco = Ctaco(bolas[-1].body.position)

barra_forca = pygame.Surface((10, 20))
barra_forca.fill(BLACK)

run = True
while run:

    clock.tick(FPS)
    spaco.step(1/FPS)
    tela.fill(BG)

    tela.blit(table_img, (0, 0))

    for i, bola in enumerate(bolas):
        for cacapa in cacapas:
            bola_x_distancia = abs(bola.body.position[0] - cacapa[0])
            bola_y_distancia = abs(bola.body.position[1] - cacapa[1])
            bola_dist = math.sqrt((bola_x_distancia ** 2) + (bola_y_distancia ** 2))

            if bola_dist <= cacapas_diametro / 2:
                if i == len(bolas) - 1:
                    VIDAS -= 1
                    bola_branca_cacapada = True
                    bola.body.position = (-100, -100)
                    bola.body.velocity = (0.0, 0.0)
                else:
                    spaco.remove(bola.body)
                    bolas.remove(bola)
                    cacapada_bolas.append(bolas_images[i])
                    bolas_images.pop(i)

    for i, bola in enumerate(bolas):
        tela.blit(bolas_images[i], (bola.body.position[0] - bola.radius, bola.body.position[1] - bola.radius))

    tacando_taco = True
    for bola in bolas:
        if int(bola.body.velocity[0]) != 0 or int(bola.body.velocity[1]) != 0:
            tacando_taco = False


    if tacando_taco == True  and JOGO_RODANDO == True:
        if bola_branca_cacapada == True:
            bolas[-1].body.position = (888, TELA_HEIGHT / 2)
            bola_branca_cacapada = False

        mouse_posicao = pygame.mouse.get_pos()
        ctaco.rect.center = bolas[-1].body.position
        x_distancia = bolas[-1].body.position[0] - mouse_posicao[0]
        y_distancia = -(bolas[-1].body.position[1] - mouse_posicao[1])
        taco_angulo = math.degrees(math.atan2(y_distancia, x_distancia))
        
        ctaco.Atualizar_angulo(taco_angulo)

        ctaco.TacoDesenhar(tela)

        if forca_taco == True and JOGO_RODANDO == True:
            forca += 150 * forca_direcao
            if forca >= forca_maxima or forca <= 0:
                forca_direcao *= -1
            for b_barra in range(math.ceil(forca / 2000)):
                tela.blit(barra_forca, (bolas[-1].body.position[0] + (b_barra * 15), bolas[-1].body.position[1] + 30))

        elif forca_taco == False and tacando_taco == True:
        
            x_pulso = math.cos(math.radians(taco_angulo))
            y_pulso = math.sin(math.radians(taco_angulo))
            bolas[-1].body.apply_impulse_at_local_point((forca * -x_pulso, forca * y_pulso), (0, 0))

            forca = 0
            forca_direcao = 1

    Desenhar_texto("VIDAS : " + str(VIDAS), FONTE, AMARELO, TELA_WIDTH - 150, TELA_HEIGHT + 10)

    for i, bola in enumerate(cacapada_bolas):
        tela.blit(bola, (10 + (i * 50), TELA_HEIGHT + 10))

    if VIDAS <= 0:
        Desenhar_texto("GAME OVER", FONTE_LARGA, AMARELO, TELA_WIDTH / 2 - 140, TELA_HEIGHT / 2 - 100)
        JOGO_RODANDO = False

    if len(bolas) == 1:
        Desenhar_texto("VOCE FOI O GANHADOR", FONTE_LARGA, AMARELO, TELA_WIDTH / 2 - 240, TELA_HEIGHT / 2 - 100)
        JOGO_RODANDO = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and tacando_taco == True:
            forca_taco = True
        if event.type == pygame.MOUSEBUTTONUP and tacando_taco == True:
            forca_taco = False
        
            
        if event.type == pygame.QUIT:
            run = False

    #spaco.debug_draw(desenha_options)
    pygame.display.update()


pygame.quit()