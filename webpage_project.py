from flask import Flask
import random
import socket
from flask import render_template
from flask import request, redirect, url_for, jsonify

from services.model_service import ModelService
from services.data_service import DataService

app = Flask(__name__)


@app.route('/')
def home():
    return redirect('main2')


@app.route('/data/data.pdf', methods=['GET'])
def download():
    return url_for('static', filename=r'/data/train.csv')


@app.route('/main', methods=['GET'])
def main_display():
    return render_template('main.html')


# with nlp model
@app.route('/main2')
def data_selection():
    # load the model as global variable
    return render_template('main2.html')


# with nlp model
@app.route('/main2', methods=['POST'])
def model_perform2():
    data_select = request.json["select_data"]
    data_select = data_select.split(";")
    index = int(data_select[0])
    file_name = data_select[1]
    data_service = DataService(file="static/data/" + file_name)
    data_select = data_service.get_item(index)
    problem = data_select["Body"] + data_select["Question"]
    output = model.forward_model(problem)
    return jsonify({"output": output})


@app.route('/getdataset', methods=['POST'])
def data_selection2():
    math_pb = []
    label = []
    if request.json["active_train"]:
        data_service = DataService(file=r"static/data/train.csv")
        ind_train = random.sample([*range(data_service.n)], 10)
        math_pb = math_pb + data_service.math_pb[ind_train].tolist()
        label = label + data_service.label[ind_train].tolist()
    if request.json["active_test"]:
        data_service = DataService(file=r"static/data/dev.csv")
        ind_test = random.sample([*range(data_service.n)], 10)
        math_pb = math_pb + data_service.math_pb[ind_test].tolist()
        label = label + data_service.label[ind_test].tolist()
    return jsonify({"math_pb": math_pb, "label": label})


if __name__ == '__main__':
    print("Loading model...")
    global model
    model = ModelService(r"static/model/output_reasoning_iteration")
    hostname = socket.gethostname()
    # getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)

    # app.run(port=8080, host="10.90.39.19", debug=True)
    app.run(port=8080, host=ip_address, debug=True)
