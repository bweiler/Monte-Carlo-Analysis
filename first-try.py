import random
import matplotlib.pyplot as plt

NECRON_WARRIOR = {
    "MOVEMENT": 5,
    "BS": 3,
    "WS": 3,
    "TOUGHNESS": 4,
    "STRENGTH": 4,
    "SAVE": 4,
    "ATTACK": 1,                
    "WOUNDS": 1,
    "LEADERSHIP": 7,
    "OBJECTIVE_CONTROL": 2,
    "DAMAGE": 1,
    "armor_penetration": 0
}

GAUSS_REAPER = {
    "range": 12,        
    "attacks": 2,
    "skill": 3,         # 3+ to hit
    "strength": 5,
    "armor_penetration": -1,
    "damage": 1
}

ASSAULT_INTERCESSOR = {
    "MOVEMENT": 6,
    "BS": 3,
    "WS": 3,
    "STRENGTH": 4,
    "ATTACK": 2,
    "TOUGHNESS": 4,
    "SAVE": 3,                # 4+ armor save
    "WOUNDS": 2,
    "LEADERSHIP": 6,
    "armor_penetration": -1,
    "OBJECTIVE_CONTROL": 2
}

BOLT_PISTOL = {
    "range": 12,        # Inches
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 4,
    "armor_penetration": 0,
    "damage": 1
}

#    "1": 0,"2": 0,"3": 0,"4": 0,"5": 0,"6": 0,"7": 0,"8": 0,"9": 0,"10": 0,"11": 0,"12": 0,"13": 0,"14": 0,"15": 0 }

def roll_dice():
    return random.randint(1, 6)

def sort_func(arg_val):
    return int(arg_val[0])

battles = 100000

#Gauss Flayer and Bolt Pistol have a rnage of 12", Gauss Reaper is rapid fire, so at half distance = 6" can attack twice

print(f"Monte Carlo Analysis of a fight between 1 Assault Intercessor (Bolt Pistol plus Chainsword) versus 1 Necron Warrior (Guass Reaper)")
print(f"The D6 is simulated as random.randint(1, 6), the total Battles are {battles}")
print(f"NOTE: The percentage died and number of battles converge well enough at 100000 battles (simulations)")
print(f" ")
for distance in range(3):
    space_marine_wound = ASSAULT_INTERCESSOR.get("WOUNDS")
    necron_wound = NECRON_WARRIOR.get("WOUNDS")
    necron_died = 0
    marine_died = 0
    old_battles = 0
    marine_battle_avg = 0
    necron_battle_avg = 0  
    necron_bars = {}
    marine_bars = {}

    for number_battles in range(battles):

        if space_marine_wound <= 0 or necron_wound <= 0:
            if space_marine_wound <= 0:
                marine_died += 1
                n_battles = number_battles - old_battles
                marine_battle_avg += n_battles
                if n_battles == 0:
                    n_battles = 1
                n_key = str(n_battles)
                if n_key in marine_bars:
                     marine_bars[n_key] += 1
                else:
                     marine_bars.setdefault(n_key,1)
            else:
                necron_died += 1
                n_battles = number_battles - old_battles
                necron_battle_avg += n_battles
                if n_battles == 0:
                    n_battles = 1
                n_key = str(n_battles)
                if n_key in necron_bars:
                     necron_bars[n_key] += 1
                else:
                     necron_bars.setdefault(n_key,1)
                
            old_battles = number_battles           
            if space_marine_wound <= 0 and necron_wound <= 0:
                print(f"Error: Wounds Marine {space_marine_wound} Necron {necron_wound}")
            space_marine_wound = ASSAULT_INTERCESSOR.get("WOUNDS")
            necron_wound = NECRON_WARRIOR.get("WOUNDS")
        if (distance == 0 or distance == 1):
            for i in range(distance + 1):
                hit_roll = roll_dice()
                if hit_roll >= NECRON_WARRIOR.get("BS"):
                    if (GAUSS_REAPER.get("strength") > ASSAULT_INTERCESSOR.get("TOUGHNESS") ):
                        D6_required = 3
                        wound_roll = roll_dice()
                        if wound_roll >= D6_required:
                            save_throw = roll_dice() + GAUSS_REAPER.get("armor_penetration")
                            if save_throw >= ASSAULT_INTERCESSOR.get("SAVE"):
                                space_marine_wound -= GAUSS_REAPER.get("damage")
            if (space_marine_wound > 0):
                hit_roll = roll_dice()
                if hit_roll >= ASSAULT_INTERCESSOR.get("BS"):
                    if (BOLT_PISTOL.get("strength") == NECRON_WARRIOR.get("TOUGHNESS") ):
                        D6_required = 4
                        wound_roll = roll_dice()
                        if wound_roll >= D6_required:
                            save_throw = roll_dice() + BOLT_PISTOL.get("armor_penetration")
                            if save_throw >= NECRON_WARRIOR.get("SAVE"):
                                necron_wound -= BOLT_PISTOL.get("damage")
        else:
            hit_roll = roll_dice()
            if hit_roll >= NECRON_WARRIOR.get("WS"):
                if (NECRON_WARRIOR.get("STRENGTH") == ASSAULT_INTERCESSOR.get("TOUGHNESS") ):
                    D6_required = 4
                    wound_roll = roll_dice()
                    if wound_roll >= D6_required:
                        save_throw = roll_dice() + NECRON_WARRIOR.get("armor_penetration")
                        if save_throw >= ASSAULT_INTERCESSOR.get("SAVE"):
                            space_marine_wound -= NECRON_WARRIOR.get("DAMAGE")
            if (space_marine_wound > 0):
                for i in range(2):
                    hit_roll = roll_dice()
                    if hit_roll >= ASSAULT_INTERCESSOR.get("WS"):
                        if (ASSAULT_INTERCESSOR.get("STRENGTH") == NECRON_WARRIOR.get("TOUGHNESS") ):
                            D6_required = 4
                            wound_roll = roll_dice()
                            if wound_roll >= D6_required:
                                save_throw = roll_dice() + ASSAULT_INTERCESSOR.get("armor_penetration")
                                if save_throw >= NECRON_WARRIOR.get("SAVE"):
                                    necron_wound -= 1
        
    match distance:
        case 0:
            print(f"Within range but not less than half: 12 - 7 inches")
        case 1:
            print(f"Within half range but not yet melee: 6 - 2 inches, Necrons can shoot twice")
        case 2:
            print(f"Melee distance, Marines have chainsword, can attack twice")
    print(f"{necron_died} Necron Died {necron_died/battles*100:.2f}% of total battles, average battles to kill {necron_battle_avg/necron_died:.1f}")
    print(f"{marine_died} Marine Died {marine_died/battles*100:.2f}% of total battles, average battles to kill {marine_battle_avg/marine_died:.1f}")
    necron_bars_s = dict(sorted(necron_bars.items(),key=sort_func))
    plt.bar(range(len(necron_bars_s)), list(necron_bars_s.values()), align='center')
    plt.xticks(range(len(necron_bars_s)), list(necron_bars_s.keys()))
    plt.xlabel("Battles")
    plt.ylabel("Died")
    plt.title(f"In {battles} Number of Necrons Died")
    plt.show()
    marine_bars_s = dict(sorted(marine_bars.items(),key=sort_func))
    plt.bar(range(len(marine_bars_s)), list(marine_bars_s.values()), align='center')
    plt.xticks(range(len(marine_bars_s)), list(marine_bars_s.keys()))
    plt.xlabel("Battles")
    plt.ylabel("Died")
    plt.title(f"In {battles} Number of Marines Died")
    plt.show()
    print(" ")

                    




