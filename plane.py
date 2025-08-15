'''
Notes: Image resizer:
https://the-image-editor.com/image/download/cmVzaXplX2ltYWdl

'''
#Minus is up, positive is down.
#3357643182965699810
#screen fading code
#https://www.youtube.com/watch?v=H2r2N7D56Uw&ab_channel=TechWithTim

#helicopterImg_array[i] = pygame.transform.flip(helicopterImg_array[i], True, False)
#flipping image code
import pygame
import random
from random import randint
import sys  
import time
import ctypes
import settings

from planebullet import *  # Importing the planebullet class
from turretclass import *  

ctypes.windll.user32.SetProcessDPIAware()
#
# # # Anywhere Before
#

pygame.init() 
pygame.mixer.init()
settings.init()

pygame.font.init()
#essentials to start the game.
start_ticks=pygame.time.get_ticks() #starter tick

#print(pygame.font.get_fonts())
#getting system's screen resolution, making it full-screen
screen = pygame.display.set_mode()
width, height = screen.get_size()

SCREEN_WIDTH = width
SCREEN_HEIGHT =  height


#changing game-name, River Raid 

pygame.display.set_caption("River Rush Remastered Version")


#Colour RGB's for game.
BG = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


#For main-menu, not needed now.
pygame.mouse.set_visible(True)

#creating plane, collision configuration and postition of aircraft.
plane_bullet = pygame.image.load("images/planes_bullet1.png").convert_alpha()
planebullet_mask = pygame.mask.from_surface(plane_bullet)
planebullet_rect = plane_bullet.get_rect()



#Helicopter-blocking
helicopter = pygame.image.load("images/helicopter.png").convert_alpha()
helicopter_rect = helicopter.get_rect()  
helicopter_rect.x = width/2
helicopter_rect.y = height/2
helicopter_mask = pygame.mask.from_surface(helicopter)

#the fuel scattered across the map so you can pick them up
fuel_collection = pygame.image.load("images/fuel.png").convert_alpha()
fuel_collection_rect = fuel_collection.get_rect()  
fuel_collection_rect.x = width/2
fuel_collection_rect.y = height/2
fuelcollection_mask = pygame.mask.from_surface(fuel_collection)

fuel_collection2 = pygame.image.load("images/fuel.png").convert_alpha()
fuel_collection_rect2 = fuel_collection2.get_rect()  
fuel_collection_rect2.x = width/2
fuel_collection_rect2.y = height/2
fuelcollection_mask2 = pygame.mask.from_surface(fuel_collection2)

fuel_collection3 = pygame.image.load("images/fuel.png").convert_alpha()
fuel_collection_rect3 = fuel_collection3.get_rect()  
fuel_collection_rect3.x = width/2
fuel_collection_rect3.y = height/2
fuelcollection_mask3 = pygame.mask.from_surface(fuel_collection3)


plane = pygame.image.load("images/planne.png").convert_alpha()
plane_mask = pygame.mask.from_surface(plane)
#load image, electric gates.

#load fuel_images
fuel_cell = pygame.image.load("images/battery_main.png").convert_alpha()
fuelcell_rect = fuel_cell.get_rect()  
fuelcell_rect.x = width/2.5
fuelcell_rect.y = height/1.15
math = width/1000
math_height = height/1080
# airplane bbox
plane_rect = plane.get_rect()   
plane_rect.x = width/2
plane_rect.y = height/1.5
math = width/1000
math_height = height/1080
#creating map_for_collision, also positioning the map
map2 = pygame.image.load("images/Level-2.png").convert_alpha()
map2 = pygame.transform.scale(map2, ((math*1000)+4, 50000))
map2_mask = pygame.mask.from_surface(map2)
map3 = pygame.image.load("images/Level-3.png").convert_alpha()
map3 = pygame.transform.scale(map3, ((math*1000)+4, 50000))
map3_mask = pygame.mask.from_surface(map3)

map = pygame.image.load("images/Level-1.png").convert_alpha()

map = pygame.transform.scale(map, ((math*1000)+4, 50000))
main_mapmask = pygame.mask.from_surface(map)

# map rendering coords
main_maprect = map.get_rect()
main_maprect.y = -50000


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
turret_rect.y = 0
#turret's bullet import images and stuff.
turret_bul = pygame.image.load("images/turret_bullet.png").convert_alpha()
turret_bul = pygame.transform.scale(turret_bul, img_size)
turretbul_mask = pygame.mask.from_surface(turret_bul)
turretbul_rect = turret_bul.get_rect()

turretbul_rect.x = -9999


looped_times = -2

time_elapsed=pygame.time.get_ticks()





