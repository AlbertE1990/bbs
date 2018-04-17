$(function () {

    var dialog = $("#banner-dialog");
    var table = $("table.table");
    var nameInput = dialog.find("input[name='name']");
    var imageInput = dialog.find("input[name='image_url']");
    var linkInput = dialog.find("input[name='link_url']");
    var priorityInput = dialog.find("input[name='priority']");
    var dialog_save_btn = dialog.find('#save-banner-btn');
    var edit_banner_btn = table.find('.edit-banner-btn');
    var delete_banner_btn = table.find('.delete-banner-btn');
    var add_banner_btn = $('#add-banner-btn');

    var id = '';

    //点击添加轮播图按钮
    add_banner_btn.click(function(){

        nameInput.val('');
        imageInput.val('');
        linkInput.val('');
        priorityInput.val('');
        dialog_save_btn.attr('data-type','add');
        id = ''

    });


    //点击对话框保存按钮
    dialog_save_btn.click(function (event) {
        event.preventDefault();
        var name = nameInput.val();
        var image_url = imageInput.val();
        var link_url = linkInput.val();
        var priority = priorityInput.val();
        var url;
        if ($(this).attr('data-type') == 'update'){
            url = '/cms/ubanners/'
        }else{
            url = '/cms/abanners/'
        }

        if (!name || !image_url || !link_url || !priority){
            xtalert.alertInfoToast('轮播图数据不完整！')
        }else{
            zlajax.post({
                'url':url,
                'data':{
                    'name':name,
                    'image_url':image_url,
                    'link_url':link_url,
                    'priority':priority,
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
    edit_banner_btn.click(function (event) {
        var tr = $(this).parent().parent();
        var name = tr.attr('data-name');
        var image_url = tr.attr('data-image');
        var link_url = tr.attr('data-link');
        var priority = tr.attr('data-priority');

        id = tr.attr('data-id');
        dialog.modal('show');
        nameInput.val(name);
        imageInput.val(image_url);
        linkInput.val(link_url);
        priorityInput.val(priority);

        dialog_save_btn.attr('data-type','update')

    });


    //点击删除按钮
    delete_banner_btn.click(function () {
        tr = $(this).parent().parent();
        id = tr.attr('data-id');
        function delete_banner(){
            zlajax.get({
                'url':'/cms/dbanners/',
                'data':{
                    'id':id
                },
                'success':function (data) {
                    if(data.code==200){
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
        xtalert.alertConfirm({
            'title':'删除',
            'msg':'你确定要删除此轮播图?',
            'confirmText':'删除',
            'text':'你确定要删除此轮播图?',
            'confirmCallback':function(){
                delete_banner();
            }

        });

    })
});
