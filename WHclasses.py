import roll
#This file keeps track of the weapons and units in these warhammer simulations

# a class for weapons
class weapon:
    def __init__(self, name, attacks, ballistic, strength, ap, damage, 
                 lethal = [False, 6], sustained = [False, 6, 1], rerollHits=[False, 0], 
                 devwounds=[False, 6], rerollWounds=[False, 0], anti=[False, 3]):
        self.name = name
        self.attacks = attacks
        self.bs = ballistic
        self.str = strength
        self.ap = ap
        self.damage = damage

        # special conditions on the weapons
        
        self.lethal = lethal # default is set to [false, 6] for rolling lethals on an unmodified 6
        self.sustained = sustained # unlike the others, sustained is [bool, crit number, number of dice added], default is false
        self.rerollHits = rerollHits # default false, set to 0 which means all will reroll
        self.rerollWounds = rerollWounds
        self.devwounds = devwounds # default [false, 6]
        self.anti = anti # default is [false, 3] for anti-monster 3+

        def imbue(self):
            def lethal(v):
                self.lethal = [True, v]
            def sustained(v, f):
                self.sustained = [True, f, v]
            def rerollHits(v):
                self.rerollHits = [True, v]
            def rerollWounds(v):
                self.rerollWounds = [True, v]
            def devWounds(v):
                self.devwounds = [True, v]
            def anti(v):
                self.anti = [True, v]
            def help():
                print("usage: weapon.imbue().lethal(6)")
                print("Imbues weapon with whatever feature you give. The first value is always the roll required")
                print("the second value (only for sustained) is the number of additional attacks")
                

    def help(self):
        print("self.name = name")
        print("self.attacks = attacks")
        print("self.bs = ballistic")
        print("self.str = strength")
        print("self.ap = ap")
        print("self.damage = damage")

        # special conditions on the weapons
        
        print("self.lethal = lethal # default is set to [false, 6] for rolling lethals on an unmodified 6")
        print("self.sustained = sustained # unlike the others, sustained is [bool, crit number, number of dice added], default is false")
        print("self.rerollHits = rerollHits # default false, set to 0 which means all will reroll")
        print("self.rerollWounds = rerollWounds")
        print("self.devwounds = devwounds # default [false, 6]")
        print("self.anti = anti # default is [false, 3] for anti-monster 3+")


