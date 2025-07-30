#!/usr/bin/env python3
"""
Spruce Compiler CLI - The main command-line interface.
"""

import os
import random
import sys
import time
from typing import Dict, List, Tuple


# ASCII Art Tree

ASCII_TREE = """
             ∪            
          ⠁╖↓⇕╛⠖          
         ⠅⠼↘╞⇖⇖╢╠⠨        
        ⠔↗↖╩⟷↗→→╞╒        
       ⠞⠭╚↑⟸╩⇒▊↓╢╬⠇       
      ⠁⠿→↗▓╨▊▒▒⇖⇘⠯⠜⊕      
      ⠘╛╙↘⟸⇓⇗╦╘╤░↔↔⊗      
    ♯⠓⠥╙╟╞╥⟵▔⇓╦╛╩╚⠿⠦⠄     
    ⠪╩╧╟╤▅⇑╖⟸╡╣╥░╬⇔╚      
     ⠟⇒╚⠻╡⟺⇗↓↘▂↑╥⇖▒⠶⠵     
   ∨⠂⠸↔╜╗╞╪⇑╥⟹⇐⟸↓⇙╠↔⠭⊕    
   ⊤╞╛╧╤╫╦╝↙⟵⟷╪↙╩▘⇙↖╗     
   ⠠⠳⠿←↘⇖╡▂⇐▝⟺⟶╠→→↗╥╧⠯∇   
  ⠔╚⠺╥╡╠⇗↖↕╟╝↖↖→╛↑╤╜║╟⠘   
  ⠋⠽╡╝╔╬↕⇗⟸↓▏▓⟵╡╫⟶╙↔⠈⠑∥   
  ⠵╕╒╛═╪→⟷⇒▂▄⇕↕⠿⇐╢╨╥╞⠓    
  ⠸←╡╤⟶╧╞↓▍▓▗↘→╜⟹⇙╫╬╪→⠧   
 ⠉╔⠬╗╜⟸⇐⟶╧↗⇖╩↙▉╕╘↓↗╨⠻╔⠣   
 ⊇♮⠮⠨╙╫⇙╢↗▉╝⟸⇔⇕╬╞↙╖⇗←⠔⊤   
 ⠉⠰╙⠽⇓╠↘↘⠹╢↙▒⟷⠿╪⇗╨╘╬⇐⠿⠥   
 ⠠⠾⠗╗⟸╨⇑╣↕╬▊▜▓╥╧⠱╣⇒╙╝╞⠼⠄  
 ∨ ⠽╪░╤═↘⇖╫⟹⇕↘→⠿⠣⟶╦╕╢⠮╖⠈  
  ⠤⠶╟╒╕↙╫▓⇑╠▔╢╙╓⠩⠮╟╣↑⠪♫⠛  
 ⠮⠒⠟╤╝▂↓⇘▊⟵▙▃⟸⠸⠿⠣⠻╬⠶⠦╙╡⠉≥ 
  ⠢╧╢╤╠⇓▍⟷█⇗╣⟺⠷╝╪⇔↔╚⠭⠻╨╠≪ 
  ⠥╡⠶⠹⠿⇑⟹▐▕⇒╣⇓⠢⟶╗⠸⠺╛║⠁♪⠣⠧ 
 ⊗⠺⠰⠂╓↙⟵⇔⇙╨▃▎⟵⠦⠳║╫╕⇑╡⠮♮   
 ⠀⠄ ⠕╗▁▓╩░▋▕▓⇗⠐⠽←╖╜╩╬╟⠷   
   ⠞↖╪⟵╪▒╣↙▒↓╟╣⠸═↔↙╗↖╔⠽   
   ⠬⇐↗╪⇘▟⇖╕▇╩╪⇑╕╡↖╠╔⠿⇐⠼⠍  
  ⊥╩↓╦╡╦⟺▊╡▒⟷▅╝⠵↕█╦⠺⠻╕⠊   
  ⠨╬▃╠╕░╛⇔╢↙⇕⇐⠲╥⠯╒╜╥╟⠗    
  ⠣↘╝⠪╖⠲╘╩╖⟺⇑╣↕╜╝╜╨╓╒╪⊤♭  
 ⠎╤↓⠍⠣↖⇔⇒⇓⠐╓╜⟷╙╢╬↑⠫⠩↑╢╞⠣  
  ⠖⠝⊕╨⇕▎╘╙╢⟺╤⟺↖╗╤╬╔⠿⠨⠘⠴⠙  
  ⠟ ⠨╫⇘║⠭↘⇖▅⠹↗⇒⇐╙↕╫╔⠩⠛⠒   
    ╚⟷╗╝←⇔⇒⠾╡←↑╕⠺╜⠷⇓⠴     
   ⠰╥╨╤╒⠪⇑▄→⠲↗╟⇗⇓╝╧╦╝⠰    
   ⠳⠞⠺⠉║⇕⇔⟶⠱⠶▂⇔▎←↖⠠⠼╗╤♯   
   ⠤⠍⠌⠋↖⇗⇖↑⠺⠳╣↗╛▂↕⠷⠹⠚⠯≫   
      ╧╩⟵⠥↘⠦╔╣╞↓←╟╒⠋      
     ⠏╓▒⇔╨⠝⠸⠵╘╧╔↘↑←⠩      
     ♬↑╖╕╚⠍⠹⠛╣▙╫↔╘→⠮      
     ∩⠼⠾⠦⠵∇═⠯╝⠤╘╕╒⠲⠺      
      ⠝⠊  ≫⠮⠴⠽⠗╛╜⠝⠏       
           ⠰⠡╚⠛⠍⠨≪        
           ╖⠲⠷⠅           
          ∧╔⠱⠾⠎           
          ⠄⠢╖⠷⠍           
          ♯⠯║╠⠞           
          ⠔╔╖╓╙           
          ⠣⠴⠺╙⠾           
          ╘⠲╨╖⠼           
         ⠘⠶⠴╟╥╖≫          
         ╓╞═⠪╥╝╙          
        ⠘→⠸⠶╢╦╜╧⠚         
       ⠘╡↔⠹╣⠲╩╟╒╥⠖        
     ∓⠧⠱╢⠯╬╟╚⠽⠽╘↓⠷⠘       
    ⠗⠰⠴⠯║⠱╗╛╓╞╧⠹╓⠜╒⠫⠗     
         ⠇≪⠋♯∧♯           
"""

