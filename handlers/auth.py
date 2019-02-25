import tornado.web
from utils.verify import verify_login
from .main import BaseHandler


class LoginHandler(BaseHandler):
    """
    用户登录模块 验证密码
    """
    def get(self, *args, **kwargs):
        # 获取登录之前的路由
        next = self.get_argument('next', '')
        self.render('login_page.html', next = next)

    def post(self, *args, **kwargs):
        # 获取传到模板中的next参数
        next = self.get_argument('next', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        # 调用验证登录模块
        if verify_login(username, password):
            self.session.set('user_id', username)
            self.redirect(next)
        else:
            self.write('failure')