class unit:
    def __init__(self, name, count, toughness, save, wounds, 
                 melee = None, ranged = None, inv = [False, 4], fnp = [False, 6], 
                 dr = [False, 1], rerollSaves = [False, 1]):
        self.name = name
        self.c = count
        self.t = toughness
        self.sv = save
        self.w = wounds

        # unit's weapons
        self.melee = melee if melee is not None else [] # this will be an array, empty by default
        self.ranged = ranged if ranged is not None else [] # this will be an array, empty by default

        #unit keywords
        self.inv = inv # an array, by default its set to false and 4++
        self.fnp = fnp # an array, by default its set to false and 6++
        self.dr = dr #damage reduction. By defeault it is set to false and 1
        self.rerollSaves = rerollSaves

    def help(self):
        print("self.name = name \n" +
        "self.c = count \n" +
        "self.t = toughness \n" +
        "self.sv = save \n" +
        "self.w = wounds \n" +

        "# unit's weapons \n" +
        "self.melee = melee if melee is not None else [] # this will be an array, empty by default \n" +
        "self.ranged = ranged if ranged is not None else [] # this will be an array, empty by default \n" +

        "#unit keywords \n" +
        "self.inv = inv # an array, by default its set to false and 4++ \n" +
        "self.fnp = fnp # an array, by default its set to false and 6++ \n" +
        "self.dr = dr #damage reduction. By defeault it is set to false and 1 \n" +
        "self.rerollSaves = rerollSaves")
    def statblock(self):
        # Header with Unit Name and Core Stats
        block = f"{'='*50}\n"
        block += f"UNIT: {self.name.upper()} ({self.c} Models)\n"
        block += f"{'='*50}\n"
        
        # Core Stats Line
        stats_line = f"T:{self.t} | SV:{self.sv}+ | W:{self.w}"
        
        # Add Invulnerable Save if present (using ++ notation)
        if self.inv[0]: 
            stats_line += f" | INV:{self.inv[1]}++"
            
        # Add Feel No Pain if present
        if self.fnp[0]: 
            stats_line += f" | FNP:{self.fnp[1]}+"
            
        # Add Damage Reduction if present
        if self.dr[0]:  
            stats_line += f" | -{self.dr[1]} DMG"
            
        block += stats_line + "\n" + "-"*50 + "\n"

        # Ranged Weapons Loop
        block += "RANGED WEAPONS:\n"
        if not self.ranged:
            block += "  None\n"
        else:
            for w in self.ranged:
                rules = []
                if w.lethal[0]: rules.append(f"Lethal({w.lethal[1]}+)")
                if w.sustained[0]: rules.append(f"Sustained({w.sustained[2]})")
                if w.devwounds[0]: rules.append("Devastating")
                if w.anti[0]: rules.append(f"Anti({w.anti[1]}+)")
                kw_str = f" [{', '.join(rules)}]" if rules else ""
                block += f"  - {w.name:.<25} A:{w.attacks} BS:{w.bs}+ S:{w.str} AP:{w.ap} D:{w.damage}{kw_str}\n"

        # Melee Weapons Loop
        block += "\nMELEE WEAPONS:\n"
        if not self.melee:
            block += "  None\n"
        else:
            for w in self.melee:
                rules = []
                if w.lethal[0]: rules.append(f"Lethal({w.lethal[1]}+)")
                if w.sustained[0]: rules.append(f"Sustained({w.sustained[2]})")
                if w.devwounds[0]: rules.append("Devastating")
                if w.anti[0]: rules.append(f"Anti({w.anti[1]}+)")
                kw_str = f" [{', '.join(rules)}]" if rules else ""
                block += f"  - {w.name:.<25} A:{w.attacks} WS:{w.bs}+ S:{w.str} AP:{w.ap} D:{w.damage}{kw_str}\n"
        
        return block

