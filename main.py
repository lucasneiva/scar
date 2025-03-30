import os
import re # Using regex for slightly more robust parsing
from dotenv import load_dotenv
import google.generativeai as genai
import time

# --- Configuration ---
PLAYER_START_HP = 50
ENEMY_NAME = "Grasping Shadow"
ENEMY_START_HP = 30
ENEMY_ATTACK_DAMAGE = 5
GEMINI_MODEL_NAME = 'gemini-2.0-flash-lite' # Or choose another suitable model

# Global variable for the model instance
gemini_model = None

def configure_gemini():
    """Loads API key and configures the Gemini client."""
    global gemini_model
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not found in .env or environment variables.")
        return False

    try:
        genai.configure(api_key=api_key)
        # Create the model instance here
        gemini_model = genai.GenerativeModel(GEMINI_MODEL_NAME)
        print(f"✅ Google GenAI configured successfully with model {GEMINI_MODEL_NAME}.")
        return True # Indicate success
    except Exception as e:
        print(f"❌ Error configuring Google GenAI: {e}")
        return False # Indicate failure

def get_combat_outcome_from_gemini(player_hp, enemy_hp, enemy_name, player_action):
    """
    Asks Gemini to determine the outcome of the player's action.
    Returns the raw text response.
    """
    if not gemini_model:
        print("❌ Error: Gemini model not initialized.")
        return None

    prompt = f"""You are the Game Master for a brutal, minimalist horror text game.
Player HP: {player_hp}
Enemy: {enemy_name} (HP: {enemy_hp})
Player Action: "{player_action}"

Describe the immediate result of the player's action in one short, visceral sentence.
Then, on NEW SEPARATE LINES, state the damage dealt using this EXACT format (use 0 if no damage):
DAMAGE_TO_ENEMY: [Number]
DAMAGE_TO_PLAYER: [Number]
"""

    print("\n... asking the void for guidance ...")
    try:
        # Add safety settings to potentially reduce refusals for violent descriptions
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        response = gemini_model.generate_content(prompt, safety_settings=safety_settings)

        # Basic check if response has text
        if response.text:
            # print(f"DEBUG: Raw LLM Response:\n{response.text}\n---") # Uncomment for debugging
            return response.text
        elif response.candidates and not response.text:
             print("⚠️ Received response, but it might be empty or blocked due to safety filters.")
             print(f"   Finish Reason: {response.candidates[0].finish_reason}")
             print(f"   Safety Ratings: {response.candidates[0].safety_ratings}")
             return "The void stares back, offering no clear result." # Return default text
        else:
            print("⚠️ Received an empty or unexpected response from Gemini.")
            return "A wave of static washes over you, the outcome unclear." # Return default text

    except Exception as e:
        print(f"❌ An error occurred while communicating with Gemini: {e}")
        return None # Indicate failure

def parse_llm_response(text):
    """
    Parses the LLM's text response to extract description and damage numbers.
    Returns (description, damage_to_enemy, damage_to_player)
    """
    damage_to_enemy = 0
    damage_to_player = 0
    description_lines = []

    # Regex to find the damage lines (more robust than simple startswith)
    enemy_damage_match = re.search(r"DAMAGE_TO_ENEMY:\s*(\d+)", text, re.IGNORECASE)
    player_damage_match = re.search(r"DAMAGE_TO_PLAYER:\s*(\d+)", text, re.IGNORECASE)

    if enemy_damage_match:
        try:
            damage_to_enemy = int(enemy_damage_match.group(1))
        except ValueError:
            print("⚠️ Warning: Could not parse damage to enemy.")
            pass # Keep default 0

    if player_damage_match:
        try:
            damage_to_player = int(player_damage_match.group(1))
        except ValueError:
            print("⚠️ Warning: Could not parse damage to player.")
            pass # Keep default 0

    # Assume description is everything BEFORE the first damage line found
    first_damage_line_index = -1
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if "DAMAGE_TO_ENEMY:" in line.upper() or "DAMAGE_TO_PLAYER:" in line.upper():
            first_damage_line_index = i
            break

    if first_damage_line_index != -1:
        description_lines = lines[:first_damage_line_index]
    else:
        # If no damage lines found, assume the whole text is description
        description_lines = lines

    # Join description lines, stripping extra whitespace
    description = "\n".join(line.strip() for line in description_lines if line.strip()).strip()

    # Handle cases where LLM might just give description without damage lines correctly
    if not description and not enemy_damage_match and not player_damage_match:
        description = text.strip() # Use the whole text if nothing else matched

    # Ensure a default description if nothing else worked
    if not description:
        description = "The action happens, but the details are murky."


    return description, damage_to_enemy, damage_to_player


