from textblob import TextBlob
import language_tool_python
from flask import Flask, request, render_template

class SpellCheckerModule:
    def __init__(self):
        self.spell_check = TextBlob("")
        self.tool = language_tool_python.LanguageTool('en-US')

    def correct_spell(self, text):
        words = text.split()
        corrected_words = []
        for word in words:
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        return " ".join(corrected_words)

    def correct_grammar(self, text):
        matches = self.tool.check(text)
        corrections = []
        for match in matches:
            corrections.append({
                'incorrect': match.context,
                'suggestions': match.replacements
            })
        return corrections, len(matches)

# Flask App
app = Flask(__name__)
spell_checker_module = SpellCheckerModule()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spell', methods=['POST', 'GET'])
def spell():
    if request.method == 'POST':
        text = request.form['text']
        corrected_text = spell_checker_module.correct_spell(text)
        grammar_corrections, grammar_mistakes = spell_checker_module.correct_grammar(text)
        return render_template('index.html', corrected_text=corrected_text, corrected_grammar=(grammar_corrections, grammar_mistakes))

@app.route('/grammar', methods=['POST', 'GET'])
def grammar():
    if request.method == 'POST':
        file = request.files['file']
        readable_file = file.read().decode('utf-8', errors='ignore')
        corrected_file_text = spell_checker_module.correct_spell(readable_file)
        corrected_file_grammar, grammar_mistakes = spell_checker_module.correct_grammar(readable_file)
        return render_template('index.html', corrected_file_text=corrected_file_text, corrected_file_grammar=(corrected_file_grammar, grammar_mistakes))

if __name__ == "__main__":
    app.run(debug=True)
