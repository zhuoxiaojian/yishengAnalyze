# -*- coding: utf-8 -*-
# @Time    : 2019/1/5 9:30
# @Author  : zjj
# @Email   : 1933860854@qq.com
# @File    : verifyUtils.py
# @Software: PyCharm

from PIL import (
    Image, ImageDraw, ImageFont, ImageFilter
)
from django.core.cache import cache
from django.conf import settings
from io import BytesIO
import random
import string
import time
import os
from .constantUtils import ConstantUtil

class Captcha:
    """
        TODO: 自定义生成图形验证码
        using:  captcha 获取图形验证码
        using: verify_captcha 验证图形验证码
    """

    def __init__(self):
        self._code = string.ascii_uppercase + string.digits
        self._width = 100  # 图片宽
        self._height = 40  # 图片高
        self._bits = 4
        self._draw_line = True  # 干扰线
        self._line_num = (1, 5)  # 干扰线数量
        self._bgcolor = 255, 255, 255
        #random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)  # 背景颜色
        self._font_path = os.path.join(settings.BASE_DIR, 'captcha/FZH4FW.TTF')
        self.captcha_code = self._generate_shuffle_str()

    # 生成随机字符串
    def _generate_shuffle_str(self):
        shuffle_list = ','.join(self._code).split(',')
        random.shuffle(shuffle_list)
        return ''.join(shuffle_list[:self._bits])

    # 生成图像
    def _generate_image(self):
        image = Image.new('RGBA', (self._width, self._height), self._bgcolor)  # 画布
        font = ImageFont.truetype(self._font_path, 24)  # 用到的字体
        draw = ImageDraw.Draw(image)  # 画笔
        text = self.captcha_code#self._generate_shuffle_str()
        # 在画布上画字着色
        for i in range(len(text)):
            font_width, font_height = font.getsize(text[i])
            draw.text((self._width / self._bits * (i + 1) - font_width,
                       (self._height - font_height) / random.randint(2, self._bits)),
                      text[i],
                      font=font, fill=(0, 0, 0))
            #fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

        # 画上干扰线
        if self._draw_line:
            self._append_line(draw)
        # 画上躁点
        self._append_points(draw)
        # 应用图形变换
        image = image.transform((self._width, self._height),
                                Image.AFFINE,
                                (1, 0, 0, 0, 1, 0),
                                Image.BILINEAR)  # 创建扭曲
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)  # 汉斯滤镜， 边界加强

        return image

    # 追加躁点
    def _append_points(self, draw):
        chance = min(100, max(0, 5))
        for w in range(self._width):
            for h in range(self._height):
                tmp = random.randint(0, 100)
                if tmp > 100 - chance:
                    draw.point((w, h), fill=(0, 0, 0))

    # 追加干扰线
    def _append_line(self, draw):
        for _ in range(random.randint(*self._line_num)):
            begin = random.randint(0, self._width), random.randint(0, self._height)
            end = random.randint(0, self._width), random.randint(0, self._height)
            draw.line([begin, end], fill=(0, 0, 0))

    def captcha(self):
        buf = BytesIO()
        im = self._generate_image()
        tk = self._cache_captcha()
        im.save(buf, 'PNG')
        im.close()
        buf.seek(0)
        return tk, buf

    # 临时记录图形验证码
    def _cache_captcha(self):
        timestamp_key = str(int(time.time() * 100000000) + random.randint(10, 99))
        cache.set(timestamp_key, self.captcha_code, ConstantUtil.VERIFY_CODE_EXPIRE)
        return timestamp_key

    # 验证图形验证码
    def verify_captcha(self, timestamp_key=None, captcha=None):
        if timestamp_key and captcha and captcha == cache.get(timestamp_key):
            # del the cache data
            cache.delete(timestamp_key)
            return True
        return False
