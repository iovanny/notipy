import os
import datetime
import psutil
import time
import requests
#REPRODUCE UN SONIDO
os.system("ffplay -nodisp -t 1 -autoexit /home/iovanny/evilmorty.mp3")
#f = os.popen('date')
#now = f.read()
#print "Today is ", now
os.system("notify-send 'Iniciando Script' --icon=battery-caution")
url = 'http://xxx.i8o9a0.com/c.php'
now = datetime.datetime.now()
print (now.strftime("%H:%M:%S"))
# CHECA LA HORA DeL DIA
if now.strftime("%H") > 14:
	print ("Son mas de las 14 horas")
else:
	print ("NO")
#CHECA LA BATERIA
i = 0
#j = 0
while i == 0:
	time.sleep(30)
	battery = psutil.sensors_battery()
	plugged = battery.power_plugged
	percent = str(battery.percent)
	if plugged==False: plugged="Not Plugged In"
	else: plugged="Plugged In"
	print(percent+'% | '+plugged)
	if ((float(percent) > 90) and (plugged is "Plugged In")):
		print ("Bateria cargada, desconecta el cargador")
		os.system("ffplay -nodisp -t 5 -autoexit /home/iovanny/fatality.m4a")
		x = requests.post(url, json = { "chat_id" : "-470845708",  "mensaje" : "La bateria esta cargada"})
		#j += 1
		#if j == 20:
			#os.system("shutdown /s /t 1");
  	if ((float(percent) < 9) and (plugged is "Not Plugged In")):
		print ("Bateria Baja, Conecta el cargador")
		os.system("ffplay -nodisp -t 25 -autoexit /home/iovanny/evilmorty.mp3")
		os.system("notify-send 'Menos de .09 de bateria' --icon=battery-caution")		
		x = requests.post(url, json = { "chat_id" : "-470845708",  "mensaje" : "La bateria se esta agotando"})




#print the response text (the content of the requested file):


