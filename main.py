import random
import matplotlib.pyplot as plt

BATTLES = 100000

# Gauss Rifle and Machine Pistol have minimum range of 12" 
# Gauss Rifle (but not Machine Pistol) fires twice at half distance 6" =< x > 2" 
# Souless Robots have no melee weapon, but the Space soldier knifesword can attack twice

# Distance constants
RANGES = {
    "Ranged Far (14 - 8 inches)",
    "Range Near (7 - 2 inches)",
    "Melee (within 1 inch)"
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
    "LEADERSHIP": 10,
    "OBJECTIVE_CONTROL": 2,
    "DAMAGE": 1,
    "ARMOR_PENETRATION": 0
}

# Souless robot melee parameters
SR_MELEE = {
    "RANGE": 1,        
    "ATTACK": 1,
    "SKILL": 3,         # 3+ to hit
    "STRENGTH": 4,
    "ARMOR_PENETRATION": 0,
    "DAMAGE": 1
}

# Souless Robot ranged Weapon
GAUSS_RIFLE = {
    "RANGE": 14,        
    "ATTACK": 2,
    "SKILL": 3,         # 3+ to hit
    "STRENGTH": 5,
    "ARMOR_PENETRATION": -2,
    "DAMAGE": 1
}

# Character 2 - Space soldier
SPACE_SOLDIER = {
    "MOVEMENT": 6,
    "BS": 3,
    "WS": 3,
    "STRENGTH": 4,
    "ATTACK": 2,
    "TOUGHNESS": 4,
    "SAVE": 3,                # 4+ armor save
    "WOUNDS": 2,
    "LEADERSHIP": 7,
    "ARMOR_PENETRATION": -1,
    "OBJECTIVE_CONTROL": 2
}

# Space soldier Melee Weapon
KNIFESWORD = {
    "RANGE": 1,        # Inches
    "ATTACK": 2,
    "SKILL": 3,         # 3+ to hit
    "STRENGTH": 4,
    "ARMOR_PENETRATION": -1,
    "DAMAGE": 1
}

# Space soldier Ranged Weapon
MACHINE_PISTOL = {
    "RANGE": 18,        # Inches
    "ATTACK": 1,
    "SKILL": 3,         # 3+ to hit
    "STRENGTH": 4,
    "ARMOR_PENETRATION": -1,
    "DAMAGE": 1
}

# Random return of 1 - 6
def roll_dice() -> int:
    return random.randint(1, 6)

# Sort function for bar graph - overrides default sort to take string length into account, i.e. default sort incorrectly, "1", "10", "11" ... "2"
def sort_func(arg_val: str) -> int:
    return int(arg_val[0])

# Attack Damage Calculation
def attack_phase(attacker, attacker_weapon, defender) -> int:
    hit_roll = roll_dice()
    if hit_roll < attacker_weapon.get("SKILL"):
        return 0
    if attacker_weapon.get("STRENGTH") > defender.get("TOUGHNESS"):
        if attacker_weapon.get("STRENGTH") >= 2*defender.get("TOUGHNESS"):
             D6_required = 2
        else:
             D6_required = 3
    else:
        if attacker_weapon.get("STRENGTH") < defender.get("TOUGHNESS"):
            if attacker_weapon.get("STRENGTH")*2 >= defender.get("TOUGHNESS"):
                D6_required = 6
            else:
                D6_required = 5
        else:
             D6_required = 4
    wound_roll = roll_dice()
    if wound_roll < D6_required:
        return 0
    save_throw = roll_dice() + attacker_weapon.get("ARMOR_PENETRATION")
    if save_throw >= defender.get("SAVE"):
        return attacker_weapon.get("DAMAGE")
    else:
        return 0

