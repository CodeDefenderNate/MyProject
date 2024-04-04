#!/usr/bin/python3
"""Garion: The Child of Light - RPG game | Nathan Haley"""
import crayons
import time

player_health = 100 # Starting health for the player
dragon_health = 1000 # Starting health for the dragon

def showInstructions():
    """Show the game instructions when called"""
    #print a main menu and the commands
    print(crayons.green("""
    Garion: The Child of Light""", bold=True))
    print(crayons.yellow("""==================================
    Commands:
      go [direction]
      get [item]
      use [item]
      teleport [room name]
    """, bold=True))

def showStatus():
    """determine the current status of the player"""
    # print the player"s current location
    print("---------------------------")
    print("You are in the " + crayons.magenta([currentRoom], bold=True))
    # print what the player is carrying
    print(crayons.blue("Inventory:", bold=True), crayons.green(str(inventory), bold=True))
    # check if there"s an item in the room, if so print it
    if "item" in rooms[currentRoom]:
      print("There is a " + crayons.green(rooms[currentRoom]["item"], bold=True))
    print("---------------------------")


# an inventory, which is initially empty
inventory = []

# a dictionary linking a room to other rooms
rooms = {

            "Great Hall" : {
                  "north" : "North Wing",
                  "south" : "South Wing",
                  "east" : "East Wing",
                  "west" : "West Wing"
                },

            "Courtyard" : { # Changed to require a key
                  "south" : "North Wing",
                  "east" : "Library",
                  "west" : "Kitchen",
                  "item" : "Red Dragon"
                },

            "Kitchen" : {
                  "south" : "Northwest Intersection",
                  "east" : "Courtyard", # Changed to require a key
                  "item" : ["Health Potion x3"]
                },

            "Library" : {
                  "south" : "Northeast Intersection",
                  "west" : "Courtyard", # Changed to require a key
                  "item" : ["Spell Scroll: Maelstrom", "Spell Scroll: Meteor", "Spell Scroll: Lightning"]
                },

            "North Wing" : {
                  "south" : "Great Hall", 
                  "east" : "Northeast Intersection",
                  "west" : "Northwest Intersection"
                  
                },

            "South Wing" : {
                  "north" : "Great Hall",
                  "east" : "Southeast Intersection",
                  "west" : "Southwest Intersection"
                },
            
            "East Wing" : {
                  "north" : "Northeast Intersection",
                  "south" : "Southeast Intersection",
                  "west" : "Great Hall"
                },

            "West Wing" : {
                  "north" : "Northwest Intersection",
                  "south" : "Southwest Intersection",
                  "east" : "Great Hall"
                },
            
            "Northwest Intersection" : {
                  "north" : "Kitchen",
                  "south" : "West Wing",
                  "east" : "North Wing"
                },
            
            "Northeast Intersection" : {
                  "north" : "Library",
                  "south" : "East Wing",
                  "west" : "North Wing"
                },
            
            "Southeast Intersection" : {
                  "north" : "East Wing",
                  "east" : "Southeast Guard Tower",
                  "west" : "South Wing"
                },

            "Southwest Intersection" : {
                  "north" : "West Wing",
                  "east" : "South Wing",
                  "west" : "Southwest Guard Tower"
                },

            "Southwest Guard Tower" : {
                  "east" : "Southwest Intersection",
                  "item" : ["Key"]
                },

            "Southeast Guard Tower" : {
                  "west" : "Southeast Intersection",
                  "item" : ["Mage Staff"]
            }


         }

# start the player in the Hall
currentRoom = "Great Hall"

showInstructions()