# Spruce Facts Database
SPRUCE_FACTS_DB: Dict[str, List[str]] = {
    "GENERAL": [
        "About 35 spruce species thrive across the cold temperate zones of the Northern Hemisphere.",
        "Spruces can live for centuries—Sitka giants often hit 500–700 years and tower over 90 m tall.",
        "Norway spruce clone 'Old Tjikko' flaunts a root system nearly 10,000 years old.",
        "Sitka spruce is the heavyweight champ—growing in pure coastal stands from California to Alaska."
    ],

    "HISTORY & CULTURE": [
        "'Spruce' traces back to Prussia—medieval Europe's timber-export hotspot.",
        "Jacques Cartier's crew cured scurvy with spruce-needle beer, courtesy of Iroquoian know-how.",
        "Spruce resin gum predates modern chewing gum—'State of Maine Pure Spruce Gum' hit shelves in 1848.",
        "Pilots prized spruce for WW I–II aircraft frames—Hughes's 'Spruce Goose' took its name seriously.",
        "Since 1933, Rockefeller Center has crowned its holiday festivities with a towering Norway spruce."
    ],

    "MUSIC": [
        "Spruce is the ultimate tonewood—guitars, violins, pianos, mandolins, harps and more all love it.",
        "Adirondack spruce ruled pre-war Martin & Gibson guitars—loud, punchy, and endlessly collectible.",
        "Sitka spruce powers most modern guitar and piano tops, delivering clear, balanced tone at any volume.",
        "Cremona's finest (Stradivari, Guarneri) carved Alpine spruce into violins that still sing in concert halls.",
        "Engelmann spruce brings a sweet, fingerstyle-friendly voice—rich overtones straight out of the box.",
        "Lutz spruce's hybrid vigor turbo-charges guitars: think bold projection, warm mids, and lightning response."
    ],

    "PHYSICS": [
        "Spruce boasts a superstar stiffness-to-weight ratio—light as a feather, stiff as… well, spruce!",
        "Sound zips along a spruce grain at ~5,000–6,000 m/s—about 15× faster than in air.",
        "It's highly anisotropic: super-stiff along the grain, more flexible across—quarter-sawing locks in perfect tone.",
        "Low internal damping means spruce rings out with long sustain instead of quickly dying away.",
        "Quarter-sawn spruce shows off 'silk' (medullary rays) that looks stunning and adds cross-grain strength."
    ]
}


