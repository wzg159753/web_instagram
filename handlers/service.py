from .main import BaseHandler
import requests
import tornado.escape
import tornado.gen
import tornado.httpclient
from utils.picture import UploadImage
from utils.verify import add_post_for
import tornado.web
from handlers.chat import MessageHandler

class syncHandler(BaseHandler):
    """
    同步api
    """
    def get(self, *args, **kwargs):
        # 获取地址url
        name = self.get_argument('name', None)
        # 请求url
        resp = requests.get(name)
        # 保存二进制图片
        with open('a.jpg', 'wb') as f:
            f.write(resp.content)


class AsyncHandler(tornado.web.RequestHandler):
    """
    异步请求图片api
    """
    # 使用异步装饰器
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        # 获取图片地址
        name = self.get_argument('name', None)
        # 获取用户名
        username = self.get_argument('username', None)
        # 获取上一次路由
        from_path = self.get_argument('from', '') == 'ws'
        if from_path:
            # 开启异步客户端
            client = tornado.httpclient.AsyncHTTPClient()
            # 用yield 发送请求  请求图片
            resp = yield client.fetch(name)
            im = UploadImage('x.jpg', self.settings.get('static_path'))
            # 将图片二进制保存
            im.save_upload(resp.body)
            im.save_thumb()
            # 返回post实例
            post = add_post_for(im.upload_path, im.thumb_path, username)
            # 构造消息
            url = 'http://192.168.35.128:8080/post/{}'.format(post.id)
            # 构造参数
            chat = MessageHandler.make_chat(url, username, img_url=im.thumb_path)
            msg = {
                # 调用tornado内置方法 将模板转化成模板字符串 将参数穿进去
                'html': tornado.escape.to_basestring(
                    self.render_string('message.html', chat=chat)
                )
            }
            MessageHandler.up_history(msg)
            MessageHandler.send_message(msg)
        else:
            self.write({'msg': 'admin is not you'})


'''另一种方法是不用ioloop协程  直接用两个异步客户端调用'''
"""
class AsyncHandler(BaseHandler):
    def get(self, *args, **kwargs):
        name = self.get_argument('name', None)
        username = self.get_argument('username', '')
        form_path = self.get_arguemt('from', '') == 'ws'
        if form_path:
            client = AsyncHttpClient()
            resp = client.fetch(name)
            im = UploadImage('x.jpg', self.settings['static_path'])
            im.save_upload(resp.body)
            im.save_thumb()
            post = add_post_for(im.upload_path, im.thumb_path, username)
            self.write(str(post.id))

"""


"""
def on_message(message):
    parse = json_decode(message)
    body = parse['body']
    url = re.search(r'(http|https)://.+?(\\.jpg|\\.png)', body)
    if url:
        http = 'http://192.168.35.128:8080/async?name={}&username={}&from=ws'.format(url.group().replace(' ', ''), self.current_user)
        client = AsyncHttpClient()
        resp = client.fetch(http)
        for i in MessageHandler.users:
            i.write_message(resp.body.decode('utf8'))

"""