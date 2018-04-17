/**
 * Created by hynev on 2017/11/25.
 */
/*
$(function () {
     var emailE = $("#inputEmail");
     var passwordE = $("#inputPassword");
    $("#submit").click(function (event) {
        event.preventDefault();
        var email = emailE.val();
        var password = passwordE.val();

       function inp_clear() {
             emailE.val('');
             passwordE.val('');
        };
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken

        zlajax.post({
            'data': {
                'email': email,
                'password':password,
            },
            'success': function (data) {
                if(data.code == 200){
                    xtalert.alertSuccessToast(data.message);
                    inp_clear();
                }
                else{
                    xtalert.alertErrorToast(data.message);
                    inp_clear();
                }
            },
            'fail': function (error) {
                console.log(error);
            }
        });

    });
});
*/
$(function () {
    var emailE = $("#inputEmail");
    var captchaE = $("#inputCaptcha");
    function inp_clear () {
        emailE.val('');
        captchaE.val('')
    };
    $("#captcha-btn").click(function () {
        email = emailE.val();
        if(!email){
            xtalert.alertInfoToast("请输入邮箱");
            return false
        }
        zlajax.get({
            'url':'/cms/email_captcha/',
            'data':{
                'email':email
            },
            'success':function (data) {
                if (data.code == 200){
                    xtalert.alertSuccessToast(data.message)
                }else{
                    xtalert.alertInfo(data.message);
                    inp_clear();
                }
            },
            'fail':function () {
                xtalert.alertNetworkError()
            }
        })
    });
    $("button[type='submit']").click(function(event){
        event.preventDefault();
        var email = emailE.val();
        var captcha = captchaE.val();
        zlajax.post({
            'data':{
                'email':email,
                'captcha':captcha
            },
            'success':function (data) {
                if(data.code == 200){
                    xtalert.alertSuccessToast(data.message);
                    inp_clear()
                }else{
                    xtalert.alertErrorToast(data.message);
                    inp_clear()
                }
            }
        });

    });
})