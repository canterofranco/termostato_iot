# termostato_iot
Termostato con Rasp Pi Pico W/2W, sensor DHT22 y relé que puede funcionar de modo manual o automático
Crear un termostato con un Raspberry Pi Pico W/2W, sensor DHT22 y relé que puede funcionar de modo manual o automático
- Programado en micropython utilizando asyncio (mqtt_as).
- Utiliza la alternativa basada en eventos.
- Se comunica mediante mqtts.
Publica periódicamente en el tópico "ID_DEL_DISPOSITIVO" los siguientes parámetros:
      - temperatura
      - humedad
      - setpoint
      - periodo
      - modo
Se envían todos las mediciones en una sola publicación en un JSON.
Se suscribe a:
      + "ID_DEL_DISPOSITIVO"/setpoint
      + "ID_DEL_DISPOSITIVO"/periodo
      + "ID_DEL_DISPOSITIVO"/destello
      + "ID_DEL_DISPOSITIVO"/modo
      + "ID_DEL_DISPOSITIVO"/relé
Almacenará de manera no volátil los parámetros de setpoint, periodo, modo y relé (ver btree).
Destellará por unos segundos cuando reciba la orden "destello" por mqtt.
Cuando recibe un mensaje con nuevos parámetros no volátiles, deberá actualizar los almacenados y actuar si es necesario.
En modo automático: El relé se accionará cuando se supere la temperatura de setpoint.
En modo manual: El relé se activará según la orden "relé" enviada por mqtt.
