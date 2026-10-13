"""
Ciacco's Submarket
Author: Kyle DeJong
Version: 1.0

A single-file Python text adventure set in a fictional supermarket ("submarket").
The player navigates interconnected departments, encounters collectible items,
and can reach different endings depending on exploration and player choices.
"""

#Instructions on all valid player commands
def navigate_options():
    #All valid moves, add-to as needed
    directions = ("go North", "go South", "go East", "go West")
    print("\nINSTRUCTIONS:\nEnter any of the following exactly, without quotes.", end="")
    print("\nMovement: ", end = "")
    for i in directions:
        print("\"" + i, end="\"| ")
    print("\nItem Pickup: \"get <Item Name>\".", end ="\n")

#A nested dictionary containing all rooms, connectors, and their directions
#Format: Key:{Key:Value}
rooms = {
    "Entrance":{"North":"Bakery", "East":"Liquor"},
    "Liquor":{"West":"Entrance"},
    "Bakery":{"South":"Entrance", "North":"Vegetables", "East":"Toiletries"},
    "Vegetables":{"South":"Bakery", "East":"Butcher", "West":"Dairy", "North":"Snacks"},
    "Dairy":{"North":"Bathroom", "East":"Vegetables"},
    "Bathroom":{"South":"Dairy", "East":"Snacks"},
    "Snacks":{"West":"Bathroom", "South":"Vegetables"},
    "Toiletries":{"North":"Butcher", "West":"Bakery"},
    "Butcher":{"West":"Vegetables", "South":"Toiletries", "North":"Lottery Desk", "East":"Exit"},
    "Lottery Desk":{"South":"Butcher"},
    "Exit":{"West":"Butcher"}
}

