#!/usr/bin/env python3
"""
Caipora: Guardiã da Amazônia
Jogo educativo sobre proteção ambiental
"""

import pygame
import sys
import os

# Adiciona o diretório src ao path
sys.path.append(os.path.dirname(__file__))

from game_compact import Game

def main():
    """Função principal do jogo"""
    try:
        print("🌳 Iniciando Caipora: Guardiã da Amazônia...")
        print("🎮 Use as teclas W, A, S e D ou setas para mover a Caipora")
        print("🎯 Proteja os animais dos caçadores!")
        print("-" * 50)
        
        game = Game()
        game.run()
        
    except ImportError as e:
        print("❌ Erro: Pygame não está instalado!")
        print("📦 Execute: pip install pygame")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
