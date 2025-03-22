import pygame
import random
import sys


clock = pygame.time.Clock()   # Ticks


pygame.init()
WINDOW_WIDTH=760
WINDOW_HEIGHT=381
screen=pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))   #Screen program
pygame.display.set_caption("Name")   #name program
pygame.display.set_icon(pygame.image.load('image/icon.png'))#-картинка програми




#Player:

player_speed = 5
player_x = 300
player_y = 300


#Jump:

is_jump = False
jump_count = 8




#Animation:

walk_right = [pygame.image.load('image/5.png').convert_alpha(),
              pygame.image.load('image/6.png').convert_alpha(),
              pygame.image.load('image/7.png').convert_alpha(),
              pygame.image.load('image/8.png').convert_alpha()]
walk_left = [pygame.image.load('image/1.png').convert_alpha(),
             pygame.image.load('image/2.png').convert_alpha(),
             pygame.image.load('image/3.png').convert_alpha(),
             pygame.image.load('image/4.png').convert_alpha()]
player_stay_left=[pygame.image.load('image/1.png').convert_alpha()]
player_stay_right=[pygame.image.load('image/5.png').convert_alpha()]

player_animation_count_right=0
player_animation_count_left=0
player_stay_left_count= 0
player_stay_right_count= 0

#Back graund:

back_graund = pygame.image.load('image/bg.png').convert()
back_graund_rect = back_graund.get_rect()
back_graund_x = 0
back_graund_speed=5



#Text:

myfont = pygame.font.Font('Font\Roboto-Black.ttf', 50)
lose_text = myfont.render('You lose',False, (193,196,199))
restart_text = myfont.render('Restart game',False, (115,132,148))
restart_text_rect = restart_text.get_rect(topleft=(250,200))

#Mobs:

mob = pygame.image.load('image/mob.png').convert_alpha()
mob_list = []

gameplay = True

mob_timer = pygame.USEREVENT +1
pygame.time.set_timer(mob_timer,random.randint(5000,10000))


#Bullets:

bullets_count = 10
bullet = pygame.image.load('image/bullet_right.png').convert_alpha()
bullets = []


#Musik:

bg_sound = pygame.mixer.Sound('sounds/bg_sounds.mp3')
bg_sound.play()


while True:
    
    #Screen
            
    screen.blit(back_graund,(back_graund_x,0))
    screen.blit(back_graund,(back_graund_x+760,0))
    screen.blit(back_graund,(back_graund_x-760,0))
    
    if gameplay:

        #Animation walk:
        
        keys = pygame.key.get_pressed()
        
        player_rect = walk_left[0].get_rect(topleft=(player_x,player_y))


        if keys[pygame.K_a]:
            screen.blit(walk_left[player_animation_count_left],(player_x,player_y))
            back_graund_x +=5
            
            
        elif keys[pygame.K_d] :
            screen.blit(walk_right[player_animation_count_right],(player_x,player_y))
            back_graund_x -=5
            
        else:
            screen.blit(player_stay_right[player_stay_right_count],(player_x,player_y))

        if  back_graund_x == 760 or back_graund_x == -760:
            back_graund_x=0
        
       # else :
           # screen.blit(walk_right[player_animation_count_right],(player_x,player_y))

        


           
        
                #тут має бути стоячий персонаж замість руху в право
                
        if player_animation_count_left ==3:
            player_animation_count_left =0
        else:
            player_animation_count_left+=1    
        if player_animation_count_right==3:
            player_animation_count_right=0
        else:
            player_animation_count_right+=1
        #обмеження в висоті і ширені        
        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
        elif keys[pygame.K_d] and player_x < 760:
            player_x += player_speed
        elif keys[pygame.K_SPACE]and player_y<780:
            is_jump = True

        #Jamp
                                                
        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True

                    
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

        #Mob
        if mob_list:
            for (i,el) in enumerate (mob_list):
                screen.blit(mob,el)
                el.x -=10

                if el.x <-100:
                    mob_list.pop(i)
                
            if player_rect.colliderect(el):
                gameplay = False
                
        #Bullets
        if bullets:
            for (i,el) in enumerate(bullets):
                screen.blit(bullet,(el.x, el.y))
                el.x += 30
                if el.x >1050:
                    bullets.pop(i)

                if mob_list:
                    for (index, mobs) in enumerate(mob_list):
                        if el.colliderect(mobs):
                            mob_list.pop(index)
                            bullets.pop(i)
        

        #windov lose
    else:
        screen.fill((87,88,89))
        screen.blit(lose_text,(300, 150))
        screen.blit(restart_text, restart_text_rect)

        mouse  = pygame.mouse.get_pos()
        if restart_text_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 300
            mob_list.clear()
            bullets.clear()
            bullets_count=10    
        
    pygame.display.update()# Update display
    #Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        #Bullets
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_e and bullets_count > 0:
            bullets.append(bullet.get_rect(topleft=(player_x+10,player_y+10)))
            bullets_count -=1
        #Mob
        if event.type == mob_timer:
            mob_list.append(mob.get_rect(topleft=(800,300)))
                
    #back_graund_rect.centerx -= back_graund_speed * (player_x - WINDOW_WIDTH // 3) / WINDOW_WIDTH*2
    #back_graund_rect.centery -= back_graund_speed * (player_y - WINDOW_HEIGHT //2) / WINDOW_HEIGHT*1
    
               
    clock.tick(60)#-FPS
    
