import os
import uuid
from PIL import Image


class UploadImage(object):
    """
    图片上传类
    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (300, 300)

    def __init__(self, name, static_path):
        self.old_name = name
        self.ext = self.get_ext()
        self.name = self.get_uuid()
        self.filename = self.ext + self.name
        self.static_path = static_path

    def get_ext(self):
        """
        获取图片后缀
        :return:
        """
        _, ext = os.path.splitext(self.old_name)
        return ext

    def get_uuid(self):
        """
        获取唯一id
        :return:
        """
        return uuid.uuid4().hex

    @property
    def upload_path(self):
        """
        获取uploads相对路径 和图片名  用于模板的展示
        :return:
        """
        return os.path.join(self.upload_dir, self.filename)

    @property
    def static_upload_path(self):
        """
        获取绝对路径 用于保存
        :return:
        """
        return os.path.join(self.static_path, self.upload_path)

    def save_upload(self, content):
        """
        保存图片到uploads目录
        :param content:
        :return:
        """
        with open(self.static_upload_path, 'wb') as f:
            f.write(content)

    @property
    def thumb_path(self):
        thumb_url = '{}_{}x{}{}'.format(self.name, self.size[0], self.size[1], self.ext)
        return os.path.join(self.thumb_dir, thumb_url)

    @property
    def static_thumb_path(self):
        return os.path.join(self.static_path, self.thumb_path)

    def save_thumb(self):
        """
        保存图片缩略图
        :return:
        """
        im = Image.open(self.static_upload_path)
        im.thumbnail(self.size)
        im.save(self.static_thumb_path)
