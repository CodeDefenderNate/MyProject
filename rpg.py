#!/usr/bin/python3
"""Garion: The Child of Light - RPG game | Nathan Haley"""
import crayons
import time
import random
import json
from fuzzywuzzy import fuzz

player_health = 100 # Starting health for the player
dragon_health = 1000 # Starting health for the dragon
health_restore_amount = 50 # Health Potions restore 50 health
inventory = {}

def slow_print(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print() # To ensure it contiues to print on a new line

def showInstructions():
    """Show the game instructions when called"""
    #slow_print a main menu and the commands
    slow_print(crayons.green("""
    Garion: The Child of Light""", bold=True))
    slow_print(crayons.yellow("""==================================
    Commands:
      go [direction]
      get [item]
      use [item]
      showspells
    """, bold=True))

def showStatus():
    """determine the current status of the player"""
    # slow_print the player"s current location
    print("---------------------------")
    slow_print("You are in the " + crayons.magenta(str(currentRoom), bold=True))
    # slow_print what the player is carrying
    inventory_text = crayons.blue("Inventory:", bold=True) + " " + crayons.green(str(inventory), bold=True)
    print(inventory_text)
    ##slow_print(crayons.blue("Inventory:", bold=True), crayons.green(str(inventory), bold=True))
    # check if there"s an item in the room, if so slow_print it
    if "item" in rooms[currentRoom]:
        room_item = rooms[currentRoom]["item"]
        if isinstance(room_item, list):
            room_item = ", ".join(map(str, room_item))
        slow_print("There is a " + crayons.green(str(room_item), bold=True))
    print("---------------------------")

def fuzzy_match(input_str, valid_options, threshold=70):
    best_match = None
    max_score = 0
    for option in valid_options:
        score = fuzz.partial_ratio(input_str.lower(), option.lower())
        if score > max_score:
            max_score = score
            best_match = option
    if max_score >= threshold:
        return best_match
    else:
        return None

def useSpell(spell_name):
    """Add the spell to the player's spell list and remove spell scrolls from inventory"""
    spell_name = spell_name.lower() 
    if spell_name.startswith("spell scroll: ") and spell_name in [item.lower() for item in inventory]:
        spell_name = spell_name.replace("spell scroll: ", "").title()
        if spell_name in spells:
            slow_print(f"You already know the spell {spell_name}!")
        else:
            spells.append(spell_name)
            inventory.remove(f"Spell Scroll: {spell_name}")
            slow_print(crayons.yellow("You have learned the spell: ", bold=True) + crayons.blue(str(spell_name) + crayons.yellow("!", bold=True), bold=True))
    else:
        slow_print(crayons.red("You can't use that item!", bold=True))

def showSpells():
    """Display the known spells"""
    if spells:
        slow_print(crayons.yellow("You know the following spells:", bold=True))
        for spell in spells:
            slow_print(crayons.green(spell))
    else:
        slow_print(crayons.red("You don't know any spells yet!", bold=True))

# List to store learned spells
spells = []

# An inventory, which is initially empty
inventory = []

# A list of dragon attacks to be randomly chosen
dragon_attacks = ["Fire Breath", "Fireball", "Tail Whip", "Claw Swipe", "Bite", "Stomp"] 

# a dictionary linking a room to other rooms
rooms = {

            "Great Hall" : {
                  "north" : "North Wing",
                  "south" : "South Wing",
                  "east" : "East Wing",
                  "west" : "West Wing"
                },

            "Courtyard" : { # Changed to require a key
                  "north" : "Dragon's Lair",
                  "south" : "North Wing",
                  "east" : "Library",
                  "west" : "Kitchen"
                },

            "Dragon's Lair" : {
                  "south" : "Courtyard",
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
                  "north" : "Courtyard", # Changed to require a key
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
previousRoom = None

showInstructions()

def main():
    global currentRoom, previousRoom, player_health, dragon_health, inventory, spells

# breaking this while loop means the game is over
    while True:
        showStatus()
        move = input("> ").lower().split(" ", 1)
    # the player MUST type something in
    # otherwise input will keep asking

        if move[0] == "use":
            if len(move) > 1:
                useSpell(move[1])
            else:
                slow_print(crayons.yellow("Please specify which item to use.", bold=True))

        elif move[0] == "showspells":
            showSpells()

        #if they type "go" first
        if move[0] == "go":
            direction = move[1]
            if direction in rooms[currentRoom]:
                previousRoom = currentRoom

            if direction in rooms[currentRoom]:
                if direction == "north" and currentRoom == "North Wing" and "Key" not in inventory:
                    slow_print(crayons.red("The door is locked. You need Key to enter the Courtyard", bold=True))
                elif direction == "east" and currentRoom == "Kitchen" and "Key" not in inventory:
                    slow_print(crayons.red("The door is locked. You need a Key to enter the Courtyard", bold=True))
                elif direction == "west" and currentRoom == "Library" and "Key" not in inventory:
                    slow_print(crayons.red("The door is locked. You need a Key to enter the Courtyard", bold=True))
                else:
                    currentRoom = rooms[currentRoom][direction]
                    slow_print("You go to the " + currentRoom + ".")
            else:
                slow_print(crayons.yellow("You can't go that way", bold=True))
        # Teleporting for developer       
        if move[0] == "teleport":
            if len(move) > 1:
                targetRoom = " ".join([word.capitalize() for word in move[1].split()])
                if targetRoom.lower() in (room.lower() for room in rooms):
                    currentRoom = targetRoom
                    slow_print(f"You have been teleported to the {currentRoom}.")
                else:
                    slow_print(crayons.red("Teleportation failed.", bold=True))
            else:
                # If they typed teleport and hit enter without a location
                while True:
                    slow_print(crayons.yellow("Please specify a location to teleport or type 'cancel' to abort teleportation:", bold=True))
                    targetRoom = input("> ").capitalize()
                    if targetRoom.lower() == "cancel":
                        slow_print(crayons.yellow("Teleportation canceled.", bold=True))
                        break
                    elif targetRoom in rooms:
                        currentRoom = targetRoom
                        slow_print(f"You have been teleported to {currentRoom}.")
                        break
                    else:
                        slow_print(crayons.yellow("The room does not exist. Pleas try again or type 'cancel' to abort.", bold=True))
        #if they type "get" first
        if move[0] == "get":
        # make two checks:
        # 1. if the current room contains an item
        # 2. if the item in the room matches the item the player wishes to get
            if "item" in rooms[currentRoom]:
                room_items = rooms[currentRoom]["item"]
            
            # Check if room_items is a list and if item is in the list
                if isinstance(room_items, list):
                    requested_item = move[1].lower()
                    normalized_items = [item.lower() for item in room_items]
                    if requested_item in normalized_items:
                    # Get the original item name from the room_items list
                        original_item_name = room_items[normalized_items.index(requested_item)]
                        inventory.append(original_item_name)
                        slow_print(crayons.green(original_item_name + " acquired!", bold=True))
                        room_items.remove(original_item_name)
                
                # If list is empty, remove the 'item' atrribute from the room
                        if not room_items:
                            del rooms[currentRoom]["item"]
                    else:
                        slow_print(crayons.red("Can't get " + move[1] + "!", bold=True))
                else:
                # If the item is a singel string
                # Add the item to inventory
                    inventory.append(room_items)
                # Display a helpful message
                    slow_print(crayons.green(room_items, bold=True) + "acuired!")
                # Delete the item key:value pair from the room's dictionary
                    if "item" in rooms[currentRoom]:
                        del rooms[currentRoom]["item"]
            # if there"s no item in the room or the item doesn"t match
            else:
            #tell them they can"t get it
                slow_print(crayons.red("Can't get "  + move[1] + "!", bold=True))

        # If a player enters a room with a monster
        # Define how a player can win

        if currentRoom == "Dragon's Lair" and "Red Dragon" in rooms[currentRoom]["item"]:
            if "Mage Staff" in inventory and spells:
                in_combat = True
                slow_print(f"{crayons.yellow("You have encountered the", bold=True)} {crayons.red("Red Dragon", bold=True)}{crayons.yellow("!", bold=True)}")
            else:
                in_combat = False
                if "Mage Staff" not in inventory:
                        slow_print(crayons.red("You do not posses the required magical items to defeat the Red Dragon!", bold=True))
                        time.sleep(1)
                    #slow_print(crayons.yellow("Turn back!"))
                if not spells:
                    slow_print(crayons.red("You need to learn at least one spell to cast!", bold=True))
                    time.sleep(1)
                slow_print(crayons.yellow("Turn back!"))
                currentRoom = previousRoom
                continue

            while in_combat:
                slow_print(f"Dragon Health {dragon_health}, Garion\'s Health {player_health}")
                slow_print(f"Do you want to (1) {crayons.red("Attack", bold=True)} or (2) use a {crayons.green("Health Potion?", bold=True)}")
                action = input("> ").strip()
        
                if action == "1":
                    # Attack the dragon
                        # Spell choice
                            slow_print(crayons.yellow("Choose a spell to cast:"))
                            time.sleep(1)
                            for idx, spell in enumerate(spells, start=1):
                                slow_print(f"{idx}. {spell}")
                            spell_choice = input("> ").strip()

                            try:
                                spell_idx = int(spell_choice) - 1
                                if 0 <= spell_idx < len(spells):
                                    selected_spell = spells[spell_idx]
                                    spell_damage = random.randint(200, 400)
                                    dragon_health -= spell_damage
                                    slow_print(crayons.yellow("You cast ") + crayons.blue(selected_spell) + crayons.yellow(" and deal ") + str(spell_damage) + crayons.yellow(" damage to the ") + crayons.red("Red Dragon") + crayons.yellow("!", bold=True))
                                
                                    if dragon_health > 0:
                                        dragon_attack = random.choice(dragon_attacks)
                                        dragon_damage = random.randint(30, 60)
                                        player_health -= dragon_damage
                                        slow_print(crayons.yellow("The ") + crayons.red("Red Dragon ") + crayons.yellow("attacks you with ") + crayons.red(dragon_attack ) + crayons.yellow(" and deals ") + crayons.yellow(str(dragon_damage)) + crayons.yellow(" damage!", bold=True))

                                else:
                                    slow_print(crayons.yellow(f"Invalid spell choice. Please select a valid spell number.", bold=True))
                            except ValueError:
                                slow_print(crayons.yellow("Invalid input. Pleast enter the number corresponding to your your chosen spell", bold=True))

                # Using Health Potions
                elif action == "2":
                    if "Health Potion x3" in inventory:
                        player_health += health_restore_amount
                    
                        if player_health > 100:
                            player_health = 100 # Each potion restores 50 health
                        slow_print(crayons.yellow("You quickly consume a ") + crayons.green("Health Potion ") + crayons.yellow("restoring your health.", bold=True))
                        inventory.append("Health Potion x2")
                        inventory.remove("Health Potion x3")

                    elif "Health Potion x2" in inventory:
                        player_health += health_restore_amount

                        if player_health > 100:
                            player_health = 100
                        slow_print(crayons.yellow("You quickly consume a ") + crayons.green("Health Potion ") + crayons.yellow("restoring your health.", bold=True))
                        inventory.append("Health Potion x1")
                        inventory.remove("Health Potion x2")
                    
                    elif "Health Potion x1" in inventory:
                        player_health += health_restore_amount

                        if player_health > 100:
                            player_health = 100
                        slow_print(crayons.yellow("You quickly consume a ") + crayons.green("Health Potion ") + crayons.yellow("restoring your health.", bold=True))
                        inventory.remove("Health Potion x1")
                    
                    elif "Health Potion x3" not in inventory or "Health Potion x2" not in inventory or "Health Potion x1" not in inventory:
                        slow_print(f"{crayons.yellow("You don't have any", bold=True)} {crayons.green("Health Potions", bold=True)} {crayons.yellow("left!", bold=True)}")
                        time.sleep(1)
                        pass
                
                if dragon_health <= 0:
                    slow_print(crayons.yellow("The ") + crayons.red("Red Dragon ") + crayons.yellow("has been defeated!\n") + crayons.green("Peace has been restored to the Kingdom!", bold=True))
                    del rooms[currentRoom]["item"]
                    player_choice = input(crayons.yellow("Would you like to start a new game?") + crayons.green(" yes/no): ", bold=True)).strip().lower()

                    if player_choice == "yes":
                        player_health = 100
                        dragon_health = 1000
                        inventory = []
                        spells = []
                        currentRoom = "Great Hall"

                        showInstructions()

                    elif player_choice == "no":
                        slow_print(crayons.yellow("Garion's journey to be continued...",bold=True))
                        exit()
                    else:
                        slow_print(crayons.red("Invalid option. Exiting the game.", bold=True))
                        exit()

                if player_health <= 0:
                    slow_print(crayons.red("You have been defeated by the Red Dragon...\n GAME OVER!", bold=True))                    
                # Ask the player if they want to start a new game or exit
                    player_choice = input(crayons.yellow("Would you like to start a new game?") + crayons.green(" yes/no): ", bold=True)).strip().lower()


                    if player_choice == "yes":
                        player_health = 100
                        dragon_health = 1000
                        inventory = []
                        spells = []
                        currentRoom = "Great Hall"

                        showInstructions()

                    elif player_choice == "no":
                        slow_print(crayons.green("Garion's journey to be continued...",bold=True))
                        exit()
                    else:
                        slow_print(crayons.red("Invalid option. Exiting the game.", bold=True))
                        exit()

if __name__ == "__main__":
    main()                    
