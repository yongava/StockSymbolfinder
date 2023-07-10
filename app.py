from flask import Flask, render_template, request
from my_search_module import search

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