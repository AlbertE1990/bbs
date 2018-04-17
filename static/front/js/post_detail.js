$(function(){
    var replyE = $('#reply');
    var submit = $('.submit-btn button');
    submit.click(function () {
        var author_id = replyE.attr('data-author');
        if (!author_id){
            xtalert.alertError('请先登录！');
            return false
        }
        var post_id = replyE.attr('data-post');
        var content = replyE.val();
        zlajax.post({
            'url':'/acomment/',
            'data':{
                'author_id':author_id,
                'post_id':post_id,
                'content':content
            },
            'success':function (data) {
                if(data.code ==200){
                    location.reload()
                }else{
                    xtalert.alertError(data.message)
                }
            }
        })
    })

})