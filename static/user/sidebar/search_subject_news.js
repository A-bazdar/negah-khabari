/**
 * Created by Morteza on 11/11/2015.
 */

var __full = true;
var __stop = true;
var auto_load = false;
$(document).on('change', 'input.all-subjects', function(){
    if($(this).prop('checked')){
        $('input.subject').prop('checked', true);
    }else{
        $('input.subject').prop('checked', false);
    }
});

var __a = true;
var loader_auto_load = $('.loader-auto-load');
$('#search_news_subject').submit(function(e){
    if(__a){
        __a = false;
        e.preventDefault();
        var btn =$('.search-news-subject-btn') ;
        btn.html(__a);
        var postData = $("#search_news_subject").serializeArray();
        jQuery.ajax(
            {
                url: '',
                type: "post",
                data: postData,
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    if (status) {
                        $('.all-news').append(value['html']);
                        if(parseInt(value['count']) < 30){
                            __full = false;
                            return
                        }
                        $('input[name=page]').val(value['page']);
                        auto_load = true;
                        load_img_news();
                        btn.html('?????');
                        __a = true;
                    }
                },
                error: function () {
                    Alert.render('error', function(){
                        btn.html('?????');
                        __a = true;
                    });
                }
            });
    }
});
$(window).scroll(function(){
    if(auto_load){
        var a = $('.footer').innerHeight();
        if($(window).scrollTop() + $(window).height() >= $(document).height() - a && __stop && __full){
            loader_auto_load.slideDown();
            __stop = false;
            var postData = $("#search_news_subject").serializeArray();
            $.ajax({
                data: postData,
                type: 'post',
                url: '',
                async: true,
                success: function(response){
                    var status = response['status'];
                    var messages = response['messages'];
                    var value = response['value'];
                    if (status){
                        $('.all-news').append(value['html']);
                        if(parseInt(value['count']) < 30){
                            loader_auto_load.slideUp();
                            __full = false;
                        }
                        $('input[name=page]').val(value['page']);
                        __stop = true;
                        loader_auto_load.slideUp();
                        load_img_news();
                    }
                }
            });
        }
    }
});
function load_img_news(){
    $.each($("img.new_news_img"),function(){
        $(this).attr("src",$(this).attr("data-src")).removeClass('new_news_img');
    });
}