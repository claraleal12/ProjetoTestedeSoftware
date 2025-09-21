import pygame
import sys
import random

class Game:
    def __init__(self):
        pygame.init()
        self.width, self.height = 1024, 768
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Caipora")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"
        self.score = self.animals_saved = self.hunters_caught = self.animals_lost = 0
        self.max_animals_lost = 5
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.caipora = Caipora(self.width // 2, self.height // 2)
        self.hunters = []
        self.animals = []
        self.effects = []
        self.spawn_timer = 0
        self.spawn_entities()
    
    def spawn_entities(self):
        for i in range(8):
            x, y = random.randint(50, self.width - 50), random.randint(50, self.height - 50)
            while abs(x - self.caipora.x) < 100 and abs(y - self.caipora.y) < 100:
                x, y = random.randint(50, self.width - 50), random.randint(50, self.height - 50)
            self.animals.append(Animal(x, y, random.choice(["onça", "arara", "tamanduá", "boto", "macaco"])))
        for _ in range(2):
            positions = [(random.randint(0, self.width), -50), (self.width + 50, random.randint(0, self.height)), 
                        (random.randint(0, self.width), self.height + 50), (-50, random.randint(0, self.height))]
            x, y = random.choice(positions)
            self.hunters.append(Hunter(x, y))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game_state = "menu" if self.game_state == "playing" else "quit"
                    if self.game_state == "quit": self.running = False
                elif event.key == pygame.K_SPACE and self.game_state == "menu":
                    self.game_state = "playing"
                elif event.key == pygame.K_r and self.game_state == "game_over":
                    self.restart()
    
    def handle_movement(self):
        if self.game_state != "playing": return
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        self.caipora.move(dx, dy)
        self.caipora.x = max(0, min(self.width - 40, self.caipora.x))
        self.caipora.y = max(0, min(self.height - 40, self.caipora.y))
        self.caipora.rect.x, self.caipora.rect.y = self.caipora.x, self.caipora.y
    
    def update_entities(self):
        if self.game_state != "playing": return
        
        # Update hunters
        for hunter in self.hunters[:]:
            hunter.update(self.animals)
            if self.caipora.rect.colliderect(hunter.rect) and not hunter.is_fleeing:
                hunter.start_fleeing()
                self.effects.append({'type': 'expulsion', 'x': hunter.rect.centerx, 'y': hunter.rect.centery, 'timer': 30, 'radius': 10})
            if hunter.x < -100 or hunter.x > self.width + 100 or hunter.y < -100 or hunter.y > self.height + 100:
                if hunter.is_fleeing:
                    self.hunters.remove(hunter)
                    self.hunters_caught += 1
                    self.score += 100
            
            # Check hunter caught animal
            for animal in self.animals:
                if hunter.rect.colliderect(animal.rect) and not animal.is_caught:
                    animal.is_caught = True
                    self.animals_lost += 1
                    if self.animals_lost >= self.max_animals_lost:
                        self.game_state = "game_over"
        
        # Update animals
        for animal in self.animals[:]:
            animal.update(self.caipora, self.hunters)
            if (self.caipora.rect.colliderect(animal.rect) and not animal.is_caught and not animal.is_saved):
                animal.is_saved = True
                self.animals_saved += 1
                self.score += 50
                self.effects.append({'type': 'save', 'x': animal.rect.centerx, 'y': animal.rect.centery, 'timer': 60, 'radius': 5})
            if animal.is_caught and animal.removal_timer > 120:
                self.animals.remove(animal)
        
        # Spawn new hunters
        self.spawn_timer += 1
        if self.spawn_timer > 300:
            positions = [(random.randint(0, self.width), -50), (self.width + 50, random.randint(0, self.height)), 
                        (random.randint(0, self.width), self.height + 50), (-50, random.randint(0, self.height))]
            x, y = random.choice(positions)
            self.hunters.append(Hunter(x, y))
            self.spawn_timer = 0
        
        # Update effects
        for effect in self.effects[:]:
            effect['timer'] -= 1
            if effect['timer'] <= 0:
                self.effects.remove(effect)
            else:
                effect['radius'] += 2 if effect['type'] == 'expulsion' else 1
    
    def draw(self):
        # Background
        self.screen.fill((34, 139, 34))
        for i in range(15):
            x, y = (i * 80) % self.width, (i * 60) % self.height
            pygame.draw.circle(self.screen, (0, 100, 0), (x, y), 25)
            pygame.draw.rect(self.screen, (139, 69, 19), (x-5, y+15, 10, 20))
        
        if self.game_state == "menu":
            self.screen.fill((0, 50, 0))
            title = pygame.font.Font(None, 72).render("CAIPORA", True, (255, 255, 0))
            subtitle = self.font.render("Guardiã da Amazônia", True, (0, 255, 0))
            self.screen.blit(title, title.get_rect(center=(self.width//2, 100)))
            self.screen.blit(subtitle, subtitle.get_rect(center=(self.width//2, 150)))
            
            instructions = [
                ("🎯 Expulse caçadores tocando neles", (255, 255, 255)),
                ("🎮 WASD/Setas: Mover CAIPORA", (255, 255, 255)),
                ("Game Over: 5 animais capturados", (255, 100, 100))
            ]
            
            y = 220
            for text, color in instructions:
                rendered = self.small_font.render(text, True, color)
                self.screen.blit(rendered, (50, y))
                y += 30
            
            if pygame.time.get_ticks() % 1000 < 500:
                start = self.font.render("Pressione ESPAÇO para começar!", True, (255, 255, 0))
                self.screen.blit(start, start.get_rect(center=(self.width//2, self.height - 50)))
        
        elif self.game_state == "playing":
            # Draw entities
            self.caipora.draw(self.screen)
            for hunter in self.hunters:
                hunter.draw(self.screen)
            for animal in self.animals:
                animal.draw(self.screen)
            
            # Draw effects
            for effect in self.effects:
                x, y = int(effect['x']), int(effect['y'])
                if effect['type'] == 'expulsion':
                    for i in range(3):
                        pygame.draw.circle(self.screen, (255, 100, 100), (x, y), effect['radius'] + i * 10, 3)
                elif effect['type'] == 'save':
                    pygame.draw.circle(self.screen, (255, 215, 0), (x, y), effect['radius'], 3)
            
            # UI
            panel = pygame.Surface((300, 100))
            panel.set_alpha(180)
            panel.fill((0, 0, 0))
            self.screen.blit(panel, (10, 10))
            
            info = [
                f"🏆 Pontos: {self.score}",
                f"💚 Salvos: {self.animals_saved}",
                f"🎯 Expulsos: {self.hunters_caught}",
                f"💔 Perdidos: {self.animals_lost}/{self.max_animals_lost}"
            ]
            
            for i, text in enumerate(info):
                color = (255, 0, 0) if i == 3 and self.animals_lost >= 4 else (255, 255, 255)
                self.screen.blit(self.small_font.render(text, True, color), (20, 20 + i * 20))
        
        elif self.game_state == "game_over":
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            texts = [
                (self.font.render("GAME OVER", True, (255, 0, 0)), self.height//2 - 50),
                (self.font.render(f"Pontuação: {self.score}", True, (255, 255, 255)), self.height//2),
                (self.small_font.render("Pressione R para reiniciar", True, (255, 255, 255)), self.height//2 + 50)
            ]
            
            for text, y in texts:
                self.screen.blit(text, text.get_rect(center=(self.width//2, y)))
        
        pygame.display.flip()
    
    def restart(self):
        self.game_state = "playing"
        self.score = self.animals_saved = self.hunters_caught = self.animals_lost = 0
        self.caipora = Caipora(self.width // 2, self.height // 2)
        self.hunters = self.animals = self.effects = []
        self.spawn_timer = 0
        self.spawn_entities()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.handle_movement()
            self.update_entities()
            self.draw()
            self.clock.tick(60)
        pygame.quit()

class Caipora:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 5
    
    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed
    
    def draw(self, screen):
        cx, cy = self.rect.center
        pygame.draw.circle(screen, (0, 255, 0), (cx, cy), 50, 2)  # Aura
        pygame.draw.circle(screen, (101, 67, 33), (cx, cy - 15), 12)  # Cabeça
        pygame.draw.circle(screen, (34, 139, 34), (cx, cy - 15), 15, 3)  # Cabelo
        pygame.draw.ellipse(screen, (0, 100, 0), (cx - 10, cy - 5, 20, 25))  # Corpo
        pygame.draw.polygon(screen, (255, 255, 0), [(cx + 8, cy), (cx, cy - 8), (cx - 8, cy), (cx, cy + 8)])  # Estrela
        text = pygame.font.Font(None, 20).render("CAIPORA", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(cx, cy - 35)))

class Hunter:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, 35, 35)
        self.speed = random.uniform(1.5, 2.5)
        self.target_animal = None
        self.direction_x = self.direction_y = 0
        self.is_fleeing = False
        self.flee_timer = 0
    
    def find_nearest_animal(self, animals):
        valid = [a for a in animals if not a.is_caught and not a.is_saved]
        return min(valid, key=lambda a: ((self.x - a.x) ** 2 + (self.y - a.y) ** 2) ** 0.5) if valid else None
    
    def update(self, animals):
        if self.is_fleeing:
            self.flee_timer -= 1
            if self.flee_timer <= 0:
                self.is_fleeing = False
            self.x += self.direction_x * (self.speed * 2)
            self.y += self.direction_y * (self.speed * 2)
        else:
            if not self.target_animal or self.target_animal.is_caught or self.target_animal.is_saved:
                self.target_animal = self.find_nearest_animal(animals)
            if self.target_animal:
                dx = self.target_animal.x - self.x
                dy = self.target_animal.y - self.y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance > 0:
                    self.direction_x = dx / distance
                    self.direction_y = dy / distance
            self.x += self.direction_x * self.speed
            self.y += self.direction_y * self.speed
        self.rect.x, self.rect.y = self.x, self.y
    
    def start_fleeing(self):
        self.is_fleeing = True
        self.flee_timer = 120
        angle = random.uniform(0, 360)
        vec = pygame.math.Vector2(1, 0).rotate(angle)
        self.direction_x, self.direction_y = vec.x, vec.y
    
    def draw(self, screen):
        cx, cy = self.rect.center
        color = (100, 0, 0) if self.is_fleeing else (200, 0, 0)
        pygame.draw.circle(screen, (255, 220, 177), (cx, cy - 12), 8)  # Cabeça
        pygame.draw.ellipse(screen, (139, 69, 19), (cx - 10, cy - 20, 20, 8))  # Chapéu
        pygame.draw.rect(screen, color, (cx - 8, cy - 5, 16, 20))  # Corpo
        if not self.is_fleeing:
            text = pygame.font.Font(None, 16).render("CAÇADOR", True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=(cx, cy - 32)))

class Animal:
    def __init__(self, x, y, animal_type):
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, 25, 25)
        self.animal_type = animal_type
        self.speed = random.uniform(0.5, 1.5)
        self.is_caught = self.is_saved = False
        self.fear_level = 0
        self.removal_timer = 0
        self.direction_x = random.choice([-1, 0, 1])
        self.direction_y = random.choice([-1, 0, 1])
        self.move_timer = 0
        self.colors = {"onça": (255, 200, 0), "arara": (0, 150, 255), "tamanduá": (139, 69, 19), 
                      "boto": (255, 192, 203), "macaco": (101, 67, 33), "genérico": (100, 255, 100)}
    
    def update(self, caipora, hunters):
        if self.is_caught:
            self.removal_timer += 1
            return
        
        if self.is_saved:
            dx = caipora.x - self.x
            dy = caipora.y - self.y
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance > 60:
                self.x += (dx / distance) * self.speed * 0.5
                self.y += (dy / distance) * self.speed * 0.5
        else:
            self.move_timer += 1
            if self.move_timer > 60:
                self.direction_x = random.choice([-1, 0, 1])
                self.direction_y = random.choice([-1, 0, 1])
                self.move_timer = 0
            
            for hunter in hunters:
                distance = ((self.x - hunter.x) ** 2 + (self.y - hunter.y) ** 2) ** 0.5
                if distance < 80:
                    flee_x = self.x - hunter.x
                    flee_y = self.y - hunter.y
                    if distance > 0:
                        self.direction_x = flee_x / distance
                        self.direction_y = flee_y / distance
                    self.fear_level = min(100, self.fear_level + 5)
                    break
            else:
                self.fear_level = max(0, self.fear_level - 1)
            
            speed_multiplier = 2 if self.fear_level > 50 else 1
            self.x += self.direction_x * self.speed * speed_multiplier
            self.y += self.direction_y * self.speed * speed_multiplier
        
        self.x = max(0, min(1024 - 25, self.x))
        self.y = max(0, min(768 - 25, self.y))
        self.rect.x, self.rect.y = self.x, self.y
    
    def draw(self, screen):
        if self.is_caught:
            size = max(5, 25 - self.removal_timer // 10)
            pygame.draw.ellipse(screen, (100, 0, 0), (self.x, self.y, size, size))
            return
        
        cx, cy = self.rect.center
        color = self.colors.get(self.animal_type, (100, 255, 100))
        pygame.draw.ellipse(screen, color, self.rect)
        
        if self.is_saved:
            pygame.draw.ellipse(screen, (0, 255, 0), self.rect, 3)
            pygame.draw.circle(screen, (255, 0, 100), (cx - 15, cy - 10), 3)  # Coração
        
        text = pygame.font.Font(None, 16).render(self.animal_type.upper(), True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(cx, cy + 20)))

if __name__ == "__main__":
    game = Game()
    game.run()