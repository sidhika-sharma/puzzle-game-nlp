# puzzle-game-nlp
A fun NLP-based puzzle game using Flask
🧩 Puzzle Game – NLP Edition:
A fun and interactive word puzzle game built in Python, enhanced with Natural Language Processing (NLP) techniques to validate and analyze words.
This project uses the NLTK library to ensure correct spelling and meaningful gameplay.

🚀 Features:
✅ Word Validation – Ensures all entered words are valid English words

🧠 NLP Integration – Uses NLTK corpus for word checking

🎮 Interactive Gameplay – User-friendly CLI-based game

🔄 Multiple Rounds – Keeps the fun going with replay options

📊 Score Tracking – Keeps track of the player’s performance

📂 Project Structure:
bash
Copy
Edit
puzzle-game-nlp/
│── game.py               # Main game logic
│── utils.py              # Helper functions
│── README.md             # Project documentation
│── requirements.txt      # Python dependencies
└── __pycache__/          # Python cache files

🛠️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/sidhika-sharma/puzzle-game-nlp.git
cd puzzle-game-nlp
2️⃣ Install Dependencies
Make sure Python is installed (>=3.8).
pip install -r requirements.txt
3️⃣ Run the Game
python game.py

📦 Dependencies
Python 3.8+
NLTK (Natural Language Toolkit)
Random (Python built-in)
Install NLTK if not already installed:
pip install nltk

🧪 How It Works
1.The game presents a scrambled set of letters
2.The player tries to form valid words
3.Words are validated using NLTK's word corpus
4.Points are awarded for correct entries
5.The player can replay or quit anytime
