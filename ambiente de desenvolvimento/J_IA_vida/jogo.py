# Jogo em python
# UFMT

# ------------------------------------------------------
# |       BIBLIOTECAS                                  |
# ------------------------------------------------------

import pygame
import pygame.display
import random
from pygame.locals import *

# ------------------------------------------------------
# |       FUNÇÕES E CLASSES                            |
# ------------------------------------------------------

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        jogador_imagem = ('Jogador.png')
        self.image = pygame.image.load(jogador_imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image, (190,60))
        self.rect = self.image.get_rect()
        self.vidas = 3  # Sistema de vidas adicionado aqui

    def update(self, pressed_keys):
        if (tecla_pressionada[K_UP]) or (tecla_pressionada[K_w]):
            self.rect.move_ip(0,-5)
        if (tecla_pressionada[K_DOWN]) or (tecla_pressionada[K_s]):
            self.rect.move_ip(0,5) 
        if (tecla_pressionada[K_LEFT]) or (tecla_pressionada[K_a]):
            self.rect.move_ip(-5,0)
        if (tecla_pressionada[K_RIGHT]) or (tecla_pressionada[K_d]):
            self.rect.move_ip(5,0)

        # Sistema de limites da tela
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > tela_altura:
            self.rect.bottom = tela_altura
        if self.rect.left < 0:
            self.rect.left = 0 
        if self.rect.right > tela_largura:
            self.rect.right = tela_largura

class Enemy(pygame.sprite.Sprite):
    ponto = 0

    def __init__(self):
        super(Enemy, self).__init__()
        inimigo_imagem = ('Inimigo.png')
        self.image = pygame.image.load(inimigo_imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect(center=(tela_largura, random.randint(0,tela_altura)))
        self.velocidade = random.uniform(1, 20)

    def update(self):
        self.rect.move_ip(-self.velocidade,0)
        if self.rect.right < 0:
            self.kill()
            if not eliminado:
                print("Não ta eliminado")
                if self.velocidade < 10:
                    Enemy.ponto = Enemy.ponto + 1
                else:
                    Enemy.ponto = Enemy.ponto + 5

class Vida(pygame.sprite.Sprite):
    def __init__(self):
        super(Vida, self).__init__()  # Corrigido: .__init__()
        vida_imagem = 'Vida.png'
        self.image = pygame.image.load(vida_imagem).convert_alpha()
        self.image = pygame.transform.scale(self.image, (90, 90))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, tela_largura - 30)
        self.rect.y = random.randint(0, tela_altura - 30)

class Arquivo():
    recorde = 0

    def LerArquivo(self):
        arquivo_save = open('save.txt', 'r')
        for linha in arquivo_save:
            Arquivo.recorde = linha
        arquivo_save.close()

    def EscreverArquivo(self):
        recorde_ponto = int(Arquivo.recorde)
        if Enemy.ponto > recorde_ponto:
            arquivo_save = open('save.txt', 'w')
            arquivo_save.write(f"{Enemy.ponto}")
            arquivo_save.close()

# ------------------------------------------------------
# |       CONFIGURAÇÕES GERAIS                         |
# ------------------------------------------------------

tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
frames = pygame.time.Clock()

tela_largura = tela.get_width()
tela_altura = tela.get_height()
pygame.display.set_caption("Meu Jogo")

fundo = pygame.image.load('Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (tela_largura, tela_altura))

# Eventos para spawn de inimigos e vidas
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

ADDVIDA = pygame.USEREVENT + 2  # Evento para spawn de vidas
pygame.time.set_timer(ADDVIDA, 10000)  # Spawn a cada 10 segundos

pygame.init()
player = Player()
arquivos_save = Arquivo()

# Grupos de sprites
inimigo = pygame.sprite.Group()
vidas_group = pygame.sprite.Group()  # Grupo para as vidas
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variáveis de controle
rodando = True
eliminado = False

# Fonte
fonte = pygame.font.SysFont('Calibri MS', 30)
fonte_morte = pygame.font.SysFont('Calibri MS', 70)

# ------------------------------------------------------
# |       LOOP DO JOGO                                 |
# ------------------------------------------------------

while rodando:
    tela.blit(fundo, (0, 0))
    tecla_pressionada = pygame.key.get_pressed()

    player.update(tecla_pressionada)
    inimigo.update()
    vidas_group.update()  # Atualiza as vidas

    for event in pygame.event.get():
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                rodando = False
            if (event.key == K_c):
                arquivos_save.LerArquivo()
        elif (event.type == QUIT):
            rodando = False
        elif event.type == ADDENEMY:
            novo_inimigo = Enemy()
            inimigo.add(novo_inimigo)
            all_sprites.add(novo_inimigo)
        elif event.type == ADDVIDA and not eliminado:  # Só spawna vidas se jogador estiver vivo
            nova_vida = Vida()
            vidas_group.add(nova_vida)
            all_sprites.add(nova_vida)

    # Verifica colisão com inimigos
    if pygame.sprite.spritecollideany(player, inimigo) and not eliminado:
        player.vidas -= 1  # Perde uma vida
        if player.vidas <= 0:  # Se acabaram as vidas
            player.kill()
            eliminado = True
            arquivos_save.LerArquivo()
            arquivos_save.EscreverArquivo()
        else:
            # Remove todos os inimigos da tela (opcional - reinicia a rodada)
            for inimigo_sprite in inimigo:
                inimigo_sprite.kill()

    # Verifica colisão com vidas
    vida_coletada = pygame.sprite.spritecollideany(player, vidas_group)
    if vida_coletada and not eliminado:
        vida_coletada.kill()  # Remove a vida coletada
        player.vidas += 1  # Adiciona uma vida
        if player.vidas > 5:  # Limite máximo de vidas (opcional)
            player.vidas = 5

    # Sistema de reinício
    if tecla_pressionada[K_r]:
        eliminado = False
        Enemy.ponto = 0
        player = Player()  # Recria o jogador com 3 vidas
        all_sprites.add(player)
        inimigo = pygame.sprite.Group()
        vidas_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        all_sprites.add(player)

    # Interface do jogo
    if not eliminado:
        # Mostra pontuação
        texto_ponto = fonte.render(f"Pontos: {Enemy.ponto}", False, (0,0,0))
        tela.blit(texto_ponto, (tela_largura - 200, 50))
        
        # Mostra vidas
        texto_vidas = fonte.render(f"Vidas: {player.vidas}", False, (0,0,0))
        tela.blit(texto_vidas, (50, 50))
        
    else:
        texto_morte = fonte_morte.render(f"Você perdeu! Seus pontos: {Enemy.ponto}. Seu recorde: {Arquivo.recorde}", False, (0,0,0))
        texto_reniciar = fonte.render("Pressione R para reiniciar ou ESC para sair", False, (0,0,0))
        
        texto_rect = texto_morte.get_rect(center=(tela_largura / 2, tela_altura / 2))
        tela.blit(texto_morte, texto_rect)
        tela.blit(texto_reniciar, (tela_largura / 2 - 200, tela_altura / 2 + 50))

    # Desenha todas as entidades
    for entity in all_sprites:
        tela.blit(entity.image, entity.rect)

    frames.tick(60)
    pygame.display.flip()

pygame.quit()