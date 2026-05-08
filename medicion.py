import uasyncio as asyncio
import ujson

async def medir(sensor, estado):
    while True:
        try:
            sensor.measure()
            estado["temp_actual"] = sensor.temperature()
            estado["hum_actual"] = sensor.humidity()
        except OSError:
            print("Error al leer el sensor")

        await asyncio.sleep(1)


async def publicar(client, estado, id_disp):
    while True:
        payload = {
            "temperatura": estado.get("temp_actual"),
            "humedad": estado.get("hum_actual"),
            "setpoint": estado["setpoint"],
            "periodo": estado["periodo"],
            "modo": estado["modo"]
        }

        print("Publicando:", payload)
        await client.publish(id_disp, ujson.dumps(payload), qos=1)

        await asyncio.sleep(estado["periodo"])