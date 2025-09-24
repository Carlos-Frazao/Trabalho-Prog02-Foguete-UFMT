# Jogo em python
# UFMT

# ------------------------------------------------------
# |       BIBLIOTECAS                                  |
# ------------------------------------------------------

import pygame
import pygame.display
import random
from  pygame.locals import *

# ------------------------------------------------------
# |       ADICIONAR SISTEMA NA QUAL NAO DEIXA          |
# |       O JOGADOR ULTRAPASSAR OS LIMITES DA TELA!    |
# |       CARLOS                                       |
# ------------------------------------------------------
# R: Beleza, sistema adicionado!


# ------------------------------------------------------
# |       FUNÇÕES E CLASSSE                            |
# ------------------------------------------------------


# ''''''CLASSE DO JOGADOR''''''
class Player(pygame.sprite.Sprite):

    # ''''''FUNÇÃO QUE CRIA O JOGADOR''''''
    def __init__(self):
        super(Player, self).__init__()

        jogador_imagem = ('Jogador.png') # Imagem do jogador

        self.image = pygame.image.load(jogador_imagem).convert_alpha() # Carrega a imagem e transforma em png
        self.image = pygame.transform.scale(self.image, (190,60)) # Tamanho da imagem do jogador
        self.rect =  self.image.get_rect() # Cria o retangulo de colisão
        self.vidas = 3 # Sistema de vidas adicionado aqui, jogador começa com 3 vidas

    # ''''''FUNÇÃO DE MOVIMENTAÇÃO DO JOGADOR''''''
    def update(self, pressed_keys):

        if (tecla_pressionada[K_UP]) or (tecla_pressionada[K_w]) :
            self.rect.move_ip(0,-5)
        if (tecla_pressionada[K_DOWN]) or (tecla_pressionada[K_s]):
            self.rect.move_ip(0,5) 
        if (tecla_pressionada[K_LEFT]) or (tecla_pressionada[K_a]):
            self.rect.move_ip(-5,0)
        if (tecla_pressionada[K_RIGHT]) or (tecla_pressionada[K_d]):
            self.rect.move_ip(5,0)

    # ------------------------------------------------------
    # |       SISTEMAS DE LIMITE DA TELA                   |
    # ------------------------------------------------------
        if self.rect.top < 0: #Verifica a parte de cima e trava o jogador
            self.rect.top = 0
        if self.rect.bottom > tela_altura: #Verifica a parte de baixo e trava o jogador
            self.rect.bottom = tela_altura
        if self.rect.left < 0: #Verifica a parte da esquerda e trava o jogador
            self.rect.left = 0 
        if self.rect.right > tela_largura: #Verifica a parte da direita e trava o jogador
            self.rect.right = tela_largura

# ''''''CLASSE DO INIMIGO''''''
class Enemy(pygame.sprite.Sprite):

    ponto = 0 # Variavel armazenando pontuação

    # ''''''FUNÇÃO QUE CRIA O INIMIGO''''''
    def __init__(self):
        super(Enemy, self).__init__()

        inimigo_imagem = ('Inimigo.png') # Imagem do inimigo

        self.image = pygame.image.load(inimigo_imagem).convert_alpha() # Carrega a imagem e transforma em png
        self.image = pygame.transform.scale(self.image,(50,50)) # Tamanho da imagem do inimigo
        self.rect = self.image.get_rect(center=(tela_largura, random.randint(0,tela_altura))) # Cria o retangulo de colisão
        self.velocidade = random.uniform(1, 20)

    #FUNÇÃO QUE MOVIMENTA O INIMIGO
    def update(self):
         self.rect.move_ip(-self.velocidade,0)

         if self.rect.right < 0: # Quando chega na posição 0 no eixo X, ele deleta o inimigo
            self.kill()

            
            if eliminado  == False: # Antes verifica se o jogador esta vivo
                print("Não ta eliminado")

                # O jogador recebe mais ponto quando o inimigo que passou por ele era mais rapido   
                if self.velocidade < 10:
                    Enemy.ponto = Enemy.ponto + 1 # Tem que usar Enemy. ponto pois estamos acessando uma variavel dentro de uma classe, ai incrementamos mais 1
                else:
                    Enemy.ponto = Enemy.ponto + 5

    # ------------------------------------------------------
    # |                 SISTEMA DE VIDA                    |
    # ------------------------------------------------------
