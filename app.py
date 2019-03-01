from flask import Flask, render_template

from lunch import get_kandelabr, get_smrtak, get_arrosto, get_v_case

app = Flask(__name__)


@app.route("/")
def index():
    data = {}
    data["kandelabr"] = get_kandelabr()
    data["smrtak"] = get_smrtak()
    data["arrosto"] = get_arrosto()
    data["v_case"] = get_v_case()

    return render_template("index.html", context=data)


if __name__ == "__main__":
    app.run(debug=False)
