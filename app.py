from flask import Flask, render_template, jsonify
import json
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
    scrape1()  # Scrape and update JSON files

    with open("scrape1_left.json", "r") as file:
        sidebar_content = json.load(file)

    with open("scrape1_text.json", "r") as file:
        main_content = json.load(file)

    return render_template("page1.html", sidebar=sidebar_content, main_content=main_content)

@app.route("/page2")
def page2():
    scrape2()  # Scrape and update JSON files

    with open("scrape2_left.json", "r") as file:
        sidebar_content = json.load(file)

    with open("scrape2_text.json", "r") as file:
        main_content = json.load(file)

    return render_template("page2.html", sidebar=sidebar_content, main_content=main_content)

@app.route("/page3")
def page3():
    scrape3()  # Scrape and update JSON files

    with open("scrape3_left.json", "r") as file:
        sidebar_content = json.load(file)

    with open("scrape3_text.json", "r") as file:
        main_content = json.load(file)

    return render_template("page3.html", sidebar=sidebar_content, main_content=main_content)

@app.route("/page4")
def page4():
    scrape4()  # Scrape and update JSON files

    with open("scrape4_left.json", "r") as file:
        sidebar_content = json.load(file)

    with open("scrape4_text.json", "r") as file:
        main_content = json.load(file)

    return render_template("page4.html", sidebar=sidebar_content, main_content=main_content)

if __name__ == "__main__":
    app.run(debug=True)
