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
dragon_attacks = ["Fire Breath", "Fireball", "Tail Whip", "Claw Swipe", "Bite", "Stomp"] # A list of dragon attacks to be randomly chosen
inventory = {}
spells = []
rooms = {}
dragon_defeated = False

def slow_print(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print() # To ensure it contiues to print on a new line

def showInstructions():
    """Show the game instructions when called"""
    #slow_print a main menu and the commands
    slow_print(crayons.cyan("""
    Garion: The Child of Light""", bold=True))
    slow_print(crayons.green("""==================================
    Commands:
      go [direction]
      use [item]
      showspells
    """, bold=True))

def initializeRooms():
    global rooms
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
                  "item" : {"Health Potion": 3}
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

def getItem(itemName, quantity=1):
    global inventory
    # Update the player's inventory with the specified quantity of the item.
    inventory[itemName] = inventory.get(itemName, 0) + quantity

    # Inform the player of the pickup.
    if quantity > 1:
        message = f"You picked up {quantity} of {itemName}"
    else:
        message = f"You picked up {itemName}"
    slow_print(crayons.yellow(message))

def showStatus():
    global currentRoom
    room = rooms[currentRoom]
    print("---------------------------")
    slow_print("You are in the " + crayons.magenta(str(currentRoom), bold=True))

    inventory_text = "Inventory: " + ", ".join([f"{crayons.green(item)}: {crayons.blue(str(count))}" for item, count in inventory.items()])
    print(crayons.blue(inventory_text, bold=True))

    if "item" in room:
        room_item = room["item"]
        items_to_remove = []

        if isinstance(room_item, dict):
            for item, quantity in room_item.items():
                if promptForItem(item, quantity):
                    getItem(item, quantity)
                    items_to_remove.append(item)

        elif isinstance(room_item, list):
            for item in list(room_item):  # Convert to list to make a copy for safe iteration
                if promptForItem(item):
                    getItem(item)
                    items_to_remove.append(item)

        elif isinstance(room_item, str):
            if promptForItem(room_item):
                getItem(room_item)
                items_to_remove.append(room_item)

        # Perform removal outside of iteration
        for item in items_to_remove:
            if isinstance(room_item, dict):
                room_item.pop(item, None)
            elif isinstance(room_item, list):
                room_item.remove(item)

        if not room_item:
            del room["item"]

    print("---------------------------")

def promptForItem(item, quantity=1):
    """Prompt the player to pick up an item."""
    slow_print(crayons.cyan("You see a " + crayons.green(item)))
    item_prompt = crayons.cyan("Do you want to pick up the ") + crayons.green(f"{item} ({quantity})" if quantity > 1 else item) + crayons.cyan("? ") + crayons.yellow("(yes/no): ", bold=True)
    print(item_prompt, end="")
    return input().lower() == "yes"

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
    # Normalize the input ot ensure consistent formatting
    normalized_spell_name = spell_name.lower()

    # Construct the inventory key to look for 
    spell_scroll_key = f"Spell Scroll: {normalized_spell_name.title()}"
    
    # Check if Spell Scroll is in the inventory
    if spell_scroll_key in inventory and inventory[spell_scroll_key] > 0:
        # Remove the "Spell Scroll: " prefix and capitalize the first letter of each word for the spell name
        clean_spell_name = ' '.join([word.capitalize() for word in normalized_spell_name.split()])

        # Add the spell to the spells list
        if clean_spell_name not in spells:
            spells.append(clean_spell_name)
            inventory[spell_scroll_key] -= 1 # Decrement the count of Spell Scrolls

            # If the count reaches 0, remove the Spell Scroll from the inventory
            if inventory[spell_scroll_key] == 0:
                del inventory[spell_scroll_key]
            slow_print(crayons.cyan("You have learned the spell: ", bold=True) + crayons.blue(clean_spell_name + crayons.cyan("!", bold=True)))
        else:
            slow_print(crayons.red("You have already learned: ", bold=True) + crayons.blue(str(spell_name) + crayons.cyan("!", bold=True)))
    else:
        slow_print(crayons.red("You don't have that Spell Scroll!", bold=True))

def showSpells():
    global spells
    """Display the known spells"""
    if spells:
        slow_print(crayons.cyan("You know the following spells:", bold=True))
        for spell in spells:
            slow_print(crayons.green(spell))
    else:
        slow_print(crayons.red("You don't know any spells yet!", bold=True))

def handleMovement(direction):
    global currentRoom, previousRoom
    if direction == "north" and currentRoom == "North Wing" or \
       direction == "east" and currentRoom == "Kitchen" or \
       direction == "west" and currentRoom == "Library":
        if "Key" in inventory: # Check for Key in inventory
            currentRoom = "Courtyard"
            slow_print(crayons.cyan("You use the ") + crayons.green("Key") + crayons.cyan(" to enter the Courtyard.", bold=True))
        else:
            slow_print(crayons.red("The door is locked. You need a Key to enter the Couryard.", bold=True))
            return # Exits the function early if there is no Key in the inventory
        
    elif direction in rooms[currentRoom]:
        previousRoom = currentRoom # Save the current room before moving
        currentRoom = rooms[currentRoom][direction]
    else:
        slow_print(crayons.red("You can't go that way!", bold=True))
        return

    if currentRoom == "Dragon's Lair":
        encounterDragon()

def encounterDragon():
    global player_health, dragon_health
    if "Mage Staff" in inventory and len(spells) > 0:
        fightDragon()
    else:
        if "Mage Staff" not in inventory:
            slow_print(crayons.red("You do not posses the required magical items to defeat the Red Dragon!", bold=True))
        if len(spells) == 0:
            slow_print(crayons.red("You need to learn at least one spell to cast!", bold=True))
        slow_print(crayons.yellow("Turn back!", bold=True))
        returnToPreviousRoom()

def returnToPreviousRoom():
    global currentRoom, previousRoom
    currentRoom = previousRoom
    previousRoom = None # Reset previousRoom after returning

def useHealthPotion():
    global player_health, inventory
    max_health = 100

    potion_key = "Health Potion"
    if inventory.get(potion_key, 0) > 0:
        player_health = min(player_health + health_restore_amount, 100) # Ensures health doesn't exceed 100
        inventory[potion_key] -= 1 # Use one potion
        slow_print(crayons.cyan("You quickly consume a ") + crayons.green("Health Potion") + crayons.cyan(", restoring your health.", bold=True))
        if inventory[potion_key] == 0:
            del inventory[potion_key]  # Remove the item from inventory if quantity is 0
    else:
        slow_print(crayons.red("You don't have any Health Potions left!", bold=True))

def fightDragon():
    global dragon_health, player_health, spells, inventory, currentRoom, rooms, dragon_defeated
    slow_print(f"{crayons.cyan("You have encountered the", bold=True)} {crayons.red("Red Dragon", bold=True)}{crayons.cyan("!", bold=True)}")

    # Continue the fight while both have health
    while dragon_health > 0 and player_health > 0:
        slow_print(f"Dragon Health {dragon_health}, Garion\'s Health {player_health}")
        slow_print(f"Do you want to (1) {crayons.red("Attack", bold=True)} or (2) use a {crayons.green("Health Potion?", bold=True)}")
        action = input(">").strip()
        
        if action == "1":
            # Attack the dragon
                # Spell choice
                    slow_print(crayons.yellow("Choose a spell to cast:"))
                    time.sleep(1)
                    for idx, spell in enumerate(spells, start=1):
                        print(f"{idx}. {spell}")
                    spell_choice = input("> ").strip()

                    try:
                        spell_idx = int(spell_choice) - 1
                        if 0 <= spell_idx < len(spells):
                            selected_spell = spells[spell_idx]
                            spell_damage = random.randint(200, 400)
                            dragon_health -= spell_damage
                            slow_print(crayons.cyan("You cast ") + crayons.blue(selected_spell) + crayons.cyan(" and deal ") + crayons.yellow(str(spell_damage)) + crayons.cyan(" damage to the ") + crayons.red("Red Dragon") + crayons.cyan("!", bold=True))
                                
                            if dragon_health > 0:
                                dragon_attack = random.choice(dragon_attacks)
                                dragon_damage = random.randint(30, 60)
                                player_health -= dragon_damage
                                slow_print(crayons.cyan("The ") + crayons.red("Red Dragon ") + crayons.cyan("attacks you with ") + crayons.red(dragon_attack ) + crayons.cyan(" and deals ") + crayons.yellow(str(dragon_damage)) + crayons.cyan(" damage!", bold=True))

                        else:
                            slow_print(crayons.yellow(f"Invalid spell choice. Please select a valid spell number.", bold=True))
                    except ValueError:
                        slow_print(crayons.yellow("Invalid input. Pleast enter the number corresponding to your your chosen spell", bold=True))
                        continue

        elif action == "2":
            useHealthPotion()
                
        if dragon_health <= 0:
            dragon_defeated = True
##            slow_print(crayons.cyan("The ") + crayons.red("Red Dragon ") + crayons.cyan("has been defeated!\n") + crayons.green("Peace has been restored to the Kingdom!", bold=True))
##            del rooms[currentRoom]["item"]
##            player_choice = input(crayons.cyan("Would you like to start a new game?") + crayons.yellow(" (yes/no): ", bold=True)).strip().lower()
##            checkGameOver(True) # Victory
##        elif player_health <= 0:
##             slow_print(crayons.red("You have been defeated by the Red Dragon...\n GAME OVER!", bold=True))
##            checkGameOver(False)
##            break
##            if player_choice == "yes":
##                resetGame()

##            elif player_choice == "no":
##                slow_print(crayons.green("Garion's journey to be continued...",bold=True))
##                exit()
##            else:
##                slow_print(crayons.red("Invalid option. Exiting the game.", bold=True))
##                exit()

##        if player_health <= 0:
##            slow_print(crayons.red("You have been defeated by the Red Dragon...\n GAME OVER!", bold=True))                    
                # Ask the player if they want to start a new game or exit
##            player_choice = input(crayons.cyan("Would you like to start a new game?") + crayons.yellow(" (yes/no): ", bold=True)).strip().lower()


##            if player_choice == "yes":
##                resetGame()

##            elif player_choice == "no":
##                slow_print(crayons.green("Garion's journey to be continued...",bold=True))
##                exit()
##            else:
##                slow_print(crayons.red("Invalid option. Exiting the game.", bold=True))
##                exit()

def checkGameOver(victory):
    global currentRoom, rooms, player_health, dragon_health, inventory, spells, dragon_defeated  # Declare globals if they're manipulated
    
    if victory:
        slow_print(crayons.cyan("The ") + crayons.red("Red Dragon ") + crayons.cyan("has been defeated!\n") + crayons.green("Peace has been restored to the Kingdom!", bold=True))
    else:
        slow_print(crayons.red("You have been defeated..."))
##    slow_print(message))
##    message = crayons.cyan("The ") + crayons.red("Red Dragon ") + crayons.cyan("has been defeated!\n") + crayons.green("Peace has been restored to the Kingdom!", bold=True)
##    slow_print(message)
    choice = input("Star a New Game? (yes/no): ").lower()
##    player_choice = input("Game Over. Start a new game? (yes/no): ").lower()
    if choice == "yes":
        return True
    else:
        return False
##    else:
##        slow_print(crayons.green("Garion's journey to be continued...",bold=True))
##        exit()


def resetGame():
    global player_health, dragon_health, inventory, spells, currentRoom, rooms
    player_health = 100
    dragon_health = 1000
    inventory = {}
    spells = []
    currentRoom = "Great Hall"
##    initializeGame()
    initializeRooms()
##    slow_print(crayons.cyan("A new journey begins...", bold=True))
    showInstructions()

    # Reset the game world to its initial state

def initializeGame():
    global player_health, dragon_health, inventory, spells, currentRoom, rooms, dragon_defeated
    player_health = 100
    dragon_health = 1000
    inventory = {}
    spells = []
    currentRoom = "Great Hall"
    initializeRooms()  # This will set up the rooms dictionary.
##    slow_print(crayons.cyan("A new journey begins...", bold=True))
    showInstructions()

# start the player in the Hall
currentRoom = "Great Hall"
previousRoom = None

def main():
    global currentRoom, previousRoom, player_health, dragon_health, inventory, spells, game_running, dragon_defeated
    game_running = True
    
    while game_running:
        initializeGame()
        dragon_defeated = False
##teleport southwest guard tower
##        showInstructions()


# breaking this while loop means the game is over
        while not dragon_defeated and player_health > 0:
            showStatus()
            move = input(">").lower().split(" ", 1)
            if len(move) < 2:
                print(crayons.yellow("Need more input."))
                continue

            if player_health <= 0 or dragon_defeated:
                game_running = checkGameOver(dragon_defeated)
                if game_running:
                    initializeGame()
    # the player MUST type something in
    # otherwise input will keep asking

            command, argument = move[0], (move[1] if len(move) > 1 else "")
##        if move[0] == "use":
            if command == "use":
                useSpell(argument)
##            if len(move) > 1:
##                useSpell(move[1])
##            else:
##                slow_print(crayons.yellow("Please specify which item to use.", bold=True))

            elif command == "showspells":
                showSpells()

##        if move[0] == "go" and len(move) > 1:
            elif command == "go":
             handleMovement(argument)

            elif command == "get":
                getItem(argument)

            elif command == "attack":
                fightDragon()

            elif command == "heal potion":
                useHealthPotion()

##            if command == "gameover":
##                checkGameOver(False)

            if player_health <= 0:
                game_running = checkGameOver(False)
            elif dragon_defeated:
                game_running =checkGameOver(True)

            if not game_running:
                slow_print(crayons.green("Garion's journey to be continued...", bold=True))

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
                            slow_print(crayons.red("Teleportation canceled.", bold=True))
                            break
                        elif targetRoom in rooms:
                            currentRoom = targetRoom
                            slow_print(f"You have been teleported to {currentRoom}.")
                            break
                        else:
                            slow_print(crayons.yellow("The room does not exist. Pleas try again or type 'cancel' to abort.", bold=True))

if __name__ == "__main__":
    main()                    
