#!/usr/bin/python
from flask import Flask, jsonify, abort, make_response, request
from subprocess import Popen, PIPE

app = Flask(__name__)

def text(tex):
	salida = []
	text = ""
	for a in tex:
		if a == "\n":
			salida.append(text)
			text = ""
		else:
			text += a
	return salida
	
def filtrar(vector):
	salida = []
	for a in vector:
		if a.find("Memory size") > -1:
			salida.append(a)
		if a.find("Number of CPUs") > -1:
			salida.append(a)
		if a.find("NIC") > -1 and a.find("disabled") == -1:
			salida.append(a)
	return salida

@app.route('/crearvm',methods = ['POST'])
def crearvm():
	if not request.json or not 'name' in request.json or not 'ostype' in request.json:
            abort(400)
	name = request.json['name']
	ostype = request.json['ostype']
	comand = "vboxmanage createvm --name " + name + " --register --ostype " + ostype
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	out = text(stdout.decode())
	return jsonify({'vms': out})
	
	
@app.route('/listvms', methods=['GET'])
def listvm():
	comand = "vboxmanage list vms"
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	if len(stdout) == 0:
		out = "No hay maquinas virtuales"
	else:
		out = text(stdout.decode())
	return jsonify({'vms': out})
	
	
@app.route('/runvm/<string:nameid>', methods=['GET'])
def runvm(nameid):
	comand = "vboxmanage startvm "+nameid+" --type headless"
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	if len(stdout) == 0:
		out = text(stderr.decode())
	else:
		out = text(stdout.decode())
	return jsonify({'vms': out})

@app.route('/stopvm/<string:nameid>', methods=['GET'])
def stopvm(nameid):
	comand = "vboxmanage controlvm "+nameid+" poweroff"
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	if len(stdout) == 0:
		out = text(stderr.decode())
	else:
		out = text(stdout.decode())
	return jsonify({'vms': out})

@app.route('/listrunning', methods=['GET'])
def listrunning():
	comand = "vboxmanage list runningvms"
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	if len(stdout) == 0:
		out = "No hay maquinas virtuales ejecutandose"
	else:
		out = text(stdout.decode())
	return jsonify({'vms': out})
	
	
@app.route('/infovm/<string:nameid>', methods=['GET'])
def infovm(nameid):
	comand = "vboxmanage showvminfo "+nameid
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	if len(stdout) == 0:
		out = text(stderr.decode())
	else:
		out = text(stdout.decode())
	return jsonify({'vms': out})
	

@app.route('/infovmdetalles/<string:nameid>', methods=['GET'])
def infovmdetalles(nameid):
	comand = "vboxmanage showvminfo "+nameid
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	if len(stdout) == 0:
		out = text(stderr.decode())
		return jsonify({'vms': out})
	else:
		out = filtrar(text(stdout.decode()))
	return jsonify({'vms': out})
	
	
################################### Modificaciones ###################################
#Modificar ram
@app.route('/modifyram', methods=['POST'])
def modifyvmram():
	if not request.json or not 'nameid' in request.json or not 'cantRam' in request.json:
            abort(400)
	nameid = request.json['nameid']
	cantRam = request.json['cantRam']
	comand = "vboxmanage modifyvm " + nameid +" --memory "+ cantRam
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	out = text(stdout.decode())
	return jsonify({'vms': out})





#Modificar cpus
@app.route('/modifynumcpus', methods=['POST'])
def modifyvmnumcpus():
	if not request.json or not 'nameid' in request.json or not 'numCpus' in request.json:
            abort(400)
	nameid = request.json['nameid']
	numCpus = request.json['numCpus']
	comand = "vboxmanage modifyvm " + nameid +" --cpus "+numCpus 
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	out = text(stdout.decode())
	return jsonify({'vms': out})


#Modificar porcentaje de cpus
@app.route('/modifycantcpus', methods=['POST'])
def modifyvmcantcpus():
	if not request.json or not 'nameid' in request.json or not 'cantCpus' in request.json:
            abort(400)
	nameid = request.json['nameid']
	cantCpus = request.json['cantCpus']
	comand = "vboxmanage modifyvm " + nameid +" --cpuexecutioncap "+cantCpus 
	salida = Popen(comand, stdout=PIPE, stderr=PIPE, shell=True)
	stdout, stderr = salida.communicate()
	print("Consola: ",len(stdout), " | ", len(stderr))
	out = text(stdout.decode())
	return jsonify({'vms': out})


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
