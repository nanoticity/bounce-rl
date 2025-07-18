import pygame, random
import pickle
import asyncio
pygame.init()

SIZE = [800, 800]
WHITE = (255, 255, 255)
AQUA = (3, 187, 133)
TEXT_COLOR = (255, 255, 255)
R, G, B = (255, 255, 255)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()

def text(text, textx, texty, size, r, g, b):
    font = pygame.font.Font(None, size)
    text = font.render(text, True, (r, g, b))
    textpos = text.get_rect(x = textx, y = texty)
    screen.blit(text, textpos) 
    pygame.display.set_caption("Bounce!")
    
    
    
def save_object(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Object saved to {filename}") 
    
def load_object(filename):
    with open(filename, 'rb') as f:
        obj = pickle.load(f)
    print(f"Object loaded from {filename}")
    return obj
    
async def run():
    paddle_length = 250

    streak = 0
    num = 1

    a = load_object('/lib/python3.12/site-packages/trained/docs/trained-python/agent.pkl')

    fps = 60

    scored = False

    streaks = [0]

    ballx = 494
    bally = 500
    ballx_add = random.choice([-3, 3])
    grav = 0
    explore_or_exploit = 0

    x_start = 300

    paddle1_startx = 330
    paddle1_starty = 770

    t0 = pygame.time.get_ticks()
    run = True
    hit = False

    while run:
        t1 = pygame.time.get_ticks()
        time = (t1 - t0) / 1000
        try:
            high_score = max(streaks)
        except:
            high_score = streak
        if high_score < streak:
            high_score = streak
        
        paddle1_endx = paddle1_startx + paddle_length
        paddle1_endy = paddle1_starty
        time = str(int(pygame.time.get_ticks() / 1000))
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    save_object(a, 'agent.pkl')
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
            print(ballx)
            
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
        
        # a.update_Q(ballx, bally, paddle1_startx, action, hit, ballx_add, streaks[-1])
        
        await asyncio.sleep(0.0166666666666667)  # 60 FPS
        
    pygame.quit()