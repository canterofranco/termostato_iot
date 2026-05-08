import ujson

def guardar_estado(estado):
    try:
        with open("estado.json", "w") as f:
            ujson.dump(estado, f)
    except Exception as e:
        print("Error FATAL guardando estado:", e)

def cargar_estado(estado):
    try:
        with open("estado.json", "r") as f:
            estado_guardado = ujson.load(f)
            estado.update(estado_guardado)
        print("Estado cargado:", estado)
    except OSError:
        print("Creando archivo...")
        guardar_estado(estado)


#importante q si se apaga y se vuelve a prender, el estado se haya guardado.