class Vida(pygame.sprite.Sprite):
    def __init__(self):
        super(Vida, self).__init__()
        vida_imagem = 'Vida.png' # Imagem do coração
        self.image = pygame.image.load(vida_imagem).convert_alpha() # Carrega a imagem e transforma em png
        self.image = pygame.transform.scale(self.image, (70, 55)) # Tamanho da imagem do coração
        self.rect = self.image.get_rect()
        # Posiciona o coração em uma posição aleatória
        self.rect.x = random.randint(0, tela_largura - 30)
        self.rect.y = random.randint(0, tela_altura - 30)

# ------------------------------------------------------
# |       SAVE DO JOGO                                 |
# ------------------------------------------------------

# ------------------------------------------------------
# |       ESTE SISTEMA É PRATICAMENTE IDENTICO         |
# |       AO QUE FOI APRENDIDO EM AULA, SÓ FIZ         |
# |       MUDANÇAS NECESSÁRIAS                         |
# ------------------------------------------------------

# ''''''CLASSE DO SALVADOR DE PONTOS''''''
class Arquivo():

    recorde = 0 # Armazena o recorde pessoal do jogador, pra mais tarde imprimir na tela

    # ''''''FUNÇÃO QUE LE O SAVE''''''
    def LerArquivo(self):
        arquivo_save = open('save.txt', 'r')
        for linha in arquivo_save:
            Arquivo.recorde = linha
        arquivo_save.close()

    # ''''''FUNÇÃO QUE ESCREVE O SAVE''''''
    def EscreverArquivo(self):

        recorde_ponto = int(Arquivo.recorde) # Transforma em string

        # VERIFICA SE TEVE RECORDE PESSOAL, SE NÃO ELE NEM ESCREVE
        if Enemy.ponto > recorde_ponto:
            arquivo_save = open('save.txt', 'w')
            arquivo_save.write(f"{Enemy.ponto}")
            arquivo_save.close()


# ------------------------------------------------------
# |       CONFIGRAÇÕES GERAIS                          |
# ------------------------------------------------------


# ''''''TELA''''''

tela = pygame.display.set_mode((0,0), pygame.FULLSCREEN) # Inicializa a tela, em tela cheia (FULLSCREEN)
frames = pygame.time.Clock()

tela_largura = tela.get_width() # Pega a largura da janela
tela_altura = tela.get_height() # Pega a altura da janela
pygame.display.set_caption("Meu Jogo") # Título da janela

fundo = pygame.image.load('Fundo.jpg').convert() # Cria o fundo do jogo, com uma imagem tambem
fundo = pygame.transform.scale(fundo, (tela_largura, tela_altura)) # Deixa imagem do tamanho da tela, ou seja, ocupando toda a tela

# Eventos para spawn de inimigos e vidas
ADDENEMY = pygame.USEREVENT + 1 # Adiciona inimigos
pygame.time.set_timer(ADDENEMY, 500) # Adiciona inimigos a cada 500 milisegundos
ADDVIDA = pygame.USEREVENT + 2  # Evento para spawn de vidas
pygame.time.set_timer(ADDVIDA, 10000)  # Spawn a cada 10 segundos

# ''''''INIMIGOS E SPRITES''''''
        
pygame.init() # Iniciliza o jogo
player = Player() # player vai ser a classe Player()
arquivos_save = Arquivo()

# Cria os sprites e adiciona o player [TODOS OS SPRITES TEM QUE SER ADICIONADOS AQUI!]
inimigo = pygame.sprite.Group()
vidas_group = pygame.sprite.Group() # Grupo de vidas
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# ''''''VARIAVEIS DE CONTROLE''''''
rodando = True # IMPORTANTE, ELA CONTROLA O LOOP DO JOGO
eliminado = False # Variavel que verifica se o jogador morreu ou não

# Fonte usada no texto de pontuação e morte
fonte = pygame.font.SysFont('Calibri MS', 30)
fonte_morte = pygame.font.SysFont('Calibri MS', 70)


# ------------------------------------------------------
# |       LOOP DO JOGO                                 |
# ------------------------------------------------------

