from flask import Flask
import random
import socket
import argparse
from flask import render_template
from flask import request, redirect, url_for, jsonify

from services.model_service import ModelService
from services.data_service import DataService, oracle_hint

parser = argparse.ArgumentParser(description='disruption prediction JET')
# data specific
parser.add_argument('--random-data', default=False, type=bool,
                    help='true is data selection random')


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
    global data_select
    data_select = request.json["select_data"]
    data_select = data_select.split(";")
    file_name = data_select[1]
    data_service = DataService(file="static/data/" + file_name)
    data_select = data_service.get_item(index)
    problem = data_select["Body"] + data_select["Question"]
    first_turn_answer = model.forward_actor_model(input_str=problem, turn=1)
    first_turn_answer = first_turn_answer.split("|")[:-1] # split and remove the last EOS
    return jsonify({"output": first_turn_answer})


@app.route('/getdataset', methods=['POST'])
def data_selection2():
    math_pb = []
    label = []
    if request.json["active_train"]:
        data_service = DataService(file=r"static/data/train.csv")
        if args.random_data:
            ind_train = random.sample([*range(data_service.n)], 10)
        else:
            ind_train = [0, 202, 563, 695, 1033, 1275, 1399, 2555, 2800, 3122]
        math_pb = math_pb + data_service.math_pb[ind_train].tolist()
        label = label + data_service.label[ind_train].tolist()
    if request.json["active_test"]:
        data_service = DataService(file=r"static/data/dev.csv")
        if args.random_data:
            ind_test = random.sample([*range(data_service.n)], 10)
        else:
            ind_test = [0, 20, 50, 66, 105, 233, 349, 555, 684, 865]
        if args.random_data:
            ind_test = random.sample([*range(data_service.n)], 10)
        math_pb = math_pb + data_service.math_pb[ind_test].tolist()
        label = label + data_service.label[ind_test].tolist()
    return jsonify({"math_pb": math_pb, "label": label})


@app.route('/callcritic', methods=['POST'])
def callcritic():
    critic_mode = request.json["critic_mode"]
    if critic_mode == "automatic":
        hint = model.forward_critic_model()
    if critic_mode == "oracle":
        generate_linear_formula = model.history[-1][1][:-6]
        true_linear_formula = data_select["linear_equation"]
        hint = oracle_hint(generate_linear_formula, true_linear_formula)
    return jsonify({"output": hint})


@app.route('/performcritic', methods=['POST'])
def performcritic():
    critic_mode = request.json["critic_mode"]
    if critic_mode == "manual":
        hint = request.json["hint_input"]
    else:
        hint = model.history[-1][2]
    second_turn_answer = model.forward_actor_model(input_str=hint, turn=2)
    second_turn_answer = second_turn_answer.split("|")[:-1] # split and remove the last EOS
    return jsonify({"output": second_turn_answer})


@app.route('/display_data', methods=['POST'])
def display_data():
    data_select = request.json["display_data"]
    data_select = data_select.split(";")
    index = int(data_select[0])
    file_name = data_select[1]
    data_service = DataService(file=r"static/data/" + file_name)
    data_select = data_service.get_math_pb(index)
    return jsonify({"label": data_select})


if __name__ == '__main__':
    args = parser.parse_args()
    print("Loading actor and critic model...")
    model = ModelService(r"static/model/output_reasoning_iteration", r"static/model/critic")
    print("Model load well")
    hostname = socket.gethostname()
    # getting the IP address using socket.gethostbyname() method
    ip_address = socket.gethostbyname(hostname)

    app.run(port=8080, host="10.90.39.19", debug=True)
    # app.run(port=8080, host=ip_address, debug=True)
