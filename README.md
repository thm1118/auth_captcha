auth_captcha
============

OpenERP module :authenticate with captcha

OpenERP7 模块，登陆时使用验证码。支持多进程

与已有的web_recapcha不同的是，web_recapcha使用的是google recpcha验证云服务，
而auth_captcha是在OpenERP Server自己生成验证码图片。 安全性方面，google验证码图片鬼画符一般，机器程序解析更困难，人都经常输错:)，安全性自然也更高，。
但由于GFW，google的服务在中国大陆一直无法保障,而国内也没有较好的第三方验证码服务。

有条件还是应该使用web_recaptcha，或者openid等更高安全方式。

服务端验证码技术使用python 模块 wheezy 系列：
$ easy_install wheezy.captcha
$ easy_install wheezy.core

服务端多进程的缓存使用redis（单进程不需要）。需要配置使用redis。
在具备redis环境下，需要安装python redis模块：
$ easy_install redis

配置说明：share.py文件中，更改配置需要重启OpenERP服务。
'prefix': 缓存key前缀,
'timeout': 验证码有效时间，默认300秒, 'profile': None,
'chars': 验证码字符，默认是'ABCDEFGHJKLMNPQRSTUVWXYZ23456789',
'max_chars': 验证码长度，默认4, 'wait_timeout': 验证码防机器程序快速尝试，默认限制为2秒后,
'redis_server': redis 服务ip地址
'redis_server_port':redis服务端口
'redis_password': redis服务密码


警告：
本模块尚未经生产环境大规模测试.
已在win7开发环境中测试无问题，在Ubuntu12.04(多进程)部署测试无问题。
请在完整测试之前，不要直接部署在正在运营的生产环境中。
限制：
1、依赖非OE依赖的python包，本身不green，应不支持win下的greenopenerp。greenopenerp发布的目的是方便入门和测试，而不是生产部署。
2、未国际化。
3、样式待改进。
4、多进程使用redis的时候，redis垃圾缓存清理机制需要改进。
5、已合并wheezy.caching 代码，后面需要进一步整合。

enjoy

