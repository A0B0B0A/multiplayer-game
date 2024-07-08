import pygame
from network import Network
import json

WIDTH, HEIGHT = 800, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Multiplayer Game(Client)")

clientNumber = 0

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
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
            self.rect.x -= self.vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < WIDTH:
            self.rect.x += self.vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.bottom < HEIGHT:
            self.rect.y += self.vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
            self.rect.y -= self.vel
        self.update()

    def update(self):
        self.rect = pygame.Rect(self.rect.x, self.rect.y, self.width, self.height)

class Bullet():
    def __init__(self, x, y, width, height, color, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 5 * direction

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        self.rect.x += self.vel

def read_pos(str):
    try:
        str = str.split(",")
        return int(str[0]), int(str[1])
    except Exception as e:
        print(f"Error reading position: {str} -> {e}")
        return 0, 0

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def redrawWindow(window, player, player2, bullets, bullets2):
    window.fill((255, 255, 255))
    player.draw(window)
    player2.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    for bullet in bullets2:
        bullet.draw(window)
    pygame.display.update()

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    print(f"Initial position: {startPos}")  # Debugging line
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(350, 600, 100, 100, (0, 0, 255))
    clock = pygame.time.Clock()
    bullets = []
    bullets2 = []
    cooldown = 0

    while run:
        clock.tick(60)
        try:
            pos_data = n.send(make_pos((p.rect.x, p.rect.y)))
            if pos_data is None:
                print("Failed to get data from server.")
                continue

            p2Pos = read_pos(pos_data)
            print(f"Player 2 position: {p2Pos}")
            p2.rect.x = p2Pos[0]
            p2.rect.y = p2Pos[1]
            p2.update()
        except Exception as e:
            print(f"Error processing player 2 position data: {e}")
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cooldown == 0:
                    bullet = Bullet(p.rect.x + p.width // 2, p.rect.y + p.height // 2, 10, 5, (0, 0, 0), 1)
                    bullets.append(bullet)
                    cooldown = 60 // 6

        for bullet in bullets[:]:
            bullet.move()
            if bullet.x > WIDTH or bullet.x < 0:
                bullets.remove(bullet)
            if bullet.rect.colliderect(p2.rect):
                print("Player 2 hit!")
                run = False

        for bullet in bullets2[:]:
            bullet.move()
            if bullet.x > WIDTH or bullet.x < 0:
                bullets2.remove(bullet)
            if bullet.rect.colliderect(p.rect):
                print("Player 1 hit!")
                run = False

        p.move()

        if cooldown > 0:
            cooldown -= 1

        data = {"player": (p.rect.x, p.rect.y), "bullets": [(bullet.x, bullet.y) for bullet in bullets]}
        try:
            reply = n.send(json.dumps(data))
            if reply is None:
                print("Failed to get response from server.")
                continue

            reply_data = json.loads(reply)
            print(f"Reply: {reply_data}")
            p2.rect.x, p2.rect.y = reply_data["player"]
            bullets2 = [Bullet(bx, by, 10, 5, (255, 0, 0), -1) for bx, by in reply_data["bullets"]]
        except Exception as e:
            print(f"Error processing server reply: {e}")
            continue

        redrawWindow(window, p, p2, bullets, bullets2)

if __name__ == "__main__":
    main()

