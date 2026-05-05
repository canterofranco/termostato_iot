import uasyncio as asyncio

async def escuchar_mensajes(client, estado, guardar_estado, destellar):
    print("Iniciando tarea de escucha de mensajes ...")
    
    async for topic, msg, retained in client.queue:
        try:
            t = topic.decode()
            m = msg.decode()
            print(f"Mensaje recibido en {t}: {m}")
            
            if t.endswith("/setpoint"):
                estado["setpoint"] = float(m)
                guardar_estado()

            elif t.endswith("/periodo"):
                estado["periodo"] = int(m)
                guardar_estado()

            elif t.endswith("/modo"):
                estado["modo"] = m
                guardar_estado()

            elif t.endswith("/destello"):
                asyncio.create_task(destellar())

            elif t.endswith("/rele") and estado["modo"] == "manual":
                estado["rele"] = int(m)
                guardar_estado()

        except Exception as e:
            print(f"Error procesando el mensaje: {e}")