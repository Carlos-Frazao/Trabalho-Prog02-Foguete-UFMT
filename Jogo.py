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


# ------------------------------------------------------
# |       FUNÇÕES E CLASSSE                            |
# ------------------------------------------------------


# ''''''CLASSE DO JOGADOR ''''''
class Player(pygame.sprite.Sprite):

    # ''''''FUNÇÃO QUE CRIA O JOGADOR''''''
    def __init__(self):
        super(Player, self).__init__()

        jogador_imagem = ('Jogador.png') # Imagem do jogador

        self.image = pygame.image.load(jogador_imagem).convert_alpha() # Carrega a imagem e transforma em png
        self.image = pygame.transform.scale(self.image, (190,60)) # Tamanho da imagem do jogador
        self.rect =  self.image.get_rect() # Cria o retangulo de colisão

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
                    Enemy.ponto = Enemy.ponto + 1 # Tem que usar Enemy.ponto pois estamos acessando uma variavel dentro de uma classe, ai incrementamos mais 1
                else:
                    Enemy.ponto = Enemy.ponto + 5


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

fundo = pygame.image.load('Fundo.jpg').convert() # Cria o fundo do jogo, com uma imagem tambem
fundo = pygame.transform.scale(fundo, (tela_largura, tela_altura)) # Deixa imagem do tamanho da tela, ou seja, ocupando toda a tela

# ''''''INIMIGOS E SPRITES''''''
ADDENEMY = pygame.USEREVENT + 1 # Adiciona inimigos
pygame.time.set_timer(ADDENEMY, 500) # Adiciona inimigos a cada 500 milisegundos
        
pygame.init() # Iniciliza o jogo
player = Player() # player vai ser a classe Player()
arquivos_save = Arquivo()

# Cria os sprites e adiciona o player
inimigo = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# ''''''VARIAVEIS DE CONTROLE''''''
rodando = True # IMPORTANTE, ELA CONTROLA O LOOP DO JOGO
eliminado = False

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

    # Verifica se o jogador apertou ESC, fechou a janela ou morreu
    for event in pygame.event.get():
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                rodando = False
            if (event.key == K_c):
                arquivos_save.LerArquivo()
        elif (event.type == QUIT):
            rodando = False
        elif (event.type == ADDENEMY):
            novo_inimigo = Enemy()
            inimigo.add(novo_inimigo)
            all_sprites.add(novo_inimigo)

    # Verifica se o jogador colidiu com um inimigo
    if pygame.sprite.spritecollideany(player, inimigo): 
        player.kill() # Elimina o jogador
        eliminado = True
        arquivos_save.LerArquivo()
        arquivos_save.EscreverArquivo()
        
    
    # Garante que só dará pontos se o jogador não foi eliminado
    if eliminado == False: 
        texto_ponto = fonte.render(f"Pontos: {Enemy.ponto}", False, (0,0,0)) #Converte o numero em string
        tela.blit(texto_ponto, (tela_largura - 200, 50)) # Desenha na tela
    elif eliminado == True:

        #Printa na tela os pontos, e o recorde de pontos, lembrando que o recorde ta dentro da classe Arquivo()
        texto_morte = fonte_morte.render(f"Você perdeu! Seus pontos: {Enemy.ponto}. Seu recorde de pontos: {Arquivo.recorde}", False, (0,0,0))
        texto_rect = texto_morte.get_rect(center=(tela_largura / 2, tela_altura / 2)) # Transformei em um retangulo porque assim da pra centralizar certinho o texto na tela
        tela.blit(texto_morte, texto_rect)

    # Desenha todas as entidades na tela
    for entity in all_sprites: 
        tela.blit(entity.image, entity.rect)

    # Atualiza toda a tela [TEM QUE SER A ULTIMA COISA CHAMADA NO LOOP!]
    frames.tick(60)
    pygame.display.flip()    

pygame.quit()