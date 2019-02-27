import tornado.web
from tornado.web import RequestHandler
from pycket.session import SessionMixin
from utils.picture import save_upload, save_thumb
from utils.verify import add_post_for, get_post_all, get_upload_post, get_post_id


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


class ExploreHandler(RequestHandler):
    def get(self, *args, **kwargs):
        img_list = get_post_all()
        self.render('explore_page.html', img_list = img_list)


class PostHandler(RequestHandler):
    def get(self, *args, **kwargs):
        p_id = get_post_id(kwargs['p_id'])
        self.render('post_page.html', p_id = p_id)


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
            # 每一个对象的filename对应图片名 ***.jpg  body对应图片二进制数据
            name = img['filename']
            content = img['body']
            # 调用保存到uploads目录的方法
            upload_path = save_upload(name, content)
            # 调用保存缩略图方法
            thumb_path = save_thumb(name, upload_path)
            post = add_post_for(upload_path, thumb_path, self.current_user)
            self.redirect('/post/{}'.format(post.id))