class combat:
    def __init__(self, attackingUnit, defendingUnit, iterations):
        self.attackingUnit = attackingUnit
        self.defendingUnit = defendingUnit
        self.iterations = iterations

        self.combatResults = {
            "attackingUnit" : {
                "name" : attackingUnit.name, 
                "size" : attackingUnit.c,
                "toughness": attackingUnit.t,
                "saves" : {
                    "base save": attackingUnit.sv,
                    "has invul?" : attackingUnit.inv[0],
                    "invulnerable save" : attackingUnit.inv[1],
                    "has FNP?" : attackingUnit.fnp[0],
                    "FNP" : attackingUnit.fnp[1],
                    "has reroll saves?" : attackingUnit.rerollSaves[0],
                    "rerolls on" : attackingUnit.rerollSaves[1]
                    },
            },
            "defendingUnit" : {
                "name" : defendingUnit.name, 
                "size" : defendingUnit.c,
                "toughness": defendingUnit.t,
                "saves" : {
                    "base save": defendingUnit.sv,
                    "has invul?" : defendingUnit.inv[0],
                    "invulnerable save" : defendingUnit.inv[1],
                    "has FNP?" : defendingUnit.fnp[0],
                    "FNP" : defendingUnit.fnp[1],
                    "has reroll saves?" : defendingUnit.rerollSaves[0],
                    "rerolls on" : defendingUnit.rerollSaves[1]
            
                    },
            },
            "iterations": 0, 
            "combats": []
                      }
        self.meleeCombat()
        self.rangedCombat()

    def meleeCombat(self):
        
        for w in self.attackingUnit.melee:
            combat = {
            "type": "melee combat",
            "weapon": {
                "name": w.name,
                "attacks": w.attacks,
                "weapon skill": w.bs,
                "strength": w.str,
                "ap": w.ap,
                "damage": w.damage,
                "special rules": {
                    # reroll hits, sustained, lethal, reroll wounds, devastating wounds, anti
                    "reroll hits": {
                        "state": w.rerollHits[0],
                        "rerolls on" : w.rerollHits[1]
                    },
                    "reroll wounds": {
                        "state" : w.rerollWounds[0],
                        "rerolls on": w.rerollWounds[1]
                    },
                    "sustained hits": {
                        "state": w.sustained[0],
                        "sustained on": w.sustained[1],
                        "sustained hits count": w.sustained[2]
                    },
                    "lethal hits": {
                        "state": w.lethal[0],
                        "lethal on": w.lethal[1]
                    },
                    "devastating wounds": {
                        "state": w.devwounds[0],
                        "devastating wounds on": w.devwounds[1]
                    },
                    "anti": {
                        "state": w.anti[0],
                        "anti on": w.anti[1]
                    }
                }
                },
            "results": []
            }
            
            for i in range(self.iterations):
                self.combatResults["iterations"] += 1
                combatTracker = {"attacks": 0, "hits": 0, "wounds": 0, "unsavedWounds": 0, 
                                 "totalDamage": 0, "damageDealt": 0, "modelsLost": 0}
                
                # --- NEW LOGIC: Variable Attacks ---
                # We resolve the dice string for each model in the unit
                total_attacks = 0
                for _ in range(self.attackingUnit.c):
                    total_attacks += roll.solve_dice(w.attacks)
    
                for a in range(total_attacks):
                    self.hit(combatTracker, w)
    
                self.tallyDead(combatTracker, w)
                combat["results"].append(combatTracker)
            self.combatResults["combats"].append(combat)
        return self.combatResults

        #     for i in range(self.iterations):
        #         self.combatResults["iterations"] += 1
        #         combatTracker = {
        #             "attacks": 0, 
        #             "hits": 0, 
        #             "wounds": 0, 
        #             "unsavedWounds": 0, 
        #             "totalDamage": 0, 
        #             "damageDealt": 0, 
        #             "modelsLost": 0
        #             }
        #         for a in range(self.attackingUnit.c * w.attacks):
        #             self.hit(combatTracker, w)

        #         self.tallyDead(combatTracker, w)
        #         combat["results"].append(combatTracker)
        #     self.combatResults["combats"].append(combat)
        # return self.combatResults
    def rangedCombat(self):
        # Reset global iteration tracker for this report
        # self.combatResults["iterations"] = 0
        # self.combatResults["combats"] = []

        for w in self.attackingUnit.ranged:
            # Setup the report metadata for this weapon
            combat_data = {
                "type": "ranged combat",
                "weapon": {
                    "name": w.name,
                    "attacks": w.attacks,
                    "ballistic skill": w.bs,
                    "strength": w.str,
                    "ap": w.ap,
                    "damage": w.damage,
                },
                "results": []
            }

            for i in range(self.iterations):
                self.combatResults["iterations"] += 1
                combatTracker = {
                    "attacks": 0, 
                    "hits": 0, 
                    "wounds": 0, 
                    "unsavedWounds": 0, 
                    "totalDamage": 0, 
                    "damageDealt": 0, 
                    "modelsLost": 0
                }

                # Determine total attacks for the whole unit
                total_attacks = 0
                for model in range(self.attackingUnit.c):
                    # 1. Resolve random attacks (e.g., 'D6')
                    base_a = roll.solve_dice(w.attacks)
                    
                    # 2. Add [Blast] bonus if applicable
                    # Rules: +1 attack for every 5 models in target unit
                    blast_bonus = 0
                    if "blast" in str(w.name).lower(): # Assuming 'Blast' is in name or keywords
                        blast_bonus = self.defendingUnit.c // 5
                    
                    total_attacks += (base_a + blast_bonus)

                # Execute the rolls
                for a in range(total_attacks):
                    self.hit(combatTracker, w)

                # Tally damage and model removal
                self.tallyDead(combatTracker, w)
                combat_data["results"].append(combatTracker)
            
            self.combatResults["combats"].append(combat_data)
            
        return self.combatResults

    def hit(self, combat, weapon):
        r = roll.roll()
        combat["attacks"] += 1
        
        if r >= weapon.bs:
            combat["hits"] += 1
            
            # Priority 1: Lethal Hits (Critical Hits skip the Wound Roll)
            if weapon.lethal[0] and r >= weapon.lethal[1]:
                combat["wounds"] += 1
                self.save(combat, weapon)
            else:
                # Priority 2: Standard Hits go to Wound Step
                self.wound(combat, weapon)
    
            # Priority 3: Sustained Hits (Extra hits go to Wound Step)
            if weapon.sustained[0] and r >= weapon.sustained[1]:
                bonus = roll.solve_dice(weapon.sustained[2])
                combat["hits"] += bonus
                for _ in range(bonus):
                    self.wound(combat, weapon)
        return combat

    def wound(self, combat, weapon):
        r = roll.roll()
        wnd = weapon.anti[1] if weapon.anti[0] is True else roll.toWound(weapon.str, self.defendingUnit.t)
        
        if r >= wnd:
            # if the hit wounds
            combat["wounds"] += 1
            
            if weapon.devwounds[0] is True and r >= weapon.devwounds[1]:
                # if the weapon has dev wounds
                combat["unsavedWounds"] += 1
            else:
                self.save(combat, weapon)
                
        elif r < wnd and weapon.rerollWounds[0] is True:
            r = self.hasReroll(weapon.rerollWounds, r)
            
            if r >= wnd:
                combat["wounds"] += 1
                
                if weapon.devwounds[0] is True and r >= weapon.devwounds[1]:
                    # if the weapon has dev wounds
                    combat["unsavedWounds"] += 1
                    
                else:
                    self.save(combat, weapon) # call next function               


    def save(self, combat, weapon):
        r = roll.roll()
        # Determine best available save (Armor vs Invul)
        armor_target = self.defendingUnit.sv - weapon.ap
        invul_target = self.defendingUnit.inv[1] if self.defendingUnit.inv[0] else 99
        
        target = min(armor_target, invul_target)
        
        if r < target:
            if self.defendingUnit.rerollSaves[0]:
                r = self.hasReroll(self.defendingUnit.rerollSaves, r)
                if r < target:
                    combat["unsavedWounds"] += 1
            else:
                combat["unsavedWounds"] += 1

    def damage(self, weapon):
        raw_dmg = roll.solve_dice(weapon.damage)
        # Apply Damage Reduction (ensure min 1)
        dmg = max(1, raw_dmg - self.defendingUnit.dr[1]) if self.defendingUnit.dr[0] else raw_dmg
        
        dd = 0
        for d in range(dmg):
            if self.defendingUnit.fnp[0]:
                r = roll.roll()
                # FNP succeeds on roll >= target (e.g. 5+)
                if r < self.defendingUnit.fnp[1]:
                    dd += 1
            else:
                dd += 1
        return dd

        
    def tallyDead(self, combat, weapon):
        modelWounds = self.defendingUnit.w
        combat["totalDamage"] = 0 # Ensure this is an int, not a string
        
        for w in range(combat["unsavedWounds"]):
            dd = self.damage(weapon)
            combat["totalDamage"] += dd # Tracking actual damage dealt
            combat["damageDealt"] += dd
    
            if dd >= modelWounds:
                combat["modelsLost"] += 1
                modelWounds = self.defendingUnit.w
            else: 
                modelWounds -= dd
        return combat


        

        
    def hasReroll(self, rerolls, r):
        if rerolls[1] == 0:
            # Full Rerolls
            return roll.roll()
        else:
            if rerolls[1] == r:
                # Reroll X's
                return roll.roll()
            else:
                return r       






