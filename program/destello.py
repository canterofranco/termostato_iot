import uasyncio as asyncio

async def destellar(led):
    for _ in range(10):
        led.toggle()
        await asyncio.sleep_ms(500)
    led.off()