lvl1 = pygame.transform.scale(map, ((math*1000)+4, 50000))

main_map = lvl1
lvl1 = pygame.transform.scale(map, ((math*1000)+4, 50000))
lvl2 = pygame.transform.scale(map2, ((math*1000)+4, 50000))

music1 = pygame.mixer.Sound("sounds/JammingSoldiers.wav")
music2 = pygame.mixer.Sound("sounds/FinalFlight.wav")
music3 = pygame.mixer.Sound("sounds/PixelatedDreams.wav")
music4 = pygame.mixer.Sound("sounds/unearthlylogistics.wav")
music5 =pygame.mixer.Sound("sounds/pianoclonkers.wav")
music6 =pygame.mixer.Sound("sounds/instrumentjungler.wav")

num = random.randint(1,6)

if num == 1:
    general_background_music = music1
elif num == 2:
    general_background_music = music2
elif num == 3:
    general_background_music = music3
elif num == 4:
    general_background_music = music4
elif num == 5:
    general_background_music = music5
elif num == 6:
    general_background_music = music6
main_audio = pygame.mixer.Channel(4)
main_audio.play(general_background_music)
#Audio handling:
milliseconds_bg_audio_playing=pygame.time.get_ticks()
turretbulx_array = []
turretbuly_array = []
turretbul_img_array = []
def turret_bullet_animation():
    global turretbulx_array, turretbuly_array, turretbul_img_array
    
    #print(turretbul_rect.x, turretbul_rect.y)
    

def music_handling():
    global music1, music2, music3, general_background_music, milliseconds_bg_audio_playing, music4, music5, music6
    main_audio = pygame.mixer.Channel(4)

    background_music_length = general_background_music.get_length()
    
    main_seconds_bg_audio=(pygame.time.get_ticks()-milliseconds_bg_audio_playing)/1000
    if main_seconds_bg_audio >= background_music_length:
        num = random.randint(1,6)

        if num == 1:
            general_background_music = music1
        elif num == 2:
            general_background_music = music2
        elif num == 3:
            general_background_music = music3
        elif num == 4:
            general_background_music = music4
        elif num == 5:
            general_background_music = music5
        elif num == 6:
            general_background_music = music6

        main_audio.play(general_background_music)
        milliseconds_bg_audio_playing=pygame.time.get_ticks()


def map_algorithim():
    global main_map,  main_maprect, main_mapmask, lvl2, lvl1, level
    #loading_of_all_maps()
    #print(main_maprect.y)
    math = width/1000
    
    #print(main_maprect.y)
    if main_maprect.y >= 0 and level == 1:   

        level = 2
        main_map = map2
        
        main_maprect = map2.get_rect()
        main_maprect.y = -50000
        main_mapmask = pygame.mask.from_surface(map2)
    if main_maprect.y >= 1000 and level == 2:   

        level = 3
        main_map = map3
        
        main_maprect = map3.get_rect()
        main_maprect.y = -50000
        main_mapmask = pygame.mask.from_surface(map3)
        
    screen.blit(main_map, main_maprect)
    #print(main_maprect.y)
    
    #lvl1 = pygame.transform.scale(map_lvl_2, ((math*1000)+4, 50000))

    #lvl1 = pygame.transform.scale(map_lvl_2, ((math*1000)+4, 50000))

    


    #creating map_for_collision, also positioning the map



    



user_fired_weapon_sfx = pygame.mixer.Sound("sounds/laserShoot.wav")



explosion1 = pygame.mixer.Sound("sounds/explosion.wav")
explosion2 = pygame.mixer.Sound("sounds/explosion2.wav")


def bullet_animation():
    global space_key_pressed

    
    return




seconds_when_shot = 0
ticks_passed=pygame.time.get_ticks()
helicopterX_array = []
helicopterY_array = []
helicopterImg_array = []
helicopter_direction_array = []






def helicopter_animation():
    global helicopter, helicopter_rect, helicopter_mask
    if main_mapmask.overlap(helicopter_mask, (helicopter_rect.x - main_maprect.x, helicopter_rect.y - main_maprect.y)):
        helicopter_rect.x = random.randint(0,width)
        helicopter_rect.y = random.randint(-3500,-500)
    
        


turretx_array = []
turrety_array = []
turretimg_array = []
target_distance = 750
distance_passed = 0
score = 0
#turretimg_appendment = pygame.transform.scale(turret, img_size)
#-----------


