import random
import matplotlib.pyplot as plt

BATTLES = 100000

# Gauss Rifle and Machine Pistol have minimum range of 12" 
# Gauss Rifle (but not Machine Pistol) fires twice at half distance 6" =< x > 2" 
# Souless Robots have no melee weapon, but the Space Marine knifesword can attack twice

# Distance constants
RANGES = {
    "Ranged Far",
    "Range Near",
    "Melee"
}

# Character 1 - Souless Robot
SOULESS_ROBOT = {
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

# Souless robot melee parameters
SR_MELEE = {
    "range": 1,        
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 5,
    "armor_penetration": 0,
    "damage": 1
}

# Souless Robot ranged Weapon
GAUSS_RIFLE = {
    "range": 12,        
    "attacks": 2,
    "skill": 3,         # 3+ to hit
    "strength": 5,
    "armor_penetration": -1,
    "damage": 1
}

# Character 2 - Space Marine
SPACE_MARINE = {
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

# Space Marine Melee Weapon
KNIFESWORD = {
    "range": 12,        # Inches
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 4,
    "armor_penetration": 0,
    "damage": 1
}

# Space Marine Ranged Weapon
MACHINE_PISTOL = {
    "range": 12,        # Inches
    "attacks": 1,
    "skill": 3,         # 3+ to hit
    "strength": 4,
    "armor_penetration": 0,
    "damage": 1
}

# Random return of 1 - 6
def roll_dice() -> int:
    return random.randint(1, 6)

# Sort function for bar graph - overrides default sort to take string length into account, i.e. default sort incorrectly, "1", "10", "11" ... "2"
def sort_func(arg_val: str) -> int:
    return int(arg_val[0])

# Attack Damage Calculation
def attack_phase(attacker, attacker_weapon, defender, D6_required) -> int:
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

def main() -> None:
      
    print(f"Monte Carlo Analysis of a fight between Space Marine (Machine Pistol plus Knifesword) versus 1 Souless Robot (Guass Rifle)")
    print(f"The D6 is simulated as random.randint(1, 6), the total Battles are {BATTLES}")
    print(f"NOTE: The percentage died and number of battles converge well enough at 100000 battles (simulations)")
    print(f" ")
    for distance in RANGES:
        space_marine_wound = SPACE_MARINE.get("WOUNDS")
        robot_wound = SOULESS_ROBOT.get("WOUNDS")
        robot_died = 0
        marine_died = 0
        old_battles = 0
        marine_battle_avg = 0
        robot_battle_avg = 0  
        robot_bars = {}
        marine_bars = {}

        for number_battles in range(BATTLES):

            if space_marine_wound <= 0 and robot_wound <= 0:
                print(f"Error: Wounds Marine {space_marine_wound} Robots {robot_wound}")
            
            if space_marine_wound <= 0 or robot_wound <= 0:
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
                if robot_wound <= 0:
                    robot_died += 1
                    n_battles = number_battles - old_battles
                    robot_battle_avg += n_battles
                    if n_battles == 0:
                        n_battles = 1
                    n_key = str(n_battles)
                    if n_key in robot_bars:
                            robot_bars[n_key] += 1
                    else:
                            robot_bars.setdefault(n_key,1)                
                old_battles = number_battles           
                space_marine_wound = SPACE_MARINE.get("WOUNDS")
                robot_wound = SOULESS_ROBOT.get("WOUNDS")

            if (distance == "Ranged Far" or distance == "Ranged Near"):
                for i in range(2):
                    space_marine_wound -= attack_phase(SOULESS_ROBOT,GAUSS_RIFLE,SPACE_MARINE,3)
                if (space_marine_wound > 0):
                    robot_wound -= attack_phase(SPACE_MARINE,MACHINE_PISTOL,SOULESS_ROBOT,4)               
            else:
                space_marine_wound -= attack_phase(SOULESS_ROBOT,SR_MELEE,SPACE_MARINE,3)
                if (space_marine_wound > 0):
                    robot_wound -= attack_phase(SPACE_MARINE,KNIFESWORD,SOULESS_ROBOT,4)                      

        if distance == "Ranged Far":
            print(f"Within range but not less than half: 12 - 7 inches")
        else:
            if distance == "Ranged Near":
                print(f"Within half range but not yet melee: 6 - 2 inches, robots can shoot twice")
            else:
                print(f"Melee distance, Marines have chainsword, can attack twice")
        print(f"{robot_died} robot Died {robot_died/BATTLES*100:.2f}% of total battles, average battles to kill {robot_battle_avg/robot_died:.1f}")
        print(f"{marine_died} Marine Died {marine_died/BATTLES*100:.2f}% of total battles, average battles to kill {marine_battle_avg/marine_died:.1f}")
        # Create Bar Graph for each character
        robot_bars_s = dict(sorted(robot_bars.items(),key=sort_func))
        plt.bar(range(len(robot_bars_s)), list(robot_bars_s.values()), align='center')
        plt.xticks(range(len(robot_bars_s)), list(robot_bars_s.keys()))
        plt.xlabel("Battles")
        plt.ylabel("Died")
        plt.title(f"In {BATTLES} Number of Robots Died")
        plt.show()
        marine_bars_s = dict(sorted(marine_bars.items(),key=sort_func))
        plt.bar(range(len(marine_bars_s)), list(marine_bars_s.values()), align='center')
        plt.xticks(range(len(marine_bars_s)), list(marine_bars_s.keys()))
        plt.xlabel("Battles")
        plt.ylabel("Died")
        plt.title(f"In {BATTLES} Number of Marines Died")
        plt.show()
        print(" ")

                    
if __name__ == '__main__':
     main()