while rodando:
        
    tela.blit(fundo, (0, 0)) # Desenha na tela o fundo do jogo
        
    tecla_pressionada = pygame.key.get_pressed() # Pega o evento de pressionar tecla

    player.update(tecla_pressionada) # Atualiza a classe Player(), e leva consigo o parametro da tecla pressionada
    inimigo.update()  # Atualiza a classe Enemy()
    vidas_group.update()  # Atualiza as vidas

    # Verifica se o jogador apertou ESC, fechou a janela ou morreu
    for event in pygame.event.get():
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                rodando = False
            if (event.key == K_c):
                arquivos_save.LerArquivo()
        elif (event.type == QUIT):
            rodando = False
        elif event.type == ADDENEMY: # Só adiciona inimigos se estiver no estado JOGANDO
            novo_inimigo = Enemy()
            inimigo.add(novo_inimigo)
            all_sprites.add(novo_inimigo)
        elif event.type == ADDVIDA and not eliminado:  # Só spawna vidas se jogador estiver vivo
            nova_vida = Vida()
            vidas_group.add(nova_vida)
            all_sprites.add(nova_vida)

    # Verifica se o jogador colidiu com um inimigo
    if pygame.sprite.spritecollideany(player, inimigo) and not eliminado: # Verifica se o jogador colidiu com um inimigo e se ele não foi eliminado
        player.vidas -= 1 # O jogador perde uma vida
        if player.vidas <= 0: # Se acabaram as vidas
            player.kill() # Elimina o jogador
            eliminado = True
            arquivos_save.LerArquivo()
            arquivos_save.EscreverArquivo()
        else:
            # Remove todos os inimigos da tela (opcional - reinicia a rodada)
            for inimigo_sprite in inimigo:
                inimigo_sprite.kill()

    # Verifica se o jogador colidiu com uma vida
    vida_coletada = pygame.sprite.spritecollideany(player, vidas_group)
    if vida_coletada and not eliminado:
        vida_coletada.kill()  # Remove a vida coletada
        player.vidas += 1  # Adiciona uma vida
        if player.vidas > 5:  # Limite máximo de vidas (opcional)
            player.vidas = 5

    # Se o jogador apertar R, ele reinicia o jogo, atualizeis as variaveis para o estado inicial, sendo que o jogador é adicionado novamente, e ficava cheio de avião na tela
    if tecla_pressionada[K_r]:
        eliminado = False
        Enemy.ponto = 0
        player = Player() # Recria o jogador com 3 vidas
        all_sprites.add(player) # Adiciona o jogador novamente
        inimigo = pygame.sprite.Group() # Reseta o grupo de inimigos
        vidas_group = pygame.sprite.Group() # Reseta o grupo de vidas
        all_sprites = pygame.sprite.Group() # Reseta o grupo de sprites
        all_sprites.add(player) # Adiciona o jogador novamente

    # Mostrando a vida na tela 
    if not eliminado: # Só mostra a vida se o jogador estiver vivo
        # Mostrar vida 
        texto_vida = fonte.render(f"Vidas: {player.vidas}", False, (0,0,0)) #Converte o numero em string
        tela.blit(texto_vida, (50, 50)) # Desenha na telas

        
    # Garante que só dará pontos se o jogador não foi eliminado
    if eliminado == False: 
        texto_ponto = fonte.render(f"Pontos: {Enemy.ponto}", False, (0,0,0)) #Converte o numero em string
        tela.blit(texto_ponto, (tela_largura - 200, 50)) # Desenha na tela
    elif eliminado == True:

        #Printa na tela os pontos, e o recorde de pontos, lembrando que o recorde ta dentro da classe Arquivo()
        texto_morte = fonte_morte.render(f"Você perdeu! Seus pontos: {Enemy.ponto}. Seu recorde de pontos: {Arquivo.recorde}", False, (0,0,0))
        
        # Informa o jogador que ele pode reiniciar ou sair do jogo
        texto_reniciar = fonte.render("Pressione R para reiniciar ou ESC para sair", False, (0,0,0))
        tela.blit(texto_reniciar, (tela_largura / 2 - 200, tela_altura / 2 + 50))

        texto_rect = texto_morte.get_rect(center=(tela_largura / 2, tela_altura / 2)) # Transformei em um retangulo porque assim da pra centralizar certinho o texto na tela
        tela.blit(texto_morte, texto_rect)

    # Desenha todas as entidades na tela
    for entity in all_sprites: 
        tela.blit(entity.image, entity.rect)

    # Atualiza toda a tela [TEM QUE SER A ULTIMA COISA CHAMADA NO LOOP!]
    frames.tick(60)
    pygame.display.flip()    

pygame.quit()