import pygame, random, pygame.freetype, asyncio
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

async def main():
    pygame.display.set_caption("Bounce!")
    paddle_length = 250

    streak = 0
    num = 1

    grav_plus = 0.5
    
    hacks = False
    hacks3 = False
    hacks4 = False
    scored = False

    streaks = []

    ballx = 300
    bally = 500
    ballx_add = 3
    grav = 0

    paddle1_startx = 330
    paddle1_starty = 770

    t0 = pygame.time.get_ticks()

    filling = False
    crazy = False
    obs = False
    glitch = False
    crazy2 = False
    title = True
    run = False
    hit = False
    while title:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                title = False
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    title = False
                    run = True
        screen.fill(AQUA)
        text("Bounce! By Nano", 115, 100, 100, 255, 255, 255)
        text("Click anywhere on the screen to play.", 90, 200, 50, 255, 255, 255)
        text("Made with Pygame and Pyodide", 240, 300, 30, 255, 255, 255)
        text("Repo: https://github.com/nanoticity/snake", 190, 350, 30, 255, 255, 255)
        text("PC: left or right arrow keys, a and d", 215, 450, 30, 255, 255, 255)
        text("Mobile: click on the left of the screen to go left", 160, 500, 30, 255, 255, 255)
        text("and click on the right side to go right", 205, 550, 30, 255, 255, 255)
        text("For High Seas 2024-2025, reused for SOM 2025", 275, 750, 30, 255, 255, 255)
        pygame.display.update()
        await asyncio.sleep(0.02)

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
            elif filling:
                screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
                
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    filling = not filling
                elif e.key == pygame.K_x:
                    crazy = not crazy
                elif e.key == pygame.K_v:
                    glitch = not glitch
                elif e.key == pygame.K_h:
                    hacks = not hacks
                elif e.key == pygame.K_r:
                    paddle_length = 250
                    grav_plus = 0.5
                    ballx = 300
                    bally = 500
                    ballx_add = 3
                    grav = 0
                elif e.key == pygame.K_b:
                    obs = not obs
                elif e.key == pygame.K_n:
                    crazy2 = not crazy2
                elif e.key == pygame.K_q:
                    hacks3 = not hacks3
                elif e.key == pygame.K_p:
                    hacks4 = not hacks4
        if not filling:
            screen.fill(AQUA)
        
        if crazy:
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        pygame.draw.circle(screen, (255, 255, 255), (ballx, bally), 33, 10)
        text("STREAK: " + str(streak) + "   HIGHSCORE: " + str(high_score), 100, 100, 50, R, G, B)
        
        if obs:
            ballx += random.randint(-50, 50)
            bally += random.randint(-50, 50)
        
        if glitch:
            pygame.time.wait(100)
        
        pygame.draw.line(screen, WHITE, (paddle1_startx, paddle1_starty), (paddle1_endx, paddle1_endy), 20)
        keys = pygame.key.get_pressed()
            
        pygame.display.flip()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            paddle1_startx -= 20
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            paddle1_startx += 20
            
        bally += grav
        ballx += ballx_add
        
        if bally <= 730:
            hit = False
            scored = False
        
        if pygame.mouse.get_pressed()[0]:
            if pygame.mouse.get_pos()[0] >= 400:
                paddle1_startx += 20
            elif pygame.mouse.get_pos()[0]< 400:
                paddle1_startx -= 20
        
        if ballx >= paddle1_startx and ballx <= paddle1_endx and bally >= 740 and bally <= 800:
            if not hit:
                grav *= -1
                hit = True
            if crazy2:
                flash = random.choice([True, False])
                direction = random.randint(1, 2)
                if direction == 1:
                    ballx_add = -50
                elif direction == 2:
                    ballx_add = 50
                num = 3
                flash = random.randint(1, 2)
                if flash == 1:
                    screen.fill((255, 0, 0))
                    pygame.display.flip()
                    pygame.time.wait(500)
            if not crazy2:
                if not hacks3:
                    ballx_add = random.randint(-15, 15)
                else:
                    ballx_add = 0
                num = 1
            if not scored:
                streak += num
                scored = True
            if grav_plus < 0.9:
                grav_plus = 0.5 + streak/100
            if not hacks4 and paddle_length >= 100:
                paddle_length -= 2
        elif bally >= 1100:
            streaks.append(streak)
            grav_plus = 0.5
            streak = 0
            paddle_length = 250 
            ballx = 300
            bally = 500
            ballx_add = 3
            grav = 0
            pygame.time.wait(500)
        elif ballx >= 770:
            ballx_add *= -1
        elif ballx <= 30:
            ballx_add *= -1
        elif bally <= 30:
            grav *= -1
        else:
            grav += grav_plus
        
        if paddle1_startx <= 0:
            paddle1_startx = 0
        elif (paddle1_startx + paddle_length) >= 800:
            paddle1_startx = 800 - paddle_length
            
        if bally <= 0:
            paddle_length = 250
            ballx = 300
            bally = 500
            ballx_add = 3
            grav = 0
        
        if hacks:
            paddle1_startx = ballx - (paddle_length / 2)
        
        await asyncio.sleep(0.016)
        
if __name__ == "__main__":
    asyncio.run(main())