def main() -> None:
      
    print(f"Monte Carlo Analysis of a fight between 1 Space Soldier (Machine Pistol plus Knifesword) versus 1 Souless Robot (Guass Rifle)")
    print(f"The D6 is simulated as random.randint(1, 6), the total Battles are {BATTLES}")
    print(f"NOTE: The percentage died and number of battles converge well enough at 100000 battles (simulations)")
    print(f" ")
    for distance in RANGES:
        space_soldier_wound = SPACE_SOLDIER.get("WOUNDS")
        robot_wound = SOULESS_ROBOT.get("WOUNDS")
        robot_died = 0
        soldier_died = 0
        old_battles = 0
        soldier_battle_avg = 0
        robot_battle_avg = 0  
        robot_bars = {}
        soldier_bars = {}

        for number_battles in range(BATTLES):

            if space_soldier_wound <= 0 and robot_wound <= 0:
                print(f"Error: Wounds soldier {space_soldier_wound} Robots {robot_wound}")
            
            if space_soldier_wound <= 0 or robot_wound <= 0:
                if space_soldier_wound <= 0:
                    soldier_died += 1
                    n_battles = number_battles - old_battles
                    soldier_battle_avg += n_battles
                    if n_battles == 0:
                        n_battles = 1
                    n_key = str(n_battles)
                    if n_key in soldier_bars:
                            soldier_bars[n_key] += 1
                    else:
                            soldier_bars.setdefault(n_key,1)
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
                space_soldier_wound = SPACE_SOLDIER.get("WOUNDS")
                robot_wound = SOULESS_ROBOT.get("WOUNDS")


            if distance == "Ranged Far (14 - 8 inches)":
                space_soldier_wound -= attack_phase(SOULESS_ROBOT,GAUSS_RIFLE,SPACE_SOLDIER)
                if (space_soldier_wound > 0):
                    robot_wound -= attack_phase(SPACE_SOLDIER,MACHINE_PISTOL,SOULESS_ROBOT)               
                 
            if distance == "Range Near (7 - 2 inches)":
                for i in range(GAUSS_RIFLE.get("ATTACK")):
                    space_soldier_wound -= attack_phase(SOULESS_ROBOT,GAUSS_RIFLE,SPACE_SOLDIER)
                if (space_soldier_wound > 0):
                    robot_wound -= attack_phase(SPACE_SOLDIER,MACHINE_PISTOL,SOULESS_ROBOT)               

            if distance == "Melee (within 1 inch)":
                space_soldier_wound -= attack_phase(SOULESS_ROBOT,SR_MELEE,SPACE_SOLDIER)
                if (space_soldier_wound > 0):
                    for i in range(KNIFESWORD.get("ATTACK")):
                        robot_wound -= attack_phase(SPACE_SOLDIER,KNIFESWORD,SOULESS_ROBOT)                      

        print(f"{distance}")
        print(f"{robot_died} Robot Died {robot_died/BATTLES*100:.2f}% of total battles, average battles to kill {robot_battle_avg/robot_died:.1f}")
        print(f"{soldier_died} Soldier Died {soldier_died/BATTLES*100:.2f}% of total battles, average battles to kill {soldier_battle_avg/soldier_died:.1f}")
        # Create Bar Graph for each character
        robot_bars_s = dict(sorted(robot_bars.items(),key=sort_func))
        plt.bar(range(len(robot_bars_s)), list(robot_bars_s.values()), align='center')
        plt.xticks(range(len(robot_bars_s)), list(robot_bars_s.keys()))
        plt.xlabel("Battles")
        plt.ylabel("Died")
        plt.title(f"{distance}\nNumber of Battles it took for A Soldier to Kill a Robot")
        plt.show()
        soldier_bars_s = dict(sorted(soldier_bars.items(),key=sort_func))
        plt.bar(range(len(soldier_bars_s)), list(soldier_bars_s.values()), align='center')
        plt.xticks(range(len(soldier_bars_s)), list(soldier_bars_s.keys()))
        plt.xlabel("Battles")
        plt.ylabel("Died")
        plt.title(f"{distance}\nNumber of of battles it took for Robot to Kill a Soldier")
        plt.show()
        print(" ")

                    
if __name__ == '__main__':
     main()



