#!/usr/bin/env python3
"""
Caipora: Guardiã da Amazônia
Jogo educativo sobre preservação ambiental e ODS 15
"""

import sys

def main():
    try:
        from game_compact import Game
        
        print("═" * 55)
        print("🌳 CAIPORA: GUARDIÃ DA AMAZÔNIA 🐆")
        print("═" * 55)
        print("🎮 Controles: W, A, S, D ou setas para mover")
        print("🎯 Objetivo: Proteja os animais dos caçadores!")
        print("🌱 Missão: Preservar a biodiversidade amazônica")
        print("═" * 55)
        print("✨ Pressione qualquer tecla para começar...")
        input()
        print("🎮 Iniciando jogo...")
        
        # Inicializa e executa o jogo
        game = Game()
        game.run()
        
    except ImportError as e:
        print(f"❌ Erro ao importar o jogo: {e}")
        print("📋 Certifique-se de que o Pygame está instalado:")
        print("   pip install pygame")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
