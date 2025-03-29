![ChatGPT Image Mar 29, 2025, 02_54_02 PM](https://github.com/user-attachments/assets/b23434e1-3c96-4fcb-b7d1-17923fd57728)

# WEAVE - World Engine Architecture for Vivid Exploration

**WEAVE** is an experimental project aiming to create a text adventure engine that blends procedural world generation powered by Large Language Models (LLMs) with a robust consistency layer managed by code. The goal is to provide an immersive exploration experience akin to reading an interactive book, where the world unfolds dynamically but maintains structural integrity and memory.

**(Early Stage / MVP Focus)**

## Core Concept

Traditional text adventures rely on pre-defined worlds. Purely LLM-driven adventures often lack consistency. WEAVE attempts to bridge this gap:

1.  **LLM as the Sensory Narrator:** The LLM is responsible for generating rich, evocative descriptions of locations, acting as the player's senses (sight, sound, smell, touch). It can also generate new areas procedurally based on context and a general world theme.
2.  **Code as the Consistency Layer:** A graph-based world model (using Python and `networkx`) maintains the definitive structure of the generated world. It tracks:
    *   **Rooms/Nodes:** Unique locations generated.
    *   **Connections/Edges:** How rooms are spatially linked (exits).
    *   **Core State:** Essential information about visited locations and potentially persistent elements (though item/state persistence is a post-MVP goal).
    *   This layer ensures that if you go North from Room A to Room B, going South from Room B correctly leads back to Room A. It provides the ground truth for the LLM's descriptions.

The primary gameplay loop focuses on **exploration**, where moving into uncharted territory triggers the LLM to generate a new location, which is then integrated into the consistent graph structure managed by the code.

## Project Goals (MVP)

*   Implement a basic game loop: `Input -> Process Command -> Update State -> Generate Narrative -> Output`.
*   Use an LLM (e.g., OpenAI's GPT series) via API calls for:
    *   Generating descriptive text for existing rooms (based on stored data).
    *   Procedurally generating descriptions for *new* rooms upon exploration.
*   Use `networkx` to manage a graph representing the explored world map.
    *   Nodes represent rooms, storing basic descriptive data.
    *   Edges represent connections between rooms (exits).
*   Ensure basic spatial consistency: Moving between connected rooms works reliably in both directions.
*   Handle basic movement commands (e.g., "north", "south", "east", "west").
*   Run as a simple console application.

## What's NOT in the MVP

*   Saving and loading game state.
*   Complex interactions (items, puzzles, NPCs).
*   Advanced Natural Language Understanding (NLU) for commands beyond basic movement.
*   Extracting complex structured data from LLM generation (e.g., automatically identifying items or specific features from generated text).
*   Combat or complex skill systems.
*   A graphical user interface.

## Technology Stack (Initial)

*   **Language:** Python 3.x
*   **LLM Interaction:** `google-generativeai` library (or equivalent for chosen provider)
*   **World Graph:** `networkx` library
*   **Configuration/State (Simple):** Potentially JSON for initial setup or simple state.

## Getting Started (Setup Instructions)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/weave.git
    cd weave
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows:
    # venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    # (You'll need to create a requirements.txt file - see below)
    ```
4.  **Configure API Key:**
    *  Use a `.env` file and the `python-dotenv` library.

5.  **Run the main script:**
    ```bash
    python main.py
    ```

## Contributing

This is currently a personal experimental project. Contributions are not actively sought at this stage, but feel free to fork the repository and experiment!

## Future Ideas (Post-MVP)

*   Implement persistence (saving/loading the graph state).
*   Add basic item interaction (get, drop, inventory).
*   Develop more robust methods for extracting structured data from LLM responses.
*   Introduce simple environmental puzzles.
*   Explore different LLM prompting strategies for varied generation and consistent tone.
*   Potentially add simple NPCs or environmental storytelling elements.

---
