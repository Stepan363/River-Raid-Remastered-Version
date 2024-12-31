'''
Notes: Image resizer:
https://the-image-editor.com/image/download/cmVzaXplX2ltYWdl

'''
#Minus is up, positive is down.
#
#screen fading code
#https://www.youtube.com/watch?v=H2r2N7D56Uw&ab_channel=TechWithTim
import pygame
pygame.font.init()



from random import randint
import pgzrun
pygame.init()
import sys
import pygame as pg

pg.init()
import time
#essentials to start the game.
start_ticks=pygame.time.get_ticks() #starter tick

print(pygame.font.get_fonts())
#getting system's screen resolution, making it full-screen
screen = pygame.display.set_mode()
width, height = screen.get_size()

SCREEN_WIDTH = width
SCREEN_HEIGHT =  height
pygame.display.toggle_fullscreen()

#changing game-name, River Raid 

pygame.display.set_caption("River Raid Remastered Version")


#Colour RGB's for game.
BG = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


#For main-menu, not needed now.
pygame.mouse.set_visible(False)

#creating plane, collision configuration and postition of aircraft.
plane_bullet = pygame.image.load("images/planes_bullet.png").convert_alpha()
planebullet_mask = pygame.mask.from_surface(plane_bullet)
planebullet_rect = plane_bullet.get_rect()




plane = pygame.image.load("images/planne.png").convert_alpha()
plane_mask = pygame.mask.from_surface(plane)
#load image, electric gates.



# airplane bbox
plane_rect = plane.get_rect()
plane_rect.x = width/2
plane_rect.y = height/1.2
math = width/1000
math_height = height/1080
#creating map_for_collision, also positioning the map
map_lvl_2 = pygame.image.load("images/Level-2.png").convert_alpha()
map_lvl_2 = pg.transform.scale(map_lvl_2, ((math*1000)+4, 50000))
map2_mask = pygame.mask.from_surface(map_lvl_2)
map_rect2 = map_lvl_2.get_rect()
map_rect2.y = -110000

map = pygame.image.load("images/Level-1_test.png").convert_alpha()
math = width/1000
math_height = height/1080
map = pg.transform.scale(map, ((math*1000)+4, 50000))
map_mask = pygame.mask.from_surface(map)

# map rendering coords
map_rect = map.get_rect()
map_rect.y = -50000


#position plane rectangle
#plane_rect.topleft = (350, 250)
#loading turret assets, adding them into the game.
turret = pygame.image.load("images/turret.png").convert_alpha()
img_size = (128, 128)
turret = pygame.transform.scale(turret, img_size)
turret_mask = pygame.mask.from_surface(turret)
turret_rect = turret.get_rect()

#turret_rect.x = 360*math
#turret_rect.y = -1500

#turret's bullet import images and stuff.
turret_bul = pygame.image.load("images/turret_bullet.png").convert_alpha()
turret_bul = pygame.transform.scale(turret_bul, img_size)
turretbul_mask = pygame.mask.from_surface(turret_bul)
turretbul_rect = turret_bul.get_rect()

turretbul_rect.x = -9999

game_speed = 3
looped_times = -2

time_elapsed=pygame.time.get_ticks()
level_one_positions_x = [200*math, 360*math, 520*math, 680*math, 840*math, 1000*math, 1160*math]
level_one_positions_y = [-1000, -1500,-2000,-2500,-3000,-3500,-4000]
turret_rect.x = level_one_positions_x[0]
turret_rect.y = level_one_positions_y[0]
def fade(width, height): 
    fade = pygame.Surface((width, height))
    fade.fill((0,0,0))
    for alpha in range(0, 50):
        
        fade.set_alpha(alpha)
        #redrawWindow()
        screen.blit(fade, (0,0))
        pygame.display.update()
        time.sleep(0.05)
