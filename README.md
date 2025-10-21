The law of large numbers states that individual random events converge on a set percentage based on reptition. For example, a coin toss will converge more and more perfectly on 50/50 with a greater number of trials. 

This was also the motivation for Markov Processes, where the underlying probablities are not completely random.

This application is a battle between two game characters with different parameters. One is more powerful with stronger attacks and greater health. The take turns attacking, using as many battles (rounds) as neccessary for one to perish.

Since the parameters change based on distance bewteen them (far, middle - ranged, close - melee), three sets of parameters are simulated.

For example, at 12" ranged attacks, the number of deaths converges approximatel-minmal at 100000 battles: Character 1 at 15.32%, and characater 2 at 7.66%

Greater numnber of battles only refines in the percentage in the hundreths, with some variance.

**Sample:**

Monte Carlo Analysis of a fight between 1 Assault Intercessor (Bolt Pistol plus Chainsword) versus 1 Necron Warrior (Guass Reaper)
The D6 is simulated as random.randint(1, 6), the total Battles are 100000
NOTE: The percentage died and number of battles converge well enough at 100000 battles (simulations)

Within range but not less than half: 12 - 7 inches
**15318 Necron Died 15.32% of total battles, average battles to kill 3.7
7655 Marine Died 7.66% of total battles, average battles to kill 5.7**
 
Within half range but not yet melee: 6 - 2 inches, Necrons can shoot twice
13718 Necron Died 13.72% of total battles, average battles to kill 2.6
17642 Marine Died 17.64% of total battles, average battles to kill 3.7
 
Melee distance, Marines have chainsword, can attack twice
19606 Necron Died 19.61% of total battles, average battles to kill 3.3
6977 Marine Died 6.98% of total battles, average battles to kill 5.2
