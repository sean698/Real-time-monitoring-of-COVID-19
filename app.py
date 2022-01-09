from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
import utils

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("main.html")

@app.route('/time')
def get_time():
    return utils.get_time()

@app.route('/c1')
def get_c1_data():
    # The front end only accept string or json(dict)
    # Convert data from tuple to json using jsonify method
    data = utils.get_c1_data()
    return jsonify({
        "confirm": int(data[0]),
        "suspect": int(data[1]),
        "heal": int(data[2]),
        "dead": int(data[3])
    })

@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({'name': tup[0], 'value': int(tup[1])})
    return jsonify({'data': res})

@app.route("/l1")
def get_l1_data():
    data = utils.get_l1_data()
    day,confirm,suspect,heal,dead = [],[],[],[],[]
    for a,b,c,d,e in data[7:]:
        # a is a datetime object
        day.append(a.strftime("%m-%d")) 
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day":day,"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})

@app.route("/l2")
def get_l2_data():
    data = utils.get_l2_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))  
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})

if __name__ == '__main__':
    app.run()