#Dict of all game items by room key, valid synonyms, descriptions before and after being taken, and a boolean to track status
#Format: Key:[Name, Synonyms, Description, Description if Taken, bool Taken]
items = {
    "Entrance":["Nothing",
                ["Nothing", "nothing"],
                "Anticipation rattles your teeth like coins in a can. Consumption is imminent, resign yourself.",
                "Having successfully taken nothing, in a most peculiar way, you find your cupidity mildly sated, yet highly annoyed. It balks at your trickery.",
                True
    ],
    "Liquor":["Bottom Shelf Spirits",
              ["Bottom Shelf Spirits","spirits","spirit","liquor","booze","alcohol"],
              "The organic matter used to ferment the contents of this plastic jug is irrelevant. It's cheap, it's strong, and it'll lift you very high before the cruel betrayal.",
              "There is a void among the lower reaches. A missing soldier among teary comrades. But libations were poured for him, or from, and isn't that honor enough?",
              True
              ],
    "Bakery":["Cheap Bread",
              ["Cheap Bread","bread","loaf of bread","loaf"],
              "The great seperator of man and beast, the first fruits of agriculture, the daily reward promised for toil. Only $1.50 a loaf, sweetened with corn syrup, with a cartoon dog on the bag.",
              "A bounty of grains even great kings would marvel at, and you greater than them all, for you have taken a loaf and refused the rest. Nobility personified. The end pieces will go to ducks.",
              True
              ],
    "Vegetables":["Potato Bag",
                 ["Potato Bag","potato", "potatoes", "spuds","bag"],
                 "Fresh from the fertile soil of Idaho, a bonanza of carbs and calories. Man may live on bread alone, but as tubers relax among kin, you know the truth lay beneath the dirt. Grains are overrated.",
                 "What a hardworking farmer has pulled from an earthen womb, you have mirrored with the 5 lb. bag of spuds. Destiny came calling for #09194398F, and being slightly over-microwaved and slathered in sour cream awaits.",
                 True
                 ],
    "Dairy":["Skim Milk",
             ["Skim Milk","milk", "skim"],
             "The secrets of the pastoral nomads have been laid bare. Among their pilfered goods, a blue cap of white sustenance. Only 2% fat, therefore, it must be healthier than foul, whole milk. Though how the drink of life "+
             "can be forced into separate parts, and insulating excess torn away, is yet another mystery of the Indo-Scythians.",
             "The gallon jug is going to be more watery and taste worse. But what you're pretty sure are health benefits are reassured by the soothing blue cap against the irritated reds.",
             True
             ],
    "Bathroom":["Spray Cleaner",
                ["Spray Cleaner","cleaner", "spray"],
                "It occurs to you, as you take in the wonderous sights, sounds, and smells of a submarket public bathroom, that the mostly full bottle of spray cleaner is unlikely to ever be used again. "+
                "The label has also been melted to away from its own contents, a mark of high quality cleaning solution. The bottle deserves a home that cares for its chemical potency.",
                "The sole clean patch of space in the bathroom was the area where the cleaner once sat in stasis. You have done a good deed today, though sterilizing your hands with some of the fluid may be wise.",
                True
                ],
    "Snacks":["Flavored Chips",
              ["Flavored Chips","chips", "bag", "chip bag"],
              "The shining bag of a processed vegetable dusted in flavor powder is your favorite kind. Memories of childhood at gatherings or while watching TV call for you, a siren to its favorite ship too sturdy to dash upon rocks. "+
              "The crinkle when you take it will be just as sweet as the first, the perfectly engineered bursts of flavor just as intense. You will never age or die.",
              "And so it was. Immortality puffed your head like a room fan turning, and it was all you ever hoped for. This calls for making your grandpa's dip recipe tonight!",
              True
              ],
    "Toiletries":["Branded Toilet Paper",
                  ["Branded Toilet Paper","toilet paper", "toilet", "paper", "brand"],
                  "Promises of quantity and comfort abound. But you are too discerning to fall for the lies in this most vital matter. You turn your nose at the false shepherds, and make haste towards the trustworthy products you see on TV.",
                  "You have walked the valley of scratchy irritation and come away clean. The powers of discernment favor you, for all the angry glares of the unchosen prove your wisdom in the plush rolls that will deliver you.",
                  True,
                  ],
    "Butcher":["Ground Beef",
               ["Ground Beef","ground","beef"],
               "A great beast laid low. The herd culled by one, expertly butchered, and ran through a mighty grinder. All to lay before you, quivering and bleeding in supplication for a masterful hunter to sup upon.",
               "The price of a pound of ground beef is higher than you remember it being years ago. You should complain to people about it. How expensive can a grass-eating cow be to raise and render anyway?",
                True
               ],
    "Lottery Desk":["Lottery Ticket",
                    ["Lottery Ticket","lottery", "ticket", "scratch off"],
                    "This time for sure. The ticket promises great riches, an end to scarcity. Forever and ever, until the end of your life. Do it. You can win. You can feel it. It's only a couple dollars, why not? This time for sure.",
                    "It won't be, but it felt good to buy it anyway. Sobriety isn't as cold as you'd expect, you rather enjoyed wasting that little bit of money. And maybe you'll win it back on a lesser prize. This time, for sure.",
                    True
                    ]
}

#Input validation function with targeted error messages
#Returns False if in error or a tuple of (command, target)
def player_action(player_input, cur_room):
    #Tokenizes the input
    cleaned_input = player_input.strip().split()
    #Error for an empty input (They just hit enter)
    if not cleaned_input:
        print("Invalid input: You did not enter a command.")
        return False
    #Error if the player did not input a 'go' or 'get' command
    elif cleaned_input[0] not in ("go", "get"):
        print("Invalid input: You did not type a \"go\" or \"get\" command.")
        return False
    #Error for only entering 'go' or 'get' without additional input
    elif len(cleaned_input) < 2:
        print("Invalid input: You did not give a direction or item with the \"go\" or \"get\" command.")
        return False
    #For rooms/items with multiple words, recombines them
    arg = " ".join(cleaned_input[1:])
    #Error if they input a 'go' command but not a valid direction
    if cleaned_input[0] == "go" and arg not in rooms[cur_room].keys():
        print("Invalid input: You did not enter a valid direction.")
        return False
    #Error if they input a 'get' command but not a valid item name
    elif cleaned_input[0] == "get" and arg not in items[cur_room][1]:
        print("Invalid input: You did not enter a valid item name.")
        return False
    #Successful 'go' action
    elif cleaned_input[0] == "go" and arg in rooms[cur_room].keys():
        return cleaned_input[0], arg
    #Successful 'get' action
    elif cleaned_input[0] == "get" and arg in items[cur_room][1]:
        return cleaned_input[0], arg
    # Catch-all for any other errors
    else:
        print("Invalid input: Unexpected input error has occurred.")
        return False

