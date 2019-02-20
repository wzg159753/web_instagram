from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('index_page.html')


class ExploreHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('explore_page.html')


class PostHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render('post_page.html', p_id = kwargs['p_id'])