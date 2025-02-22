from flask import Flask, render_template
from scraper1 import scrape_website as scrape1
from scraper2 import scrape_website as scrape2
from scraper3 import scrape_website as scrape3
from scraper4 import scrape_website as scrape4

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/page1")
def page1():
    content = scrape1()
    return render_template("page1.html", content=content)

@app.route("/page2")
def page2():
    content = scrape2()
    return render_template("page2.html", content=content)

@app.route("/page3")
def page3():
    content = scrape3()
    return render_template("page3.html", content=content)

@app.route("/page4")
def page4():
    content = scrape4()
    return render_template("page4.html", content=content)

if __name__ == "__main__":
    app.run(debug=True)
