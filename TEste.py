# Jogo em python
# UFMT

# ------------------------------------------------------
# |     BIBLIOTECAS                                    |
# ------------------------------------------------------

import pygame
import pygame.display
import random
from  pygame.locals import *

# ------------------------------------------------------
# |     ADICIONAR SISTEMA NA QUAL NAO DEIXA            |
# |     O JOGADOR ULTRAPASSAR OS LIMITES DA TELA!      |
# |     CARLOS                                         |
# ------------------------------------------------------

# ------------------------------------------------------
# |     FUNÇÕES E CLASSSE                              |
# ------------------------------------------------------


# ''''''CLASSE DO JOGADOR ''''''
class Player(pygame.sprite.Sprite):

    # ''''''FUNÇÃO QUE CRIA O JOGADOR''''''
    def __init__(self):
        super(Player, self).__init__()

        jogador_imagem = ('Jogador.png') # Imagem do jogador

        self.image = pygame.image.load(jogador_imagem).convert_alpha() # Carrega a imagem e transforma em png
        self.image = pygame.transform.scale(self.image, (190,60)) # Tamanho da imagem do jogador
        self.rect =  self.image.get_rect(center=(100, tela_altura / 2)) # << MODIFICADO: Posição inicial

    # ''''''FUNÇÃO DE MOVIMENTAÇÃO DO JOGADOR''''''
    def update(self, pressed_keys):

        if (pressed_keys[K_UP]) or (pressed_keys[K_w]) : # << MODIFICADO: Usando o parâmetro correto
            self.rect.move_ip(0,-5)
        if (pressed_keys[K_DOWN]) or (pressed_keys[K_s]):
            self.rect.move_ip(0,5)
        if (pressed_keys[K_LEFT]) or (pressed_keys[K_a]):
            self.rect.move_ip(-5,0)
        if (pressed_keys[K_RIGHT]) or (pressed_keys[K_d]):
            self.rect.move_ip(5,0)

        # << NOVO: Lógica para manter o jogador na tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > tela_largura:
            self.rect.right = tela_largura
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= tela_altura:
            self.rect.bottom = tela_altura


# ''''''CLASSE DO INIMIGO''''''
class Enemy(pygame.sprite.Sprite):

    ponto = 0 # Variavel armazenando pontuação

    # ''''''FUNÇÃO QUE CRIA O INIMIGO''''''
    def __init__(self):
        super(Enemy, self).__init__()

        inimigo_imagem = ('Inimigo.png') # Imagem do inimigo

        self.image = pygame.image.load(inimigo_imagem).convert_alpha() # Carrega a imagem e transforma em png
        self.image = pygame.transform.scale(self.image,(50,50)) # Tamanho da imagem do inimigo
        self.rect = self.image.get_rect(center=(tela_largura + 20, random.randint(0,tela_altura))) # Cria o retangulo de colisão
        self.velocidade = random.uniform(1, 20)

    #FUNÇÃO QUE MOVIMENTA O INIMIGO
    def update(self):
         self.rect.move_ip(-self.velocidade,0)

         if self.rect.right < 0: # Quando chega na posição 0 no eixo X, ele deleta o inimigo
            self.kill()
            # << MODIFICADO: A verificação de 'eliminado' não é mais necessária aqui
            # O jogador recebe mais ponto quando o inimigo que passou por ele era mais rapido
            if self.velocidade < 10:
                Enemy.ponto = Enemy.ponto + 1 # Tem que usar Enemy. ponto pois estamos acessando uma variavel dentro de uma classe, ai incrementamos mais 1
            else:
                Enemy.ponto = Enemy.ponto + 5


# ------------------------------------------------------
# |     SAVE DO JOGO                                   |
# ------------------------------------------------------

# ''''''CLASSE DO SALVADOR DE PONTOS''''''
class Arquivo():

    recorde = 0 # Armazena o recorde pessoal do jogador, pra mais tarde imprimir na tela

    # ''''''FUNÇÃO QUE LE O SAVE''''''
    def LerArquivo(self):
        try: # << MODIFICADO: Previne erro se o arquivo não existir
            arquivo_save = open('save.txt', 'r')
            linha = arquivo_save.readline()
            if linha:
                Arquivo.recorde = int(linha.strip())
            arquivo_save.close()
        except (FileNotFoundError, ValueError):
            Arquivo.recorde = 0


    # ''''''FUNÇÃO QUE ESCREVE O SAVE''''''
    def EscreverArquivo(self):
        # VERIFICA SE TEVE RECORDE PESSOAL, SE NÃO ELE NEM ESCREVE
        if Enemy.ponto > Arquivo.recorde:
            Arquivo.recorde = Enemy.ponto
            arquivo_save = open('save.txt', 'w')
            arquivo_save.write(f"{Enemy.ponto}")
            arquivo_save.close()


# ------------------------------------------------------
# |     CONFIGRAÇÕES GERAIS                            |
# ------------------------------------------------------

pygame.init() # Iniciliza o jogo

# ''''''TELA''''''
tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
frames = pygame.time.Clock()

