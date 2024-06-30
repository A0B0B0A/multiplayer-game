import pygame
from network import Network

WIDTH, HEIGHT = 800, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game(Client)")

clientNumber = 0
fire_png = pygame.image.load('patron.png')
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


def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(350, 600, 100, 100, (0, 0, 255))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2Pos = read_pos(n.send(make_pos((p.rect.x, p.rect.y))))
        p2.rect.x = p2Pos[0]
        p2.rect.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

        p.move()
        redrawWindow(window, p, p2)

main()