# --- Main Game Loop ---
if __name__ == "__main__":
    print("--- SCAR - Minimal Viable Prototype ---")

    if not configure_gemini():
        print("\n❌ Critical Error: Could not configure Gemini. Exiting.")
        exit() # Exit if setup fails

    # Initialize Game State
    player_hp = PLAYER_START_HP
    enemy_hp = ENEMY_START_HP
    turn = 1

    print("\n-----------------------------------------")
    print(f"You encounter the {ENEMY_NAME}!")
    print("-----------------------------------------")

    # Combat Loop
    while player_hp > 0 and enemy_hp > 0:
        print(f"\n--- Turn {turn} ---")
        print(f"Your HP: {player_hp}/{PLAYER_START_HP}")
        print(f"{ENEMY_NAME} HP: {enemy_hp}/{ENEMY_START_HP}")
        print("-----------------")

        # --- Player Turn ---
        action = input("What do you do?> ")
        if not action:
            print("You hesitate, doing nothing.")
            time.sleep(1)
            llm_description = "Hesitation offers no advantage."
            dmg_to_enemy = 0
            dmg_to_player = 0
        else:
            llm_response_text = get_combat_outcome_from_gemini(player_hp, enemy_hp, ENEMY_NAME, action)

            if llm_response_text:
                llm_description, dmg_to_enemy, dmg_to_player = parse_llm_response(llm_response_text)
            else:
                # Handle LLM communication failure
                llm_description = "The connection to the void falters. Your action has no discernible effect."
                dmg_to_enemy = 0
                dmg_to_player = 0

        # Print outcome description
        print(f"\n{llm_description}")
        time.sleep(1) # Pause for effect

        # Apply damage from player's action
        if dmg_to_enemy > 0:
            print(f"💥 You damage the {ENEMY_NAME} for {dmg_to_enemy} HP!")
            enemy_hp -= dmg_to_enemy
            enemy_hp = max(0, enemy_hp) # Ensure HP doesn't go below 0

        if dmg_to_player > 0:
            print(f"🩸 Your action causes you {dmg_to_player} HP damage!")
            player_hp -= dmg_to_player
            player_hp = max(0, player_hp) # Ensure HP doesn't go below 0

        # Check if enemy died
        if enemy_hp <= 0:
            print("\n-----------------------------------------")
            print(f"🎉 You have vanquished the {ENEMY_NAME}!")
            print("-----------------------------------------")
            break # Exit combat loop

        # Check if player died from their own action
        if player_hp <= 0:
            print("\n-----------------------------------------")
            print(f"💀 Your own maneuver proves fatal. You have died.")
            print("-----------------------------------------")
            break # Exit combat loop

        print("...")
        time.sleep(2) # Pause before enemy turn

        # --- Enemy Turn ---
        print(f"\nThe {ENEMY_NAME} lashes out!")
        time.sleep(1)
        print(f"🩸 It hits you for {ENEMY_ATTACK_DAMAGE} damage!")
        player_hp -= ENEMY_ATTACK_DAMAGE
        player_hp = max(0, player_hp) # Ensure HP doesn't go below 0

        # Check if player died from enemy attack
        if player_hp <= 0:
            print("\n-----------------------------------------")
            print(f"💀 The {ENEMY_NAME} overcomes you. You have died.")
            print("-----------------------------------------")
            break # Exit combat loop

        turn += 1 # Increment turn counter

    print("\n--- Game Over ---")
