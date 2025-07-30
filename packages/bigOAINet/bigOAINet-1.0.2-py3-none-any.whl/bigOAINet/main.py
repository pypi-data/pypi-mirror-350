import asyncio
from mxupy import ApiServer
import bigOAINet as bigo

chatServer = None


async def startup_event():
    global chatServer
    print("HI, I am BigOAI!\nLong time no see.")
    # 必须在unicorn.run之后执行
    chatServer = bigo.ChatServer()
    asyncio.create_task(chatServer.run())


async def shutdown_event():
    print("ApiServer: bye bye!")
    chatServer.stop()


def go():
    ApiServer().run(startup_event, shutdown_event)
