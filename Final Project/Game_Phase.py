from pygame import *
from pygame.sprite import *
from pygame.mixer import *
import Game_Classes as cl
import random

#Startmenu function to be called
def Start_Menu():

    #Set the variables and displays
    main_frame = display.set_mode((1080,720))
    breaker = True

    #creating buttons
    start_button = cl.Button("Press to Start", 540,360)
    help_button = cl.Button("How to Play", 540,440, backcolor = cl.light_green)

    #grouping sprites
    start_menu_sprites = Group(start_button, help_button)

    #main startmenu loop
    while breaker:
        main_frame.fill(cl.white)
        start_menu_sprites.draw(main_frame)
        display.update()

        #checks if quit button is clicked
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks if start button is clicked
            elif ev.type == MOUSEBUTTONDOWN:
                if start_button.rect.collidepoint(mouse.get_pos()):
                    breaker = False

                if help_button.rect.collidepoint(mouse.get_pos()):
                    help_menu()


def help_menu():
    #Set the variables and displays
    main_frame = display.set_mode((1080,720))
    breaker = True
    helpbackground = cl.BackGround("HelpBackground.png")

    #creating buttons
    back_button = cl.Button("Back to Menu", 150,45)

    #grouping sprites
    help_menu_sprites = Group(helpbackground,back_button)

    #main startmenu loop
    while breaker:
        main_frame.fill(cl.white)
        help_menu_sprites.draw(main_frame)
        display.update()

        #checks if quit button is clicked
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks if start button is clicked
            elif ev.type == MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(mouse.get_pos()):
                    breaker = False


#defining main game
def Main_Game_Display():

    #Set the displays
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))
    breaker = True
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    main_game_backgroundup = cl.BackGround("MainGameBackgroundup_V1.png")
    #height = 98, width = 1080

    #set the variables
    global log, money, initial_time, total_log, total_money, rates, housestage, cut_timeneeded, car
    log = 10
    money = 0
    total_log = 0
    total_money = 0
    cut_progress = 0
    rates = 100
    housestage = 0
    cut_timeneeded = 60
    car = False

    #creating buttons and sprites
    market_button = cl.Button("Market", 50, 45)
    stats_button = cl.Button("Stats", 375,45)
    upgrade_button = cl.Button("Upgrade", 750,45)
    drive_button = cl.Button("Nocturnal Drive", 250,80)
    normal_button = cl.Button("Regular Drive", 750,80)
    go_home_button = cl.Button("Go Home", 1000,45)
    player = cl.Player()


    #grouping sprites
    main_game_sprites = Group(main_game_background, main_game_backgroundup, player, 
        market_button, stats_button, upgrade_button, go_home_button)
    trees = Group()

    #taking initial times
    initial_time = pygame.time.get_ticks()
    tree_timer = pygame.time.get_ticks()

    #setting movement as false
    moveleft = False
    moveup = False
    movedown = False
    moveright = False
    swingmode = False

    #setting mini menu as false
    showmarketoptions = False

    #creating clock
    ingameclock = pygame.time.Clock()

    #Main game loop
    while breaker:

        #setting frame per second cap to 60
        ingameclock.tick(60)

        #main event checking
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks if market is pressed
            elif ev.type == MOUSEBUTTONDOWN:
                
                #checks if car is present when market is pressed
                if market_button.rect.collidepoint(mouse.get_pos()):
                    if car == True and showmarketoptions == False:
                        main_game_sprites.add(drive_button)
                        main_game_sprites.add(normal_button)
                        showmarketoptions = True

                    elif car == True and showmarketoptions == True:
                        main_game_sprites.remove(drive_button)
                        main_game_sprites.remove(normal_button)
                        showmarketoptions = False

                    else:
                        MarketMenu()

                #Checks if stats is pressed
                if stats_button.rect.collidepoint(mouse.get_pos()):
                    StatsMenu()

                #checks if upgrade is pressed
                if upgrade_button.rect.collidepoint(mouse.get_pos()):
                    UpgradeMenu()

                if drive_button.rect.collidepoint(mouse.get_pos()):
                    result = Driving_Phase()
                    if result == True:
                        MarketMenu(result)

                if normal_button.rect.collidepoint(mouse.get_pos()):
                    MarketMenu()

                if go_home_button.rect.collidepoint(mouse.get_pos()):
                    House()

            #checks if button is being pressed
            elif ev.type == KEYDOWN:
                if ev.key == K_LEFT:
                    moveleft = True
                    player.direction("left")

                elif ev.key == K_RIGHT:
                    moveright = True
                    player.direction("right")

                elif ev.key == K_DOWN:
                    movedown = True

                elif ev.key == K_UP:
                    moveup = True

                elif ev.key == K_z:
                    swingmode = True

            #checks if button is let go
            elif ev.type == KEYUP:

                if ev.key == K_LEFT:
                    moveleft = False

                elif ev.key == K_RIGHT:
                    moveright = False

                elif ev.key == K_DOWN:
                    movedown = False

                elif ev.key == K_UP:
                    moveup = False

                elif ev.key == K_z:
                    swingmode = False

        #Checks if movement is true and direction
        if moveleft == True:
            if player.x >= 8:
                player.move(-5,0)

        if moveright == True:
            if player.x <= 1058:
                player.move(5,0)

        if movedown == True:
            if player.y <= 574:
                player.move(0,5)

        if moveup == True:
            if player.y >= 102:
                player.move(0,-5)

        #checks if player is swinging
        if swingmode == True:
            player.swingstance()
            for temptree in trees:
                if player.rect.colliderect(temptree):
                    if cut_progress >= cut_timeneeded:
                        trees.remove(temptree)
                        log += 1
                        total_log += 1
                        cut_progress = 0
                    else:
                        cut_progress += 1

        if swingmode == False:
            player.defaultstance()

        #checks if it is 3 seconds and spawns a tree
        if pygame.time.get_ticks() - tree_timer >= 3000:
            temptree = cl.Tree()
            trees.add(temptree)
            tree_timer = pygame.time.get_ticks()

        for sprites in main_game_sprites:
            if isinstance(sprites,cl.Button):
                if sprites.rect.collidepoint(mouse.get_pos()):
                    sprites.change_colour(cl.white)
                
                else:
                    sprites.change_colour(cl.black)

        
        #updating screen
        main_frame.fill(cl.light_green)
        trees.draw(main_frame)
        main_game_sprites.draw(main_frame)
        display.update()

