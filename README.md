auth_captcha
============

OpenERP  module :authenticate with captcha

OpenERP7 模块，登陆时使用验证码。

验证码使用 
与已有的web_recapcha不同的是，web_recapcha使用的是google recpcha验证云服务，而auth_captcha是在OpenERP Server自己生成验证码图片。
安全性方面，肯定是web_recaptcha高多了。但由于众所周知的防火长城问题，google的服务在中国大陆一直无法保障,而国内也没有较好的第三方验证码服务。

有条件还是应该使用web_recaptcha，或者openid等更高安全方式。


服务端验证码技术使用python包wheezy.captcha，默认是300秒超时，2秒内禁止登陆等时间控制。
配置在share.py 中，更高配置需要重启OpenERP服务。

安装wheezy.captcha ： $ easy_install wheezy.captcha。


警告：本模块尚未经生产环境大规模测试，只在win7开发环境中测试无问题。 请在完整测试之前，不要直接部署在正在运营的生产环境中。


enjoy

