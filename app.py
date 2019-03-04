from flask import Flask, render_template

from lunch import get_kandelabr, get_smrtak, get_arrosto, get_v_case
from datetime import datetime

from Lunch.lunch import get_menus

app = Flask(__name__)


@app.route("/")
def index():
    menus = get_menus()
    data = {}
    data["kandelabr"] = get_kandelabr(menus)
    data["smrtak"] = get_smrtak(menus)
    data["arrosto"] = get_arrosto(menus)
    data["v_case"] = get_v_case()
    data["date"] = datetime.now().strftime("%d.%m. %Y")

    return render_template("index.html", context=data)


if __name__ == "__main__":
    app.run(debug=False)
