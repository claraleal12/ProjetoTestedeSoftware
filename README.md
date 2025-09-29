Caipora: Guardiã da Floresta

Este projeto é um template para o desenvolvimento de um jogo utilizando Python e a biblioteca Pygame, com foco em testes de software, aplicação de boas práticas de desenvolvimento e conscientização ambiental.


src/: Código-fonte do jogo


## ▶️ Como Executar o Jogo

1. Instale as dependências do projeto:
   ```
   pip install -r requirements.txt
   ```
2. Execute o jogo com o comando:
   ```
   python src/main.py
   ```



## 🎮 Objetivo do Jogo

Este jogo é inspirado na lenda brasileira da Caipora, uma entidade protetora das florestas e dos animais silvestres. A proposta do jogo é unir entretenimento e conscientização ambiental, utilizando elementos do folclore nacional para destacar a importância da preservação da fauna brasileira.

O jogador assume o papel da Caipora, cuja missão é proteger os animais da Floresta Amazônica de caçadores ilegais. Para isso, deve agir rapidamente para localizar e capturar os caçadores antes que consigam capturar os animais espalhados pelo cenário.



## 🕹️ Dinâmica e Mecânicas do Jogo

- O jogo é ambientado na Floresta Amazônica, com representação visual de elementos naturais e animais típicos do Brasil, como a onça-pintada, arara-azul, tamanduá-bandeira, entre outros.
- O jogador controla a Caipora, que se movimenta pelo mapa da floresta em busca dos caçadores.
- Os caçadores surgem aleatoriamente em diferentes pontos do mapa e tentam alcançar os animais para capturá-los.
- A cada animal capturado pelos caçadores, o jogador recebe uma penalidade. O objetivo é impedir que um número crítico de animais seja capturado.
- O jogo é dividido em fases progressivas, nas quais a dificuldade aumenta gradualmente, com mais caçadores, mais animais a proteger e obstáculos adicionais no cenário.
- O jogador vence a fase ao capturar todos os caçadores antes que o número limite de animais seja perdido.



## 🌱 Propósito Educativo

Além de proporcionar uma experiência divertida, o jogo tem como objetivo educar e conscientizar sobre os perigos da caça ilegal e a importância da preservação das espécies brasileiras. Ao utilizar a figura da Caipora, o jogo valoriza o folclore nacional e promove o respeito ao meio ambiente de forma lúdica e acessível.



## 📋 Requisitos do Sistema

- O jogador deve conseguir mover a Caipora pelo mapa usando as teclas direcionais.
- Caçadores e animais aparecem em posições aleatórias a cada fase.
- O sistema deve registrar o número de animais capturados e protegidos.
- O jogo deve aumentar a dificuldade progressivamente, com mais caçadores e obstáculos.
- Interface intuitiva, com feedback visual e sonoro ao jogador.
- O jogo deve exibir mensagens de vitória, derrota e transição de fases.



## 📑 Plano de Teste

O plano de teste do projeto visa garantir a qualidade e o correto funcionamento das principais funcionalidades do jogo. Os testes abrangem:

- Movimentação do personagem principal (Caipora).
- Surgimento aleatório de caçadores e animais.
- Registro e atualização da pontuação e penalidades.
- Progressão de fases e aumento de dificuldade.
- Exibição de mensagens e feedbacks ao usuário.
- Testes de desempenho e estabilidade do jogo.



## ✅ Casos de Teste

- **CT01:** Verificar se a Caipora se move corretamente nas quatro direções.
- **CT02:** Garantir que caçadores aparecem em posições aleatórias a cada fase.
- **CT03:** Confirmar que o jogo termina quando o limite de animais capturados é atingido.
- **CT04:** Testar se a pontuação aumenta ao capturar caçadores.
- **CT05:** Validar transição entre fases e aumento de dificuldade.
- **CT06:** Verificar se as mensagens de vitória e derrota são exibidas corretamente.
- **CT07:** Testar se os sons e animações são reproduzidos nos eventos principais.



## 📊 Diagramas

- **Diagrama de Casos de Uso:**  
  O diagrama de casos de uso apresenta as principais interações do jogador com o sistema, incluindo movimentação, captura de caçadores, proteção dos animais e progressão de fases.  
  [Ver diagrama de casos de uso](docs/diagrama_casos_uso.pdf)

- **Diagrama de Classes:**  
  O diagrama de classes detalha a estrutura do código, mostrando as principais classes do jogo, como `Caipora`, `Animal`, `Cacador`, `Fase`, e suas relações.  
  [Ver diagrama de classes](docs/diagrama_classes.pdf)



## 📄 Documentação Complementar

Para mais detalhes sobre requisitos, plano de teste, casos de teste e diagramas, consulte a pasta `docs/` deste projeto.