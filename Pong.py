import pygame
import random

# NEXT UPDATE: Fix collisions with top of the player rectangle.
               #Add scoring points

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

    def checkWallCollision(self, screen_height, screen_width, radius):
        #Check wall collisions
        if self.y < 0 + radius or self.y > screen_height - radius:
            self.speed[1] *= -1
        if self.x < 0 + radius or self.x > screen_width - radius:
            self.speed[0] *= -1
    
    def checkPlayerCollision(self, playerRect):
        
        player_object = pygame.Rect(playerRect.x, playerRect.y, playerRect.width, playerRect.height)
        pongball_object = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2) 
        
        if pongball_object.colliderect(player_object):
            # Check if the ball hits the front of the player
            if pongball_object.right >= player_object.left:  
                self.speed[0] *= -1

def ballDirection():
    #Randomly pick a ball direction and speed at the start of the game.  
    random.seed()
    starting_speeds = [-2, 2]
    ball_direction_x = random.choice(starting_speeds)
    ball_direction_y = random.choice(starting_speeds)
    
    return ball_direction_x, ball_direction_y

def main():
    
    # Define screen dimensions
    screen_width = 800
    screen_height = 600

    # Define the width and height of player rectangle
    rect_width = 25
    rect_height = 80

    #Define PongBall
    pongBall_radius = 10
    pongBall_speed = ballDirection()
    
    #Define Starting timer
    timer_pos = (screen_width // 2 - 100, screen_height // 32)
    starting_timer = 120

    #Define starting score
    player_score_pos = (screen_width // 32, screen_height // 32)
    ai_score_pos = (screen_width // 1.2, screen_height // 32)
    player_score = 0
    ai_score = 0

    # Define colors
    background = (0, 0, 0)
    actorColor = (230, 255, 255)
    
    #Setup and start Pong game
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    # Spawn Objects
    playerRect = PlayerRectangle((screen_width - rect_width) // 16, (screen_height - rect_height) // 2, rect_width, rect_height, actorColor, 5)
    pongBall = PongBall((screen_width - pongBall_radius) // 2, (screen_height - pongBall_radius) // 2, pongBall_radius, actorColor, pongBall_speed)


    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Logic to countdown timer ("// 1000" for milliseconds to seconds)
        clock_timer = pygame.time.get_ticks()
        current_timer = starting_timer - clock_timer // 1000
        
        #Render clock and exit game when it hits zero
        timer_text = pygame.font.SysFont(None, 36)
        render_timer = timer_text.render("Time: " + str(current_timer) + " seconds", True, (230, 255, 255))

        #Render scoreboard for both players
        player_ui = pygame.font.SysFont(None, 36)
        ai_ui = pygame.font.SysFont(None, 36)

        render_player_ui = player_ui.render("Score: " + str(player_score), True, (230, 255, 255))
        render_ai_ui = ai_ui.render("Score: " + str(ai_score), True, (230, 255, 255))

        #Player movement
        keys = pygame.key.get_pressed()
        playerRect.move(keys, screen_height)

        #Fill screen and draw objects
        screen.fill(background)
        playerRect.draw(screen)
        pongBall.draw(screen)

        pongBall.checkWallCollision(screen_height, screen_width, pongBall_radius)
        pongBall.checkPlayerCollision(playerRect)
        pongBall.move()       

        #render timer to screen
        screen.blit(render_timer, timer_pos)
        screen.blit(render_player_ui, player_score_pos)
        screen.blit(render_ai_ui, ai_score_pos)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
        #If timer hits 0, close game (Fix later with game over screen)
        if current_timer <= 0:
            running = False

    pygame.quit()
main()
