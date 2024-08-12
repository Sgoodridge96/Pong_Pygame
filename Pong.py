import pygame
import random               

pygame.init()
winning_score = 5

class PlayerRectangle:
    def __init__(self, x, y, width, height, color, speed):
        #initialize variables
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed

    def move(self, keys, screen_height):
        #set keys to player movement
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < screen_height - self.height:
            self.y += self.speed
    
    def ai_move(self, ball, screen_height):
        # AI anticipates where the ball is heading
        ai_center = self.y + self.height // 2

        # Adjust speed based on distance to the ball
        if abs(ball.y - ai_center) > self.height // 4:
            if ball.y > ai_center:
                self.y += min(self.speed, abs(ball.y - ai_center))
            elif ball.y < ai_center:
                self.y -= min(self.speed, abs(ball.y - ai_center))

        # Ensure the AI paddle stays within screen bounds
        if self.y < 0:
            self.y = 0
        if self.y > screen_height - self.height:
            self.y = screen_height - self.height

            

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def reset(self):
        #reset player
        self.x = self.spawn_x
        self.y = self.spawn_y
        

class PongBall:
    def __init__(self, x, y, radius, color, speed):
        #initialize variables
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = list(speed)

    def move(self):
        #move ball
        self.x += self.speed[0]
        self.y += self.speed[1]

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
    
    def reset(self):
        #reset the ball
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.speed = initialBallDirection()
        

    def checkWallCollision(self, screen_height):
        #Check upper and lower wall collisions
        if self.y < 0 + self.radius or self.y > screen_height - self.radius:
            self.speed[1] *= -1


    def checkPlayerCollision(self, player_rect, ai_rect):

        # Check collision with the front of the player  
        if self.x - self.radius <= player_rect.x + player_rect.width and self.x > player_rect.x:
            if self.y >= player_rect.y and self.y <= player_rect.y + player_rect.height:
                self.speed[0] *= -1
                self.x = player_rect.x + player_rect.width + self.radius  #Move ball to front of player to prevent the ball from sticking 
                player_updated_speed = []
                for i in self.speed:
                    player_updated_speed.append(i * 1.1)
                self.speed = player_updated_speed

        # Check collision with the top or bottom with the player
        if self.x >= player_rect.x and self.x <= player_rect.x + player_rect.width:
            if self.y - self.radius <= player_rect.y + player_rect.height and self.y > player_rect.y:
                self.speed[1] *= -1
                self.y = player_rect.y + player_rect.height + self.radius  
            elif self.y + self.radius >= player_rect.y and self.y < player_rect.y + player_rect.height:
                self.speed[1] *= -1
                self.y = player_rect.y - self.radius  

        # Check collision with the front of the AI
        if self.x + self.radius >= ai_rect.x and self.x < ai_rect.x + ai_rect.width:
            if self.y >= ai_rect.y and self.y <= ai_rect.y + ai_rect.height:
                self.speed[0] *= -1
                self.x = ai_rect.x - self.radius
                ai_updated_speed = []
                for i in self.speed:
                    ai_updated_speed.append(i * 1.1)
                self.speed = ai_updated_speed

        # Check collision with the top or bottom of the AI
        if self.x >= ai_rect.x and self.x <= ai_rect.x + ai_rect.width:
            if self.y - self.radius <= ai_rect.y + ai_rect.height and self.y > ai_rect.y:
                self.speed[1] *= -1
                self.y = ai_rect.y + ai_rect.height + self.radius  
            elif self.y + self.radius >= ai_rect.y and self.y < ai_rect.y + ai_rect.height:
                self.speed[1] *= -1
                self.y = ai_rect.y - self.radius  

    #Update score and reset the ball
    def score(self, screen_width, player_score, ai_score, player_rect, ai_rect):
        if self.x > screen_width - self.radius:
            
            self.reset()
            player_rect.reset()
            ai_rect.reset()
            player_score += 1
            if player_score >= winning_score:
                return player_score, ai_score, True
            pygame.time.delay(500)
            
        if self.x < 0 + self.radius:
            
            self.reset()
            player_rect.reset()
            ai_rect.reset()
            ai_score += 1
            if ai_score >= winning_score:
                return player_score, ai_score, True
            pygame.time.delay(500)
            
        return player_score, ai_score, False
       

def initialBallDirection(): 
    random.seed()
    x_direction = random.choice([-1, 1])
    y_direction = random.choice([-1, 1])
    speed = [x_direction * random.randint(2, 3), y_direction * random.randint(2, 4)]
    return speed


def main():
    
    # Define screen dimensions
    screen_width = 800
    screen_height = 600

    # Define the width and height of player rectangle
    rect_width = 25
    rect_height = 80

    #Define PongBall
    pongBall_radius = 10
    pongBall_speed = initialBallDirection()
    
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

    #define gameover
    game_over = False
    
    #Setup and start Pong game
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Pong")

    # Spawn Objects
    player_rect = PlayerRectangle((screen_width - rect_width) // 16, (screen_height - rect_height) // 2, rect_width, rect_height, actorColor, 5)
    ai_rect = PlayerRectangle((screen_width - rect_width) // 1.07, (screen_height - rect_height) // 2, rect_width, rect_height, actorColor, 5)
    pong_ball = PongBall((screen_width - pongBall_radius) // 2, (screen_height - pongBall_radius) // 2, pongBall_radius, actorColor, pongBall_speed)


    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not game_over:

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
            player_rect.move(keys, screen_height)
            ai_rect.ai_move(pong_ball, screen_height)

            #Fill screen and draw objects
            screen.fill(background)
            player_rect.draw(screen)
            ai_rect.draw(screen)
            pong_ball.draw(screen)

            pong_ball.checkWallCollision(screen_height)
            pong_ball.checkPlayerCollision(player_rect, ai_rect)
            (player_score, ai_score, game_over) = pong_ball.score(screen_width, player_score, ai_score, player_rect, ai_rect)
            pong_ball.move()

            if current_timer <= 0:
                game_over = True

        if game_over or current_timer <= 0:
            game_over_text = pygame.font.SysFont(None, 50).render("Game Over", True, (230, 255, 255))
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - game_over_text.get_height() // 2))   

        #render timer to screen
        screen.blit(render_timer, timer_pos)
        screen.blit(render_player_ui, player_score_pos)
        screen.blit(render_ai_ui, ai_score_pos)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
        #If timer hits 0, close game (Fix later with game over screen)

    pygame.quit()

main()