#defining menu for Market button
def MarketMenu(result = None):
    global money, log, total_money, rates

    #creating display
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))

    #creating background and buttons
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    market_background = cl.BackGround("Market_Background V1.png")

    #creating buttons
    sell_button = cl.Button("Sell All", 540,550,120)
    back_button = cl.Button("Back to Game", 100,150,42, cl.white)
    money_button = cl.Button("Money: %d"%money, 300,450,50)
    log_button = cl.Button("Log: %d"%log, 700,450,50)
    if result:
        doublerate = rates*2
        rates_button = cl.Button("Rates: %d"%doublerate, 850,150,50, color = cl.red)
    else:
        rates_button = cl.Button("Rates: %d"%rates, 850,150,50, color = cl.white)

    #grouping sprites
    market_sprites = Group(main_game_background, market_background, sell_button, back_button, money_button, log_button, 
        rates_button)

    #Main market loop
    breaker = True
    while breaker:

        #creating and updating screen
        main_frame.fill(cl.light_green)
        market_sprites.draw(main_frame)
        display.update()

        #main event checking
        for ev in event.get():
            #checks if quit button is clicked
            if ev.type == QUIT:
                pygame.quit()
                exit()

            if ev.type == MOUSEBUTTONDOWN:
                #checks if back button is clicked
                if back_button.rect.collidepoint(mouse.get_pos()):
                    breaker = False

                #checks if sell button is clicked
                if sell_button.rect.collidepoint(mouse.get_pos()):
                    if result:
                        money += log * (rates * 2)
                        total_money += log * (rates * 2)
                        log = 0

                    else:
                        money += log * rates
                        total_money += log * rates
                        log = 0

        #updates money and logs
        money_button.update_message("Money: %d"%money)
        log_button.update_message("Log: %d"%log)

