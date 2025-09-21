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
        self.game_state = "menu"  # "menu", "playing", "paused", "game_over"
        
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
        
        # Efeitos visuais
        self.effects = []  # Lista de efeitos visuais temporários
        
        # Gerar entidades iniciais
        self.spawn_initial_entities()
    
    def add_effect(self, x, y, effect_type):
        """Adiciona efeito visual"""
        timers = {'expulsion': 30, 'save': 60}
        radii = {'expulsion': 10, 'save': 5}
        self.effects.append({'type': effect_type, 'x': x, 'y': y, 'timer': timers[effect_type], 'radius': radii[effect_type]})
    
    def update_effects(self):
        """Atualiza efeitos visuais"""
        for effect in self.effects[:]:
            effect['timer'] -= 1
            if effect['timer'] <= 0:
                self.effects.remove(effect)
            else:
                effect['radius'] += 2 if effect['type'] == 'expulsion' else 1
    
    def draw_effects(self):
        """Desenha efeitos visuais"""
        for effect in self.effects:
            x, y = int(effect['x']), int(effect['y'])
            
            if effect['type'] == 'expulsion':
                # Ondas de choque
                alpha = int(255 * (effect['timer'] / 30))
                for i in range(3):
                    radius = effect['radius'] + (i * 10)
                    intensity = max(0, alpha - (i * 50))
                    if intensity > 0:
                        pygame.draw.circle(self.screen, (255, 100, 100), (x, y), radius, 3)
            
            elif effect['type'] == 'save':
                # Estrela dourada
                if effect['timer'] > 0:
                    r = effect['radius']
                    star_points = [(x + r * 2 * pygame.math.Vector2(1, 0).rotate(i * 144 - 90).x,
                                   y + r * 2 * pygame.math.Vector2(1, 0).rotate(i * 144 - 90).y) for i in range(5)]
                    inner_points = [(x + r * pygame.math.Vector2(1, 0).rotate(i * 144 + 72 - 90).x,
                                    y + r * pygame.math.Vector2(1, 0).rotate(i * 144 + 72 - 90).y) for i in range(5)]
                    
                    points = []
                    for i in range(5):
                        points.extend([star_points[i], inner_points[i]])
                    
                    if len(points) >= 6:
                        pygame.draw.polygon(self.screen, (255, 215, 0), points)
    
    def spawn_initial_entities(self):
        """Cria caçadores e animais iniciais"""
        for i in range(8):
            x, y = random.randint(50, self.width - 50), random.randint(50, self.height - 50)
            while abs(x - self.caipora.x) < 100 and abs(y - self.caipora.y) < 100:
                x, y = random.randint(50, self.width - 50), random.randint(50, self.height - 50)
            self.animals.append(Animal(x, y, random.choice(["onça", "arara", "tamanduá", "boto", "macaco"])))
        
        for _ in range(2):
            self.spawn_hunter()
    
    def spawn_hunter(self):
        """Spawna um novo caçador na borda da tela"""
        positions = [(random.randint(0, self.width), -50), (self.width + 50, random.randint(0, self.height)), 
                    (random.randint(0, self.width), self.height + 50), (-50, random.randint(0, self.height))]
        x, y = random.choice(positions)
        self.hunters.append(Hunter(x, y))
    
    def handle_events(self):
        """Trata eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.game_state == "playing":
                        self.game_state = "menu"
                    else:
                        self.running = False
                elif event.key == pygame.K_SPACE and self.game_state == "menu":
                    self.game_state = "playing"
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
            if self.caipora.rect.colliderect(hunter.rect) and not hunter.is_fleeing:
                hunter.start_fleeing()
                self.add_effect(hunter.rect.centerx, hunter.rect.centery, 'expulsion')
            
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
                self.add_effect(animal.rect.centerx, animal.rect.centery, 'save')
        
        # Remove animais capturados após um tempo e caçadores que fugiram
        self.animals = [a for a in self.animals if not a.should_remove()]
        
        # Remove caçadores que fugiram da tela
        for hunter in self.hunters[:]:
            if (hunter.x < -100 or hunter.x > self.width + 100 or 
                hunter.y < -100 or hunter.y > self.height + 100):
                if hunter.is_fleeing:
                    self.hunters.remove(hunter)
                    self.hunters_caught += 1
                    self.score += 100
        
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
        
        # Atualiza efeitos visuais
        self.update_effects()
    
    def draw_background(self):
        """Desenha o fundo da floresta"""
        self.screen.fill(self.colors['forest_green'])
        for i in range(15):
            x, y = (i * 80) % self.width, (i * 60) % self.height
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
        
        texts = [
            (self.font.render("GAME OVER", True, self.colors['red']), self.height//2 - 50),
            (self.font.render(f"Pontuação Final: {self.score}", True, self.colors['white']), self.height//2),
            (self.small_font.render("Pressione R para reiniciar", True, self.colors['white']), self.height//2 + 50)
        ]
        
        for text, y in texts:
            self.screen.blit(text, text.get_rect(center=(self.width//2, y)))
    
    def restart_game(self):
        """Reinicia o jogo"""
        self.game_state = "playing"
        self.score = self.animals_saved = self.hunters_caught = self.animals_lost = 0
        self.caipora = Caipora(self.width // 2, self.height // 2)
        self.hunters = self.animals = self.effects = []
        self.hunter_spawn_timer = self.animal_spawn_timer = 0
        self.spawn_initial_entities()
    
    def draw_menu(self):
        """Desenha tela de menu inicial"""
        self.screen.fill((0, 50, 0))
        
        # Título
        title = pygame.font.Font(None, 72).render("CAIPORA", True, (255, 255, 0))
        subtitle = self.font.render("Guardiã da Amazônia", True, (0, 255, 0))
        self.screen.blit(title, title.get_rect(center=(self.width//2, 100)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(self.width//2, 150)))
        
        # Instruções compactas
        instructions = [
            ("🎯 OBJETIVO:", (255, 255, 0)),
            ("• Expulse caçadores tocando neles", (255, 255, 255)),
            ("• Proteja animais ficando próximos", (255, 255, 255)),
            ("🎮 CONTROLES:", (255, 255, 0)),
            ("• WASD/Setas: Mover CAIPORA", (255, 255, 255)),
            ("• Game Over: 5 animais capturados", (255, 100, 100))
        ]
        
        y = 220
        for text, color in instructions:
            rendered = self.small_font.render(text, True, color)
            self.screen.blit(rendered, (50, y))
            y += 25
        
        # Exemplos visuais
        examples = [
            (Caipora(150, y + 20), "← CAIPORA (Você)"),
            (Hunter(150, y + 80), "← CAÇADOR (Inimigo)"),
            (Animal(150, y + 140, "onça"), "← ANIMAIS (Proteger)")
        ]
        
        for i, (entity, desc) in enumerate(examples):
            entity.draw(self.screen)
            text = self.small_font.render(desc, True, (255, 255, 255))
            self.screen.blit(text, (200, y + 30 + i * 60))
        
        # Botão de início
        if pygame.time.get_ticks() % 1000 < 500:
            start = self.font.render("Pressione ESPAÇO para começar!", True, (255, 255, 0))
            self.screen.blit(start, start.get_rect(center=(self.width//2, self.height - 50)))
    
    def draw_game_ui(self):
        """Desenha interface do jogo melhorada"""
        # Painel principal
        panel = pygame.Surface((300, 120))
        panel.set_alpha(180)
        panel.fill((0, 0, 0))
        self.screen.blit(panel, (10, 10))
        
        # Info compacta
        info = [
            (f"🏆 Pontos: {self.score}", (255, 255, 0)),
            (f"💚 Salvos: {self.animals_saved}", (0, 255, 0)),
            (f"🎯 Expulsos: {self.hunters_caught}", (255, 100, 100)),
            (f"💔 Perdidos: {self.animals_lost}/{self.max_animals_lost}", 
             (255, 0, 0) if self.animals_lost >= self.max_animals_lost - 1 else (255, 255, 255))
        ]
        
        for i, (text, color) in enumerate(info):
            self.screen.blit(self.small_font.render(text, True, color), (20, 20 + i * 22))
        
        # Controles
        controls_panel = pygame.Surface((200, 50))
        controls_panel.set_alpha(150)
        controls_panel.fill((0, 0, 0))
        self.screen.blit(controls_panel, (10, self.height - 60))
        
        self.screen.blit(self.small_font.render("WASD: Mover | ESC: Menu", True, (255, 255, 255)), (20, self.height - 50))
        
        # Dica
        if self.hunters:
            tip = self.small_font.render("💡 Toque nos caçadores!", True, (255, 255, 0))
            tip_rect = tip.get_rect(center=(self.width//2, 30))
            pygame.draw.rect(self.screen, (0, 0, 0), tip_rect.inflate(20, 10))
            pygame.draw.rect(self.screen, (255, 255, 0), tip_rect.inflate(20, 10), 2)
            self.screen.blit(tip, tip_rect)
    
    def draw(self):
        """Desenha tudo na tela"""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_background()
            
            # Desenha entidades
            self.caipora.draw(self.screen)
            
            for hunter in self.hunters:
                hunter.draw(self.screen)
            
            for animal in self.animals:
                animal.draw(self.screen)
            
            # Efeitos visuais
            self.draw_effects()
            
            # UI do jogo
            self.draw_game_ui()
        elif self.game_state == "game_over":
            self.draw_background()
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
        self.width = 45
        self.height = 45
        self.speed = 5
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.protection_radius = 80
    
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
        cx, cy = self.rect.center
        
        # Aura de proteção
        pygame.draw.circle(screen, (0, 255, 0), (cx, cy), self.protection_radius, 2)
        
        # Corpo humanoide
        pygame.draw.circle(screen, (101, 67, 33), (cx, cy - 15), 12)  # Cabeça
        pygame.draw.circle(screen, (34, 139, 34), (cx, cy - 15), 15, 3)  # Cabelo
        pygame.draw.ellipse(screen, (0, 100, 0), (cx - 10, cy - 5, 20, 25))  # Corpo
        pygame.draw.circle(screen, (101, 67, 33), (cx - 15, cy), 5)  # Braços
        pygame.draw.circle(screen, (101, 67, 33), (cx + 15, cy), 5)
        pygame.draw.circle(screen, (139, 69, 19), (cx - 8, cy + 20), 6)  # Pernas
        pygame.draw.circle(screen, (139, 69, 19), (cx + 8, cy + 20), 6)
        
        # Estrela mágica
        star_points = [(cx + 8 * pygame.math.Vector2(1, 0).rotate(i * 144 - 90).x, 
                       cy + 8 * pygame.math.Vector2(1, 0).rotate(i * 144 - 90).y) for i in range(5)]
        pygame.draw.polygon(screen, (255, 255, 0), star_points)
        
        # Texto identificador
        text = pygame.font.Font(None, 20).render("CAIPORA", True, (255, 255, 255))
        text_rect = text.get_rect(center=(cx, cy - 35))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(4, 2))
        screen.blit(text, text_rect)


class Hunter:
    """Classe que representa os caçadores ilegais"""
    
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.width = self.height = 35
        self.speed = random.uniform(1.5, 2.5)
        self.rect = pygame.Rect(x, y, 35, 35)
        self.target_animal = None
        self.direction_x = self.direction_y = 0
        self.is_fleeing = False
        self.flee_timer = 0
    
    def find_nearest_animal(self, animals):
        """Encontra o animal mais próximo"""
        valid_animals = [a for a in animals if not a.is_caught and not a.is_saved]
        if not valid_animals:
            return None
        return min(valid_animals, key=lambda a: ((self.x - a.x) ** 2 + (self.y - a.y) ** 2) ** 0.5)
    
    def update(self, animals):
        """Atualiza o caçador"""
        if self.is_fleeing:
            self.flee_timer -= 1
            if self.flee_timer <= 0:
                self.is_fleeing = False
            # Move para fora da tela
            self.x += self.direction_x * (self.speed * 2)
            self.y += self.direction_y * (self.speed * 2)
        else:
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
    
    def start_fleeing(self):
        """Caçador começa a fugir"""
        self.is_fleeing = True
        self.flee_timer = 120
        angle = random.uniform(0, 360)
        vec = pygame.math.Vector2(1, 0).rotate(angle)
        self.direction_x, self.direction_y = vec.x, vec.y
    
    def draw(self, screen):
        """Desenha o caçador na tela"""
        cx, cy = self.rect.center
        color = (100, 0, 0) if self.is_fleeing else (200, 0, 0)
        
        # Corpo humanoide
        pygame.draw.circle(screen, (255, 220, 177), (cx, cy - 12), 8)  # Cabeça
        pygame.draw.ellipse(screen, (139, 69, 19), (cx - 10, cy - 20, 20, 8))  # Chapéu
        pygame.draw.ellipse(screen, (101, 67, 33), (cx - 8, cy - 25, 16, 10))
        pygame.draw.rect(screen, color, (cx - 8, cy - 5, 16, 20))  # Corpo
        pygame.draw.circle(screen, (255, 220, 177), (cx - 12, cy), 4)  # Braços
        pygame.draw.circle(screen, (255, 220, 177), (cx + 12, cy), 4)
        pygame.draw.rect(screen, (0, 0, 139), (cx - 6, cy + 15, 5, 12))  # Pernas
        pygame.draw.rect(screen, (0, 0, 139), (cx + 1, cy + 15, 5, 12))
        
        if self.is_fleeing:
            # Linhas de movimento
            for i in range(3):
                lx = cx - (self.direction_x * (10 + i * 5))
                ly = cy - (self.direction_y * (10 + i * 5))
                pygame.draw.line(screen, (255, 255, 0), (lx, ly - 2), (lx, ly + 2), 2)
        else:
            # Rifle
            gx = cx + self.direction_x * 25
            gy = cy + self.direction_y * 25
            pygame.draw.line(screen, (64, 64, 64), (cx, cy), (gx, gy), 4)
            pygame.draw.circle(screen, (32, 32, 32), (gx, gy), 3)
            # Texto
            text = pygame.font.Font(None, 16).render("CAÇADOR", True, (255, 255, 255))
            text_rect = text.get_rect(center=(cx, cy - 32))
            pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(2, 1))
            screen.blit(text, text_rect)


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
        cx, cy = self.rect.center
        color = self.colors.get(self.animal_type, self.colors["genérico"])
        
        if self.is_caught:
            size = max(5, self.width - self.removal_timer // 10)
            pygame.draw.ellipse(screen, (100, 0, 0), (self.x, self.y, size, size))
            return
        
        # Desenha forma base
        pygame.draw.ellipse(screen, color, self.rect)
        
        # Detalhes específicos
        if self.animal_type == "onça":
            [pygame.draw.circle(screen, (0, 0, 0), (cx + random.randint(-8, 8), cy + random.randint(-8, 8)), 2) for _ in range(4)]
        elif self.animal_type == "arara":
            pygame.draw.polygon(screen, (255, 200, 0), [(cx + 10, cy - 5), (cx + 15, cy), (cx + 10, cy + 5)])
        elif self.animal_type == "tamanduá":
            pygame.draw.ellipse(screen, (100, 50, 0), (cx + 8, cy - 3, 12, 6))
        elif self.animal_type == "boto":
            pygame.draw.ellipse(screen, (255, 150, 200), (cx + 8, cy - 2, 8, 4))
        elif self.animal_type == "macaco":
            pygame.draw.circle(screen, color, (cx - 12, cy + 8), 4)
        
        # Estados visuais
        if self.is_saved:
            pygame.draw.ellipse(screen, (0, 255, 0), self.rect, 3)
            hx, hy = cx - 15, cy - 10
            pygame.draw.circle(screen, (255, 0, 100), (hx, hy), 3)
            pygame.draw.circle(screen, (255, 0, 100), (hx + 4, hy), 3)
            pygame.draw.polygon(screen, (255, 0, 100), [(hx - 2, hy + 2), (hx + 6, hy + 2), (hx + 2, hy + 6)])
        
        if self.fear_level > 20 and not self.is_caught and not self.is_saved:
            fear_width = int(20 * (self.fear_level / 100))
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 8, fear_width, 3))
            if self.fear_level > 70:
                pygame.draw.circle(screen, (255, 255, 0), (cx, cy - 15), 6)
                pygame.draw.rect(screen, (255, 0, 0), (cx - 1, cy - 18, 2, 8))
                pygame.draw.circle(screen, (255, 0, 0), (cx, cy - 8), 1)
        
        # Nome
        text = pygame.font.Font(None, 16).render(self.animal_type.upper(), True, (255, 255, 255))
        text_rect = text.get_rect(center=(cx, cy + 20))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(2, 1))
        screen.blit(text, text_rect)