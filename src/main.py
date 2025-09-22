import pygame
import sys

pygame.init()

# Configurações da janela
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Meu Jogo com Pygame')

# Loop principal
enquanto_rodando = True
while enquanto_rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            enquanto_rodando = False
    tela.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()