#-----------
def turret_animation():
    
    global turret, score, turret_rect, turret_mask, time_elapsed,  the_math, the_math_2,  distance_passed, target_distance
    #if plane_crashed() == True:
    return False

    

        
    turret_img = turret
    turretimg_array.append(turret_img)
    tur_mask_clone = pygame.mask.from_surface(turret_img)
    max_attempts = 100
    attempts = 0
    valid_position_found = False

    while not valid_position_found and attempts < max_attempts:
        x = random.randint(100, width - 100)
        y = random.randint(-800, -200)
        if main_mapmask.overlap(tur_mask_clone, (x - main_maprect.x, y - main_maprect.y)):
            
            turretx_array.append(x)
            turrety_array.append(y)
            valid_position_found = True
        attempts += 1

    if not valid_position_found:
        
        turretx_array.append(x)
        turrety_array.append(y)
'''
for i in range(len(turretimg_array)):
    if i < len(turrety_array):
    #print(turret_rect.x, turret_rect.y)
        if turrety_array[i] > height:
            turretx_array.pop(i)
            turrety_array.pop(i)
            turretimg_array.pop(i)
            
        
        
        
        
        


        
            

        
    if turret_mask.overlap(planebullet_mask, (planebullet_rect.x - turret_rect.x, planebullet_rect.y - turret_rect.y)):
        # if bullet hits turret
        score = score + 10
    # bullet flying to the right of the screen
    turretbul_rect.x = turretbul_rect.x + 4
    
    turretbul_rect.y = turret_rect.y - 8#??? че я тут написал
    seconds=(pygame.time.get_ticks()-time_elapsed)/1000
    
    #the locations where the turret has to be, after disappears off the screen. Coords.
    
    # turret_draw_on_screen
    #the place where they all teleport to their allocated places, after they disappear off screen.


    


    
    #when the turret disappears out of view, move it to it's new position. 
    
'''
    
#percentage of fuel at the start of the game.
red_hue = 0
green_hue = 250
width_length = 322
fuel = 100
depletion_rate = 0.150 #milliseconds
fuel_bar_timer=pygame.time.get_ticks()
def fuel_bar():
    global red_hue, green_hue, fuel, fuel_bar_timer, width_length, fuel, score, turret_class_array
    seconds_passed_fuel=(pygame.time.get_ticks()-fuel_bar_timer)/1000

    if seconds_passed_fuel >= depletion_rate:
        fuel -= 1
        fuel_bar_timer=pygame.time.get_ticks()
        if fuel > 50:
            red_hue += 5
            width_length -= 3.22
        elif fuel > 0 and fuel <= 50:
            green_hue -= 5
            width_length -= 3.22
        elif fuel <= 0:
            #plane_crashed()
            fuel = 100
            turret_class_array = []
            red_hue = 0
            green_hue = 250
            plane_exploded()
            score = 0
            width_length = 322
    
    #total 500, max should be 250
    #100/500 = 0.2, exactly 0.4 a percent of fuel lost, chagne colour by 0.4
    color = (red_hue, green_hue, 0)  
    rect = pygame.Rect(width/2.46, height/1.13, width_length, 70)  # x, y, width, height
    pygame.draw.rect(screen, color, rect)
    
    

    
turretsbullet_direction = []
turretsbullet_x = []
turretsbullet_y = []
turret_bullet_img = pygame.image.load('images/turret_bullet.png')
turret_bullets = []
turretsbullet_x = []
turretsbullet_y = []

turret_fire_timer = 0

turretsbullet_x = []
turretsbullet_y = []
turretsbullet_direction = []
BULLET_FIRE_INTERVAL = 150
turret_fire_timer = 0

def bullet_animationturrets():
    global turret_bullet_img, turretsbullet_x, turretsbullet_y, turret_fire_timer, score, plane_mask, plane_rect, turret_class_array
    for i in range(len(turretsbullet_x)):
        if i < len(turretsbullet_x):
            turretbulletimg = pygame.mask.from_surface(turret_bullet_img)
            if plane_mask.overlap(turretbulletimg, (turretsbullet_x[i] - plane_rect.x, turretsbullet_y[i] - plane_rect.y)):
                plane_exploded()
                
                turretsbullet_x = []
                turretsbullet_y = []
                turret_class_array= []

    turret_fire_timer += 1
    if turret_fire_timer >= BULLET_FIRE_INTERVAL:
        for turret in turret_class_array:
            turretsbullet_x.append(turret.rect.x)
            turretsbullet_y.append(turret.rect.y)
            turretsbullet_direction.append(turret.direction)
        turret_fire_timer = 0


    for i in range(len(turretsbullet_x)):
        
        #print(i, turretsbullet_direction[i])
        if turretsbullet_direction[i] == 0:
            turretsbullet_x[i] -= 5
            
            screen.blit(pygame.transform.flip(pygame.image.load('images/turret_bullet.png'), True, False), (turretsbullet_x[i], turretsbullet_y[i]))
        elif turretsbullet_direction[i] == 1:
            turretsbullet_x[i] += 5
            screen.blit(turret_bullet_img, (turretsbullet_x[i], turretsbullet_y[i]))
            #helicopterImg_array[i] = 
        turretsbullet_y[i] += settings.game_speed


    remove_indices = []
    for i in range(len(turretsbullet_x)):
        if (turretsbullet_x[i] < 0 or turretsbullet_x[i] > width or
            turretsbullet_y[i] > height):
            remove_indices.append(i)

    for i in reversed(remove_indices):
        turretsbullet_x.pop(i)
        turretsbullet_y.pop(i)
        turretsbullet_direction.pop(i)
    


        
            
        




