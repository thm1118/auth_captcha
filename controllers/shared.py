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
from wheezy.caching import MemoryCache
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

cache = MemoryCache()

adp = os.path.abspath(config['addons_path'])
CourierNew = os.path.join(adp, 'auth_captcha', 'controllers', 'fonts',  'CourierNew-Bold.ttf')
LiberationMono = os.path.join(adp, 'auth_captcha', 'controllers', 'fonts', 'LiberationMono-Bold.ttf')

captcha_image = captcha(drawings=[
    background(),
    text(fonts=[CourierNew,
        LiberationMono],
        drawings=[
            warp(),
            rotate(),
            offset()
        ]),
    curve(),
    noise(),
    smooth()
])

captcha_con = {
    'prefix': 'captcha:', 'namespace': None,
    'timeout': 300, 'profile': None,
    'chars': 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789',
    'max_chars': 4, 'wait_timeout': 2,
    'challenge_key': 'c', 'turing_key': 'turing_number',
    'enabled': True
}