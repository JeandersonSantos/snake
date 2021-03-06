import pygame
from pygame.locals import *

TAMANHO_TELA = 640, 480
TAMANHO = 64
COR_NAVE = (0, 128, 255)

def init():
    global TELA
    TELA = pygame.display.set_mode(TAMANHO_TELA)

class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, cor, tx=TAMANHO, ty=TAMANHO, imagem=None):
        super(Nave, self).__init__()
        self.x = x
        self.y = y
        self.ox = x
        self.oy = y
        self.cor = cor
        self.tx = tx; self.ty = ty
        self.velocidade = 10
        
        self.imagem = imagem
        self.carregar()
     
    def carregar(self):
        if self.imagem is None:
            return
        self.imagem = pygame.image.load("imagens/" + self.imagem)
     
    def apaga(self):
        pygame.draw.rect(TELA, (0,0,0), (self.ox, self.oy, self.tx, self.ty) )
        
    def kill(self):
        self.apaga()
        super(Nave, self).kill()
        
    def desenha(self):
        self.rect = pygame.Rect ( (self.x, self.y, self.tx, self.ty) )
        self.apaga()
        if not self.imagem:
            pygame.draw.rect(TELA, self.cor, self.rect)
        else:
            TELA.blit(self.imagem, self.rect)
        self.ox = self.x
        self.oy = self.y
        
class Tiro(Nave):
    def atualiza(self, inimigos):
        self.y -= self.velocidade
        self.desenha()
        if self.y < 0:
            self.kill()
        for inimigo in inimigos:
            if self.rect.colliderect(inimigo.rect):
                inimigo.kill()
    
class Inimigo(Nave):
    def __init__(self, x, y, imagem=None):
        cor = (255, 0,0)
        super(Inimigo, self).__init__(x, y, cor, TAMANHO, TAMANHO, imagem)
        self.velocidade = 5

        
    def atualiza(self):
        self.x += self.velocidade
        if self.x > TAMANHO_TELA[0]:
            self.x = 0
            self.y += TAMANHO + 10
            if self.y >= TAMANHO_TELA[1]:
                print("Voce morreu")
                raise Exception("Voce morreu")
        self.desenha()
    

MAX_TIROS = 10
MAX_INIMIGOS = 10
def principal():
    inimigo = Inimigo(0, 0)
    x = TAMANHO_TELA[0] // 2
    y = TAMANHO_TELA[1] - TAMANHO
    nave = Nave(x, y, COR_NAVE, imagem="nave.png")
    velocidade = 10
    tiros = pygame.sprite.Group()
    velocidade_inimigo = 5
    inimigos = pygame.sprite.Group()
    inimigos.add(inimigo)
    contador = 0 
    while True:
        if contador > 30 and len(inimigos) < MAX_INIMIGOS:
            inimigos.add(Inimigo(0, 0))
            contador = 0
        contador += 1
        pygame.event.pump()
        teclas = pygame.key.get_pressed()
        if teclas[K_LEFT]:
            nave.x -= velocidade
        elif teclas[K_RIGHT]:
            nave.x += velocidade
        if teclas[K_ESCAPE]:
            break
        if teclas[K_SPACE] and len(tiros) <= MAX_TIROS:
            tiro = Tiro(nave.x + TAMANHO//2, TAMANHO_TELA[1] - TAMANHO,
                        (255, 255,255), 12, 23)
            tiros.add(tiro)

        nave.desenha()

        for inimigo in inimigos:
            inimigo.atualiza()

        for tiro in tiros:
            tiro.atualiza(inimigos)            
        
        pygame.display.flip()
        pygame.time.delay(30)

try:
    init()
    principal()
finally:
    pygame.quit()
    
