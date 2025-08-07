from flask import Flask, render_template, request, redirect, url_for, flash
from fuzzywuzzy import fuzz
from nltk.corpus import words
from spellchecker import SpellChecker
from textblob import TextBlob
import nltk
try:
    words.words()
except LookupError:
    nltk.download('words')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Sample puzzles for each level
puzzles = {
    'easy': [
        {"question": "I speak without a mouth and hear without ears. What am I?", "answer": "echo", "hint": "It's something sound-related."},
        {"question": "What has keys but can't open locks?", "answer": "piano", "hint": "It's something musical."}
    ],
    'medium': [
        {"question": "What can travel around the world while staying in the corner?", "answer": "stamp", "hint": "It involves sending letters."},
        {"question": "What has a heart that doesn’t beat?", "answer": "artichoke", "hint": "It's a kind of vegetable."}
    ],
    'hard': [
        {"question": "The more you take, the more you leave behind. What am I?", "answer": "footsteps", "hint": "It’s related to walking."},
        {"question": "I have branches, but no fruit, trunk or leaves. What am I?", "answer": "bank", "hint": "Think finance."}
    ]
}

# Setup spellchecker
spell = SpellChecker()
valid_words = set(words.words())

# Helper function to analyze sentiment
def analyze_sentiment(text):
    blob = TextBlob(text)
    sentiment_score = blob.sentiment.polarity
    return sentiment_score

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to start the game at the chosen level
@app.route('/start', methods=['POST'])
def start_game():
    level = request.form['level']
    return redirect(url_for('play', level=level, puzzle_index=0))

# Route to handle playing the game
@app.route('/play', methods=['GET', 'POST'])
def play():
    level = request.args.get('level') or request.form.get('level')
    puzzle_index = int(request.args.get('puzzle_index', 0)) or int(request.form.get('puzzle_index', 0))

    if request.method == 'POST':
        if 'level_change' in request.form:
            new_level = request.form['new_level']
            if new_level:
                if new_level == 'continue':
                    return redirect(url_for('play', level=level, puzzle_index=puzzle_index))
                else:
                    return redirect(url_for('play', level=new_level, puzzle_index=0))
        
        answer = request.form.get('action', "").strip().lower() or ""
        expected_answer = puzzles[level][puzzle_index]['answer']
        hint = puzzles[level][puzzle_index]['hint']

        # Spell check
        misspelled = spell.unknown([answer])
        if misspelled:
            corrected = spell.correction(answer)
            if corrected and corrected != answer:
                answer = corrected
                flash(f"Did you mean: {corrected}?", category='error')

        # Fuzzy matching for close answers
        if fuzz.ratio(answer, expected_answer) > 80 or fuzz.partial_ratio(answer, expected_answer) > 80:
            flash("Correct! Moving to the next puzzle.", category='success')
            if puzzle_index == len(puzzles[level]) - 1:
                return redirect(url_for('congrats', level=level))
            else:
                puzzle_index += 1
                return redirect(url_for('play', level=level, puzzle_index=puzzle_index))

        # Sentiment analysis for frustration
        if analyze_sentiment(answer) < 0:
            return render_template('switch_level.html', current_level=level, puzzle_index=puzzle_index)

        flash("Sorry, your answer is incorrect. Try again.", category='error')
        return render_template('play.html', question=puzzles[level][puzzle_index]['question'],
                               hint=hint, puzzle_index=puzzle_index, level=level)

    # If GET request, show the question
    puzzle = puzzles[level][puzzle_index]
    return render_template('play.html', question=puzzle['question'], hint=puzzle['hint'],
                           puzzle_index=puzzle_index, level=level, show_level_change=False)

# Route for handling level switch
@app.route('/switch_level', methods=['POST'])
def switch_level():
    new_level = request.form['new_level']
    if new_level:
        return redirect(url_for('play', level=new_level, puzzle_index=0))
    return redirect(url_for('play', level=request.form['current_level'], puzzle_index=request.form['puzzle_index']))

# Route for congratulations page
@app.route('/congrats')
def congrats():
    level = request.args.get('level')
    if level == 'easy':
        flash("Congratulations! You've completed the Easy level. Moving on to Medium.", category='success')
        return redirect(url_for('play', level='medium', puzzle_index=0))
    elif level == 'medium':
        flash("Congratulations! You've completed the Medium level. Moving on to Hard.", category='success')
        return redirect(url_for('play', level='hard', puzzle_index=0))
    elif level == 'hard':
        flash("Congratulations! You've completed all levels!", category='success')
        return redirect(url_for('end'))

# Route for the end page
@app.route('/end')
def end():
    return render_template('end.html')

if __name__ == '__main__':
    app.run(debug=True)