#defining menu for stats button
def StatsMenu():

    #Set the displays
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))
    breaker = True
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    main_game_backgroundup = cl.BackGround("MainGameBackgroundup_V1.png")
    #height = 98, width = 1080

    #setting variables
    global log, money, initial_time, total_log, total_money, rates, housestage, cut_timeneeded, car

    
    time_spent = (pygame.time.get_ticks() - initial_time) / 1000
    minutes_spent = time_spent/60
    seconds_spent = time_spent%60
    hours_shown = minutes_spent/60
    minutes_shown = minutes_spent%60


    #creating buttons
    back_button = cl.Button("Back to Game", 100,150,42, backcolor = cl.light_green)
    total_money_button = cl.Button("Total Earned: %d"%total_money, 540, 150,42)
    total_log_button = cl.Button("Total Trees Cut: %d"%total_log, 540, 200, 42)
    total_time_button = cl.Button("Time Spent: %dhours %dminutes %dseconds"%(hours_shown, minutes_shown, seconds_spent), 540, 250, 42)
    housestagenum = cl.Button("Current House Stage: %d"%housestage, 540, 300,42)
    save_button = cl.Button("Save Game", 100,550,42)
    load_button = cl.Button("Load Game", 100,600,42)

    #grouping sprites
    stats_shown = Group(main_game_background, main_game_backgroundup, total_money_button, total_log_button, total_time_button, 
        housestagenum,)

    stats_buttons = Group(back_button, save_button, load_button)

    #Main stats menu loop
    while breaker:

        #creating and updating screen
        main_frame.fill(cl.light_green)
        stats_shown.draw(main_frame)
        stats_buttons.draw(main_frame)
        display.update()

        #main event checking
        for ev in event.get():
            #checks if quit is pressed
            if ev.type == QUIT:
                pygame.quit()
                exit()

            if ev.type == MOUSEBUTTONDOWN:
                #checks if back button is pressed
                if back_button.rect.collidepoint(mouse.get_pos()):
                    breaker = False

                #checks if save button is pressed
                if save_button.rect.collidepoint(mouse.get_pos()):
                    save_varlist = [log,money,initial_time,total_log,total_money,rates,housestage,cut_timeneeded,car]
                    
                    tempfile = open("Save.txt", "w")

                    #writes every variable in a text file
                    for data in save_varlist:
                        tempfile.write("%s\n" %str(data))
                        
                    tempfile.close()

                #checks if load button is pressed
                if load_button.rect.collidepoint(mouse.get_pos()):
                    tempfile = open("save.txt")
                    tempsavelist = tempfile.read().split("\n")

                    #set all the variables to the ones in the file
                    log = int(tempsavelist[0])
                    money = int(tempsavelist[1])
                    initial_time = int(tempsavelist[2])
                    total_log = int(tempsavelist[3])
                    total_money = int(tempsavelist[4])
                    rates = int(tempsavelist[5])
                    housestage = int(tempsavelist[6])
                    cut_timeneeded = int(tempsavelist[7])
                    car = tempsavelist[8]

                    tempfile.close()
                    

        #checks if buttons in group stats_button is hovered
        for sprite in stats_buttons:
            if sprite.rect.collidepoint(mouse.get_pos()):
                sprite.change_colour(cl.white)
            else:
                sprite.change_colour(cl.black)

        #update time spent
        minutes_spent = time_spent/60
        seconds_spent = time_spent%60
        hours_shown = minutes_spent/60
        minutes_shown = minutes_spent%60
        time_spent = (pygame.time.get_ticks() - initial_time) / 1000
        
        #updates buttons
        total_time_button.update_message("Time Spent: %dhours %dminutes %dseconds"%(hours_shown, minutes_shown, seconds_spent))
        total_money_button.update_message("Total Earned: %d"%total_money)
        total_log_button.update_message("Total Trees Cut: %d"%total_log)
        total_time_button.update_message("Time Spent: %dhours %dminutes %dseconds"%(hours_shown, minutes_shown, seconds_spent))
        housestagenum.update_message("Current House Stage: %d"%housestage)


