import json
import asyncio
import traceback
import websockets
import bigOAINet as bigo
from http import HTTPStatus

from mxupy import read_config, array_contains


class ChatServer:

    def __init__(self):
        """初始化"""
        # 聊天室列表
        self.rooms = []
        # 读取配置信息
        chat_server = read_config().get("chat_server", {})
        # 域名、端口
        self.host = chat_server.get("host", "0.0.0.0")
        self.port = int(chat_server.get("port", "8086"))

        # 用sessionId作为key，因为智能体调用需要会话id
        self.agentCallers = {}

        # 创建 stop Future 对象
        self.stop_future = asyncio.get_running_loop().create_future()

    def get_room(self, roomId):
        """获取聊天室"""
        return next((room for room in self.rooms if room.roomId == roomId), None)

    def get_user(self, room, userId):
        """获取用户"""
        return next((user for user in room.roomUsers if user.userId == userId), None)

    async def fill_room_and_user(self, roomId, userId, websocket):
        """填充房间信息和用户持有websocket，如果房间不存在则从服务器获取"""
        room = self.get_room(roomId)
        if room is None:
            im = bigo.RoomControl.inst().get_one_by_id(roomId, recurse=True)
            if im.success:
                room = im.data
                self.rooms.append(room)
            else:
                raise ValueError(f"Room with ID {roomId} not found")

        user = self.get_user(room, userId)
        if user is not None:
            user.ws = websocket

        return room, user

    async def handle_client(self, websocket):
        try:

            while True:
                msg = await websocket.recv()
                data = json.loads(msg)

                # 获取各个字段的信息
                room_id = data.get("roomId")
                session_id = data.get("sessionId")
                # conversation_id = data.get("conversationId")
                agent_id = data.get("agentId")
                user_id = data.get("userId")
                # inputs = data.get('inputs')
                # prompt = data.get('prompt')
                # files = data.get('files')

                # 填充房间信息
                room, user = await self.fill_room_and_user(room_id, user_id, websocket)

                # 消息中包含了房间Id、会话Id、智能体Id、用户Id、inputs、prompt、files
                if not array_contains(self.agentCallers, 'sessionId', session_id):
                    self.agentCallers[str(session_id)] = bigo.AgentCaller(agent_id, user_id, session_id)

                response = self.agentCallers[str(session_id)].call(data)
                for chunk in response.iter_lines():
                    # 群发
                    if self.agentCallers[str(session_id)].agent.canGroup:
                        for user1 in room.roomUsers:
                            await user.ws.send(json.dumps(chunk.decode("utf-8")))
                    # 私发
                    else:
                        await websocket.send(json.dumps(chunk.decode("utf-8")))

        except websockets.exceptions.ConnectionClosedError as e:
            print("客户端断开：", e)
            traceback.print_exc()
        except Exception as e:
            print("websockets异常：", e)
            traceback.print_exc()

    async def run(self):
        """运行"""
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"ChatServer started on ws://{self.host}:{self.port}")
            await self.stop_future

    def stop(self):
        print("ChatServer: bye bye!")
        self.stop_future.set_result(None)
