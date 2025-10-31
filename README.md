The law of large numbers states that individual random events converge on a set percentage through a large number of trials.

For example, tossing a coin. The greater the number of tosses, the more the avaerge result will converge on 50/50. 

In combat gaming, parameters such as character health, attack power, number of attacks, aiming ability, distance, etc. create a probabilistic outcome.

This application simulates a battle between two game characters, plus random dice rolls. After a large enough number of battles (trials), the win / loss percentages will converge. 

A practical use could be balancing characters for gameplay (challenging but not frustrating).

The parameters for the characters change based on distance, i.e. ranged attacks (gun, arrow) versus melee attacks (sword, mace). 

In this case, three ranges are used. The ranges have different parameters, and this demonstrates how they change outcomes. A user can study parameters and develop a strategy.

In testing, the number of trials to converge will be tradeoff of accuracy versus time or compute resources.

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
 