def get_random_fact() -> str:
    """Get a random spruce fact from the database."""
    # Flatten all facts into a single list
    all_facts = []
    for category, facts in SPRUCE_FACTS_DB.items():
        all_facts.extend(facts)
    
    return random.choice(all_facts)


# Character sets for dynamic mutations
TREE_CHARS = "⠁⠂⠃⠄⠅⠆⠇⠈⠉⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗⠘⠙⠚⠛⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"
BRANCH_CHARS = "╔╗╚╝╞╡╤╧╪╫╬╭╮╯╰╱╲╳"
SYMBOL_CHARS = "↑↓←→↔↕↖↗↘↙⇐⇑⇒⇓⇔⇕⇖⇗⇘⇙⇚⇛⇜⇝⇞⇟⇠⇡⇢⇣⇤⇥⇦⇧⇨⇩⇪⇫⇬⇭⇮⇯⇰⇱⇲⇳⇴⇵⇶⇷⇸⇹⇺⇻⇼⇽⇾⇿"
BLOCK_CHARS = "▁▂▃▄▅▆▇█▉▊▋▌▍▎▏▐▔▕▖▗▘▙▚▛▜▝▞▟"
SPECIAL_CHARS = "∧∨∩∪⊕⊗⊤⊥♯♮♭♪♫≪≫∇∓"


def get_char_variants(char: str) -> List[str]:
    """Get similar character variants for mutation effects."""
    if char in TREE_CHARS:
        return [char] + random.sample(TREE_CHARS, min(3, len(TREE_CHARS)))
    elif char in BRANCH_CHARS:
        return [char] + random.sample(BRANCH_CHARS, min(2, len(BRANCH_CHARS)))
    elif char in SYMBOL_CHARS:
        return [char] + random.sample(SYMBOL_CHARS, min(2, len(SYMBOL_CHARS)))
    elif char in BLOCK_CHARS:
        return [char] + random.sample(BLOCK_CHARS, min(2, len(BLOCK_CHARS)))
    elif char in SPECIAL_CHARS:
        return [char] + random.sample(SPECIAL_CHARS, min(2, len(SPECIAL_CHARS)))
    else:
        return [char]


def mutate_line(line: str, mutation_chance: float = 0.15) -> str:
    """Apply random character mutations to a line."""
    if not line.strip():
        return line
    
    mutated = []
    for char in line:
        if char != ' ' and random.random() < mutation_chance:
            variants = get_char_variants(char)
            mutated.append(random.choice(variants))
        else:
            mutated.append(char)
    return ''.join(mutated)


def add_growth_sparkles(line: str, sparkle_chance: float = 0.08) -> str:
    """Add occasional sparkle effects during growth."""
    sparkles = "✦✧✨⋆★☆"
    if not line.strip():
        return line
    
    # Add sparkles at random positions
    chars = list(line)
    for i, char in enumerate(chars):
        if char != ' ' and random.random() < sparkle_chance:
            chars[i] = random.choice(sparkles)
    
    return ''.join(chars)


