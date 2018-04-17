$(function(){
    $('#captcha').click(function () {
        var newsrc = '../captcha/?x='+Math.random();
        $(this).attr('src',newsrc)
    });

    $('#graph-captcha').keyup(function () {
        var cap_val = $(this).val();
        if(cap_val.length==4){
            $('#cap-icon').removeClass('glyphicon-question-sign');
            zlajax.get({
            'url':'/captcha/check/',
            'data':{
                'cap_val':cap_val
            },
            'success':function (data) {
                if(data.code==200){
                    $('#cap-icon').removeClass('i-fail glyphicon-remove-sign')
                        .addClass('i-success glyphicon-ok-sign');
                }else{
                   $('#cap-icon').removeClass('i-success glyphicon-ok-sign')
                        .addClass('i-fail glyphicon-remove-sign');
                }


            }
        })
        }else {
            $('#cap-icon').addClass('glyphicon-question-sign').removeClass('i-fail i-success')
        }
    });

    $('#signup-submit-btn').click(function (event) {
        event.preventDefault();
        var telephone = $('#telephone').val();
        var username = $('#username').val();
        var password1 = $('#password1').val();
        var password2 = $('#password2').val();
        var graph_captcha = $('#graph-captcha').val();
        zlajax.post({
            'url':'/signup/',
            'data':{
                'telephone':telephone,
                'username':username,
                'password1':password1,
                'password2':password2,
                'graph_captcha':graph_captcha
            },
            'success':function (data) {
                if(data.code == 200){
                    var return_to = $('#return-to').text();
                    xtalert.alertConfirm({
                        'title':'注册成功！',
                        'confirmText':'返回登录页面',
                        'cancelText':'返回首页',
                        'confirmCallback':function () {
                            location.href = '/login/'
                        },
                        'cancelCallback':function () {
                            location.href = '/'
                        }
                    });

                }else{
                    xtalert.alertError(data.message)
                }
            },
            'fail':function () {
                xtalert.alertNetworkError();
            }
        }
    )
    });

    $('#login-submit-btn').click(function (event) {
        event.preventDefault();
        var tel = $('#telephone').val();
        var pwd = $('#password').val();
        var graph_captcha = $('#graph-captcha').val();
        zlajax.post({
            'url':'/login/',
            'data':{
                'telephone':tel,
                'password':pwd,
                'graph_captcha':graph_captcha
            },
            'success':function (data) {
                if (data.code == 200){
                    var return_to = $('#return-to').text();
                    xtalert.alertConfirm({
                        'title': '登录成功！',
                        'confirmText': '返回之前页面',
                        'cancelText': '返回首页',
                        'confirmCallback': function () {
                            if (return_to){
                                location.href = return_to
                            }else{
                                location.href = '/'
                            }

                        },
                        'cancelCallback': function () {
                            location.href = '/'
                        }
                    })
                }else{
                    xtalert.alertErrorToast(data.message)
                }

            },
            'fail':function () {
                xtalert.alertNetworkError();
            }

        })
    })
})