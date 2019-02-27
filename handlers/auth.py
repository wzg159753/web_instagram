import tornado.web
from utils.verify import verify_login, user_add
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


class SignupHandler(BaseHandler):
    """
    注册逻辑
    """
    def get(self, *args, **kwargs):
        self.render('signup_page.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        sex = self.get_argument('sex', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        if password1 == password2:
            result = user_add(username, sex, password1)
            if result:
                self.session.set('user_id', username)
                self.redirect(result['msg'])
            else:
                self.redirect('/signup?msg={}'.format(result['msg']))

        else:
            self.redirect('/signup?msg={}'.format('password is not '))