def clear_screen() -> None:
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def animate_tree_growth() -> None:
    """Animate the tree growing from bottom to top with dynamic mutations."""
    tree_lines = ASCII_TREE.strip().split('\n')
    max_tree_width = max(len(line) for line in tree_lines) if tree_lines else 0
    
    # Clear screen and position cursor
    clear_screen()
    
    # Animate tree growing from bottom to top
    for i in range(len(tree_lines)):
        clear_screen()
        
        # Print empty lines to position the partial tree at the bottom
        empty_lines = len(tree_lines) - i - 1
        for _ in range(empty_lines):
            print()
        
        # Print the tree lines from bottom up to current position with mutations
        for j in range(len(tree_lines) - i, len(tree_lines)):
            line = tree_lines[j]
            
            # Apply different effects based on growth stage
            if j == len(tree_lines) - i:  # The newest/growing edge
                # New growth gets sparkles and higher mutation
                line = add_growth_sparkles(line, sparkle_chance=0.12)
                line = mutate_line(line, mutation_chance=0.25)
            elif j > len(tree_lines) - i - 3:  # Recent growth
                # Recent growth gets some mutation
                line = mutate_line(line, mutation_chance=0.15)
            else:  # Established growth
                # Older parts get subtle mutations to stay "alive"
                line = mutate_line(line, mutation_chance=0.08)
            
            print(line)
        
        # Variable timing for more organic feel
        base_delay = 0.06
        variation = random.uniform(-0.02, 0.02)
        time.sleep(max(0.02, base_delay + variation))
    
    # Show the complete tree with subtle ongoing mutations for a few cycles
    for cycle in range(8):
        clear_screen()
        
        for line in tree_lines:
            # Very subtle mutations to keep it alive
            mutated_line = mutate_line(line, mutation_chance=0.05)
            print(mutated_line)
        
        time.sleep(0.15)
    
    # Final pause with the original tree
    clear_screen()
    for line in tree_lines:
        print(line)
    time.sleep(0.5)


def animate_text_display() -> None:
    """Animate the display of welcome text and spruce fact."""
    # Get a random fact and format it
    fact = get_random_fact()
    
    # Create the text content
    welcome_lines = [
        "",
        "spruce compiler is still growing",
        "",
        "    maybe one day I'll be",
        "       a soundboard...",
        "",
        "",
    ]
    
    # Format the fact with line breaks for haiku-like appearance
    words = fact.split()
    formatted_fact_lines = []
    current_line = ""
    
    for word in words:
        if len(current_line + " " + word) > 35:  # Wrap at ~35 chars for haiku feel
            if current_line:
                formatted_fact_lines.append(current_line.strip())
                current_line = word
            else:
                formatted_fact_lines.append(word)
        else:
            current_line = current_line + " " + word if current_line else word
    
    if current_line:
        formatted_fact_lines.append(current_line.strip())
    
    # Add formatted fact lines with indentation
    fact_lines = [""]
    for line in formatted_fact_lines:
        fact_lines.append(f"   {line}")
    
    all_text_lines = welcome_lines + fact_lines
    
    # Get tree lines for positioning
    tree_lines = ASCII_TREE.strip().split('\n')
    max_tree_width = max(len(line) for line in tree_lines) if tree_lines else 0
    
    # Animate text appearing line by line
    for i in range(len(all_text_lines) + 1):
        clear_screen()
        
        # Print tree with text lines revealed so far
        text_start_line = 35  # Start text around middle of tree
        for j, tree_line in enumerate(tree_lines):
            # Add very subtle life to the tree during text phase
            if random.random() < 0.03:  # Very low chance for subtle movement
                tree_line = mutate_line(tree_line, mutation_chance=0.04)
            
            tree_part_padded = tree_line.ljust(max_tree_width + 4)
            
            # Add text if we're in the text region and have revealed this line
            text_index = j - text_start_line
            if text_index >= 0 and text_index < len(all_text_lines) and text_index < i:
                right_part = all_text_lines[text_index]
            else:
                right_part = ""
            
            print(f"{tree_part_padded}{right_part}")
        
        time.sleep(0.35)  # Pause between text lines
    
    # Final pause to let user read the complete message
    time.sleep(1.0)
    print()  # Final newline


def display_welcome() -> None:
    """Display the animated welcome sequence."""
    animate_tree_growth()
    animate_text_display()


def main() -> None:
    """Main entry point for the spruce CLI."""
    try:
        display_welcome()
    except KeyboardInterrupt:
        print("\n👋 Thanks for visiting the spruce!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Oops! Something went wrong: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 