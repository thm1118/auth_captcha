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
{
    'name': "Authentication with captcha",
    'version' : "0.3",
    'author': "Tiger",
    'website' : "https://github.com/thm1118/",
    "license": "AGPL-3",
    'category': "Tools",
    'images': ['images/screenshot.jpg', ],
    'description': """
OpenERP module :authenticate with captcha
===============================================
OpenERP7 模块，登陆时使用验证码。

与已有的web_recapcha不同的是，web_recapcha使用的是google recpcha验证云服务，
而auth_captcha是在OpenERP Server自己生成验证码图片。 安全性方面，google验证码图片鬼画符一般，机器程序解析更困难，人都经常输错:)，安全性自然也更高，。
但由于GFW，google的服务在中国大陆一直无法保障,而国内也没有较好的第三方验证码服务。

有条件还是应该使用web_recaptcha，或者openid等更高安全方式。

服务端验证码技术使用python 模块 wheezy 系列：
$ easy_install wheezy.captcha
$ easy_install wheezy.caching
$ easy_install wheezy.core

配置说明：share.py文件中，更改配置需要重启OpenERP服务。
'prefix': 缓存key前缀,
'timeout': 验证码有效时间，默认300秒, 'profile': None,
'chars': 验证码字符，默认是'ABCDEFGHJKLMNPQRSTUVWXYZ23456789',
'max_chars': 验证码长度，默认4, 'wait_timeout': 验证码防机器程序快速尝试，默认限制为2秒后,



警告：
本模块尚未经生产环境大规模测试，已在win7开发环境中测试无问题，在Ubuntu12.04部署测试无问题。 请在完整测试之前，不要直接部署在正在运营的生产环境中。
限制：
1、依赖非OE依赖的python包，本身不green，应不支持win下的greenopenerp。greenopenerp发布的目的是方便入门和测试，而不是生产部署。
2、未国际化。
3、样式待改进。
    """,
    'depends': [
        'web',
    ],
    'js': [
        'static/src/js/captcha.js'
    ],
    'css': [

    ],
    'qweb': [
        'static/src/xml/captcha.xml'
    ],
    'installable': True,
    'auto_install': False,
    'web_preload': False,
}
