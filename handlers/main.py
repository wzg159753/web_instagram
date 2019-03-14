import tornado.web
from tornado.web import RequestHandler
from pycket.session import SessionMixin
from utils.picture import UploadImage
from utils.verify import add_post_for, get_upload_post, get_post_id, paginations, get_user_likes, get_user, add_like, is_like_exits, delete_like, count_like, is_atte_exits, add_atte_prople, delete_atte,delete_upload_img


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
        print(post.id)
        like_prople = count_like(post.id)
        print(like_prople)
        self.render('post_page.html', post = post, like_prople=like_prople)


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
    """
    用户个人页面 包含上传和喜欢
    """
    def get(self, *args, **kwargs):
        # 提前获取个人当前用户id
        my = get_user(self.current_user)
        # 用于获取不通用户的个人页面
        username = self.get_argument('name', '')
        # 如果没有这个参数  就代表是当前用户的个人页
        if not username:
            username = self.current_user
        # 获取用户
        user = get_user(username)
        # 获取用户上传的图片
        upload_posts = get_upload_post(user.username)
        # 获取用户喜欢的图片
        like_post = get_user_likes(user.username)
        # 获取该用户是否已经关注  或添加关注
        atte = is_atte_exits(my.id, user.id)
        self.render('profile_page.html',
                    upload_posts=upload_posts,
                    user=user,
                    like_post=like_post,
                    atte = atte
                    )



class LoginoutHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.session.delete('user_id')
        self.redirect('/login')


class LikeHandler(BaseHandler):
    """
    用户添加喜欢  与heart.js的ajax交互 接收一个post请求
    """
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        # 获取ajax传来的pid
        pid = self.get_argument('pid', '')
        user = get_user(self.current_user)
        # 判断当前用户是否已经喜欢了 这张图片
        if not is_like_exits(user.id, int(pid)):
            # 如果没喜欢就添加喜欢
            add_like(user.id, int(pid))
        else:
            # 如果喜欢了就 删除喜欢
            delete_like(user.id, int(pid))
        # 对用户喜欢表操作完成后 立即执行统计图片被喜欢数
        like_prople = count_like(int(pid))
        # 讲被喜欢数发送的ajax前端
        self.write({'result': 1, "count": str(like_prople)})


class AtteHandler(BaseHandler):
    """
    用户添加关注
    """
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        # 获取被关注用户
        y_id = self.get_argument('yid', '')
        user = get_user(self.current_user)
        # 判断该用户是否已经被关注
        if not is_atte_exits(user.id, int(y_id)):
            # 如果没有就添加关注
            add_atte_prople(user.id, int(y_id))
        else:
            # 如果已经被关注就取消关注
            delete_atte(user.id, int(y_id))


class DeleteHandler(BaseHandler):
    """
    删除用户上传的图片
    """
    def get(self, *args, **kwargs):
        # 先获取当前用户
        user = get_user(self.current_user)
        # 获取点击删除时传来的参数 pid为图片id pnm为用户id
        key = self.get_argument('pid', '')
        pnm = self.get_argument('pnm', '')
        # 判断传来的用户id是不是当前用户id  判断是否是自己上传的
        if user.id == int(pnm):
            # 判断该图片是否添加喜欢了
            if is_like_exits(user.id, int(key)):
                # 如果添加喜欢就删除喜欢
                delete_like(user.id, int(key))
            # 删除图片
            delete_upload_img(user.id, int(key))
            self.redirect('/')

        else:
            self.write("<script>alert('用户权限不够')</script>")


