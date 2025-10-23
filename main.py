import random
import matplotlib.pyplot as plt

BATTLES = 100000

# Gauss Reaper and Bolt Pistol have minimum range of 12" 
# Gauss Reaper is typed as rapid fire, so at half distance 6" =< x > 2" it can attack twice
# Necrons have no melee weapon, the chainsword can attack twice

# Distance constants
RANGES = {
    "Ranged Far",
    "Range Near",
    "Melee"
}

# Character 1 - Necron Warrior with Gauss Reaper ranged weapon, no melee weapon
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

NECRON_MELEE = {
    "range": 1,        
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 5,
    "armor_penetration": 0,
    "damage": 1
}

GAUSS_REAPER = {
    "range": 12,        
    "attacks": 2,
    "skill": 3,         # 3+ to hit
    "strength": 5,
    "armor_penetration": -1,
    "damage": 1
}

# Character 2 - Assult Intercessor (Space Marine) with Bolt Pistol (ranged weapon) and Chainsword (melee weapon)
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

CHAINSWORD = {
    "range": 12,        # Inches
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 4,
    "armor_penetration": 0,
    "damage": 1
}

BOLT_PISTOL = {
    "range": 12,        # Inches
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 4,
    "armor_penetration": 0,
    "damage": 1
}

def roll_dice() -> int:
    return random.randint(1, 6)

def sort_func(arg_val: str) -> int:
    return int(arg_val[0])

def shoot_phase(attacker, attacker_weapon, defender, D6_required) -> int:
    hit_roll = roll_dice()
    if hit_roll < attacker.get("BS"):
        return 0
    wound_roll = roll_dice()
    if wound_roll < D6_required:
        return 0
    save_throw = roll_dice() + attacker_weapon.get("armor_penetration")
    if save_throw >= defender.get("SAVE"):
        return attacker_weapon.get("damage")
    else:
        return 0

print(f"Monte Carlo Analysis of a fight between 1 Assault Intercessor (Bolt Pistol plus Chainsword) versus 1 Necron Warrior (Guass Reaper)")
print(f"The D6 is simulated as random.randint(1, 6), the total Battles are {BATTLES}")
print(f"NOTE: The percentage died and number of battles converge well enough at 100000 battles (simulations)")
print(f" ")
for distance in RANGES:
    space_marine_wound = ASSAULT_INTERCESSOR.get("WOUNDS")
    necron_wound = NECRON_WARRIOR.get("WOUNDS")
    necron_died = 0
    marine_died = 0
    old_battles = 0
    marine_battle_avg = 0
    necron_battle_avg = 0  
    necron_bars = {}
    marine_bars = {}

    for number_battles in range(BATTLES):

        if space_marine_wound <= 0 and necron_wound <= 0:
            print(f"Error: Wounds Marine {space_marine_wound} Necron {necron_wound}")
        
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
            if necron_wound <= 0:
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
            space_marine_wound = ASSAULT_INTERCESSOR.get("WOUNDS")
            necron_wound = NECRON_WARRIOR.get("WOUNDS")

        if (distance == "Ranged Far" or distance == "Ranged Near"):
            for i in range(2):
                space_marine_wound -= shoot_phase(NECRON_WARRIOR,GAUSS_REAPER,ASSAULT_INTERCESSOR,3)
            if (space_marine_wound > 0):
                necron_wound -= shoot_phase(ASSAULT_INTERCESSOR,BOLT_PISTOL,NECRON_WARRIOR,4)               
        else:
            space_marine_wound -= shoot_phase(NECRON_WARRIOR,NECRON_MELEE,ASSAULT_INTERCESSOR,3)
            if (space_marine_wound > 0):
                necron_wound -= shoot_phase(ASSAULT_INTERCESSOR,CHAINSWORD,NECRON_WARRIOR,4)                      

    if distance == "Ranged Far":
        print(f"Within range but not less than half: 12 - 7 inches")
    else:
        if distance == "Ranged Near":
            print(f"Within half range but not yet melee: 6 - 2 inches, Necrons can shoot twice")
        else:
            print(f"Melee distance, Marines have chainsword, can attack twice")
    print(f"{necron_died} Necron Died {necron_died/BATTLES*100:.2f}% of total battles, average battles to kill {necron_battle_avg/necron_died:.1f}")
    print(f"{marine_died} Marine Died {marine_died/BATTLES*100:.2f}% of total battles, average battles to kill {marine_battle_avg/marine_died:.1f}")
    necron_bars_s = dict(sorted(necron_bars.items(),key=sort_func))
    plt.bar(range(len(necron_bars_s)), list(necron_bars_s.values()), align='center')
    plt.xticks(range(len(necron_bars_s)), list(necron_bars_s.keys()))
    plt.xlabel("Battles")
    plt.ylabel("Died")
    plt.title(f"In {BATTLES} Number of Necrons Died")
    plt.show()
    marine_bars_s = dict(sorted(marine_bars.items(),key=sort_func))
    plt.bar(range(len(marine_bars_s)), list(marine_bars_s.values()), align='center')
    plt.xticks(range(len(marine_bars_s)), list(marine_bars_s.keys()))
    plt.xlabel("Battles")
    plt.ylabel("Died")
    plt.title(f"In {BATTLES} Number of Marines Died")
    plt.show()
    print(" ")

                    