# breaking this while loop means the game is over
while True:
    showStatus()
    move = input("> ").lower().split(" ", 1)
    # the player MUST type something in
    # otherwise input will keep asking
    ## move = ""
    ## while move == "":  
        ## move = input("> ").lower()
    ## move = move.split(" ", 1)

    # normalizing input:
    # .lower() makes it lower case, .split() turns it to a list
    # therefore, "get golden key" becomes ["get", "golden key"]          
    ## move = move.lower().split(" ", 1)

    #if they type "go" first
    if move[0] == "go":
        direction = move[1]
        if direction in rooms[currentRoom]:
            if direction == "east" and currentRoom == "Kitchen" and "Key" not in inventory:
                print(crayons.red("The door is locked. You need a Key to enter the Courtyard", bold=True))
            elif direction == "west" and currentRoom == "Library" and "Key" not in inventory:
                print(crayons.red("The door is locked. You need a Key to enter the Courtyard", bold=True))
            else:
                currentRoom = rooms[currentRoom][direction]
                print("You go to the " + currentRoom + ".")
        else:
            print(crayons.yellow("You can't go that way", bold=True))
        # Check that they are allowed wherever they want to go
        ## if move[1] in rooms[currentRoom]:
            # Check if they have the key for Courtyard
            ## if move[1] == "Courtyard" and "Key" not in inventory:
               ## print(crayons.red("The door to the Courtyard is locked. You need a Key to enter.", bold=True))
            ## else:
               ## currentRoom = rooms[currentRoom][move[1]]
        ## else:    
           ## print(crayons.red("You can't go that way!", bold=True))
    if move[0] == "teleport":
        if len(move) > 1:
            targetRoom = " ".join([word.capitalize() for word in move[1].split()])
            if targetRoom.lower() in (room.lower() for room in rooms):
                currentRoom = targetRoom
                print(crayons.yellow("You have been teleported to the {currentRoom}.", bold=True))
            else:
                print("Teleportation failed.")
        else:
            # If they typed teleport and hit enter without a location
            while True:
                print(crayons.yellow("Please specify a location to teleport or type 'cancel' to abort teleportation:", bold=True))
                targetRoom = input("> ").capitalize()
                if targetRoom.lower() == "cancel":
                    print(crayons.yellow("Teleportation canceled.", bold=True))
                    break
                elif targetRoom in rooms:
                    currentRoom = targetRoom
                    print(crayons.yellow("You have been teleported to {currentRoom}.", bold=True))
                    break
                else:
                    print(crayons.yellow("The room does not exist. Pleas try again or type 'cancel' to abort.", bold=True))
    #if they type "get" first
    if move[0] == "get":
        # make two checks:
        # 1. if the current room contains an item
        # 2. if the item in the room matches the item the player wishes to get
        if "item" in rooms[currentRoom]:
            room_items = rooms[currentRoom]["item"]
            # Check if room_items is a list and if item is in the list
            ## if isinstance(room_items, list) and move[1] in [item.lower() for item in room_items]:
            if isinstance(room_items, list):
                requested_item = move[1].lower()
                normalized_items = [item.lower() for item in room_items]
                if requested_item in normalized_items:
                    # Get the original item name from the room_items list
                    original_item_name = room_items[normalized_items.index(requested_item)]
                    inventory.append(original_item_name)
                    print(crayons.green(original_item_name + " acquired!", bold=True))
                # Find the item's index in the list
                ## item_index = [item.lower() for item in room_items].index(move[1])
                # Add the item to their inventory
                ## inventory.append(room_items[item_index])
                # Display a helpful message
                ## print(crayons.green(room_items[item_index], bold=True) + " aquired!")
                # Remove the item from the room's list
                ## del room_items[item_index]
                    room_items.remove(original_item_name)
                # If list is empty, remove the 'item' atrribute from the room
                    if not room_items:
                        del rooms[currentRoom]["item"]
                else:
                    print(crayons.red("Can't get " + move[1] + "!", bold=True))
            else:
                # If the item is a singel string
                # Add the item to inventory
                inventory.append(room_items)
                # Display a helpful message
                print(crayons.green(room_items, bold=True) + "acuired!")
                # Delete the item key:value pair from the room's dictionary
                if "item" in rooms[currentRoom]:
                    del rooms[currentRoom]["item"]
        # if there"s no item in the room or the item doesn"t match
        else:
            #tell them they can"t get it
            print(crayons.red("Can't get " + move[1] + "!", bold=True))

        ## If a player enters a room with a monster
        ## Define how a player can win

    if currentRoom == "Courtyard" and "Red Dragon" in rooms[currentRoom]["item"]:
        in_combat = True
        print(f"{crayons.yellow("You have encountered the", bold=True)} {crayons.red("Red Dragon", bold=True)}!")

        while in_combat:
            print(f"Dragon Health {dragon_health}, Garion\"s Health {player_health}")
            print(f"Do you want to (1) {crayons.red("Attack", bold=True)} or (2) use a {crayons.green("Health Potion?", bold=True)}")
            action = input("> ").strip()
        
            if action == "1":
                # Attack the dragon
                if any("Mage Staff" == item for item in inventory) and any ("Spell Scroll: Maelstrom" == item for item in inventory):
                    dragon_health -= 333 # Dragon loses a third of it"s health
                    print(f"You use your {crayons.green("Mage Staff", bold=True)} and the {crayons.green("Spell Scroll: Maelstrom", bold=True)} against the {crayons.red("Red Dragon", bold=True)}...")
                    time.sleep(1)
                    print("Causing significant damage!")
                    time.sleep(1)
                    if dragon_health <= 0:
                        print(f"{crayons.yellow("The", bold=True)} {crayons.red("Red Dragon", bold=True)} {crayons.yellow("has been defeated!", bold=True)}")
                        time.sleep(1)
                        print(crayons.blue("Peace and balance have finally been restored in the Kingdom...", bold=True))
                        time.sleep(1)
                        print(crayons.blue("Garion's tale to be continued...", bold=True))
                        del rooms[currentRoom]["item"]
                        in_combat = False
                        exit()
                    
                elif ["Mage Staff"] not in inventory and ["Spell Scroll: Maelstrom"] not in inventory:
                    print(f"{crayons.yellow("You do not posses the required magical items to defeat the", bold=True)} {crayons.red("Red Dragon", bold=True)}")
                    time.sleep(1)
                    print(crayons.yellow("Turn back!", bold=True))
                    time.sleep(1)
                    in_combat = False
                    continue

                # Dragon attacks back
                player_health -= 50
                print(f"The {crayons.red("Red Dragon", bold=True)} retaliates, hurling a {crayons.red("Fire Ball", bold=True)} causing severe damage to you!")
                if player_health <= 0:
                    print(f"The {crayons.red("Red Dragon", bold=True)} engulfs you in fire!")
                    time.sleep(1)
                    print(crayons.yellow("You have been defeated...", bold=True))
                    time.sleep(1)
                    print(crayons.red("Game Over!", bold=True))
                    exit()

            elif action == "2":
                if "Health Potion x3" in inventory:
                    player_health += 50 # Each potion restores 50 health
                    print(f"You quickly consume a {crayons.green("Health Potion", bold=True)}, restoring your health.")
                    inventory.append("Health Potion x2")
                    inventory.remove("Health Potion x3")
                elif "Health Potion x2" in inventory:
                    player_health += 50
                    print(f"You quickly consume a {crayons.green("Health Potion", bold=True)}, restoring your health.")
                    inventory.append("Health Potion x1")
                    inventory.remove("Health Potion x2")
                elif "Health Potion x1" in inventory:
                    player_health += 50
                    print(f"You quickly consume a {crayons.green("Health Potion", bold=True)}, restoring you health.")
                    inventory.remove("Health Potion x1")
                elif "Health Potion x3" not in inventory or "Health Potion x2" not in inventory or "Health Potion x1" not in inventory:
                    print(f"{crayons.yellow("You don't have any", bold=True)} {crayons.green("Health Potions", bold=True)} {crayons.yellow("left!", bold=True)}")
                    time.sleep(1)
                    
                    

        # This check prevents the loop from immediatly prompting again without showing the outcome of the action
        if in_combat:
            print(f"{crayons.red("Red Dragon's")} health is now {dragon_health}. Your health is now {player_health}")
