e##############################################################
Como ejecutar:

1.
docker build -t ranniex/flask .

2.
docker run --rm -it --privileged=true -p 5000:5000 \
  -v /dev/vboxdrv:/dev/vboxdrv \
  -v /etc/init.d/vboxdrv:/etc/init.d/vboxdrv \
  -v $(pwd):/myhome \
  ranniex/flask /bin/bash
3.
\myhome# python3 funciones.py
#############################################################

 Desde otra terminal

#############################################################
Comandos para el taller

4. Listar las Maquinas Virtuales
curl -i http://localhost:5000/listvms

5. Crear Maquinas Virtuales
curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Maquina1", "ostype":"fedora"}' http://localhost:5000/crearvm
curl -i -H "Content-Type: application/json" -X POST -d '{"name": "Maquina2", "ostype":"fedora"}' http://localhost:5000/crearvm

6. Listar maquinas en ejecucion
curl -i http://localhost:5000/listrunning

7. Ejecutar una maquina
curl -i http://localhost:5000/runvm/Maquina1
7.1 Apagar una maquina
curl -i http://localhost:5000/stopvm/Maquina1

8. Mostrar informacion de una maquina
curl -i http://localhost:5000/infovm/Maquina1

9. Modificar RAM
curl -i -H "Content-Type: application/json" -X POST -d '{"nameid": "Maquina1", "cantRam":"2048"}' http://localhost:5000/modifyram


10. Mofificar numero de cpus
curl -i -H "Content-Type: application/json" -X POST -d '{"nameid": "Maquina1", "numCpus":"1"}' http://localhost:5000/modifynumcpus
11. Mofificar cantidad de cpus
curl -i -H "Content-Type: application/json" -X POST -d '{"nameid": "Maquina1", "cantCpus":"56"}' http://localhost:5000/modifycantcpus