seconds_when_shot = 0
ticks_passed=pygame.time.get_ticks()
def plane_shoot_command():
        global ticks_passed, seconds_when_shot
        seconds_when_shot=(pygame.time.get_ticks()-ticks_passed)/1000
        

        if seconds_when_shot < 0.5:
            planebullet_rect.y = planebullet_rect.y  - 20
        else:
            ticks_passed=pygame.time.get_ticks()
            planebullet_rect.x = -9999
        
        
        

the_chosen_one = -1
picked_coordinates = 0
def turret_animation():
    global turret, turret_rect, turret_mask, time_elapsed, picked_coordinates, level_one_positions_x, level_one_positions_y, the_math, the_math_2, the_chosen_one
    if turret_mask.overlap(planebullet_mask, (planebullet_rect.x - turret_rect.x, planebullet_rect.y - turret_rect.y)):
        picked_coordinates = picked_coordinates + 1
        if the_chosen_one == 0:
            turret_rect.y = level_one_positions_y[picked_coordinates] - the_math
        elif the_chosen_one == 1:
            turret_rect.y = level_one_positions_y[picked_coordinates] - the_math_2
        turret_rect.x = level_one_positions_x[picked_coordinates]
    turretbul_rect.x = turretbul_rect.x + 4
    
    turretbul_rect.y = turret_rect.y - 8
    seconds=(pygame.time.get_ticks()-time_elapsed)/1000
    if seconds >= 1.2: 
        time_elapsed=pygame.time.get_ticks()
        turretbul_rect.x = turret_rect.x + 70
    math = width/1000
    #the locations where the turret has to be, after disappears off the screen. Coords.
    level_one_positions_x = [200*math, 362.5*math, 425*math, 20*math, 250*math, 200*math, 170*math, 10*math, 650*math, 10*math, 215*math, -99999999]
    level_one_positions_y = [-1000, -200, -200,-200,-200,-700,-1650,-850, -450,-300, -2000, -999999999]
    # turret_draw_on_screen
    #the place where they all teleport to their allocated places, after they disappear off screen.
    calculated_math_for_erase = height-(height/1.2)


    #print(picked_coordinates, turret_rect.x, turret_rect.y, plane_rect.y + calculated_math_for_erase)
    
    if turret_rect.y >= 0:
        the_chosen_one = 0
        the_math = height - turret_rect.y
    elif turret_rect.y < 0:
        the_chosen_one = 1
        the_math_2 = height + abs(turret_rect.y)
    
    #when the turret disappears out of view, move it to it's new position. 
    turret_rect.x = level_one_positions_x[picked_coordinates]
    
    if plane_rect.y+calculated_math_for_erase < turret_rect.y: 
        #turretbul_rect.x = turret_rect.x + 70
        picked_coordinates = picked_coordinates + 1
        #turretbul_rect.x = turret_rect.x + 70
        if the_chosen_one == 0:
            turret_rect.y = level_one_positions_y[picked_coordinates] - the_math
        elif the_chosen_one == 1:
            turret_rect.y = level_one_positions_y[picked_coordinates] - the_math_2
        #turretbul_rect.x = turret_rect.x + 70
        return True



    
    
    


def plane_exploded():
    global game_speed, picked_coordinates
    game_speed = 0
    picked_coordinates = 0
    turret_rect.x = level_one_positions_x[picked_coordinates]
    if the_chosen_one == 0:
        turret_rect.y = level_one_positions_y[picked_coordinates] - the_math
    elif the_chosen_one == 1:
        turret_rect.y = level_one_positions_y[picked_coordinates] - the_math_2
    pygame.display.update()
    pygame.mixer.music.load("sounds/explosion2.wav")
    pygame.mixer.music.play()
    fade(width, height)
    game_speed = 3
    map_rect.y = -50000
    #turret_rect.y = -1000
    turret_animation()
    map_rect2.y = -110000
    
    pygame.mixer.music.load("sounds/sound2.wav")
    pygame.mixer.music.play()

