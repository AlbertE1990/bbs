$(function(){
    var post_li = $('.post-group-head li');
    post_li.click(function () {
        $(this).siblings().removeClass('active');
        $(this).addClass('active');
    })
})