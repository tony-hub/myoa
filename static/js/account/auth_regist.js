
//获取cookie
function get_cookie(name) {
    var xsrf_cookies = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return xsrf_cookies[1];
}

//注册用户函数
$(document).ready(function(){
    get_image_code();

    //点击获取图形验证码
    $('#a_code').click(function () {
        get_image_code();
    });


    //点击获取手机验证码
    $('#captcha-btn').click(function (event) {
        event.preventDefault();
        //获取焦点时隐藏消息标签
        $(".mobile").focus(function () {
            $(".mobile-message").hide();
        });
        //获取手机号码
        var mobile = $('.mobile').val();
        //如果没有手机号提示输入手机号
        if (!mobile) {
            $(".mobile-message").html("请输入手机号码！");
            $(".mobile-message").show();
            return;
        }

        var self = $(this);
        var timeCount = 60;
        //设置不能点击
        self.attr('disabled', 'disabled');
        // 设置当前倒计时
        var timer = setInterval(function () {
            self.text(timeCount);
            timeCount--;
            if (timeCount <= 0) {
                self.text('获取验证码');
                self.removeAttr('disabled');
                clearInterval(timer);
            }
        }, 1000);
        // 发送ajax的请求

        var captcha = $('.captcha').val();

        $.ajax({
            'url': '/account/send_mobile_code/',
            'type': "post",
            'data': {
                'mobile': mobile,
                'code': code,
                'captcha': captcha
            },
            'headers': {
                "X-CSRFToken": get_cookie("csrftoken")
            },
            'success': function (data) {
                if (data['status'] != 200) {   //如果返回非200的状态
                    swal({
                        'title': '出问题了',
                        'text': data['msg'],
                         'showConfirmButton': true,
                        'type': 'error',
                        'timer': 1500
                    });
                    get_image_code();
                    self.text('获取验证码');          //
                    self.removeAttr('disabled');
                    clearInterval(timer);
                } else {
                    get_image_code();
                    swal({
                        'title': '干得漂亮',
                        'text': '验证码已发送至' + data['msg'] +','+ '请注意查收！',
                        'type': 'success',
                        'showConfirmButton': true
                    });
                }
            }
        });

    });
    //注册
    $('#submit').click(
        function(){
            event.preventDefault();
             console.log($('#mobile_captcha').val())
            $.ajax({
                    'url':'/account/user_regist/',
                    'type':'post',
                    'data':{
                        'mobile_captcha':$('#mobile_captcha').val(),
                        'mobile':$('#mobile').val(),
                        'captcha':$('#captcha').val(),
                        'code' :$('#code').val(),
                        'name':$('#name').val(),
                       'password1':$('#password1').val(),
                        'password2':$('#password2').val()
                    },
                    'headers':{ "X-CSRFToken":get_cookie('csrftoken')},
                    'success':function(data){
                        if(data['status'] == 200){
                            swal({
                                'title':'干得漂亮',
                                'text':data['msg'],
                                'type':'success',
                                'showConfirmButton':true,
                                'timer':1500
                        },function(){
                                  window.location = $('#login_url').val()
                            });

                        }else {
                            swal({
                                'title':'出问题了',
                                'text':data['msg'],
                                'type':'error',
                                'showConfirmButton':false,
                                'showConfirmButton':true,
                                'timer':1500
                            }, function () {
                                get_image_code();
                            })
                        }
                    }
                })
        })
});