#game loop
def plane_crashed():
    global looped_times, plane_rect, picked_coordinates, ticks_milsec2, the_chosen_one
    #turret_rect.y = -1000
    turret_rect.x = level_one_positions_x[picked_coordinates]
    if the_chosen_one == 0:
        turret_rect.y = level_one_positions_y[picked_coordinates] - the_math
    elif the_chosen_one == 1:
        turret_rect.y = level_one_positions_y[picked_coordinates] - the_math_2
    pygame.mixer.music.load("sounds/explosion.wav")
    pygame.mixer.music.play()
    #loads images of exploded planes.
    plane1 = pygame.image.load('images/planne1_exp.png')
    plane2 = pygame.image.load('images/planne2_exp.png')
    plane3 = pygame.image.load('images/planne3_exp.png')
    plane4 = pygame.image.load('images/planne4_exp.png')
    plane5 = pygame.image.load('images/planne5_exp.png')
    picked_coordinates = 0
    #animation of planes when they explode, game freezes and only shows animations where you have crashed.
    if looped_times == 0:
        screen.blit(plane1,(plane_rect.x, plane_rect.y)) 
        
        #pygame.display.update()
        time.sleep(0.1)
        #screen.fill(BG)
        
    
    if looped_times == 1:
        screen.blit(plane2,(plane_rect.x, plane_rect.y)) 
        #pygame.display.update()
        time.sleep(0.1)
        #screen.fill(BG)
        
    
    if looped_times == 2:
        screen.blit(plane3,(plane_rect.x, plane_rect.y))
        #pygame.display.update()
        time.sleep(0.1)
        #screen.fill(BG)
        
    if looped_times == 3:
        screen.blit(plane4,(plane_rect.x, plane_rect.y)) 
        #pygame.display.update()
        time.sleep(0.1)
        #screen.fill(BG)
        
        
    #looped times 4, we finish the animations, and return the plane to it's original spot.
    if looped_times == 4:
        pygame.font.init()
        screen.blit(plane5,(plane_rect.x, plane_rect.y)) 
        #pygame.display.update()
        time.sleep(0.1)
        #screen.fill(BG)       
        fade(width, height)
        the_chosen_one = -1
        plane_rect.x = width/2
        plane_rect.y = height/1.2
        map_rect.y = -50000
        map_rect2.y = -110000
        looped_times = -1
        pygame.mixer.music.load("sounds/sound2.wav")
        pygame.mixer.music.play()
        turret_animation()

        
        
        
    if map_mask.overlap(plane_mask, (plane_rect.x - map_rect.x, plane_rect.y - map_rect.y)) or  map2_mask.overlap(plane_mask, (plane_rect.x - map_rect2.x, plane_rect.y - map_rect2.y)):
        looped_times += 1
        #print(looped_times)
        #ticks_milsec2=pygame.time.get_ticks()
        return True
    #increment looped times to show sequenced animations.
    
        
    return False


#------------------------------------------------
game_is_paused = 0
seconds = 0
seconds1 = 0
seconds2 = 0
start_ticks=pygame.time.get_ticks()
def paused_game():
    global game_is_paused, game_speed, seconds, start_ticks
    seconds=(pygame.time.get_ticks()-start_ticks)/1000
    
    
    pygame.init()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_p] and seconds >= 5:
        start_ticks=pygame.time.get_ticks()
        
        if game_is_paused == 1:
            game_is_paused = 0 
            game_speed = 3
            


        else:
            game_is_paused = 1
            
    
    if game_is_paused == 0:
        
        return False
        
    else:
        return True
    
    
    
pygame.mixer.music.load("sounds/sound2.wav")
pygame.mixer.music.play()

ticks_milsec=pygame.time.get_ticks()
ticks_milsec1=pygame.time.get_ticks()
ticks_milsec2=pygame.time.get_ticks()

