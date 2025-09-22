#!/usr/bin/env python3
"""
Caipora: Guardiã da Amazônia
Jogo educativo sobre preservação ambiental e ODS 15
"""

import sys

def main():
    try:
        from game_compact import Game
        
        print("🌳 Iniciando Caipora: Guardiã da Amazônia...")
        print("🎮 Use as teclas W, A, S e D ou setas para mover a Caipora")
        print("🎯 Proteja os animais dos caçadores!")
        print("-" * 50)
        
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