tela_largura = tela.get_width()
tela_altura = tela.get_height()
pygame.display.set_caption("Meu Jogo")

fundo = pygame.image.load('Fundo.jpg').convert()
fundo = pygame.transform.scale(fundo, (tela_largura, tela_altura))

# ''''''INIMIGOS E SPRITES''''''
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 500)

# << MODIFICADO: Inicialização movida para uma função de reiniciar
player = None
arquivos_save = Arquivo()
arquivos_save.LerArquivo()

inimigo = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()


# ''''''VARIAVEIS DE CONTROLE''''''
rodando = True
estado_jogo = 'MENU' # << NOVO: Controla se estamos no menu, jogando ou em game over

# Fonte usada no texto de pontuação e morte
fonte = pygame.font.SysFont('Calibri MS', 30)
fonte_morte = pygame.font.SysFont('Calibri MS', 70)
fonte_reiniciar = pygame.font.SysFont('Calibri MS', 40)
fonte_titulo = pygame.font.SysFont('Calibri MS', 90) # << NOVO: Fonte para o título


# << NOVO: Função para resetar/iniciar o jogo
def reiniciar_jogo():
    global player, all_sprites, inimigo, estado_jogo
    Enemy.ponto = 0
    player = Player()
    all_sprites = pygame.sprite.Group()
    inimigo = pygame.sprite.Group()
    all_sprites.add(player)
    estado_jogo = 'JOGANDO'


# ------------------------------------------------------
# |     LOOP DO JOGO                                   |
# ------------------------------------------------------

while rodando:

    # O loop de eventos agora lida com inputs para todos os estados do jogo
    for event in pygame.event.get():
        if event.type == QUIT:
            rodando = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                rodando = False
            # Se estiver no MENU, a tecla ENTER inicia o jogo
            if estado_jogo == 'MENU' and event.key == K_RETURN:
                reiniciar_jogo()
            # Se estiver na tela de GAME OVER, a tecla 'R' reinicia
            if estado_jogo == 'GAME_OVER' and event.key == K_r:
                reiniciar_jogo()

        # Só adiciona inimigos se estiver no estado JOGANDO
        if event.type == ADDENEMY and estado_jogo == 'JOGANDO':
            novo_inimigo = Enemy()
            inimigo.add(novo_inimigo)
            all_sprites.add(novo_inimigo)


    # Desenha o fundo em todos os estados
    tela.blit(fundo, (0, 0))

    # --- Lógica e Desenho baseados no estado do jogo ---

    if estado_jogo == 'MENU':
        # << NOVO: Desenha a tela de Título/Menu
        titulo_texto = fonte_titulo.render("Corrida Espacial", True, (255, 255, 255))
        titulo_rect = titulo_texto.get_rect(center=(tela_largura / 2, tela_altura / 2 - 100))
        tela.blit(titulo_texto, titulo_rect)

        instrucao_texto = fonte_reiniciar.render("Pressione ENTER para começar", True, (200, 200, 200))
        instrucao_rect = instrucao_texto.get_rect(center=(tela_largura / 2, tela_altura / 2 + 50))
        tela.blit(instrucao_texto, instrucao_rect)

    elif estado_jogo == 'JOGANDO':
        # Roda a lógica principal do jogo
        tecla_pressionada = pygame.key.get_pressed()
        player.update(tecla_pressionada)
        inimigo.update()

        # Verifica colisão
        if pygame.sprite.spritecollideany(player, inimigo):
            player.kill()
            arquivos_save.EscreverArquivo() # Salva o recorde
            estado_jogo = 'GAME_OVER' # Muda para a tela de game over

        # Desenha os sprites do jogo
        for entity in all_sprites:
            tela.blit(entity.image, entity.rect)

        # Desenha a pontuação
        texto_ponto = fonte.render(f"Pontos: {Enemy.ponto}", True, (0,0,0))
        tela.blit(texto_ponto, (20, 20))

    elif estado_jogo == 'GAME_OVER':
        # Mostra a tela de "Game Over"
        texto_morte = fonte_morte.render(f"Você perdeu! Pontos: {Enemy.ponto}", True, (200,0,0))
        texto_morte_rect = texto_morte.get_rect(center=(tela_largura / 2, tela_altura / 2 - 50))
        tela.blit(texto_morte, texto_morte_rect)

        texto_recorde = fonte.render(f"Seu recorde: {Arquivo.recorde}", True, (0,0,0))
        texto_recorde_rect = texto_recorde.get_rect(center=(tela_largura / 2, tela_altura / 2 + 10))
        tela.blit(texto_recorde, texto_recorde_rect)

        texto_reiniciar = fonte_reiniciar.render("Pressione 'R' para jogar novamente", True, (0, 0, 0))
        texto_reiniciar_rect = texto_reiniciar.get_rect(center=(tela_largura / 2, tela_altura / 2 + 80))
        tela.blit(texto_reiniciar, texto_reiniciar_rect)

        # Desenha os inimigos restantes na tela
        for entity in all_sprites:
            tela.blit(entity.image, entity.rect)


    # Atualiza a tela inteira no final do loop
    frames.tick(60)
    pygame.display.flip()

pygame.quit()