def plane_exploded():
    global fuel_collection_rect, turretsbullet_y,turretsbullet_direction,  turretsbullet_x, turretx_array, turrety_array, turretimg_array,the_math, the_math_2 , score, fuel, red_hue, green_hue, width_length, helicopterX_array, helicopterY_array, helicopterImg_array, helicopter_direction_array 
    settings.game_speed = 0
    score = 0
    the_math = 0
    the_math_2 = 0



    exploded_channel1 = pygame.mixer.Channel(6)
    exploded_channel1.play(explosion2)

    settings.game_speed = 3
    main_maprect.y = -50000
    #turret_rect.y = -1000
    turret_animation()
    turretsbullet_y = []
    turretsbullet_x = []
    turretsbullet_direction = []
    fuel_collection_rect3.x = -500
    fuel_collection_rect3.y = -500
    fuel_collection_rect2.x = -500
    fuel_collection_rect2.y = -500
    fuel_collection_rect.x = -500
    fuel_collection_rect.y = -500
    fuel = 100
    red_hue = 0
    green_hue = 250
    width_length = 322
    turretx_array = []
    turrety_array = []
    turretimg_array = []
    helicopterX_array = []
    helicopterY_array = []
    helicopterImg_array = []
    helicopter_direction_array = []
    
crash_countdown=pygame.time.get_ticks()
time_elapsed_crash=0
#game loop



def returned_crash():
    return True



def plane_crashed():

    global fuel_collection_rect, turretsbullet_y, turretsbullet_x,turretsbullet_direction, turret_class_array, turretimg_array, turrety_array, turretx_array, fuel, red_hue, helicopterY_array, helicopterX_array,helicopterImg_array , helicopter_direction_array, green_hue, width_length, looped_times, plane_rect, ticks_milsec2, crash_countdown, the_math_2, the_math, score, time_elapsed_crash
    #turret_rect.y = -1000

    if looped_times == -2:
        crash_countdown=pygame.time.get_ticks()
    
    plane1 = pygame.image.load('images/planne1_exp.png')
    plane2 = pygame.image.load('images/planne2_exp.png')
    plane3 = pygame.image.load('images/planne3_exp.png')
    plane4 = pygame.image.load('images/planne4_exp.png')
    plane5 = pygame.image.load('images/planne5_exp.png')

    #animation of planes when they explode, game freezes and only shows animations where you have crashed.
    
    
        
    
    time_elapsed_crash=(pygame.time.get_ticks()-crash_countdown)/1000
    if looped_times == -2:
        screen.blit(plane1,(plane_rect.x, plane_rect.y)) 
        pygame.display.flip()
        time.sleep(0.1)
        looped_times = 1
        quit_game()

        #screen.fill(BG)
        

    if looped_times == 1:
        screen.blit(plane2,(plane_rect.x, plane_rect.y))
        pygame.display.flip() 
        time.sleep(0.1)
        looped_times += 1
        
        quit_game()
        #screen.fill(BG)    
        
    
    if looped_times == 2:
        screen.blit(plane3,(plane_rect.x, plane_rect.y))
        pygame.display.flip()
        time.sleep(0.1)
        looped_times += 1
        
        quit_game()
        #screen.fill(BG)
        
    if looped_times == 3:
        screen.blit(plane4,(plane_rect.x, plane_rect.y)) 
        pygame.display.flip()
        time.sleep(0.1)
        looped_times += 1
        
        quit_game()
        #screen.fill(BG)
        
        
    #looped times 4, we finish the animations, and return the plane to it's original spot.
    if looped_times == 4:
        screen.blit(plane5,(plane_rect.x, plane_rect.y)) 
        pygame.display.flip()
        
        looped_times = -2
        time.sleep(0.1)
        
        quit_game()
        #screen.fill(BG)       
        crash_countdown=pygame.time.get_ticks()

        plane_rect.x = width/2
        plane_rect.y = height/1.5   
        main_maprect.y = -50000

        picked_coordinates = 0
        score = 0
        time_elapsed_crash=0
        
        turret_animation()
        
        turretsbullet_y = []
        fuel_collection_rect3.x = -500
        fuel_collection_rect3.y = -500
        fuel_collection_rect2.x = -500
        fuel_collection_rect2.y = -500
        fuel_collection_rect.x = -500
        fuel_collection_rect.y = -500
        turretsbullet_x = []
        turretsbullet_direction = []
        turret_class_array = []
        the_math = 0
        the_math_2 = 0
        exploded_channel2 = pygame.mixer.Channel(1)
        exploded_channel2.play(explosion1)
        helicopterX_array = []
        helicopterY_array = []
        helicopterImg_array = []
        helicopter_direction_array = []
        turretx_array = []
        turrety_array = []
        turret_class_array = []
        turretimg_array = []
        fuel = 100
        red_hue = 0
        green_hue = 250
        width_length = 322
        #loads images of exploded planes.
        

    
        
    '''
    if main_mapmask.overlap(plane_mask, (plane_rect.x - main_maprect.x, plane_rect.y - main_maprect.y)) or  map2_mask.overlap(plane_mask, (plane_rect.x - main_maprect2.x, plane_rect.y - main_maprect2.y)):
        looped_times += 1
        #print(looped_times)
        #ticks_milsec2=pygame.time.get_ticks()
        return True
    #increment looped times to show sequenced animations.
    
        
    return False
    '''
