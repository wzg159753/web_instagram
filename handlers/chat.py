import uuid
from datetime import datetime
from tornado.escape import json_decode
import tornado.escape
from .main import BaseHandler
from tornado.websocket import WebSocketHandler
from pycket.session import SessionMixin


class RoomHandler(BaseHandler):
    """
    聊天室
    """
    def get(self, *args, **kwargs):
        self.render('room.html', messages=MessageHandler.historys)


class MessageHandler(WebSocketHandler, SessionMixin):
    """
    聊天室后端逻辑
    """
    users = set() # 新建一个用户集合组
    historys = [] # 历史消息
    history_size = 5 # 历史消息大小

    def get_current_user(self):
        """
        重写current_user 获取用户名
        :return:
        """
        return self.session.get('user_id', None)

    def open(self, *args, **kwargs):
        """
        websocket打开连接的方法
        :param args:
        :param kwargs:
        :return:
        """
        # 将每一个连接的用户添加到用户组
        MessageHandler.users.add(self)

    def on_close(self):
        """
        websocket关闭连接方法
        :return:
        """
        MessageHandler.users.remove(self)

    def on_message(self, message):
        """
        向页面发送消息方法
        :param message:
        :return:
        """
        # 解析js中websocket传来的消息  是一个json格式的字典 {‘body’：html}
        parsed = json_decode(message)
        # 构造参数
        chat = {
            'id': uuid.uuid4(),
            'body': parsed['body'],
            'username': self.current_user,
            'create_time': datetime.now(),
        }
        # 生成消息  给每一个用户发送一个html
        msg = {
            # 调用tornado内置方法 将模板转化成模板字符串 将参数穿进去
            'html': tornado.escape.to_basestring(
                self.render_string('message.html', chat = chat)
            )
        }
        MessageHandler.historys.append(msg)
        if len(MessageHandler.historys) > MessageHandler.history_size:
            MessageHandler.historys = MessageHandler.historys[-5:]

        for user in MessageHandler.users:
            user.write_message(msg)

