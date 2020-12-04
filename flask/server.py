#!venv/bin/python3
from api import esmart
from flask import render_template, Flask, request, jsonify
import logging

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
	return render_template('index.html')

@app.route("/ChgSts", methods=['GET', 'POST'])
def chgSts():
	if request.method == 'GET':
		ChgSts=esmart()
		return jsonify(ChgSts.ctlEsmart(ChgSts.config.getChgSts))

@app.route("/BatParam", methods=['GET', 'POST'])
def batParam():
	if request.method == 'GET':
		BatParam=esmart()
		return jsonify(BatParam.ctlEsmart(BatParam.config.getBatParam))

@app.route("/Log", methods=['GET', 'POST'])
def Log():
	if request.method == 'GET':
		Log=esmart()
		return jsonify(Log.ctlEsmart(Log.config.getLog))


@app.route("/Parameters", methods=['GET', 'POST'])
def Parameters():
	if request.method == 'GET':
		Parameters=esmart()
		return jsonify(Parameters.ctlEsmart(Parameters.config.getParameters))


@app.route("/LoadParam", methods=['GET', 'POST'])
def LoadParam():
	if request.method == 'GET':
		LoadParam=esmart()
		return jsonify(LoadParam.ctlEsmart(LoadParam.config.getLoadParam))

@app.route("/ChgDebug", methods=['GET', 'POST'])
def ChgDebug():
	if request.method == 'GET':
		ChgDebug=esmart()
		return jsonify(ChgDebug.ctlEsmart(ChgDebug.config.getChgDebug))

@app.route("/RemoteControl", methods=['GET', 'POST'])
def RemoteControl():
	if request.method == 'GET':
		RemoteControl=esmart()
		return jsonify(RemoteControl.ctlEsmart(RemoteControl.config.getRemoteControl))

@app.route("/ProParam", methods=['GET', 'POST'])
def ProParam():
	if request.method == 'GET':
		ProParam=esmart()
		return jsonify(ProParam.ctlEsmart(ProParam.config.getProParam))

@app.route("/Information", methods=['GET', 'POST'])
def Information():
	if request.method == 'GET':
		Information=esmart()
		return jsonify(Information.ctlEsmart(Information.config.getInformation))

@app.route("/TempParam", methods=['GET', 'POST'])
def TempParam():
	if request.method == 'GET':
		TempParam=esmart()
		return jsonify(TempParam.ctlEsmart(TempParam.config.getTempParam))

@app.route("/EngSave", methods=['GET', 'POST'])
def EngSave():
	if request.method == 'GET':
		EngSave=esmart()
		return jsonify(EngSave.ctlEsmart(EngSave.config.getEngSave))


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug=True)
