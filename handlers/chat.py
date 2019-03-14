import uuid
import re
import tornado.ioloop
import tornado.httpclient
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
        body = parsed['body']
        url = re.search('(http|https)://.+?(\\.jpg|\\.png)', body)

        if url:
            client = tornado.httpclient.AsyncHTTPClient()
            http = 'http://192.168.35.128:8080/async?name={}&username={}&from=ws'.format(url.group().replace(' ', ''), self.current_user)
            # ioloop的回调方法  将请求放到后台运行 后台要是一个异步api接口
            tornado.ioloop.IOLoop.current().spawn_callback(client.fetch, http)
            chat = MessageHandler.make_chat('图片正在处理...')
            msg = {
                # 调用tornado内置方法 将模板转化成模板字符串 将参数穿进去
                'html': tornado.escape.to_basestring(
                    self.render_string('message.html', chat=chat)
                )
            }
            # 只对自己发送消息
            self.write_message(msg)
        else:
        # 生成消息  给每一个用户发送一个html
            chat = MessageHandler.make_chat(body, self.current_user)
            msg = {
                # 调用tornado内置方法 将模板转化成模板字符串 将参数穿进去
                'html': tornado.escape.to_basestring(
                    self.render_string('message.html', chat = chat)
                )
            }
            # 添加历史和发送消息
            MessageHandler.up_history(msg)
            MessageHandler.send_message(msg)




    @classmethod
    def make_chat(cls, body, username='System', img_url=None):
        """
        构造参数方法
        :param body:
        :param username:
        :param img_url:
        :return:
        """
        return {
            'id': uuid.uuid4(),
            'body': body,
            'username': username,
            'img_url': img_url,
            'create_time': datetime.now(),
        }

    @classmethod
    def up_history(cls, msg):
        """
        添加历史方法
        :param msg:
        :return:
        """
        MessageHandler.historys.append(msg)
        if len(MessageHandler.historys) > MessageHandler.history_size:
            MessageHandler.historys = MessageHandler.historys[-5:]

    @classmethod
    def send_message(cls, msg):
        """
        群发消息方法
        :param msg:
        :return:
        """
        for user in MessageHandler.users:
            user.write_message(msg)





















class UploadMessageHandler(WebSocketHandler, SessionMixin):
    """
    聊天室后端逻辑
    """

    def get_current_user(self):
        """
        重写current_user 获取用户名
        :return:
        """
        return self.session.get('user_id', None)

    # def open(self, *args, **kwargs):
    #     """
    #     websocket打开连接的方法
    #     :param args:
    #     :param kwargs:
    #     :return:
    #     """
    #     # 将每一个连接的用户添加到用户组
    #
    #
    # def on_close(self):
    #     """
    #     websocket关闭连接方法
    #     :return:
    #     """


    def on_message(self, message):
        """
        向页面发送消息方法
        :param message:
        :return:
        """
        self.write_message({'msg': 'ok'})
