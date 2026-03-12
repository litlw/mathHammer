from bs4 import BeautifulSoup
import re
import WHclasses as wh
import os

def run_parser(path, html_file):
    html_filepath = os.path.join(path, html_file)
    with open(html_filepath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    units_registry = {}

    # Helper to find T, SV, W stats in the hex bubbles
    def get_stat(card, label):
        char_divs = card.find_all('div', class_='modelCharacteristic')
        for div in char_divs:
            lbl = div.find('div', style=re.compile('font-size: 0.9em'))
            if lbl and lbl.text.strip() == label:
                val = div.find('div', style=re.compile('background: rgb'))
                return val.text.strip().replace('"', '').replace('+', '')
        return "0"

    for card in soup.find_all('div', type='card'):
        header = card.find('div', style=re.compile('font-size: 2.5em'))
        if not header: continue
        
        unit_name = header.find('span').text.strip()

        # --- NEW: Extract Unit Size (Count) ---
        unit_count = 1  # Default for characters
        
        # Search for patterns like '10x', '2x', or '6 Models' in the whole card text
        # 1. Look for spans containing 'Nx' (used for things like Triarchal Menhirs)
        count_span = card.find('span', string=re.compile(r'\d+x'))
        if count_span:
            unit_count = int(re.search(r'(\d+)', count_span.text).group(1))
        
        # 2. Look in the model options text (used for Warriors, Grey Hunters, etc.)
        options_div = card.find('div', class_='model-options')
        if options_div:
            opt_text = options_div.text.strip()
            # Matches '10x Warrior' or '6 Models'
            match = re.search(r'(\d+)\s*x|(\d+)\s*Models', opt_text)
            if match:
                # Capture whichever group found the number
                val = match.group(1) if match.group(1) else match.group(2)
                unit_count = int(val)

        # 1. Create Unit Object with the extracted count
        new_unit = wh.unit(
            name = unit_name,
            count = unit_count,
            toughness = int(get_stat(card, 'T')),
            save = int(get_stat(card, 'SV')),
            wounds = int(get_stat(card, 'W'))
        )

        # 2. Extract Defensive Abilities (Invuln / FNP)
        abilities_text = card.get_text().lower()
        if "invulnerable save" in abilities_text:
            inv_m = re.search(r'invulnerable save.*?(\d+)\+', abilities_text)
            if inv_m: new_unit.inv = [True, int(inv_m.group(1))]
        
        if "feel no pain" in abilities_text:
            fnp_m = re.search(r'feel no pain (\d+)\+', abilities_text)
            if fnp_m: new_unit.fnp = [True, int(fnp_m.group(1))]

        # 3. Parse Weapons (Associated with this Unit Card)
        weapon_tables = card.find_all('table', class_='weapons-table')
        for table in weapon_tables:
            is_melee = "Melee" in table.get_text()
            for row in table.find_all('tr'):
                cols = row.find_all('td', class_='align-middle')
                if not cols: continue
                
                w_name = row.find('span', style='font-weight: bold').text.strip()
                
                # Handle Variable Attacks/Damage (D6, D3, etc.)
                a_raw = cols[1].text.strip()
                d_raw = cols[5].text.strip()

                w_obj = wh.weapon(
                    name = w_name,
                    attacks = int(a_raw) if a_raw.isdigit() else a_raw,
                    ballistic = int(cols[2].text.strip()[0]) if cols[2].text.strip()[0].isdigit() else 0,
                    strength = int(cols[3].text.strip()),
                    ap = int(cols[4].text.strip()),
                    damage = int(d_raw) if d_raw.isdigit() else d_raw
                )
                
                # Map parsed keywords here if needed...

                if is_melee: new_unit.melee.append(w_obj)
                else: new_unit.ranged.append(w_obj)

        units_registry[unit_name] = new_unit

    return units_registry
