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
import logging
import os
import openerp
import openerp.addons.web.http as oeweb
from openerp.addons.web.controllers.main import Session
from openerp.addons.web.session import OpenERPSession
from shared import cache
from shared import captcha_image
from shared import captcha_con
import random
import StringIO
from time import time
from wheezy.core.uuid import shrink_uuid
from uuid import uuid4
from openerp import pooler

_logger = logging.getLogger(__name__)

#----------------------------------------------------------
# Controller
#----------------------------------------------------------
class CaptchaController(oeweb.Controller):
    _cp_path = '/auth_captcha'

    @openerp.addons.web.http.jsonrequest
    def get_challenge_code(self, req):
        if captcha_con['challenge_key'] not in req.params:
            challenge_code = shrink_uuid(uuid4())
        else:
            challenge_code = req.params[captcha_con['challenge_key']][0]
        re = {
            'challenge_code': challenge_code
        }
        return re

    @openerp.addons.web.http.httprequest
    def get_captcha_image(self, req, challenge_code=None):
        turing_number = ''.join(random.sample(captcha_con['chars'], captcha_con['max_chars']))

        if not cache.set(captcha_con['prefix'] + challenge_code, (int(time()), turing_number),
                         captcha_con['timeout'], captcha_con['namespace']):
            image_data = self.placeholder(req, 'logo.png')
        else:
            _logger.debug(u"验证码缓存增加：key="+captcha_con['prefix'] + challenge_code+u",value=("+
                         str(int(time()))+u","+turing_number+u"),timeout="+str(captcha_con['timeout'])+
                         u",namesapce="+captcha_con['namespace'])
            image_captcha = captcha_image(turing_number)
            output = StringIO.StringIO()
            image_captcha.save(output, "JPEG")
            image_data = output.getvalue()
            output.close()

        headers = [
            ('Content-Type', 'image/jpg'),
            ('Cache-Control', 'no-cache'),
            ('Content-Length', len(image_data)),
        ]
        return req.make_response(image_data, headers)

    def placeholder(self, req, image='placeholder.png'):
        addons_path = oeweb.addons_manifest['web']['addons_path']
        return open(os.path.join(addons_path, 'web', 'static', 'src', 'img', image), 'rb').read()

class Captcha_Session(Session):
    @openerp.addons.web.http.jsonrequest
    def authenticate(self, req, db, login, password, challenge_code=None, turing_number=None, base_location=None):
        return self.validate(db, login, challenge_code, turing_number) and \
               Session.authenticate(self, req, db, login, password, base_location)

    def validate(self, db, login, challenge_code, turing_number):
        #return True
        #判断模块是否安装：如果未安装，则直接验证通过。
        if not self.auth_captcha_is_installed(db):
            _logger.debug(u"数据库'"+db+u"'未安装验证码，跳过验证！")
            return True
        if not captcha_con['enabled']:
            return False

        if not challenge_code or not turing_number:
            _logger.debug(u"用户'"+login+u"'challenge_code或turing_number为空，验证失败！")
            return False

        if len(challenge_code) != 22:
            _logger.debug(u"用户'"+login+u"'challenge_code长度不等于22，验证失败！")
            return False

        if len(turing_number) != captcha_con['max_chars']:
            _logger.debug(u"用户'"+login+u"'turing_number长度不等于"+str(captcha_con['max_chars'])+u"，验证失败！")
            return False

        key = captcha_con['prefix'] + challenge_code
        data = cache.get(key, captcha_con['namespace'])
        if not data:
            _logger.debug(u"用户'"+login+u"'缓存内未找到key='"+key+u"'对应验证码，验证失败")
            #_logger.debug(u"所有已缓存："+str(cache.items))
            return False
        cache.delete(key, 0, captcha_con['namespace'])
        issued, turing_number_cache = data
        if issued + captcha_con['wait_timeout'] > int(time()):
            _logger.debug(u"用户'"+login+u"'验证码录入太快，少于预设的wait_timeout："+str(captcha_con['wait_timeout'])+u"秒，验证失败！")
            return False
        if turing_number_cache != turing_number.upper():
            _logger.debug(u"用户'"+login+u"'提交的验证码--'"+turing_number.upper()+u"'不等于应提供的--'"+turing_number_cache+"'")
            return False

        _logger.debug(u"用户'"+login+u"'验证码"+turing_number+u"通过")
        return True

    def auth_captcha_is_installed(self, db):
        cr = pooler.get_db(db).cursor()
        try:
            cr.execute("SELECT id FROM ir_module_module WHERE name='auth_captcha' and state='installed'")
            module_id = cr.fetchone()
        except openerp.exceptions:
            _logger.debug(u"获取验证码模块是否已安装，查询失败!",exc_info=True)
        finally:
            cr.close()

        return module_id






# vim:expandtab:tabstop=4:softtabstop=4:shiftwidth=4:
