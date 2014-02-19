openerp.auth_captcha = function(instance) {
    instance.auth_captcha = instance.auth_captcha || {};
    var _t = instance.web._t;

    instance.web.Login.include({
        init: function(parent, action) {
            this._super(parent, action);
            this.on("challenge_code_change_trigger", this, this.challenge_code_change);
        },
        start: function() {
            var self = this;
            self.$el.find("form .oe_login_captcha").click(self.proxy(self.get_challenge_code));

            return this._super().always(
               self.proxy(self.get_challenge_code)
            );
        },

        get_challenge_code: function(){
            var self = this;
            self.rpc("/auth_captcha/get_challenge_code", {}).then(function(result) {
                    self.$("form input[name=challenge_code]").val(result.challenge_code);
                    self.trigger("challenge_code_change_trigger", result.challenge_code);
             });
        },

        challenge_code_change : function(challenge_code) {
            $("form .oe_login_captcha").attr("src","/auth_captcha/get_captcha_image"+"?challenge_code="+self.$("form input[name=challenge_code]").val());
        },

        on_submit: function(ev) {
            if(ev) {
                ev.preventDefault();
            }
            var db = this.$("form [name=db]").val();
            if (!db) {
                this.do_warn(_t("Login"), _t("No database selected !"));
                return false;
            }
            var login = this.$("form input[name=login]").val();
            var password = this.$("form input[name=password]").val();
            var turing_number = this.$("form input[name=turing_number]").val();
            var challenge_code = this.$("form input[name=challenge_code]").val();
            this.do_login(db, login, password, challenge_code, turing_number);
        },

        do_login: function (db, login, password, challenge_code, turing_number) {
            var self = this;
            self.hide_error();
            self.$(".oe_login_pane").fadeOut("slow");
            return this.session.session_authenticate(db, login, password, challenge_code, turing_number).then(function() {
                self.remember_last_used_database(db);
                if (self.has_local_storage && self.remember_credentials) {
                    localStorage.setItem(db + '|last_login', login);
                }
                self.trigger('login_successful');
            }, function () {
                self.$(".oe_login_pane").fadeIn("fast", function() {
                    self.show_error(_t("用户名，密码或验证码错误！"));
                    return self.get_challenge_code();
                });
            });
        }
    });

    instance.web.Session.include({
        session_authenticate: function(db, login, password, challenge_code, turing_number, _volatile) {
            var self = this;
            var base_location = document.location.protocol + '//' + document.location.host;
            var params = { db: db, login: login, password: password, challenge_code: challenge_code, turing_number:turing_number, base_location: base_location };
            return this.rpc("/web/session/authenticate", params).then(function(result) {
                if (!result.uid) {
                    return $.Deferred().reject();
                }
                _.extend(self, result);
                if (!_volatile) {
                    self.set_cookie('session_id', self.session_id);
                }
                return self.load_modules();
            });
        }
    });
};
