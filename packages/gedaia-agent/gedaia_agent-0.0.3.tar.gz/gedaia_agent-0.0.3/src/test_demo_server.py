import asyncio

from aig.demo.server.math_server import start_demo_server


if __name__=='__main__': 
    asyncio.run(start_demo_server(port=8005))