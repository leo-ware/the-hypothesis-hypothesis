from flask import Flask, render_template, request, redirect
import requests
import atoma

app = Flask(__name__)


def search_arxiv(query):
    payload = requests.get(f"http://export.arxiv.org/api/query?search_query=all:{query}&max_results=5")
    feed = atoma.parse_atom_bytes(payload.content)
    return feed.entries


@app.route('/')
def index():
    try:
        q = request.args['query']
        responses = search_arxiv(q) if q else ""
        links = [(item.id_.replace('abs', 'pdf') + ".pdf") for item in responses]
        results = zip(links, responses)
        print(links)
    except KeyError:
        q = ""
        results = []
    return render_template("index.html", query=q, results=results)


@app.route('/entry')
def entry():
    try:
        link = request.args['pdf']
    except KeyError:
        redirect('/')
    "https://arxiv.org/pdf/2101.10285.pdf"
    return render_template("entry.html", link=link)


if __name__ == '__main__':
    app.run()
