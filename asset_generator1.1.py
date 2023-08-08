def determine_category(psd_file):
    if "player" in psd_file.lower():
        return "player"
    elif "monster" in psd_file.lower():
        return "monster"
    elif "wand" in psd_file.lower():
        return "wand"
    else:
        return "default"

def group_layers_by_variation(layers):
    grouped = {}
    for layer in layers:
        base_name = ' '.join(layer.name.split()[:-1])  # Alles außer der letzten Nummer
        if base_name not in grouped:
            grouped[base_name] = []
        grouped[base_name].append(layer)
    return grouped

def generate_combinations(grouped_layers):
    return product(*grouped_layers.values())

def generate_variations(psd_file, max_variations=20):
    psd = psd_tools.PSDImage.open(psd_file)
    category = determine_category(psd_file)

    grouped_layers = group_layers_by_variation(psd)

    combinations = generate_combinations(grouped_layers)

    selected_combinations = sample(list(combinations), min(max_variations, len(grouped_layers)))

    for i, comb in enumerate(selected_combinations):
        output_psd = psd_tools.PSDImage(width=psd.width, height=psd.height)
        for layer in comb:
            output_psd.append(layer)
        output_psd.save(f'{category}_{i}.psd')

if __name__ == "__main__":
    generate_variations('player.psd')
import psd_tools
from itertools import product
from random import sample

def determine_category(psd_file):
    if "player" in psd_file.lower():
        return "player"
    elif "monster" in psd_file.lower():
        return "monster"
    elif "wand" in psd_file.lower():
        return "wand"
    else:
        return "default"

def group_layers_by_variation(layers):
    grouped = {}
    for layer in layers:
        base_name = ' '.join(layer.name.split()[:-1])  # Alles außer der letzten Nummer
        if base_name not in grouped:
            grouped[base_name] = []
        grouped[base_name].append(layer)
    return grouped

def generate_combinations(grouped_layers):
    return product(*grouped_layers.values())

def generate_variations(psd_file, max_variations=20):
    psd = psd_tools.PSDImage.open(psd_file)
    category = determine_category(psd_file)

    grouped_layers = group_layers_by_variation(psd)

    combinations = generate_combinations(grouped_layers)

    selected_combinations = sample(list(combinations), min(max_variations, len(grouped_layers)))

    for i, comb in enumerate(selected_combinations):
        output_psd = psd_tools.PSDImage(width=psd.width, height=psd.height)
        for layer in comb:
            output_psd.append(layer)
        output_psd.save(f'{category}_{i}.psd')

def choose_psd_file():
    # Liste alle PSD-Dateien im aktuellen Verzeichnis auf
    psd_files = [f for f in os.listdir() if f.endswith('.psd')]
    
    # Wenn keine PSD-Dateien gefunden werden, beenden
    if not psd_files:
        print("Keine PSD-Dateien im aktuellen Verzeichnis gefunden.")
        return None

    # Zeige dem Benutzer eine Liste der verfügbaren PSD-Dateien
    print("Bitte wählen Sie eine PSD-Datei aus:")
    for i, file in enumerate(psd_files, 1):
        print(f"{i}. {file}")

    # Lass den Benutzer eine Datei auswählen
    while True:
        try:
            choice = int(input("Geben Sie die Nummer der gewünschten Datei ein: "))
            if 1 <= choice <= len(psd_files):
                return psd_files[choice - 1]
            else:
                print("Ungültige Auswahl. Bitte versuchen Sie es erneut.")
        except ValueError:
            print("Bitte geben Sie eine gültige Nummer ein.")

if __name__ == "__main__":
    selected_file = choose_psd_file()
    if selected_file:
        generate_variations(selected_file)