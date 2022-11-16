from flask import Flask
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


@app.route('/main2')
def data_selection():
    return render_template('main2.html')


@app.route('/main2', methods=['POST'])
def model_perform2():
    data_select = request.json["select_data"]
    data_select = data_select.split(";")
    index = int(data_select[0])
    file_name = data_select[1]
    data_service = DataService(file=r"static/data/" + file_name)
    data_select = data_service.get_item(index)
    return jsonify({"output": data_select["Answer"]})


@app.route('/getdataset', methods=['POST'])
def data_selection2():
    math_pb = []
    label = []
    if request.json["active_train"]:
        data_service = DataService(file=r"static/data/train.csv")
        math_pb = math_pb + data_service.math_pb.tolist()[0:10]
        label = label + data_service.data["label"].values.tolist()[0:10]
    if request.json["active_test"]:
        data_service = DataService(file=r"static/data/dev.csv")
        math_pb = math_pb + data_service.math_pb.tolist()[0:10]
        label = label + data_service.data["label"].values.tolist()[0:10]
    return jsonify({"math_pb": math_pb, "label": label})


if __name__ == '__main__':
    hostname = socket.gethostname()
    # getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)

    # app.run(port=8080, host="10.90.39.19", debug=True)
    app.run(port=8080, host=ip_address, debug=True)
