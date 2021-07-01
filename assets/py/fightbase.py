import math
import assets.py.charbase as charbase
import time
curtime = time.time()
import random


""" FIXME

Build character building function
Build opponent
rebuild timer function
build command queue
build unload function
    With awarding experience
    offloading new stats
    track winner
Rebuild it to track with the new backend
remove deprecated functions

"""
aghast = charbase.Aghast()
skynet = charbase.Skynet()

#Roll to hit. "type" will refer to different attacks so that this function is multipurpose
def rth(ch, vict, type): 
    # This will wind up having to be significantly more complex
    # because of the nature of different classes having some varies hit or damage effects.
    if ch.is_dead != True and vict.is_dead != True:
        if type == "auto":
            hitroll = dice_roll( ch.hitroll[0], ch.hitroll[1] ) # Call the dice roll function
            if hitroll >= vict.ac:   # If it clears their armor class
                dbp(ch, vict, type)           # Call on the Dodge Block and Parry function
            else:                       # Otherwise
                miss("miss")               # Send it to the miss function with "hit"

# After a hit registers, run the dbp function, short for dodge, block and parry
def dbp(ch, vict, type): # dodge block parry
    # Check dodge roll
    dodge = vict.dodge
    dodgeroll = dice_roll( 1, 100 )
    if dodgeroll <= dodge:
        miss("dodge")
        return

    # Check block roll
    block = vict.block
    blockroll = dice_roll( 1, 100 )
    if blockroll <= block:
        miss("block")
        return

    # Check parry roll
    parry = vict.parry
    parryroll = dice_roll( 1, 100 )
    if parryroll <= parry:
        miss("parry")
        return

    # If damage isn't prevented, calculate damage
    dmg(ch,vict, type)

# dmg( Damage ) function for calculating damage and checking for death
def dmg(ch, vict, type):
    damage_dice = ch.damage[0]  # Collect the number of damage dice to be rolled
    damage_sides = ch.damage[1] # and how many facets those dice have
    damage_resistance = ch.dr  # Collect the damage resistance
    damage = dice_roll( damage_dice, damage_sides)    #roll damage
    damage -= damage_resistance   #subtract vict["dr"]
    vict.hp -= damage    #apply damage
    print(f"You hit your opponent with some force ({damage})") # this will someday refer to a function full of different descriptors for different damage amounts
    if vict.hp <= 0:
        victory(ch, vict)

def miss(case):
    if case == "miss":
        print("You swing for your opponent, but miss.")
    if case == "dodge":
        print("You swing for your opponent, but your attack is dodged.")
    if case == "block":
        print("You swing for your opponent, but your attack is blocked.")
    if case == "parry":
        print("You swing for your opponent, but your attack is parried.")

def auto_atk(ch, vict):
    spd = ch.speed
    aps = spd // 40
    ch.speed = spd % 40 
    for attacks in range(0, aps):
        rth(ch, vict, "auto")

def victory(ch, vict):
    vict.is_dead = True
    print(f"{vict.name} is incapacitated and will die soon, if not aided.")

def turn_timer(player1, player2):
    print("")
    print(f"<hp: {player1.hp}/{player1.max_hp}>")
    tick(player1, player2)
    time.sleep(3)
    turn_queue(player1, player2)

def turn_queue(player1, player2):
    if player1.is_dead == False and player2.is_dead == False:
        auto_atk(player1, player2)
        auto_atk(player2, player1)
        turn_timer(player1, player2)

def tick(player1, player2):
    player1.speed += player1.speed_max
    player2.speed += player2.speed_max

def dice_roll(dice, sides):
    rolls = []
    result = 0
    for i in range(0,dice):
        n = random.randint(0,sides)
        rolls.append(n)
    for x in rolls:
        result += x
    return result



