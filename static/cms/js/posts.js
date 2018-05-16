$(function(){
    var delete_btn = $('.delete-btn');
    var highlight_btn = $('.highlight-btn');
    var unhighlight_btn = $('.unhighlight-btn');


    //点击加精
    highlight_btn.click(function () {
        var post_id = $(this).parent().parent().attr('data-id');
        zlajax.post({
            'url':'/cms/hpost/',
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data.code == 200){
                    location.reload()
                }
            },
            'fail':function () {
                xtalert.alertNetworkError()
            }
        })
    });

    //点击取消加精
    unhighlight_btn.click(function () {
        var post_id = $(this).parent().parent().attr('data-id');
        zlajax.post({
            'url':'/cms/uhpost/',
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data.code == 200){
                    location.reload()
                }
            },
            'fail':function () {
                xtalert.alertNetworkError()
            }
        })
    })

});