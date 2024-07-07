import pygame
from network import Network

WIDTH, HEIGHT = 800, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game(Client)")



clientNumber = 0

font = pygame.font.SysFont('Arial', 30)
class Player():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 4
    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a] )and self.rect.x > 0:
            self.rect.x -= self.vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.vel
        if( keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
            self.rect.y += self.vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.rect.y -= self.vel
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        self.update()

    def fire(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        self.update()

    def update(self):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

class Button:
    def __init__(self, text, position, font, color, text_color, action, width_color):
        self.text = text
        self.position = position
        self.font = font
        self.color = color
        self.text_color = text_color
        self.action = action
        self.width_color = width_color
        self.label = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.label.get_width() + 20,
                                self.label.get_height() + 20)
        self.visible = True

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)
            pygame.draw.rect(screen, self.width_color, self.rect, width=5)
            screen.blit(self.label, (self.position[0] + 10, self.position[1] + 10))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

    def hide(self, screen):
        self.visible = False

    def show(self, screen):
        self.visible = True

def start_game():
    global screen
    screen = 'game'

game_start_btn = Button("Start game", (173, 170), font, (107, 128, 115), (0, 0, 0), start_game, (255, 255, 255))

buttons_menu = [game_start_btn]

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])
def redrawWindow(window, player, player2):
    window.fill((255, 255, 255))
    player.draw(window)
    player2.draw(window)
    pygame.display.update()

screen = "menu"

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(350, 600, 100, 100, (0, 0, 255))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        if screen == "menu":
            for button in buttons_menu:
                button.draw(window)
        if screen == "game":
            p2Pos = read_pos(n.send(make_pos((p.rect.x, p.rect.y))))
            p2.rect.x = p2Pos[0]
            p2.rect.y = p2Pos[1]
            p2.update()
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if screen == 'menu':
                    for button in buttons_menu:
                        if button.is_clicked(mouse_pos):
                            button.action()
                
        p.move()
        redrawWindow(window, p, p2)

main()