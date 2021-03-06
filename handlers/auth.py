import tornado.web
from .main import BaseHandler



class LoginHandler(BaseHandler):
    """
    用户登录模块 验证密码
    """
    def get(self, *args, **kwargs):
        # 获取登录之前的路由
        next = self.get_argument('next', '/')
        self.render('login_page.html', next = next)

    def post(self, *args, **kwargs):
        # 获取传到模板中的next参数
        next = self.get_argument('next', '')
        username = self.get_argument('username', '')
        password = self.get_argument('password', '')
        # 调用验证登录模块
        info = self.user.verify_login(username, password)
        if info:
            # 如果next不为空， 就说明是跳转过来的
            if next is not None:
                self.session.set('user_id', username)
                self.redirect(next)
            else:
                # 如果next为空  就说明是直接进login路由的
                self.session.set('user_id', username)
                self.redirect(next)
        else:
            self.write("<script>alert('用户或密码错误')</script>")


class SignupHandler(BaseHandler):
    """
    注册逻辑
    """
    def get(self, *args, **kwargs):
        # 获取返回的msg信息  记录用户操作的错误
        msg = self.get_argument('msg', '')
        self.render('signup_page.html', msg=msg)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        sex = self.get_argument('sex', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        # 判断第一次和第二次密码是否相同
        if password1 == password2:
            # 如果相同  就调用注册函数
            result = self.user.signup_user(username, password1, sex)
            if result['status'] ==  200:
                # 如果注册成功 就直接设置为登录状态
                self.session.set('user_id', username)
                self.redirect(result['msg'])
            else:
                # 如果注册失败 就再次向signup发一次请求  携带msg参数 展示的页面
                self.redirect('/signup?msg={}'.format(result['msg']))

        else:
            self.redirect('/signup?msg={}'.format('password is not '))


class ChangeSignHandler(BaseHandler):
    """
    修改用户信息
    """
    def get(self, *args, **kwargs):
        self.render('change_page.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        user = self.dbs.orm.get_user()
        username = self.get_argument('username', '').replace(' ', '')
        password = self.get_argument('password', '').replace(' ', '')
        sex = self.get_argument('sex', '')
        if user.username == username:
            info = self.dbs.orm.update_user(user.username, username, sex, password)
            if info:
                # 如果修改成功就把session信息删除  重新登录
                self.session.delete('user_id')
                self.redirect('/login')
        else:
            self.write('<script>alert("用户权限不够")</script>')