moved_distance = 0
while True:
    pygame.font.init()
    my_font = pygame.font.SysFont('nanummyeongjo', 80)
    if map_rect.y < 0 and map_rect.y > -50000:
        level = 1
    elif map_rect.y > -100000 and map_rect.y <= 50000:
        level = 2
    elif map_rect.y <= -100000:
        level = 3
    text_surface = my_font.render('Level ' + str(level), False, (0, 0, 0))     
    





    turret_animation()
    # audio playing, restarts track when ended.
    seconds=(pygame.time.get_ticks()-ticks_milsec)/1000
    if seconds >= 19:
        pygame.mixer.music.load("sounds/sound2.wav")
        ticks_milsec=pygame.time.get_ticks()
        pygame.mixer.music.play()
    #collision detection, with map or one of the turrets.
    if map_mask.overlap(plane_mask, (plane_rect.x - map_rect.x, plane_rect.y - map_rect.y)):
        #print("go!")
        plane_crashed()
    elif map2_mask.overlap(plane_mask, (plane_rect.x - map_rect2.x, plane_rect.y - map_rect2.y)):
        plane_crashed()
    
    elif turretbul_mask.overlap(plane_mask, (plane_rect.x - turretbul_rect.x, plane_rect.y - turretbul_rect.y)):
        plane_exploded()
        
    else:
        if paused_game() == False:
            if turret_rect.y < -50:
                pass
            map_rect.y = map_rect.y + game_speed
            map_rect2.y = map_rect2.y + game_speed
            turret_rect.y = turret_rect.y + game_speed

            #print(game_speed)
        else:
            game_speed = 0
        moved_distance = moved_distance + game_speed
        #get mouse coordinates
        pos = pygame.mouse.get_pos()
        #print(pos[0]/math, pos[1]-moved_distance)
        #update background
        screen.fill(BG)
        
        #check collision between plane and map.
        seconds2=(pygame.time.get_ticks()-ticks_milsec2)/1000
        #draw plane and level
        screen.blit(plane, plane_rect)
        screen.blit(map, map_rect)
        screen.blit(turret, turret_rect)
        screen.blit(map_lvl_2, map_rect2)
        screen.blit(plane_bullet, planebullet_rect)
        if seconds2 < 999999999999999:
            m1 = height - 80
            m2 = width / 100
            screen.blit(text_surface, (m2,m1))

        screen.blit(turret_bul, turretbul_rect)
        #event handler from keyboard.
        keys = pygame.key.get_pressed()
        

        
        #Controls of the map, and plane    
        if paused_game() == False:
            if keys[pygame.K_RIGHT] and plane_rect.x <= 1872:
                plane_rect.x = plane_rect.x + 2
            if keys[pygame.K_LEFT] and plane_rect.x >= -8:
                plane_rect.x = plane_rect.x - 2
            if keys[pygame.K_UP] and seconds1 > 0.1:
                ticks_milsec1=pygame.time.get_ticks()
                if game_speed < 5:
                    game_speed = game_speed + 1
            if seconds_when_shot < 0.5:
                plane_shoot_command()
            if keys[pygame.K_SPACE]:
                plane_shoot_command()
                planebullet_rect.x = plane_rect.x-3
                planebullet_rect.y = plane_rect.y-40
            if keys[pygame.K_DOWN] and seconds1 > 0.1:
                ticks_milsec1=pygame.time.get_ticks()
                if game_speed > 1:
                    game_speed = game_speed - 1
            seconds1=(pygame.time.get_ticks()-ticks_milsec1)/1000
    
    for event in pygame.event.get():
        pygame.display.update()
        if event.type == pygame.QUIT:
            run = False
    #print(game_speed)
    #updates display ( Very important for making games, I always forgot. )
    
    pygame.display.flip()
    
    if turret_animation() == True:
        pass
        #turretbul_rect.x = turret_rect.x + 70
    if keys[pygame.K_q]:
        pygame.quit()