#menu for upgrades
def UpgradeMenu():
    global money, log, rates, housestage, cut_timeneeded, rates, car

    #creating display
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))

    #creating background and buttons
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    upgrade_background = cl.BackGround("Upgrade_Background V1.png")

    #setting variables
    purchaseable_stage = housestage + 1
    houseprice = purchaseable_stage * 500
    rate_price = rates*2.5
    purchaseable_rate = rates+10
    carprice = 1000
    purchaseable_speed = cut_timeneeded - 10
    if cut_timeneeded <= 0:
        speedprice = 0
    else:
        speedprice = 48000/cut_timeneeded

    #creating buttons
    back_button = cl.Button("Back to Game", 100,50,42, cl.white)
    money_button = cl.Button("Money: %d"%money, 900,125,50, color = cl.white)
    log_button = cl.Button("Log: %d"%log, 900,175,50, color = cl.white)
    buy_house_button = cl.Button("Buy: %d"%houseprice, 120, 550, 42, color = cl.white)
    buy_house = cl.Button("House Stage %d"%purchaseable_stage, 120, 500, 42, color = cl.white)
    buy_rate_button = cl.Button("Buy: %d"%rate_price, 350,550,42,color = cl.white)
    buy_rate = cl.Button("Rates = %d"%purchaseable_rate, 350,500,42,color = cl.white)
    buy_car_button = cl.Button("Buy: %d"%carprice, 600,550,42,color = cl.white)
    buy_car = cl.Button("Car", 600,500,42,color = cl.white)
    buy_speedup = cl.Button("Cut Speed: %d Ticks"%purchaseable_speed, 850,500,42,color = cl.white)
    buy_speedup_button = cl.Button("Buy: %d"%speedprice, 850,550,42,color = cl.white)

    #grouping sprites
    upgrade_sprites = Group(main_game_background, upgrade_background, back_button, money_button, log_button, buy_house, 
        buy_house_button,   buy_rate_button, buy_rate, buy_car_button, buy_car, buy_speedup, buy_speedup_button)

    #Main market loop
    breaker = True
    while breaker:

        #creating and updating screen
        main_frame.fill(cl.light_green)
        upgrade_sprites.draw(main_frame)
        display.update()

        #main event checking
        for ev in event.get():
            #checks if quit button is clicked
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks for event: mouse button
            if ev.type == MOUSEBUTTONDOWN:
                if back_button.rect.collidepoint(mouse.get_pos()):
                    breaker = False

                if buy_house_button.rect.collidepoint(mouse.get_pos()):
                    if money >= houseprice and housestage < 5:
                        money -= houseprice
                        housestage += 1
                        houseprice = (housestage + 1) * 500
                        purchaseable_stage += 1

                if buy_rate_button.rect.collidepoint(mouse.get_pos()):
                    if money >= rate_price:
                        money -= rate_price
                        rates += 10
                        purchaseable_rate += 10
                        rate_price = rates * 2.5

                if buy_car_button.rect.collidepoint(mouse.get_pos()):
                    if money >= carprice and car == False:
                        money -= carprice
                        car = True

                if buy_speedup_button.rect.collidepoint(mouse.get_pos()):
                    if money >= speedprice and cut_timeneeded > 0:
                        money -= speedprice
                        cut_timeneeded -= 10
                        purchaseable_speed = cut_timeneeded - 10
                        if cut_timeneeded <=0:
                            speedprice = None
                        else:
                            speedprice = 48000/cut_timeneeded

        #updates button
        money_button.update_message("Money: %d"%money)
        log_button.update_message("Log: %d"%log)
        buy_rate_button.update_message("Buy: %d"%rate_price)
        buy_rate.update_message("Rates = %d"%purchaseable_rate)

        
        #updates housestage button and caps the housestage to 5
        if housestage < 5:
            buy_house.update_message("House Stage %d"%purchaseable_stage)
            buy_house_button.update_message("Buy: %d"%houseprice)

        else:
            buy_house.update_message("House Completed")
            buy_house_button.update_message("Bought")

        #updates buy for car into bought if purchased
        if car == True:
            buy_car_button.update_message("Bought")

        if cut_timeneeded > 0:
            buy_speedup.update_message("Cut Speed: %d Ticks"%purchaseable_speed)
            
            buy_speedup_button.update_message("Buy: %d"%speedprice)

        else:
            buy_speedup.update_message("Cut Speed: Maxed")
            buy_speedup_button.update_message("Bought")