def quit_game():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        for i in range(50):
            print("CODE QUIT, USER HAS EXITED GAME")
        pygame.quit()
    if keys[pygame.K_F4] and keys[pygame.K_LALT]:
        for i in range(50):
            print("CODE QUIT, USER HAS EXITED GAME")
        pygame.quit()

#pygame.display.toggle_fullscreen()


print(width, height, "HERE")
#------------------------------------------------

seconds = 0
seconds1 = 0
seconds2 = 0
start_ticks=pygame.time.get_ticks()

    
    
    

space_key_pressed = 0
ticks_milsec=pygame.time.get_ticks()
ticks_milsec1=pygame.time.get_ticks()
ticks_milsec2=pygame.time.get_ticks()
ticks_spacebar=pygame.time.get_ticks()
blocks_passed = 0
couldnt_find = 0
moved_distance = 0
milliseconds_bg_audio_playing=pygame.time.get_ticks()
menu = 1
helicopterspawnrate = 500
level = 1
turret_class_array = []
plane_bullets = []
turret_looped= 0 
def turret_alg():
    global distance_passed, couldnt_find, score, turret_looped
    distance_passed += settings.game_speed
    if distance_passed >= target_distance:
        distance_passed = 0
        turret_class_array.append(Turretclass(turret_rect))
        

        #main_mapmask.overlap(fuelcollection_mask, (fuel_collection_rect.x - main_maprect.x, fuel_collection_rect.y - main_maprect.y)):
        turret_class_array[len(turret_class_array)-1].rect.y = random.randint(-600, -200)
        turret_class_array[len(turret_class_array)-1].rect.x = random.randint(0, width)
        turret_mask_clones = pygame.mask.from_surface(turret_class_array[len(turret_class_array)-1].image)
        for i in range(100):
            if main_mapmask.overlap(turret_mask_clones, (turret_class_array[len(turret_class_array)-1].rect.x - main_maprect.x, turret_class_array[len(turret_class_array)-1].rect.y - main_maprect.y)) == None:
                turret_class_array[len(turret_class_array)-1].rect.y = random.randint(-450, -100)
                turret_class_array[len(turret_class_array)-1].rect.x = random.randint(0, width)
            else:
                #print(i)
                break
            if i == 99:
                couldnt_find = 1
        if couldnt_find == 1:
            turret_class_array.pop(len(turret_class_array)-1)
            couldnt_find = 0
            return 
            
        elif couldnt_find == 0:
            for turret in turret_class_array[:]:
                if turret.direction == 'null':
                    
                    if turret.rect.x > plane_rect.x:
                        turret.image = pygame.transform.flip(turret.image, True, False)
                        turret.direction = 0
                        #print("flipped")
                    elif turret.rect.x < plane_rect.x:
                        turret.direction = 1
                        #print("ignored")
                        #print(turret.rect.x)
    for turret in turret_class_array[:]:
        turret_looped += 1
        for bullet in plane_bullets:
                #print("works")
    
            turret_mask_clones = pygame.mask.from_surface(turret.image)
            bullet_mask_clones = pygame.mask.from_surface(bullet.image)
            if turret_mask_clones.overlap(bullet_mask_clones, (bullet.rect.x - turret.rect.x, bullet.rect.y - turret.rect.y)):
                score += 1
                turret_class_array.pop(turret_looped-1)
    turret_looped = 0
                            
                            
                                
                                
