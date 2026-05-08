from mqtt_as import MQTTClient
from mqtt_local import config
import uasyncio as asyncio
import dht
import machine
import ujson
import binascii

from persistencia import cargar_estado, guardar_estado
from medicion import medir, publicar
from control_termostato import control_termostato
from escuchar_mensajes import escuchar_mensajes
from destello import destellar

SERVER = config['server']
ID_DISPOSITIVO = binascii.hexlify(machine.unique_id()).decode()

led = machine.Pin("LED", machine.Pin.OUT)
rele = machine.Pin(16, machine.Pin.OUT, value=1)
sensor = dht.DHT22(machine.Pin(15))


estado = { #parametros no volatiles
    'setpoint': 20,
    'periodo':20, #cada tiempo publica 
    'modo': 'automatico',
    'rele':0, #0 esta off 1 prendido
}

cargar_estado(estado)

async def main(client):
    await client.connect()
    await asyncio.sleep(2)  # Give broker time
    
    await client.subscribe(ID_DISPOSITIVO + "/setpoint", qos=1)
    await client.subscribe(ID_DISPOSITIVO + "/periodo", qos=1)
    await client.subscribe(ID_DISPOSITIVO + "/destello", qos=1)
    await client.subscribe(ID_DISPOSITIVO + "/modo", qos=1)
    await client.subscribe(ID_DISPOSITIVO + "/rele", qos=1)
    
    print("Suscripciones realizadas")

    asyncio.create_task(medir(sensor, estado))
    asyncio.create_task(publicar(client, estado, ID_DISPOSITIVO))
    asyncio.create_task(control_termostato(rele, estado))
    
    asyncio.create_task(
        escuchar_mensajes(
            client,
            estado,
            guardar_estado,
            lambda: destellar(led)
        )
    )

    while True:
        await asyncio.sleep(60)


# Set up client
MQTTClient.DEBUG = True  # Optional
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()
    asyncio.new_event_loop()