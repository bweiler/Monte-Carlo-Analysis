This is a simulation of a game of combat between two characters. The outcome of the game is the death / survival of one character. Each character had numerical parameters such as 
attack power and health. Dice throws add randomness. A turn is a called battle.

The program records the battles, and number of deaths. These are normalized to create probabilities. 

The characters approach one another, amd the parameters change based on the distance between them - ranged attacks (gun, arrow) versus melee attacks (sword, mace). 

Three seperate distances are used. The program outputs figures from matplotlib (line graphs)

**Sample Output:**

Binomial simulation of deaths between a Space Soldier (Machine Pistol plus Knifesword) and a Souless Robot (Guass Rifle)
Battle Simulations: 100000

Ranged Far (14 - 8 inches)
Robot Deaths:   67.2% Battles Mean: 3.66 var: 16.18
Soldier Deaths: 32.8% Battles Mean: 2.69 var: 19.13
 
Range Near (7 - 2 inches)
Robot Deaths:   44.8% Battles Mean: 1.67 var: 5.86
Soldier Deaths: 55.2% Battles Mean: 2.95 var: 4.24
 
Melee (within 1 inch)
Robot Deaths:   73.5% Battles Mean: 2.41 var: 5.46
Soldier Deaths: 26.5% Battles Mean: 1.39 var: 7.53
 
