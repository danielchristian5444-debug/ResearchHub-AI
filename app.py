from flask import Flask, render_template, request, jsonify
import wikipedia

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    query = data.get('question', '').strip()

    if not query:
        return jsonify({'answer': 'Please ask me something!'})

    # Handle basic greetings without hitting Wikipedia
    greetings = {
        'hello': 'Hi there! Ask me anything and I\'ll look it up on Wikipedia! 😊',
        'hi': 'Hey! What would you like to know about?',
        'help': 'Just type any topic — like "Albert Einstein" or "Python programming" — and I\'ll fetch info from Wikipedia!',
        'joke': 'Why did the chatbot go to school? To improve its learning algorithms! 😄',
        'bye': 'Goodbye! Come back anytime! 👋',
        'goodbye': 'See you later! 👋',
    }

    for key, response in greetings.items():
        if key in query.lower():
            return jsonify({'answer': response})

    # Fetch from Wikipedia
    answer = get_wikipedia_summary(query)
    return jsonify({'answer': answer})

def get_wikipedia_summary(query):
    try:
        page = wikipedia.page(query)
        summary = page.content[:3000]
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:5])
        return f"Your query is ambiguous. Did you mean: {options}?"
    except wikipedia.exceptions.PageError:
        # Try searching if exact page not found
        results = wikipedia.search(query)
        if results:
            page = wikipedia.page(results[0])
            return page.content[:3000]
        return "Sorry, I couldn't find any information on that topic. Try rephrasing!"
    except Exception as e:
        return f"Something went wrong: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)