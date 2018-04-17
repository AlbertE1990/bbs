$(function () {

    var dialog = $("#board-dialog");
    var nameInput = dialog.find("input[name='name']");

    var table = $('table.table');
    var edit_board_btn = table.find('.edit-board-btn');
    var delete_board_btn = table.find('.delete-board-btn');
    var add_board_btn= $('#add-board-btn');
    var dialog_save_btn = dialog.find('#save-board-btn');
    var id = '';

    //点击添加板块图按钮
    add_board_btn.click(function(){
        nameInput.val('');
        dialog_save_btn.attr('data-type','add');
        id = ''

    });


    //点击模态框保存按钮
    dialog_save_btn.click(function (event) {
        event.preventDefault();
        var name = nameInput.val();

        var url;
        if ($(this).attr('data-type') == 'update'){
            url = '/cms/uboard/'
        }else{
            url = '/cms/aboard/'
        }

        if (!name){
            xtalert.alertInfoToast('请输入板块名称！')
        }else{
            zlajax.post({
                'url':url,
                'data':{
                    'name':name,
                    'id':id
                },
                'success':function (data) {
                    if (data.code == 200){
                        location.reload();
                    }else {
                        xtalert.alertError(data.message)
                    }
                },
                'fail':function () {
                    xtalert.alertNetworkError()
                }
            })
        }
    });


    //点击编辑按钮
    edit_board_btn.click(function (event) {
        var tr = $(this).parent().parent();
        var raw_name = tr.attr('data-name');
        id = tr.attr('data-id');
        dialog.modal('show');
        nameInput.val(raw_name);
        dialog_save_btn.attr('data-type','update')

    });


    //点击删除按钮
    delete_board_btn.click(function (event) {
        var tr = $(this).parent().parent();
        var id = tr.attr('data-id');
        var delete_board = function () {
            zlajax.post({
                'url':'/cms/dboard/',
                'data':{
                    'id':id
                },
                'success':function (data) {
                    if(data.code == 200){
                        location.reload();
                    }else{
                        xtalert.alertError(data.message)
                    }
                },
                'fail':function () {
                    xtalert.alertNetworkError()
                }
            })
        };
        swal({
            title: '提示',
            showCancelButton: true,
            showConfirmButton: true,
            confirmButtonText:'删除',
            cancelButtonText: '取消',
            text: '确定要删除此轮播图?'
        },function (isConfirm) {
            if(isConfirm){
                delete_board();

            }

        })

    })

});