#Greeting message
print("\nWelcome to Ciacco's Submarket!\n"+'_'*20)
print("It's like a supermarket, only cheaper, since our prices head straight down!")
print("Let our deals, and gravity, fill your heart with more food than you can stomach!")
print('_'*20)

#Set the starting room
current_room = "Entrance"
#Display movement instructions
navigate_options()
#Create player inventory/number of times refused an item/list of all visited rooms/and if they took "nothing" from the entrance
inventory = []
num_refuse = 0
visited_rooms = ["Entrance"]
took_nothing = False

#Once per main loop iteration, output the location, inventory, check if they've reached the exit, exit the game if so, and display connecting rooms
def update_status():
    #Displays the room the player is in and their inventory
    print("\nSTATUS:")
    print("Current Location: {}".format(current_room))
    print("Shopping Cart: {}.".format("Nothing. For shame" if not inventory else inventory))

    #Reaching the Exit immediately ends the game and displays ending text depending on the player's choice
    #The possible ends are: {"Collected all items->Leave the store", "Collected only some items->Not allowed to leave", "Visited every room and took nothing->Allowed to ""leave"" in an ambiguous way", "Any other combination->Not allowed to leave"}
    if current_room == "Exit":
        print("\nThe smell of sickly copper fades as you push your squeaking cart down the long, dimly hallway to the exit."
              "\nThere doesn't appear to be a check-out line at all, and this is not where you came in."
              "\nInstead, a portly, middle-aged man stands by the rusted doors to the outside."
              "\nHis smile is wide and his teeth outnumber yours twice over."
              "\nAs you glance over your shoulder, there is nothing behind you but a smooth wall."
              "\nHunger drove you here, pushed you to push the cart through the aisles."
              "\nNow Hunger judges your banditry as saliva drips down both your chins.")

        if len(inventory) == len(items)-1:
            print("\nAh, dear customer. Our most favored, respectable customer."
                  "\nYou have done all of at Ciacco's Submarket so proud. Not a single temptation left to languish on the shelves."
                  "\nDid you enjoy your time here? Did you rush so you could leave?")
            print("\nIt amused us that you had to think twice about your purchases, an entire {} times!".format(num_refuse) if num_refuse != 0 else "\nAnd not for a second did you doubt your need to feed! All instinct and passion, a beautiful beast!")
            print("\nSo wonderfully spilling over with avarice, you even took something from where there was nothing" if took_nothing else "\nThough you could stand to try a little harder, reach lower depths. Think outside the box")
            print("\nRegardless, you are here, your cart is full. We are so happy for you. Go now, please. Exit to the east and we will bar the doors behind you. As it should be, as it was."
                  "\nWe will bow our heads in awe, beloved customer, our most hungry steward, until you return to the land of dust and pain."
                  "\nAt least, until sweet, eternal Hunger rouses again. See you tomorrow, beloved customer.")
        elif len(inventory) < len(items)-1 and len(inventory) > 0:
            print("\nOh my, dear customer. Poor, confused, ravenous customer."
                  "\nYou must be terribly confused. Starving, even. Your cart isn't quite full."
                  "\nWe put such effort into making our displays catch the eye, convince you of what you need."
                  "\nBut you missed a few stops, and that won't do.")
            print("\nBut it was clearly in haste, you simply need to take your time, enjoy the spectacle more. Listen to your gut." if num_refuse == 0 else "You're all frazzled up! Running around, hesitating. We understand. We care.")
            print("\nWe know you're meant to be here. One of us, really, part of the family. It isn't easy to stand in the entrance and embrace hunger for the love of it!" if took_nothing else "Though we may be in error, this submarket might not be for you just yet.")
            print("\nSuch as it is, we can't be having you leaving just yet. You've had a taste of Ciacco's Submarket, and I'm afraid we don't allow teetotalers to wander away.")
            print("\nAs the man puts a hand on your shoulder, and you see the light go out from his eyes, an old and terrible hunger grips your stomach."
                  "\nWhen he turns you around, you don't resist, and the long hallway back to the Butcher is open again. "
                  "\nWouldn't it be a dream to live here and eat forever?")
        elif len(inventory) == 0 and len(visited_rooms) == len(rooms):
            print("\nThe man's smile fades away like an old ache finally healed. "
                  "\nHe folds in on himself, muttering nonsense as his eyes drop from yours and settle on his shoes.")
            print("\nYou faintly hear him make mention that coveting nothing is still coveting, maybe." if took_nothing else "\nYou catch stray words of him amazed that even nothing could gets its hooks in you.")
            print("\nThe rusted doors swing open, and in lieu of a staircase back to the surface, there is a green field under a clear sky."
                  "\nYou've never seen this place before, but it's entirely familiar. "
                  "\nHunger shies away from you as you leave your empty cart behind. "
                  "\nYour stomach is very full as the wail of the starving clings to your heels."
                  "\nAt the edge of the field, you spot some kind of fruit tree, nestled between berry bushes."
                  "\nYou leave the submarket and all its works behind to the reward of temperance.")
        else:
            print("\nThe heavy man puts a stern hand on your shoulder and spins you around."
                  "\nA quick exit means the customer left untested, and never found the depths of their hunger."
                  "\nThat won't do."
                  "\nTo leave the submarket too soon, thinking yourself better than those that wander the halls, is terribly prideful after all."
                  "\nWho are you to think you have something better to do with your, oh so limited, time?"
                  "\nAvoidance has a place, but not after you've willfully descended."
                  "\nThere's a sale on cheese-stuffed hotdog bites, you know. Maybe a free sample will clear the matter up."
                  "\nWhen you look back towards the exist, you only see more aisles.")
        return False

    #Informs the player of all the valid adjoining rooms every iteration
    print("Nearby Departments: ", end="")
    for i in rooms[current_room]:
        print(rooms[current_room][i] + " -> " + i, end=" | ")
    #Inform the player if an item is in the room still
    print("\nProduct of Fixation: {}.".format(items[current_room][0] if items[current_room][-1] else "You need nothing more"))

    return True

