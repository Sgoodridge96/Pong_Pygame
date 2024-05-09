import pygame
import random

# NEXT UPDATE: COLLISIONS FOR PLAYER WITH PONG BALL
#              Adding an AI player to play against

pygame.init()

class PlayerRectangle:
    def __init__(self, x, y, width, height, color, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self, keys, screen_height):
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.height:
            self.y += self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class PongBall:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = list(speed)

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def checkCollisions(self, screen_height, screen_width):
        if self.y < 0 or self.y > screen_height:
            self.speed[1] *= -1
        if self.x < 0 or self.x > screen_width:
            self.speed[0] *= -1


def ballDirection():
    #Randomly pick a ball direction and speed at the start of the game.  
    random.seed()
    ball_direction_x = random.randint(-3,3)
    ball_direction_y = random.randint(-3,3)

    #Make sure the ball can't go straight up and down or left to right.  
    if ball_direction_x == 0:
        ball_direction_x += 1
    if ball_direction_y == 0:
        ball_direction_y += 1
    
    print(ball_direction_y)
    return ball_direction_x, ball_direction_y



def main():

    ## Game Definitions ##
    ####################################################################################################

    # Set up the screen dimensions
    screen_width = 800
    screen_height = 600

    # Define the width and height of the rectangle
    rect_width = 25
    rect_height = 80

    #Define PongBall
    pongBall_radius = 10
    pongBall_speed = ballDirection()

    #pygame uses milliseconds, set 6000 milliseconds to convert to 60 seconds later
    clock = pygame.time.Clock()
    clock_timer = 6000

    # Define colors
    background = (0, 0, 0)
    actorColor = (230, 255, 255)

    ####################################################################################################

    #Setup and start Pong game

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    # Spawn Rectangle (position, size, color, speed)
    playerRect = PlayerRectangle((screen_width - rect_width) // 16, (screen_height - rect_height) // 2, rect_width, rect_height, actorColor, 5)
    pongBall = PongBall((screen_width - pongBall_radius) // 2, (screen_height - pongBall_radius) // 2, pongBall_radius, actorColor, pongBall_speed)

    running = True

    while running:
        
        clock_timer -= 1
        if clock_timer <= 0:
            running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Render clock and turn off game when it hits zero
        print(screen_width, screen_height)
        timer_text = pygame.font.SysFont(None, 36)
        render_timer = timer_text.render("Time: " + str(clock_timer // 1000), True, (230, 255, 255))

        keys = pygame.key.get_pressed()
        playerRect.move(keys, screen_height)

        screen.fill(background)
        playerRect.draw(screen)
        pongBall.checkCollisions(screen_height, screen_width)
        pongBall.move()
        pongBall.draw(screen)

        
        screen.blit(render_timer, (350, 25))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
main()
