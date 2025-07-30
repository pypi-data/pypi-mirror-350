import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import mxupy as mu

import uvicorn

mu.glb["config"] = {
    "httpServer": "http://0.0.0.0:7862",
    "userDataPath": os.getcwd() + "\\userdata",
    "m3u8FilePath": os.getcwd() + "\\m3u8File",
    "schedule":0,
}

def bigOAIManGo():
    from routers import basics
    from routers import myCatechism
    from routers import myModel
    from routers import myModelAndVideos
    from routers import myProject
    from routers import myScript
    from routers import myVoice
    from routers import myVoiceModel
    from routers import myCatechismAttachment
    from routers import news

    app = FastAPI()

    # 配置 CORS 中间件
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],  # 允许所有域进行跨域请求，生产环境时应更为安全地配置
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(basics.router)
    app.include_router(myCatechism.router)
    app.include_router(myModel.router)
    app.include_router(myModelAndVideos.router)
    app.include_router(myProject.router)
    app.include_router(myScript.router)
    app.include_router(myVoice.router)
    app.include_router(myVoiceModel.router)
    app.include_router(myCatechismAttachment.router)
    app.include_router(news.router)

    @app.on_event("shutdown")
    async def on_shutdown():
        '''
        因uvicorn是一个ASGI服务器，它处理了所有中断，所以，只能重载这个函数来完成类似中断的工作
        '''
        print('httpManager stoped!')

    parts = mu.glb["config"]['httpServer'].split("//")[1]
    host, port = parts.split(":")
    print('httpManager started!')

    uvicorn.run(app, host=host, port=int(port))


def stop():
    # uvicorn 没有 stop 方法，但是会抛出一个异常，导致 uvicorn 退出，这是一种简单的方法
    uvicorn.stop()


if __name__ == "__main__":
    bigOAIManGo()