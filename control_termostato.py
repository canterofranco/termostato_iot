import uasyncio as asyncio

async def control_termostato(rele, estado):
    while True:
        if estado['modo'] == 'automatico':
            if estado['temperatura'] > estado['setpoint']:
                rele.value(0)
            else:
                rele.value(1)

        elif estado['modo'] == 'manual':
            rele.value(0 if estado['rele'] == 1 else 1)

        await asyncio.sleep(5)