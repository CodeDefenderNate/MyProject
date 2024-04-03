#!/usr/bin/python3
"""Garion the Sorcerer RPG game | Nathan Haley"""
import crayons
import time

def showInstructions():
    """Show the game instructions when called"""
    #print a main menu and the commands
    print('''
    Garion the Sorcerer
    ========
    Commands:
      go [direction]
      get [item]
    ''')

def showStatus():
    """determine the current status of the player"""
    # print the player's current location
    print('---------------------------')
    print('You are in the ' + currentRoom)
    # print what the player is carrying
    print('Inventory:', inventory)
    # check if there's an item in the room, if so print it
    if "item" in rooms[currentRoom]:
      print('There is a ' + rooms[currentRoom]['item'])
    print("---------------------------")


# an inventory, which is initially empty
inventory = []

# a dictionary linking a room to other rooms
rooms = {

            'Great Hall' : {
                  'north' : 'North Wing',
                  'south' : 'South Wing',
                  'east' : 'East Wing',
                  'west' : 'West Wing'
                },

            'Courtyard' : {
                  'south' : 'North Wing',
                  'east' : 'Library',
                  'west' : 'Kitchen',
                  'item' : 'Red Dragon'
                },

            'Kitchen' : {
                  'south' : 'Northwest Intersection',
                  'east' : 'Courtyard',
                  'item' : 'Health Potion x3'
                },

            'Library' : {
                  'south' : 'Northeast Intersection',
                  'west' : 'Courtyard',
                  'item' : 'Spell Scroll: Maelstrom'
                },

            'North Wing' : {
                  'north' : 'Courtyard',
                  'east' : 'Northeast Intersection',
                  'west' : 'Northwest Intersection',
                  'south' : 'Great Hall'
                },

            'South Wing' : {
                  'north' : 'Great Hall',
                  'east' : 'Southeast Intersection',
                  'west' : 'Southwest Intersection'
                },
            
            'East Wing' : {
                  'north' : 'Northeast Intersection',
                  'south' : 'Southeast Intersection',
                  'west' : 'Great Hall'
                },

            'West Wing' : {
                  'north' : 'Northwest Intersection',
                  'south' : 'Southwest Intersection',
                  'east' : 'Great Hall'
                },
            
            'Northwest Intersection' : {
                  'north' : 'Kitchen',
                  'south' : 'West Wing',
                  'east' : 'North Wing'
                },
            
            'Northeast Intersection' : {
                  'north' : 'Library',
                  'south' : 'East Wing',
                  'west' : 'North Wing'
                },
            
            'Southeast Intersection' : {
                  'north' : 'East Wing',
                  'east' : 'SE Guard Tower',
                  'west' : 'South Wing'
                },

            'Southwest Intersection' : {
                  'north' : 'West Wing',
                  'east' : 'South Wing',
                  'west' : 'SW Guard Tower'
                },

            'SW Guard Tower' : {
                  'east' : 'Southwest Intersection',
                  'item' : 'Key'
                },

            'SE Guard Tower' : {
                  'west' : 'Southeast Intersection',
                  'item' : 'Mage Staff'
            }


         }

# start the player in the Hall
currentRoom = 'Great Hall'

showInstructions()

# breaking this while loop means the game is over
while True:
    showStatus()

    # the player MUST type something in
    # otherwise input will keep asking
    move = ''
    while move == '':  
        move = input('>')

    # normalizing input:
    # .lower() makes it lower case, .split() turns it to a list
    # therefore, "get golden key" becomes ["get", "golden key"]          
    move = move.lower().split(" ", 1)

    #if they type 'go' first
    if move[0] == 'go':
        #check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            #set the current room to the new room
            currentRoom = rooms[currentRoom][move[1]]
        # if they aren't allowed to go that way:
        else:
            print('You can\'t go that way!')

    #if they type 'get' first
    if move[0] == 'get' :
        # make two checks:
        # 1. if the current room contains an item
        # 2. if the item in the room matches the item the player wishes to get
        if "item" in rooms[currentRoom] and rooms[currentRoom]['item'].lower() == move[1]:
            #add the item to their inventory
            inventory.append(rooms[currentRoom]['item'])
            #display a helpful message
            print(rooms[currentRoom]['item'] + ' aquired!')
            #delete the item key:value pair from the room's dictionary
            del rooms[currentRoom]['item']
        # if there's no item in the room or the item doesn't match
        else:
            #tell them they can't get it
            print('Can\'t get ' + move[1] + '!')

        ## If a player enters a room with a monster
        ## Define how a player can win

    if currentRoom == 'Courtyard' and 'Key' in inventory and 'Health Potion x3' in inventory and 'Mage Staff' in inventory and 'Spell Scroll: Maelstrom' in inventory:
        print('The Red Dragon uses its Fire Breath on you!')
        time.sleep(1)
        print('You used a Health Potion!')
        time.sleep(1)
        print('Maelstrom cast!')
        time.sleep(1)
        print('The fabled Red Dragon has finally been defeated... balance has been restored\nGAME OVER!')
        break

    
        ## If a player enters a room with a monster
    elif 'item' in rooms[currentRoom] and 'Red Dragon' in rooms[currentRoom]['item']:
        print('A Red Dragon has used its Fire Breath on you!...')
        time.sleep(1)
        print('GAME OVER!')
        break