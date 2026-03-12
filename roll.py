import random
import pandas as pd
import matplotlib.pyplot as plt
import re

def solve_dice(value):
    """Turns strings like 'D6', 'D3', 'D6+2' into integers. Returns ints as-is."""
    if isinstance(value, int):
        return value
    
    value = str(value).upper().replace(" ", "")
    # Match pattern: Optional multiplier, D, Dice sides, Optional modifier
    # e.g., '2D6+2'
    match = re.match(r'(\d+)?D(\d+)([+-]\d+)?', value)
    if match:
        num_dice = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0
        
        total = sum(random.randint(1, sides) for _ in range(num_dice)) + modifier
        return max(1, total) # 40k rules: damage/attacks usually can't be less than 1
    
    return 0 # Fallback

#this rolls dice
def roll ():
    return random.randint(1, 6)

def reRolls (rolled, goal, fullRerolls, partialreRolls):
    # check for failure
    if fullRerolls[0]:
        # put reroll logic in here 
        if rolled < goal:
            return roll()

    elif partialRerolls[0]:
        if rolled == partialRerolls[1]:
            return roll()

    else:
        return rolled

# # this is a function to roll dice and return how many "pass"
# def rollDice (dCount):
#     results = []
#     for i in range(dCount):
#         results.append(roll())
#     return results

    
###################################
# this is for the combat tracking #
###################################

# this is a function to determine the required roll for a wound roll
def toWound(strength, toughness):
     # 1. Check the strongest advantage first
    if strength >= 2 * toughness:
        return 2
    
    # 2. Check if strength is simply higher than toughness
    elif strength > toughness:
        return 3
    
    # 3. Check for equality
    elif strength == toughness:
        return 4
    
    # 4. Check the weakest disadvantage (Strength is half or less)
    elif strength <= (toughness / 2):
        return 6
        
    # 5. If none of the above, Strength must be less than Toughness but more than half
    else:
        return 5

###############################
# this is for running reports #
###############################

# make a report


def announce(data):
    attacking_unit = data['attackingUnit']['name']
    attacker_count = data['attackingUnit']['size']
    defending_unit = data['defendingUnit']['name']
    
    print(f"\n{'='*60}")
    print(f"COMBAT REPORT: {attacker_count}x {attacking_unit} vs {defending_unit}")
    print(f"{'='*60}")

    for combat in data["combats"]:
        df_results = pd.DataFrame(combat["results"])
        weapon_name = combat['weapon']['name']
        weapon_type = combat['type'].upper()

        # 1. Print Text Statistics
        print(f"\nREPORT FOR {weapon_type}: {weapon_name}")
        print(f"-{'-'*45}")
        print(f"Avg Damage per activation:      {df_results['damageDealt'].mean():.2f}")
        print(f"Avg Models killed per turn:     {df_results['modelsLost'].mean():.2f}")
        print(f"Max Damage recorded:            {df_results['damageDealt'].max()}")
        
        # 2. Generate Frequency Distribution Graph
        plt.figure(figsize=(10, 5))
        
        # Calculate frequency of each damage value
        # .sort_index() ensures the X-axis counts up 0, 1, 2, 3...
        distribution = df_results['damageDealt'].value_counts().sort_index()
        
        distribution.plot(kind='bar', color='steelblue', edgecolor='black', alpha=0.8)
        
        # Formatting the Graph
        plt.title(f"Damage Distribution: {weapon_name}\n({attacker_count} Models vs {defending_unit})", fontsize=12)
        plt.xlabel("Total Damage Dealt in One Turn", fontsize=10)
        plt.ylabel("Frequency (Number of Iterations)", fontsize=10)
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        
        # Optional: Add data labels on top of bars for precision
        for i, val in enumerate(distribution):
            plt.text(i, val + (data['iterations']*0.01), str(val), ha='center', va='bottom', fontsize=8)

        plt.tight_layout()
        plt.show()

        # 3. Print the standard summary table below the graph
        summary = df_results.agg(['min', 'median', 'mean', 'max']).transpose()
        print("\nStatistical Summary:")
        print(summary.round(2))
        print(f"\n{'='*60}")