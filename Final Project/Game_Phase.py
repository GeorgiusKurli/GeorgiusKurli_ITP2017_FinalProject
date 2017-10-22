from pygame import *
from pygame.sprite import *
import Game_Classes as cl

#Startmenu function to be called
def Start_Menu():
    pygame.init()

    #Set the variables and displays
    main_frame = display.set_mode((1080,720))
    breaker = True
    start_button = cl.Button("Press to Start", 540,360)
    start_menu_sprites = Group(start_button)

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
    global log, money, initial_time, total_log, total_money
    log = 0
    money = 0
    total_log = 0
    total_money = 0

    #creating buttons and sprites
    market_button = cl.Button("Market", 50, 45)
    stats_button = cl.Button("Stats", 375,45)
    upgrade_button = cl.Button("Upgrade", 750,45)
    player = cl.Player()



    #grouping sprites
    main_game_sprites = Group(main_game_background, main_game_backgroundup, player, market_button, stats_button, upgrade_button)
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

    #creating first tree
    temptree = cl.Tree()
    trees.add(temptree)

    #Main game loop
    while breaker:

        #creating and updating screen
        main_frame.fill(cl.light_green)
        trees.draw(main_frame)
        main_game_sprites.draw(main_frame)
        display.update()

        #main event checking
        for ev in event.get():
            if ev.type == QUIT:
                pygame.quit()
                exit()

            elif ev.type == MOUSEBUTTONDOWN:
                if market_button.rect.collidepoint(mouse.get_pos()):
                    MarketMenu()

                if stats_button.rect.collidepoint(mouse.get_pos()):
                    StatsMenu()

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
            if player.x >=8:
                player.move(-10,0)

        elif moveright == True:
            if player.x <= 1058:
                player.move(10,0)

        elif movedown == True:
            if player.y <= 574:
                player.move(0,10)

        elif moveup == True:
            if player.y >= 102:
                player.move(0,-10)

        #checks if player is swinging
        if swingmode == True:
            player.swingstance()
            for temptree in trees:
                if player.rect.colliderect(temptree):
                    trees.remove(temptree)
                    log += 1
                    total_log += 1


        if swingmode == False:
            player.defaultstance()

        #checks if it is 3 seconds and spawns a tree
        if pygame.time.get_ticks() - tree_timer >= 3000:
            temptree = cl.Tree()
            trees.add(temptree)
            tree_timer = pygame.time.get_ticks()

#defining menu for Market button
def MarketMenu():
    global money, log, total_money

    #creating display
    pygame.display.set_caption("Tree Cutting Simulation")
    main_frame = display.set_mode((1080,720))

    #creating background and buttons
    main_game_background = cl.BackGround("MainGameBackground_V2.png")
    market_background = cl.BackGround("Market_Background V1.png")

    #creating buttons
    sell_button = cl.Button("Sell", 540,550,120)
    back_button = cl.Button("Back to Game", 100,150,42, cl.white)
    money_button = cl.Button("Money: %d"%money, 300,450,50)
    log_button = cl.Button("Log: %d"%log, 700,450,50)

    #grouping sprites
    market_sprites = Group(main_game_background, market_background, sell_button, back_button, money_button, log_button)

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
                    money += log * 100
                    total_money += log * 100
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
    global log, money, initial_time, total_log, total_money
    time_spent = (pygame.time.get_ticks() - initial_time) / 1000


    #creating buttons
    back_button = cl.Button("Back to Game", 100,150,42)
    total_money_button = cl.Button("Total Earned: %d"%total_money, 250, 300,42)
    total_log_button = cl.Button("Total Trees Cut: %d"%total_log, 250, 400, 42)
    total_time_button = cl.Button("Time Spent: %d"%time_spent, 250, 500, 42)

    #grouping sprites
    stats_shown = Group(main_game_background, main_game_backgroundup, back_button, total_money_button, total_log_button, total_time_button)


    #Main stats menu loop
    while breaker:

        #creating and updating screen
        main_frame.fill(cl.white)
        stats_shown.draw(main_frame)
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

        #update time spent
        time_spent = (pygame.time.get_ticks() - initial_time) / 1000
        total_time_button.update_message("Total Time Spent: %d"%time_spent)
