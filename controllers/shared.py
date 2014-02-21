# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Author:            Tiger <tanhongming@hotmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#from wheezy.caching import MemoryCache
import logging
from wheezy.captcha.image import captcha
from wheezy.captcha.image import background
from wheezy.captcha.image import curve
from wheezy.captcha.image import noise
from wheezy.captcha.image import smooth
from wheezy.captcha.image import text
from wheezy.captcha.image import offset
from wheezy.captcha.image import rotate
from wheezy.captcha.image import warp
import os
from openerp.tools.config import config
import memory

_logger = logging.getLogger(__name__)

captcha_con = {
    'prefix': 'captcha:', 'namespace': 'www.example.com',
    'timeout': 300, 'profile': None,
    'chars': 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789',
    'max_chars': 4, 'wait_timeout': 2,
    'challenge_key': 'c', 'turing_key': 'turing_number',
    'enabled': True,
    'redis_server': '127.0.0.1',
    'redis_server_port': 6379,
    'redis_password': None
}

class WrapperRedis(object):
    def __init__(self):
        _logger.debug(u"使用Redis")
        self.r = redis.StrictRedis(host=captcha_con['redis_server'],
                                   port=captcha_con['redis_server_port'], password=captcha_con['redis_password'], db=0)

    #fixme:时间控制
    def set(self, key, value, time=0, namespace=None):
        now = int(unixtime())
        time = memory.expires(now, time)
        lvalue = list(value)
        lvalue.append(time)
        lvalue[0] = str(lvalue[0])
        lvalue[2] = str(lvalue[2])
        wrap_value = ','.join(lvalue)
        _logger.debug(u"redis设置：key="+key+u",value="+wrap_value)
        return self.r.set(key, wrap_value)

    def get(self, key, namespace=None):
        wrap_value = self.r.get(key)
        if wrap_value:
            _logger.debug(u"redis获取：key="+key+u",wrap_value="+wrap_value)
            lvalue = wrap_value.split(',')
            time = int(lvalue[2])
            value = lvalue[:2]
            _logger.debug(u"redis获取：key="+key+u",value="+','.join(value))
            value[0] = int(value[0])
            now = int(unixtime())

            if now < time:
                return value
            else:
                _logger.debug(u"redis：key="+key+u",时间超时，清除")
                self.r.delete(key)
        return None

    def delete(self, key, seconds=0, namespace=None):
        _logger.debug(u"redis：key="+key+u"被清除")
        return self.r.delete(key)

if config['workers']:
    import redis
    from time import time as unixtime
    cache = WrapperRedis()
else:
    from memory import MemoryCache
    cache = MemoryCache()

adp = os.path.abspath(config['addons_path'])
CourierNew = os.path.join(adp, 'auth_captcha', 'controllers', 'fonts',  'CourierNew-Bold.ttf')
LiberationMono = os.path.join(adp, 'auth_captcha', 'controllers', 'fonts', 'LiberationMono-Bold.ttf')

captcha_image = captcha(drawings=[
    background(),
    text(fonts=[CourierNew, LiberationMono], drawings=[warp(), rotate(), offset()]),
    curve(),
    noise(),
    smooth()
])


