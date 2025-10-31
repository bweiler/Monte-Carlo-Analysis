import random
import matplotlib.pyplot as plt

BATTLES = 100000

# Gauss Rifle and Machine Pistol have minimum range of 12" 
# Gauss Rifle (but not Machine Pistol) fires twice at half distance 6" =< x > 2" 
# Souless Robots have no melee weapon, but the Space soldier knifesword can attack twice

# Distance constants
RANGES = (
    (0, "Ranged Far (14 - 8 inches)"),
    (1, "Range Near (7 - 2 inches)"),
    (2, "Melee (within 1 inch)")
)

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

# Sort function for bar graph - overrides default sort to take string length into account.
# Default sorts incorrectly, "1", "10" ... "2", should be "1","2" ... "10"
def sort_func(arg_val: str) -> int:
    return int(arg_val[0])

# Attack Damage Calculation
# First argument unused, but may use later
def attack_phase(attacker, attacker_weapon, defender) -> int:
    hit_roll = roll_dice()
    wound_threshold = 0
    if hit_roll < attacker_weapon.get("SKILL"):
        return 0
    if attacker_weapon.get("STRENGTH") > defender.get("TOUGHNESS"):
        if attacker_weapon.get("STRENGTH") >= 2*defender.get("TOUGHNESS"):
             wound_threshold = 2
        else:
             wound_threshold = 3
    else:
        if attacker_weapon.get("STRENGTH") < defender.get("TOUGHNESS"):
            if attacker_weapon.get("STRENGTH")*2 >= defender.get("TOUGHNESS"):
                wound_threshold = 6
            else:
                wound_threshold = 5
        else:
             wound_threshold = 4
    wound_roll = roll_dice()
    if wound_roll < wound_threshold:
        return 0
    save_throw = roll_dice() + attacker_weapon.get("ARMOR_PENETRATION")
    if save_throw >= defender.get("SAVE"):
        return attacker_weapon.get("DAMAGE")
    else:
        return 0

# MAIN
def main() -> None:
      
    print(f" ")
    print(f"Binomial simulation of deaths between a Space Soldier (Machine Pistol plus Knifesword) and a Souless Robot (Guass Rifle)\nBattle Simulations: {BATTLES}")
    print(f" ")
    for i_index, distance_text in RANGES:
        space_soldier_wound = SPACE_SOLDIER.get("WOUNDS")
        robot_wound = SOULESS_ROBOT.get("WOUNDS")
        robot_died = 0
        soldier_died = 0
        old_battles = 0
        robot_bars = {}
        soldier_bars = {}
        
        for number_battles in range(BATTLES):

            if space_soldier_wound <= 0 and robot_wound <= 0:
                print(f"Error: Wounds soldier {space_soldier_wound} Robots {robot_wound}")
            
            if space_soldier_wound <= 0 or robot_wound <= 0:
                if space_soldier_wound <= 0:
                    soldier_died += 1
                    n_battles = number_battles - old_battles
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


            if i_index == 0:
                space_soldier_wound -= attack_phase(SOULESS_ROBOT,GAUSS_RIFLE,SPACE_SOLDIER)
                if (space_soldier_wound > 0):
                    robot_wound -= attack_phase(SPACE_SOLDIER,MACHINE_PISTOL,SOULESS_ROBOT)               
            else:     
                if i_index == 1:
                    for i in range(GAUSS_RIFLE.get("ATTACK")):
                        space_soldier_wound -= attack_phase(SOULESS_ROBOT,GAUSS_RIFLE,SPACE_SOLDIER)
                    if (space_soldier_wound > 0):
                        robot_wound -= attack_phase(SPACE_SOLDIER,MACHINE_PISTOL,SOULESS_ROBOT)               
                else:
                    space_soldier_wound -= attack_phase(SOULESS_ROBOT,SR_MELEE,SPACE_SOLDIER)
                    if (space_soldier_wound > 0):
                        for i in range(KNIFESWORD.get("ATTACK")):
                            robot_wound -= attack_phase(SPACE_SOLDIER,KNIFESWORD,SOULESS_ROBOT)                      

        total_deaths = soldier_died + robot_died
        r_deaths = robot_died / total_deaths * 100.0
        s_deaths = soldier_died / total_deaths * 100.0
  
        # Create Bar Graph for each character
        # Robot Figures (graphs)
        robot_bars_tmp = {}
        robot_bars_tmp = dict(sorted(robot_bars.items(),key=sort_func))
        r_counter = 0 #range of values, may use later, i.e. len()
        r_mean = 0
        r_tmp = 0
        for key,value in robot_bars_tmp.items():
             r_tmp = value/total_deaths
             r_mean += int(key) * r_tmp
             robot_bars_tmp[key] = r_tmp
             r_counter += 1                 
        r_var = 0 
        for key,value in robot_bars_tmp.items():
             r_var += ((int(key) - r_mean) ** 2) * value
        robot_bars_s = {}
        robot_bars_s = robot_bars_tmp
        plt.plot(range(len(robot_bars_s)), list(robot_bars_s.values()))
        plt.xticks(range(len(robot_bars_s)), list(robot_bars_s.keys()))
        plt.xlabel("Battles")
        plt.ylabel("Probability of Death")
        plt.title(f"{distance_text}\nProbably of Number of Battles for Soldier to Kill a Robot\n{r_deaths:.1f}% Mean: {r_mean:.2f} var: {r_var:.2f}")
        plt.savefig(f"Graph_Output\\{distance_text}_Robot.png", dpi=300, bbox_inches='tight')
        plt.clf()

        # Soldier Figures (graphs)
        soldier_bars_tmp = {}
        soldier_bars_tmp = dict(sorted(soldier_bars.items(),key=sort_func))
        s_counter = 0
        s_mean = 0
        s_tmp = 0
        for key,value in soldier_bars_tmp.items():
             s_tmp = value/total_deaths
             s_mean += int(key) * s_tmp
             soldier_bars_tmp[key] = s_tmp
             s_counter += 1 
        s_var = 0
        for key,value in robot_bars_tmp.items():
             s_var += ((int(key) - s_mean) ** 2) * value
        soldier_bars_s = soldier_bars_tmp
        plt.plot(range(len(soldier_bars_s)), list(soldier_bars_s.values()))
        plt.xticks(range(len(soldier_bars_s)), list(soldier_bars_s.keys()))
        plt.xlabel("Battles")
        plt.ylabel("Probability of Death")
        plt.title(f"{distance_text}\nProbably of Number of Battles for Robot to Kill a Soldier\n{s_deaths:.1f}% Mean: {s_mean:.2f} var: {s_var:.2f}")
        plt.savefig(f"Graph_Output\\{distance_text}_Soldier.png", dpi=300, bbox_inches='tight')
        plt.clf()
        # Console Output
        print(f"{distance_text}")
        print(f"Robot Deaths:\t{r_deaths:.1f}% Battles Mean: {r_mean:.2f} var: {r_var:.2f}\nSoldier Deaths:\t{s_deaths:.1f}% Battles Mean: {s_mean:.2f} var: {s_var:.2f}")
        print(" ")

                    
if __name__ == '__main__':
     main()



