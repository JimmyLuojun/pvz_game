#src/pvz_game/main.py
import os
from dotenv import load_dotenv
from pvz_game.engine import GameEngine

# Load environment variables from .env file
load_dotenv()

def main():
    game = GameEngine()
    game.run()

if __name__ == "__main__":
    main()
