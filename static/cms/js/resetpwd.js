/**
 * Created by hynev on 2017/11/25.
 */

$(function () {
     var oldpwdE = $("#oldpassword");
     var newpwd1E = $("#newpassword1");
     var newpwd2E = $("#newpassword2");
    $("#submit").click(function (event) {

        var oldpassword = oldpwdE.val();
        var newpassword1 = newpwd1E.val();
        var newpassword2 = newpwd2E.val();
        var inp_clear = function () {
             oldpwdE.val('');
             newpwd1E.val('');
             newpwd2E.val('');
        };
        // event.preventDefault
        // 是阻止按钮默认的提交表单的事件
        event.preventDefault();
        if (newpassword1 != newpassword2){
            xtalert.alertErrorToast('两次密码不一致!');
            inp_clear();
            return false
        };

        // 1. 要在模版的meta标签中渲染一个csrf-token
        // 2. 在ajax请求的头部中设置X-CSRFtoken

        zlajax.post({
            'url': '/cms/resetpwd/',
            'data': {
                'oldpassword': oldpassword,
                'newpassword1': newpassword1,
                'newpassword2': newpassword2
            },
            'success': function (data) {
                if(data.code == 200){
                    xtalert.alertSuccessToast(data.message);
                    inp_clear();
                }
                else{
                    xtalert.alertInfoToast(data.message);
                    inp_clear();
                }
            },
            'fail': function (error) {
                 xtalert.alertNetworkError()
            }
        });

    });
});