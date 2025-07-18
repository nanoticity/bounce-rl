import pygame, random
import agent
import asyncio
pygame.init()

SIZE = [800, 800]
WHITE = (255, 255, 255)
AQUA = (3, 187, 133)
TEXT_COLOR = (255, 255, 255)
R, G, B = (255, 255, 255)

screen = pygame.display.set_mode(SIZE)

def text(text, textx, texty, size, r, g, b):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, (r, g, b))
    textpos = text.get_rect(x = textx, y = texty)
    screen.blit(text, textpos) 

pygame.display.set_caption("Bounce!")

t0 = pygame.time.get_ticks()
async def run():
    hit = False
    fps = 10000
    paddle_length = 250
    streak = 0
    num = 1
    scored = False
    streaks = [0]
    ballx = 300
    bally = 500
    ballx_add = random.choice([-3, 3])
    grav = 0
    paddle1_startx = 330
    paddle1_starty = 770
    a = agent.Agent()
    run = True
    while run:
        try:
            high_score = max(streaks)
        except:
            high_score = streak
        if high_score < streak:
            high_score = streak
        
        paddle1_endx = paddle1_startx + paddle_length
        paddle1_endy = paddle1_starty
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
                
        screen.fill(AQUA)
        
        pygame.draw.circle(screen, (255, 255, 255), (ballx, bally), 33, 10)
        text("STREAK: " + str(streak) + "   HIGHSCORE: " + str(high_score), 100, 100, 50, R, G, B)
        
        pygame.draw.line(screen, WHITE, (paddle1_startx, paddle1_starty), (paddle1_endx, paddle1_endy), 20)
            
        pygame.display.flip()
            
        bally += grav
        ballx += ballx_add
        
        if bally <= 730:
            hit = False
            scored = False
        
        if ballx >= paddle1_startx and ballx <= paddle1_endx and bally >= 740 and bally <= 800:
            if not hit:
                grav *= -1
                hit = True
                # ballx_add = random.randint(-15, 15)
                # ballx_add = random.choice([-3, 3])
                num = 1
            if not scored:
                streak += num
                scored = True
        elif bally >= 1100:
            streaks.append(streak)
            a.score_sources.append(a.expore_or_exploit == 0)
            a.update_Q(ballx, bally, paddle1_startx, action, hit, ballx_add, streaks[-1])
            streak = 0
            paddle_length = 250 
            old_ballx = ballx
            ballx = old_ballx
            if ballx < 33:
                ballx = 33
            elif ballx > 767:
                ballx = 767
            old_ballx_add = ballx_add
            ballx_add = old_ballx_add
            old_paddle1_startx = paddle1_startx
            paddle1_startx = old_paddle1_startx
            bally = 500
            grav = 0
            a.game_count += 1
            print(a.alpha)
            if random.uniform(0, 1) < a.epsilon:
                a.expore_or_exploit = 1
                print("explore")
                fps = 10000
            else:
                a.expore_or_exploit = 0
                print("exploit")
                fps = 60

        elif ballx >= 770:
            ballx_add *= -1
        elif ballx <= 30:
            ballx_add *= -1
        elif bally <= 30:
            grav *= -1
        else:
            grav = min(grav + 0.5, 15)
        if paddle1_startx <= 0:
            paddle1_startx = 0
        elif (paddle1_startx + paddle_length) >= 800:
            paddle1_startx = 800 - paddle_length
            
        if bally <= 0:
            paddle_length = 250
            paddle1_startx = 330
            ballx = 300
            bally = 500
            ballx_add = 3
            grav = 0
        
        action = a.get_action(ballx, ballx_add, paddle1_startx)
        if action == 0:  # Move left
            paddle1_startx -= 20
        elif action == 1:  # Move right
            paddle1_startx += 20
        
        a.update_Q(ballx, bally, paddle1_startx, action, hit, ballx_add, streaks[-1])
        
        await asyncio.sleep(1/fps)
    
if __name__ == "__main__":
    asyncio.run(run())