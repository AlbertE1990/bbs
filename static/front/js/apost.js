$(function () {
    var ue = UE.getEditor('editor',{
       'serverUrl':'/ueditor/upload/'
    });
    var submit_btn = $('#submit_btn');
    var titleInput = $("input[name='title']");
    var boardSelect = $("select[name='board-id']");
    submit_btn.click(function(event){
        event.preventDefault();
        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = ue.getContent();
        zlajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'board_id':board_id,
                'content':content
            },
            'success':function (data) {
                if (data.code == 200){
                    xtalert.alertConfirm({
                        'type':'success',
                        'msg':data.message,
                        'confirmText':'再发一篇！',
                        'cancelText':'不来了',
                        'confirmCallback':function () {
                            titleInput.val('');
                            boardSelect.val('');
                            ue.setContent('')
                        },
                        'cancelCallback':function () {
                            location.href='/'
                        }
                    })
                }else {
                    xtalert.alertError(data.message)
                }
            },
            'fail':function () {
                xtalert.alertNetworkError()
            }
        })

    })
})

