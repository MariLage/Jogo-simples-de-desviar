import pygame
import random

pygame.init();
largura, altura = 400, 600;
tela = pygame.display.set_mode((largura, altura));
clock = pygame.time.Clock();

jogador = pygame.Rect(180, 500, 40, 40);
velocidade = 5;
obstaculos = [];
colisoes = 0;
game_over = False;

# --- Configuração de Fontes ---
# Fonte para o contador de colisões
fonte_contador = pygame.font.SysFont('Arial', 24); 
# Fonte para a mensagem de Game Over
fonte_game_over = pygame.font.SysFont('Arial', 40); 

def criar_obstaculos():
    x = random.randint(0, largura - 40);
    return pygame.Rect(x, -40, 40, 40);

while True:
    if not game_over:
        # --- Gerenciamento de Eventos e Lógica do Jogo ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit();
                exit();

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT] and jogador.left > 0:
            jogador.x -= velocidade;
        if teclas[pygame.K_RIGHT] and jogador.right < largura:
            jogador.x += velocidade;

        if random.randint(1, 30) == 1:
            obstaculos.append(criar_obstaculos())
        
        for obstaculo in obstaculos:
            obstaculo.y += 5;
            if obstaculo.colliderect(jogador):
                colisoes += 1;
                obstaculos.remove(obstaculo); # Remove o obstáculo colidido para não contar duas vezes
                
                # Exibir a mensagem "DANO"
                mensagem_dano = fonte_game_over.render('DANO!', True, (255, 40, 0));
                retangulo_dano = mensagem_dano.get_rect(center=(largura // 2, altura // 2));
                tela.blit(mensagem_dano, retangulo_dano);
                pygame.display.flip();
                pygame.time.delay(300); # Pausa o jogo por 0.5 segundos para a mensagem aparecer

                if colisoes >= 4:
                    game_over = True;
        
        obstaculos = [obstaculo for obstaculo in obstaculos if obstaculo.y < altura];

        # --- Lógica de Desenho na Tela ---
        tela.fill((40, 40, 40)) # Fundo cinza escuro

        # Desenha os obstáculos
        for obstaculo in obstaculos:
            pygame.draw.rect(tela, (255, 0, 0), obstaculo);
        
        # Desenha o jogador
        pygame.draw.rect(tela, (0, 255, 0), jogador);

        # Desenha o contador de colisões no canto superior esquerdo
        texto_colisoes = fonte_contador.render(f"Colisões: {colisoes}", True, (255, 255, 255));
        tela.blit(texto_colisoes, (10, 10));

    else: # Se o jogo terminou (game_over é True)
        # Exibe a tela de Game Over
        tela.fill((0, 0, 0)) # Fundo preto
        texto_final = fonte_game_over.render("GAME OVER", True, (255, 255, 255));
        retangulo_texto_final = texto_final.get_rect(center=(largura // 2, altura // 2));
        tela.blit(texto_final, retangulo_texto_final);
        
        texto_placar = fonte_contador.render(f"Colisões: {colisoes}", True, (255, 255, 255));
        retangulo_placar = texto_placar.get_rect(center=(largura // 2, altura // 2 + 50));
        tela.blit(texto_placar, retangulo_placar);
        
        # O loop de eventos ainda precisa rodar para que a janela possa ser fechada
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit();
                exit();
    
    pygame.display.flip();
    clock.tick(60);