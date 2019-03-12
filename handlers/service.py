from .main import BaseHandler
import requests
import tornado.gen
import tornado.httpclient
from utils.picture import UploadImage
from utils.verify import add_post_for
import tornado.web

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
        self.redirect('/post/{}'.format(post.id))