while True:
    #print(main_maprect.y)
    music_handling()
    screen.fill(BG)
    quit_game()
    helicopter_animation()
    map_algorithim()
    turret_alg()
    bullet_animationturrets()
    for i in range(len(turretimg_array)):
        screen.blit(turretimg_array[i], (turretx_array[i], turrety_array[i]))
        turrety_array[i] += settings.game_speed
    
    
                        

                        
    for turret in turret_class_array[:]:
        turret.update()
        turret.draw(screen)
        if turret.rect.y > height:
            turret_class_array.remove(turret)
            #print("hi")
            #print("passed", len(turret_class_array))
            #print(turret.rect.y)
    if menu == 1:
        my_font = pygame.font.SysFont('nanummyeongjo', 80)
        
        text_surface = my_font.render('Level ' + str(level), False, (0, 0, 0))
        text_surface2 = my_font.render('Score ' + str(score), False, (0, 0, 0))       
        
        random_int2 = random.randint(-3500, -600)
        random_int= random.randint(50, width-50)

        if height+500 < fuel_collection_rect.y or main_mapmask.overlap(fuelcollection_mask, (fuel_collection_rect.x - main_maprect.x, fuel_collection_rect.y - main_maprect.y)):
            fuel_collection_rect.x = random_int
            fuel_collection_rect.y = random_int2
        if height+random.randint(300,900) < fuel_collection_rect2.y or main_mapmask.overlap(fuelcollection_mask2, (fuel_collection_rect2.x - main_maprect.x, fuel_collection_rect2.y - main_maprect.y)): 
            fuel_collection_rect2.x = random_int
            fuel_collection_rect2.y = random_int2
        if height+random.randint(300,700) < fuel_collection_rect3.y or main_mapmask.overlap(fuelcollection_mask3, (fuel_collection_rect3.x - main_maprect.x, fuel_collection_rect3.y - main_maprect.y)): 
            fuel_collection_rect3.x = random_int
            fuel_collection_rect3.y = random_int2
        if height+random.randint(300,800) < helicopter_rect.y: 
            helicopter_rect.x = random.randint(0,width)
            helicopter_rect.y = random.randint(-3500,-500)
        
        
        for bullet in plane_bullets[:]:
            fuel_collection_masks = pygame.mask.from_surface(fuel_collection)
            bullet_mask_clones = pygame.mask.from_surface(bullet.image)
            if fuel_collection_masks.overlap(bullet_mask_clones, (bullet.rect.x - fuel_collection_rect.x, bullet.rect.y - fuel_collection_rect.y)):
                score += 2
                fuel_collection_rect.x = random_int
                fuel_collection_rect.y = random_int2
            fuel_collection_masks = pygame.mask.from_surface(fuel_collection2)
            if fuel_collection_masks.overlap(bullet_mask_clones, (bullet.rect.x - fuel_collection_rect2.x, bullet.rect.y - fuel_collection_rect2.y)):
                score += 2
                fuel_collection_rect2.x = random_int
                fuel_collection_rect2.y = random_int2
            fuel_collection_masks = pygame.mask.from_surface(fuel_collection3)
            if fuel_collection_masks.overlap(bullet_mask_clones, (bullet.rect.x - fuel_collection_rect3.x, bullet.rect.y - fuel_collection_rect3.y)):
                score += 2
                fuel_collection_rect3.x = random_int
                fuel_collection_rect3.y = random_int2




        blocks_passed += settings.game_speed
        #print(blocks_passed, helicopterspawnrate)
        for i in range(len(helicopterImg_array)):
            for bullet in plane_bullets[:]:
                if i < len(helicopterImg_array):
                    helicopter_mask_clones = pygame.mask.from_surface(helicopterImg_array[i])
                    bullet_mask_clones = pygame.mask.from_surface(bullet.image)
                    if bullet_mask_clones.overlap(helicopter_mask_clones, (helicopterX_array[i] - bullet.rect.x, helicopterY_array[i] - bullet.rect.y)):
                        helicopterY_array.pop(i)
                        helicopterX_array.pop(i)
                        helicopterImg_array.pop(i)
                        helicopter_direction_array.pop(i)
                        score += 1 
                    
        if blocks_passed >= helicopterspawnrate:
            helicopterspawnrate = 500
            blocks_passed = 0
            helicopter_timer = pygame.time.get_ticks()
            helicopterImg_array.append(pygame.image.load("images/helicopter.png"))
            check_island_spawn = random.randint(0, width)
            helicopterY_array.append(-300)
            #7print("hi")
            for i in range(len(helicopterImg_array)):
                helicopter_mask_clones = pygame.mask.from_surface(helicopterImg_array[i])
                while main_mapmask.overlap(helicopter_mask_clones, (check_island_spawn - main_maprect.x, helicopterY_array[i] - main_maprect.y)):
                    
                    check_island_spawn = random.randint(0, width)
            helicopterX_array.append(check_island_spawn)
            
            

            random_int = random.randint(1,2)
            if random_int == 1:
                helicopter_direction_array.append(1)
            else:
                helicopter_direction_array.append(2)
                helicopterImg_array[i] = pygame.transform.flip(helicopterImg_array[i], True, False)
        
        for i in range(len(helicopterImg_array)):
            if i < len(helicopterY_array):
                if plane_mask.overlap(helicopter_mask_clones, (helicopterX_array[i] - plane_rect.x, helicopterY_array[i] - plane_rect.y)):
                    helicopterY_array = []
                    helicopterX_array = []
                    helicopterImg_array = []
                    helicopter_direction_array = []
                    turretimg_array = []
                    turretx_array = []
                    turrety_array = []
                    turret_class_array = []
                    main_maprect.y = -50000
                    plane_exploded()
                    score = 0
                    break
                
                helicopterY_array[i] += settings.game_speed
                if helicopter_direction_array[i] == 1:
                    helicopterX_array[i] -= 4
                else:
                    helicopterX_array[i] += 4
                helicopter_mask_clones = pygame.mask.from_surface(helicopterImg_array[i])
                if main_mapmask.overlap(helicopter_mask_clones, (helicopterX_array[i] - main_maprect.x, helicopterY_array[i] - main_maprect.y)) or helicopterX_array[i] <= 0 or helicopterX_array[i] >= width:
                    if helicopter_direction_array[i] == 1:
                        helicopter_direction_array[i] = 2
                        helicopterX_array[i] += 16
                        helicopterImg_array[i] = pygame.transform.flip(helicopterImg_array[i], True, False)
                    else:
                        helicopter_direction_array[i] = 1
                        helicopterX_array[i] -= 16
                        helicopterImg_array[i] = pygame.transform.flip(helicopterImg_array[i], True, False)
                screen.blit(helicopterImg_array[i], (helicopterX_array[i], helicopterY_array[i]))
                if helicopterY_array[i] > height:
                    helicopterY_array.pop(i)
                    helicopterX_array.pop(i)
                    helicopterImg_array.pop(i)
                    helicopter_direction_array.pop(i)
        
        turret_animation()
        # audio playing, restarts track when ended.
        seconds=(pygame.time.get_ticks()-ticks_milsec)/1000
        if seconds >= 19:


            ticks_milsec=pygame.time.get_ticks()

        #collision detection, with map or one of the turrets.
        if main_mapmask.overlap(plane_mask, (plane_rect.x - main_maprect.x, plane_rect.y - main_maprect.y)):
            #print("go!")
            plane_crashed()
            score = 0
            returned_crash()


        
        elif turretbul_mask.overlap(plane_mask, (plane_rect.x - turretbul_rect.x, plane_rect.y - turretbul_rect.y)):
            plane_exploded()
            score = 0
            
        else:
            if 1 == 1:
                if turret_rect.y < -50:
                    pass
                main_maprect.y = main_maprect.y + settings.game_speed

                turret_rect.y = turret_rect.y + settings.game_speed
                fuel_collection_rect.y = fuel_collection_rect.y + settings.game_speed
                fuel_collection_rect2.y = fuel_collection_rect2.y + settings.game_speed
                fuel_collection_rect3.y = fuel_collection_rect3.y + settings.game_speed
                

                #print(settings.game_speed)
            else:
                settings.game_speed = 0
            moved_distance = moved_distance + settings.game_speed
            #get mouse coordinates
            pos = pygame.mouse.get_pos()
            #print(pos[0]/math, pos[1]-moved_distance)
            #update background
            
            
            #check collision between plane and map.
            seconds2=(pygame.time.get_ticks()-ticks_milsec2)/1000
            #draw plane and level
            screen.blit(plane, plane_rect)
            
            #screen.blit(turret, turret_rect)
            screen.blit(fuel_cell, fuelcell_rect)
            screen.blit(fuel_collection, fuel_collection_rect)
            screen.blit(fuel_collection2, fuel_collection_rect2)
            screen.blit(fuel_collection3, fuel_collection_rect3)
            #screen.blit(plane_bullet, planebullet_rect)
            
            if seconds2 < 999999999999999999999999999999999999999999999999999999999999999999:
                m1 = height - 80
                m2 = width / 100
                screen.blit(text_surface, (m2,m1))
            m1 = height - 80
            m2 = width - 300
            screen.blit(text_surface2, (m2,m1))

            screen.blit(turret_bul, turretbul_rect)
            #event handler from keyboard.
            keys = pygame.key.get_pressed()
            fuel_bar()
            


                
            #this part makes soup
            if fuelcollection_mask.overlap(plane_mask ,(plane_rect.x - fuel_collection_rect.x, plane_rect.y - fuel_collection_rect.y)):
                fuel = 100
                red_hue = 0
                green_hue = 250
                width_length = 322
                
            if fuelcollection_mask2.overlap(plane_mask ,(plane_rect.x - fuel_collection_rect2.x, plane_rect.y - fuel_collection_rect2.y)):
                fuel = 100
                red_hue = 0
                green_hue = 250
                width_length = 322
               
            if fuelcollection_mask3.overlap(plane_mask ,(plane_rect.x - fuel_collection_rect3.x, plane_rect.y - fuel_collection_rect3.y)):
                fuel = 100
                red_hue = 0
                green_hue = 250
                width_length = 322
               

            

            if main_mapmask.overlap(fuelcollection_mask3, (fuel_collection_rect3.x - main_maprect.x, fuel_collection_rect3.y - main_maprect.y)) or  main_mapmask.overlap(fuelcollection_mask2, (fuel_collection_rect2.x - main_maprect.x, fuel_collection_rect.y - main_maprect.y)) or  main_mapmask.overlap(fuelcollection_mask3, (fuel_collection_rect.x - main_maprect.x, fuel_collection_rect.y - main_maprect.y)):
                fuel_collection_rect.x = random.randint(-3500, -600)
                fuel_collection_rect.y = random.randint(50, width-50)

            
            #Controls of the map, and plane    
            if 1 == 1:
                if keys[pygame.K_RIGHT] and plane_rect.x <= width - 30:
                    plane_rect.x = plane_rect.x + 4
                if keys[pygame.K_LEFT] and plane_rect.x >= -8:
                    plane_rect.x = plane_rect.x - 4
                
                if keys[pygame.K_UP] and seconds1 > 0.1:
                    ticks_milsec1=pygame.time.get_ticks()
                    if settings.game_speed < 10:
                        settings.game_speed = settings.game_speed + 1

                if keys[pygame.K_SPACE] and secondsspacebar > 0.3:
                    
                    ticks_spacebar=pygame.time.get_ticks()
                    space_key_pressed += 1
                    laser_pew = pygame.mixer.Channel(7)
                    laser_pew.play(user_fired_weapon_sfx)
                    plane_bullets.append(Planebullet(plane_rect))
                for bullet in plane_bullets[:]:
                    for j in range(len(turretx_array)):
                        if j >= len(turretx_array):
                            break
                        assert j < len(turretx_array)  
                        
                        bullet_mask_clones = pygame.mask.from_surface(bullet.image)
                        if turret_mask.overlap(bullet_mask_clones, (bullet.rect.x - turretx_array[j], bullet.rect.y - turrety_array[j])):
                            score += 1
                            turretx_array.pop(j)
                            turrety_array.pop(j)
                            turretimg_array.pop(j)
                    bullet.update()
                    bullet.draw(screen)
                    if bullet.off_screen(height):
                        plane_bullets.remove(bullet)
                             
                if keys[pygame.K_DOWN] and seconds1 > 0.1:
                    ticks_milsec1=pygame.time.get_ticks()
                    if settings.game_speed > 3:
                        settings.game_speed = settings.game_speed - 1
                seconds1=(pygame.time.get_ticks()-ticks_milsec1)/1000
                secondsspacebar=(pygame.time.get_ticks()-ticks_spacebar)/1000
        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
        #print(settings.game_speed)
        #updates display ( Very important focr making games, I always forgot. )
    
    
    pygame.display.flip()
            #turretbul_rect.x = turret_rect.x + 70
        

'''
Transport has personal line, arrange between planets, transport ores.
Every ore has it's own colour, and show a line between planets.
Once a transporter is built, it automatically moves between planets.


Scouts and transporters can also have simplified ui, in capital,  you can add routes to specific ships before they are built, so you don't forget where to go

'''




'''

No code peeking :)






'''
