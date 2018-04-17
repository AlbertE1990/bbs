$(function(){
    var delete_btn = $('.delete-btn');
    var highlight_btn = $('.highlight-btn');
    var unhighlight_btn = $('.unhighlight-btn');
    var post_id = delete_btn.parent().parent().attr('data-id');

    highlight_btn.click(function () {
        zlajax.post({
            'url':'/hpost/',
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

})