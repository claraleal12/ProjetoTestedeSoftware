import pygame
import sys
import random

class Game:
    """Classe principal que controla o jogo da Caipora"""
    
    def __init__(self):
        pygame.init()
        
        # Configurações da tela
        self.width = 1024
        self.height = 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Caipora: Guardiã da Amazônia")
        
        # Clock para controlar FPS
        self.clock = pygame.time.Clock()
        self.fps = 60
        
        # Estado do jogo
        self.running = True
        self.game_state = "playing"  # "playing", "paused", "game_over"
        
        # Pontuação e estatísticas
        self.score = 0
        self.animals_saved = 0
        self.hunters_caught = 0
        self.animals_lost = 0
        self.max_animals_lost = 5  # Game over se perder 5 animais
        
        # Cores
        self.colors = {
            'forest_green': (34, 139, 34),
            'dark_green': (0, 100, 0),
            'brown': (139, 69, 19),
            'white': (255, 255, 255),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'yellow': (255, 255, 0),
            'orange': (255, 165, 0)
        }
        
        # Entidades do jogo
        self.caipora = Caipora(self.width // 2, self.height // 2)
        self.hunters = []
        self.animals = []
        
        # Font para textos
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Timer para spawn
        self.hunter_spawn_timer = 0
        self.animal_spawn_timer = 0
        
        # Gerar entidades iniciais
        self.spawn_initial_entities()
    
    def spawn_initial_entities(self):
        """Cria caçadores e animais iniciais"""
        # Spawn animais
        animal_types = ["onça", "arara", "tamanduá", "boto", "macaco"]
        for i in range(8):
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            # Evita spawn muito próximo da Caipora
            while abs(x - self.caipora.x) < 100 and abs(y - self.caipora.y) < 100:
                x = random.randint(50, self.width - 50)
                y = random.randint(50, self.height - 50)
            animal_type = random.choice(animal_types)
            self.animals.append(Animal(x, y, animal_type))
        
        # Spawn hunters iniciais
        for i in range(2):
            self.spawn_hunter()
    
    def spawn_hunter(self):
        """Spawna um novo caçador na borda da tela"""
        side = random.randint(1, 4)
        if side == 1:  # Topo
            x = random.randint(0, self.width)
            y = -50
        elif side == 2:  # Direita
            x = self.width + 50
            y = random.randint(0, self.height)
        elif side == 3:  # Baixo
            x = random.randint(0, self.width)
            y = self.height + 50
        else:  # Esquerda
            x = -50
            y = random.randint(0, self.height)
        
        self.hunters.append(Hunter(x, y))
    
    def handle_events(self):
        """Trata eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_state == "game_over":
                    self.restart_game()
    
    def handle_movement(self):
        """Trata movimento da Caipora"""
        if self.game_state != "playing":
            return
            
        keys = pygame.key.get_pressed()
        dx = dy = 0
        
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = 1
        
        self.caipora.move(dx, dy)
        
        # Mantém Caipora dentro da tela
        self.caipora.x = max(0, min(self.width - self.caipora.width, self.caipora.x))
        self.caipora.y = max(0, min(self.height - self.caipora.height, self.caipora.y))
        self.caipora.update_rect()
    
    def update_entities(self):
        """Atualiza todas as entidades"""
        if self.game_state != "playing":
            return
        
        # Atualiza caçadores
        for hunter in self.hunters[:]:
            hunter.update(self.animals)
            
            # Verifica colisão com Caipora
            if self.caipora.rect.colliderect(hunter.rect):
                self.hunters.remove(hunter)
                self.hunters_caught += 1
                self.score += 100
            
            # Verifica se caçador capturou animal
            for animal in self.animals[:]:
                if hunter.rect.colliderect(animal.rect) and not animal.is_caught:
                    animal.is_caught = True
                    animal.caught_by_hunter = True
                    self.animals_lost += 1
                    if self.animals_lost >= self.max_animals_lost:
                        self.game_state = "game_over"
        
        # Atualiza animais
        for animal in self.animals:
            animal.update(self.caipora, self.hunters)
            
            # Verifica se animal foi salvo pela Caipora
            if (self.caipora.rect.colliderect(animal.rect) and 
                not animal.is_caught and not animal.is_saved):
                animal.is_saved = True
                self.animals_saved += 1
                self.score += 50
        
        # Remove animais capturados após um tempo
        self.animals = [a for a in self.animals if not a.should_remove()]
        
        # Spawn novos caçadores
        self.hunter_spawn_timer += 1
        if self.hunter_spawn_timer > 300:  # A cada 5 segundos
            self.spawn_hunter()
            self.hunter_spawn_timer = 0
        
        # Spawn novos animais ocasionalmente
        self.animal_spawn_timer += 1
        if self.animal_spawn_timer > 600 and len(self.animals) < 10:
            animal_types = ["onça", "arara", "tamanduá", "boto", "macaco"]
            x = random.randint(50, self.width - 50)
            y = random.randint(50, self.height - 50)
            animal_type = random.choice(animal_types)
            self.animals.append(Animal(x, y, animal_type))
            self.animal_spawn_timer = 0
    
    def draw_background(self):
        """Desenha o fundo da floresta"""
        self.screen.fill(self.colors['forest_green'])
        
        # Desenha algumas "árvores" simples
        for i in range(15):
            x = (i * 80) % self.width
            y = (i * 60) % self.height
            pygame.draw.circle(self.screen, self.colors['dark_green'], (x, y), 25)
            pygame.draw.rect(self.screen, self.colors['brown'], (x-5, y+15, 10, 20))
    
    def draw_ui(self):
        """Desenha interface do usuário"""
        # Painel de informações
        info_texts = [
            f"Pontuação: {self.score}",
            f"Animais Salvos: {self.animals_saved}",
            f"Caçadores Capturados: {self.hunters_caught}",
            f"Animais Perdidos: {self.animals_lost}/{self.max_animals_lost}"
        ]
        
        for i, text in enumerate(info_texts):
            color = self.colors['white']
            if i == 3 and self.animals_lost >= self.max_animals_lost - 1:
                color = self.colors['red']
            
            rendered_text = self.font.render(text, True, color)
            self.screen.blit(rendered_text, (10, 10 + i * 40))
        
        # Controles
        controls = [
            "WASD/Setas: Mover Caipora",
            "ESC: Sair"
        ]
        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, self.colors['white'])
            self.screen.blit(control_text, (10, self.height - 60 + i * 25))
    
    def draw_game_over(self):
        """Desenha tela de game over"""
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        game_over_text = self.font.render("GAME OVER", True, self.colors['red'])
        score_text = self.font.render(f"Pontuação Final: {self.score}", True, self.colors['white'])
        restart_text = self.small_font.render("Pressione R para reiniciar", True, self.colors['white'])
        
        # Centraliza textos
        game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 50))
        score_rect = score_text.get_rect(center=(self.width//2, self.height//2))
        restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 50))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
    
    def restart_game(self):
        """Reinicia o jogo"""
        self.__init__()
    
    def draw(self):
        """Desenha tudo na tela"""
        self.draw_background()
        
        # Desenha entidades
        self.caipora.draw(self.screen)
        
        for hunter in self.hunters:
            hunter.draw(self.screen)
        
        for animal in self.animals:
            animal.draw(self.screen)
        
        # UI
        self.draw_ui()
        
        # Game over overlay
        if self.game_state == "game_over":
            self.draw_game_over()
        
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        while self.running:
            self.handle_events()
            self.handle_movement()
            self.update_entities()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()


class Caipora:
    """Classe que representa a Caipora, protagonista do jogo"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def move(self, dx, dy):
        """Move a Caipora"""
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def update_rect(self):
        """Atualiza o retângulo de colisão"""
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        """Desenha a Caipora na tela"""
        # Corpo da Caipora (verde escuro)
        pygame.draw.ellipse(screen, (0, 100, 0), self.rect)
        # Marca distintiva (círculo amarelo no centro)
        center_x = self.rect.centerx
        center_y = self.rect.centery
        pygame.draw.circle(screen, (255, 255, 0), (center_x, center_y), 8)


class Hunter:
    """Classe que representa os caçadores ilegais"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 30
        self.speed = random.uniform(1.5, 2.5)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.target_animal = None
        self.direction_x = 0
        self.direction_y = 0
    
    def find_nearest_animal(self, animals):
        """Encontra o animal mais próximo"""
        nearest_animal = None
        min_distance = float('inf')
        
        for animal in animals:
            if not animal.is_caught and not animal.is_saved:
                distance = ((self.x - animal.x) ** 2 + (self.y - animal.y) ** 2) ** 0.5
                if distance < min_distance:
                    min_distance = distance
                    nearest_animal = animal
        
        return nearest_animal
    
    def update(self, animals):
        """Atualiza o caçador"""
        # Encontra animal alvo
        if not self.target_animal or self.target_animal.is_caught or self.target_animal.is_saved:
            self.target_animal = self.find_nearest_animal(animals)
        
        # Move em direção ao animal alvo
        if self.target_animal:
            dx = self.target_animal.x - self.x
            dy = self.target_animal.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            
            if distance > 0:
                self.direction_x = dx / distance
                self.direction_y = dy / distance
        
        # Move
        self.x += self.direction_x * self.speed
        self.y += self.direction_y * self.speed
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        """Desenha o caçador na tela"""
        # Caçador (retângulo vermelho)
        pygame.draw.rect(screen, (200, 0, 0), self.rect)
        # Arma (linha preta)
        center_x = self.rect.centerx
        center_y = self.rect.centery
        end_x = center_x + self.direction_x * 20
        end_y = center_y + self.direction_y * 20
        pygame.draw.line(screen, (0, 0, 0), (center_x, center_y), (end_x, end_y), 3)


class Animal:
    """Classe que representa os animais da floresta"""
    
    def __init__(self, x, y, animal_type="genérico"):
        self.x = x
        self.y = y
        self.width = 25
        self.height = 25
        self.speed = random.uniform(0.5, 1.5)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.animal_type = animal_type
        self.is_caught = False
        self.is_saved = False
        self.caught_by_hunter = False
        self.fear_level = 0
        self.removal_timer = 0
        
        # Movimento aleatório
        self.direction_x = random.choice([-1, 0, 1])
        self.direction_y = random.choice([-1, 0, 1])
        self.move_timer = 0
        
        # Cores por tipo de animal
        self.colors = {
            "onça": (255, 200, 0),
            "arara": (0, 150, 255),
            "tamanduá": (139, 69, 19),
            "boto": (255, 192, 203),
            "macaco": (101, 67, 33),
            "genérico": (100, 255, 100)
        }
    
    def update(self, caipora, hunters):
        """Atualiza o animal"""
        if self.is_caught:
            self.removal_timer += 1
            return
        
        if self.is_saved:
            # Animal salvo fica próximo da Caipora
            dx = caipora.x - self.x
            dy = caipora.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 60:  # Mantém distância da Caipora
                self.x += (dx / distance) * self.speed * 0.5
                self.y += (dy / distance) * self.speed * 0.5
        else:
            # Movimento natural
            self.move_timer += 1
            if self.move_timer > 60:  # Muda direção a cada segundo
                self.direction_x = random.choice([-1, 0, 1])
                self.direction_y = random.choice([-1, 0, 1])
                self.move_timer = 0
            
            # Foge de caçadores próximos
            for hunter in hunters:
                distance = ((self.x - hunter.x) ** 2 + (self.y - hunter.y) ** 2) ** 0.5
                if distance < 80:
                    # Foge do caçador
                    flee_x = self.x - hunter.x
                    flee_y = self.y - hunter.y
                    if distance > 0:
                        self.direction_x = flee_x / distance
                        self.direction_y = flee_y / distance
                    self.fear_level = min(100, self.fear_level + 5)
                    break
            else:
                self.fear_level = max(0, self.fear_level - 1)
            
            # Move
            speed_multiplier = 2 if self.fear_level > 50 else 1
            self.x += self.direction_x * self.speed * speed_multiplier
            self.y += self.direction_y * self.speed * speed_multiplier
        
        # Mantém dentro da tela
        self.x = max(0, min(1024 - self.width, self.x))
        self.y = max(0, min(768 - self.height, self.y))
        self.rect.x = self.x
        self.rect.y = self.y
    
    def should_remove(self):
        """Verifica se o animal deve ser removido"""
        return self.is_caught and self.removal_timer > 120  # Remove após 2 segundos
    
    def draw(self, screen):
        """Desenha o animal na tela"""
        color = self.colors.get(self.animal_type, self.colors["genérico"])
        
        if self.is_caught:
            # Animal capturado fica vermelho e diminui
            color = (100, 0, 0)
            size = max(5, self.width - self.removal_timer // 10)
            rect = pygame.Rect(self.x, self.y, size, size)
        elif self.is_saved:
            # Animal salvo tem borda verde
            rect = self.rect
            pygame.draw.ellipse(screen, (0, 255, 0), rect, 3)
        else:
            rect = self.rect
        
        # Desenha o animal
        pygame.draw.ellipse(screen, color, rect)
        
        # Indicador de medo
        if self.fear_level > 20 and not self.is_caught and not self.is_saved:
            fear_width = int(20 * (self.fear_level / 100))
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 8, fear_width, 3))