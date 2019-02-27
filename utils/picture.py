import glob
import os
from PIL import Image
from dbs.modules import Post

def save_upload(name, content):
    """
    保存图片到uploads上传目录
    :param name: 图片名  ***.png or .jpg
    :param content: 图片二进制数据
    :return:
    """
    upload_path = 'static/uploads/{}'.format(name)
    with open(upload_path, 'wb') as f:
        f.write(content)
    return upload_path


def save_thumb(name, upload_path):
    """
    保存缩略图到thumbs目录
    :param name: 图片名 ***.jpg
    :param upload_path: 要打开的uploads里面的图片路径
    :return:
    """
    size = (256, 256)
    # 将文件分割成一个元组（‘name’, ‘.jpg’）
    title, ext = os.path.splitext(name)
    im = Image.open(upload_path)
    # pillow库的 生成缩略图方法
    im.thumbnail(size)
    thumb_path = 'static/thumbs/{}_{}x{}{}'.format(title, size[0], size[1], ext)
    im.save(thumb_path)
    return thumb_path



def get_glob(path):
    """
    返回图片的路径列表
    :param path: 存放图片的目录名
    :return:
    """
    return glob.glob('static/{}/*'.format(path))