#Main game loop
while(True):
    #When the game hits the Exit room, end upon returning
    if not update_status():
        break

    #Gather player input and test if it's valid
    try:
        action_input = input("\nWhat would you like to do? ")
    except (EOFError, KeyboardInterrupt):
        print("\nLeaving Ciacco\'s Submarket. Goodbye.")
        break
    action = player_action(action_input, current_room)
    #If there is an action, i.e., a valid input check what action it is and execute
    if action:
        #If a move action, set the player's current location to that room and append the room to list of visited rooms if not already in
        if action[0] == "go":
            current_room = rooms[current_room][action[1]]
            if current_room not in visited_rooms:
                visited_rooms.append(current_room)
        #If a get action, check if it's already been taken
        elif action[0] == "get":
            temp_item = items[current_room]
            #If it's still there, print the normal description and prompt the player to take it(y/n)
            if temp_item[-1]:
                print("\n"+temp_item[2])
                try:
                    take = input("Take the {} (y/n)? ".format(temp_item[0])).strip().lower()
                except (EOFError, KeyboardInterrupt):
                    print("\nLeaving Ciacco\'s Submarket. Goodbye.")
                    break
                #If they take it, flip the flag and add the item to the inventory, except in the case of the "nothing" in the entrance
                if take == "y":
                    #Print the "taken" dialogue
                    print("\n"+temp_item[3])
                    temp_item[-1] = False
                    if temp_item[0] != "Nothing":
                        inventory.append(temp_item[0])
                    #If the secret entrance "nothing" is taken, special message, flip the flag for finding it
                    else:
                        print("\nIt's harder to get a firm hold on nothing than you ever considered.\n")
                        took_nothing = True
                #If they refuse to take the item, make note, increment the counter
                elif take == "n":
                    print("\nSelf control briefly asserts itself and you step away.")
                    num_refuse += 1
                #If any other input, thematic error message implying eagerness to consume
                else:
                    print("\nInvalid input: The fever for products has caused you to mash the keyboard. Enter \"y\" or \"n\" only.")
            #If the item flag is "taken", i.e., False, then if they try to take the item again, make mention it's gone.
            else:
                print("\nYou already took all the submarket wanted to give. There is nothing more to help you.")
   #If there is no valid action, redisplay the input options
    else:
        navigate_options()




