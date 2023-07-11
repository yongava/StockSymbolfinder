#app,py
from flask import Flask, render_template, request
from my_search_module import search
import openai
import json

api_key = "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"

def search(prompt):
    print(f"prompt {prompt}")

    system_prompt = "You are a helpful API. that get user input to find the most related public company and then answer as a symbol. The answer pattern is like API style by this template {'company_symbol':'AAPL', 'company_name':'Apple, Inc.', 'opinion':'Because ....'} p.s. it's okay that it not directly related but try to answer as template, p.s.1 if you can find answerresponse {'company_symbol':'AAPL', 'company_name':'Apple, Inc.'} else answer {'company_symbol':'None', 'company_name':'None', 'opinion':'I cannot find related symbol'}"
    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_prompt},
        {"role": "user", "content": "What is the company that is the most related to : '" + prompt + "'"}],
        temperature=0,
    )


    print("OpenAI API Result:")
    print(completion.choices[0].message.content)
    
    try:
        # Try to parse the string to JSON
        result = json.loads(completion.choices[0].message.content.replace("'", '"'))
    except json.decoder.JSONDecodeError:
        print("Failed to parse the message content to JSON")
        return None

    logo_url = f"https://logo.clearbit.com/{result['company_symbol']}.com"
    result['logo_url'] = logo_url.replace(" ", "")


    return result
    
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def search_query():
    search_result = []
    if request.method == 'POST':
        text = request.form.get('text')
        search_result = search(text)  # Using the function you created
    return render_template("search.html", search_result=search_result)
  
if __name__ == '__main__':
    app.run(debug=True)