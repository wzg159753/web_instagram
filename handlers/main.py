import tornado.web
from tornado.web import RequestHandler
from pycket.session import SessionMixin
from utils.picture import UploadImage
from utils.verify import add_post_for, get_post_all, get_upload_post, get_post_id, paginations


class BaseHandler(RequestHandler, SessionMixin):
    """
    session登录验证基类
    """
    def get_current_user(self):
        """
        重写current_user  返回用户名  供其他路由调用
        :return:
        """
        return self.session.get('user_id', None)


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """获取图片路径列表"""
        path_list = get_upload_post(self.current_user)
        self.render('index_page.html', path_list=path_list)


class ExploreHandler(BaseHandler):
    def get(self, *args, **kwargs):
        number = self.get_argument('page', '1')
        page = paginations(number)
        self.render('explore_page.html', page=page, number=number)


class PostHandler(BaseHandler):
    def get(self, *args, **kwargs):
        post = get_post_id(kwargs['p_id'])
        self.render('post_page.html', post = post)


class UploadHandler(BaseHandler):
    """上传图片逻辑"""
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload_page.html')

    def post(self, *args, **kwargs):
        # 获取所有的input type=file 的字典 用字典取值获取name=image的对象列表
        img_list = self.request.files.get('image')
        # 获取的是一个列表  因为可能有多个相同name
        for img in img_list:
            name = img['filename']
            content = img['body']
            # 实例化一个图片保存类
            im = UploadImage(name, self.settings['static_path'])
            # 调用保存到uploads目录的方法
            im.save_upload(content)
            # 调用保存缩略图方法
            im.save_thumb()
            post = add_post_for(im.upload_path, im.thumb_path, self.current_user)
            self.redirect('/post/{}'.format(post.id))


class PorfileHandler(BaseHandler):
    def get(self, *args, **kwargs):
        username = self.get_argument('name', '')
        print(username)

class LoginoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.session.delete('user_id')
        self.redirect('/login')