#driving phase
def Driving_Phase():

    #Set the displays
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))
    breaker = True
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    main_game_backgroundup = cl.BackGround("MainGameBackgroundup_V1.png")
    #height = 98, width = 1080

    #creating sprites
    car = cl.Car()

    road = Group()
    driving_phase_sprites = Group(main_game_background, main_game_backgroundup, car)

    #taking initial times
    initial_drivingtime = pygame.time.get_ticks()
    road_timer = pygame.time.get_ticks()

    #setting movement as false
    moveleft = False
    moveright = False

    #creating clock
    ingameclock = pygame.time.Clock()

    #creating first road coordinate
    tempxcoor = 540

    #declaring that car is on road
    onroad = True

    #loads and plays music
    pygame.mixer.music.load("Deja Vu Initial D.mp3")
    pygame.mixer.music.play()

    #Main stats menu loop
    while breaker:

        #capping fps to 60
        ingameclock.tick(60)

        #creating and updating screen
        main_frame.fill(cl.dark_green)
        road.draw(main_frame)
        driving_phase_sprites.draw(main_frame)
        display.update()


        #main event checking
        for ev in event.get():
            #checks if quit is pressed
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks if button is being pressed
            elif ev.type == KEYDOWN:

                if ev.key == K_LEFT:
                    moveleft = True

                elif ev.key == K_RIGHT:
                    moveright = True

            #checks if button is let go
            elif ev.type == KEYUP:

                if ev.key == K_LEFT:
                    moveleft = False

                elif ev.key == K_RIGHT:
                    moveright = False

        #Checks if movement is true for left or right
        if moveleft == True:
            if car.x >=8:
                car.move(-1,0)

        elif moveright == True:
            if car.x <= 1058:
                car.move(1,0)

        #creating roads every 0.1 seconds
        if pygame.time.get_ticks() - road_timer >= 100:
            sway = random.randint(-10,10)
            tempxcoor = tempxcoor + sway
            temproad = cl.Road(tempxcoor)
            road.add(temproad)
            road_timer = pygame.time.get_ticks()

        #makes object move downwards and remove roads that leave the screen
        for object in road:
            object.movedown()
            if object.y >= 720:
                road.remove(object)

        #after 5 seconds, game starts to check if car is offroad
        if pygame.time.get_ticks() - initial_drivingtime >= 2000:

            if spritecollideany(car, road):

                onroad = True
            else:
                onroad = False
        #set winning conditions
        if pygame.time.get_ticks() - initial_drivingtime >= 35000:
            breaker = False
            return Success_Menu()
        #checks if car is offroad
        if onroad == False:
            breaker = False
            return Crash_Menu()

#menu when car crashes
def Crash_Menu():
    global log

    #Set the variables and displays
    main_frame = display.set_mode((1080,720))
    breaker = True
    logs_lost = int(log*0.2)
    log -= logs_lost

    #creating buttons
    youcrash_sign = cl.Button("You went offroad!", 540,100,100)
    logslost_sign = cl.Button("You lost %d logs!"%logs_lost, 540, 250)
    continue_button = cl.Button("Continue", 540,360)

    #grouping sprites
    start_menu_sprites = Group(continue_button, youcrash_sign, logslost_sign)

    #main startmenu loop
    while breaker:
        main_frame.fill(cl.white)
        start_menu_sprites.draw(main_frame)
        display.update()

        #checks if quit button is clicked
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks if start button is clicked
            elif ev.type == MOUSEBUTTONDOWN:
                if continue_button.rect.collidepoint(mouse.get_pos()):
                    pygame.mixer.music.stop()
                    breaker = False
                    result = False
                    return result

def Success_Menu():
    #Set the variables and displays
    main_frame = display.set_mode((1080,720))
    breaker = True

    #creating buttons
    youreach_sign = cl.Button("You reached your destination!", 540,100,100)
    continue_button = cl.Button("Continue", 540,360)

    #grouping sprites
    start_menu_sprites = Group(continue_button, youreach_sign)

    #main startmenu loop
    while breaker:
        main_frame.fill(cl.white)
        start_menu_sprites.draw(main_frame)
        display.update()

        #checks if quit button is clicked
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()

            #checks if start button is clicked
            elif ev.type == MOUSEBUTTONDOWN:
                if continue_button.rect.collidepoint(mouse.get_pos()):
                    pygame.mixer.music.stop()
                    breaker = False
                    result = True
                    return result

def House():
    #Set the displays
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))
    breaker = True
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    main_game_backgroundup = cl.BackGround("MainGameBackgroundup_V1.png")
    #height = 98, width = 1080

    #check which housestage is active
    if housestage == 0:
        housepicture = cl.BackGround("Home 0.png")

    elif housestage == 1:
        housepicture = cl.BackGround("Home 1.png")

    elif housestage == 2:
        housepicture = cl.BackGround("Home 2.png")

    elif housestage == 3:
        housepicture = cl.BackGround("Home 3.png")

    elif housestage == 4:
        housepicture = cl.BackGround("Home 4.png")

    elif housestage == 5:
        housepicture = cl.BackGround("Home 5.png")

    
    #creating buttons
    back_button = cl.Button("Back to Game", 100,45,42)
    
    #grouping sprites
    house_menu_sprites = Group(housepicture, main_game_background, main_game_backgroundup, back_button,)


    #Main house menu loop
    while breaker:

        #creating and updating screen
        main_frame.fill(cl.white)
        house_menu_sprites.draw(main_frame)
        display.update()

        #main event checking
        for ev in event.get():
            #checks if quit is pressed
            if ev.type == QUIT:
                pygame.quit()
                exit()

            if ev.type == MOUSEBUTTONDOWN:
                #checks if back button is pressed
                if back_button.rect.collidepoint(mouse.get_pos()):
                        breaker = False
