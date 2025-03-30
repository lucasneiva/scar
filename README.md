
![ChatGPT Image Mar 30, 2025, 07_59_24 PM](https://github.com/user-attachments/assets/34591dd2-61b8-47eb-b319-3ff0d3bc0ebe)

# SCAR - Simulated Combat Action Resolver

**SCAR** is an experimental project that creates a brutal, horror-focused text adventure with a revolutionary combat system powered by Large Language Models (LLMs). Players navigate a nightmarish realm where bodily harm, sanity, and survival are constantly at stake, with combat outcomes determined through natural language processing.

**(Early Development / Core Combat Focus)**

## Core Concept

SCAR takes a different approach to text-based gaming by focusing on visceral, detailed combat in a horrifying world:

1. **Natural Language Combat**: Players describe their actions in plain language, and the LLM interprets and judges the outcomes based on character stats, enemy attributes, and environmental factors.

2. **Body Horror Survival**: The game tracks specific body parts and injuries, creating a detailed damage system where players might lose limbs, suffer debilitating wounds, or experience grotesque transformations.

3. **Procedural Nightmare Generation**: Each playthrough generates unique horrifying enemies and environments, ensuring no two runs are alike.

4. **Psychological Horror**: Beyond physical threats, the game tracks sanity, hunger, and other survival elements that add layers of tension to every decision.

The primary gameplay loop focuses on **surviving encounters** with nightmarish entities while managing deteriorating physical and mental states.

## Project Goals (Immediate Focus)

* Implement the core combat system: `Player Description → Parse Intent → Apply Stats → LLM Judgment → Apply Outcomes`.
* Use an LLM (Gemini) to:
  * Generate unique, horrifying enemies with distinct characteristics and behaviors.
  * Interpret player combat actions and determine realistic outcomes.
  * Create vivid, disturbing descriptions of injuries and effects.
* Create a detailed character state system that tracks:
  * Individual body parts and their condition.
  * Status effects (bleeding, infection, broken bones, etc.).
  * Mental state and sanity.
* Build a fair but unpredictable combat resolution system that respects player stats while allowing for creative approaches.
* Run as a simple console application with text-based interface.

## Combat System Design

* **Input Flexibility**: Players can describe actions naturally ("I lunge at the creature's exposed eye while covering my wounded arm")
* **Contextual Awareness**: The system tracks previous actions, environmental conditions, and current injuries
* **Consequence Modeling**: Injuries affect future performance in realistic ways
* **Brutal Realism**: Combat is dangerous, quick, and often devastating

## Technology Stack

* **Language:** Python 3.x
* **LLM Interaction:** `google-generativeai` library (Gemini model)
* **State Management:** JSON or similar for character/enemy state
* **User Interface:** Console-based with formatted text output

## Future Expansion (Post-Combat System)

* Implement procedural world generation for exploration.
* Add resource management and scavenging mechanics.
* Develop progression systems that provide some advantages on subsequent runs.
* Create a simple narrative framework to explain the nightmarish realm.
* Potentially add minimal visual elements to enhance the horror experience.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/scar.git
   cd SCAR
   ```

2. **Set up environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key:**
   Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

5. **Run the prototype:**
   ```bash
   python combat_prototype.py
   ```

## Contributing

This is currently a personal experimental project. Contributions are not actively sought at this stage, but feel free to fork the repository and experiment!

---

> *"In SCAR, survival is temporary. Horror is eternal."*
