/**
 * Created by Morteza on 11/13/2015.
 */

$(document).on('click','.show_option_news', function(){
    var data_news = $(this).attr('data-news');
    if($(this).hasClass('closedp')) {
        $(this).removeClass('closedp').addClass('open');
        $('.dropdown-option-container[data-news=' + data_news + ']').slideDown();
    }
    else {
        $(this).removeClass('open').addClass('closedp');
        $('.dropdown-option-container[data-news=' + data_news + ']').slideUp();
    }
});


$(document).on('click', '.option-news.note', function (e) {
    var data_action = $(this).attr('data-action');
    if($(this).hasClass('closedp')){
        $('.second-level-drop-down').css('display','none');
        $(this).removeClass('closedp').addClass('open');
        $('.comment_news_dropdown[data-action=' + data_action + ']').slideDown();
    }
    else{
        $(this).removeClass('open').addClass('closedp');
        $('.comment_news_dropdown[data-action=' + data_action + ']').slideUp();
    }
});


//$(document).on('keyup', 'input[name=option-news-note]', function (e) {
//    if (e.keyCode == '13') {
//        var elm = $(e.target);
//        var news = elm.attr('data-news');
//        var note = elm.val();
//        if(note != ''){
//            var postData = [
//                {name: 'news_id', value: news},
//                {name: 'note', value: note},
//                {name: '_xsrf', value: xsrf_token},
//                {name: 'action', value: 'add'}
//            ];
//            jQuery.ajax(
//            {
//                url: option_news_note_url,
//                type: "post",
//                data: postData,
//                success: function (response) {
//                    var status = response['status'];
//                    var value = response['value'];
//                    if (status) {
//                        $('.option-news-note-success[data-news=' + news + ']').fadeIn().fadeOut();
//                    }
//                }
//            });
//        }
//    }
//});


$(document).on('click', '.send-comment', function(e){
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var note = $('.comment-text[data-news='+ news +']').val();
    if(note != ''){
        var postData = [
            {name: 'news_id', value: news},
            {name: 'note', value: note},
            {name: '_xsrf', value: xsrf_token},
            {name: 'action', value: 'add'}
        ];
        jQuery.ajax(
        {
            url: option_news_note_url,
            type: "post",
            data: postData,
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                if (status) {
                    elm.removeClass('fa-paper-plane-o colorBlue').addClass('fa-check-circle-o colorGreen');
                    setTimeout(function () {
                        elm.removeClass('fa-check-circle-o colorGreen').addClass('fa-paper-plane-o colorBlue');
                    }, 400);
                }
            }
        });
    }
});


$(document).on('click', '.option-news.star', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var postData = [
        {name: 'news_id', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: 'add'}
    ];
    jQuery.ajax(
    {
        url: option_news_star_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                if(value == 'add'){
                    elm.removeClass('fa-star-o');
                    elm.addClass('colorOrange fa-star');
                }else{
                    elm.removeClass('colorOrange fa-star');
                    elm.addClass('fa-star-o');
                }
            }
        }
    });
});


$(document).on('click', '.option-news.important', function (e) {
    var data_action = $(this).attr('data-action');
    if($(this).hasClass('closedp')){
        $('.second-level-drop-down').css('display','none');
        $(this).removeClass('closedp').addClass('open');
        $('.important_news_dropdown[data-action=' + data_action + ']').slideDown();
    }
    else{
        $(this).removeClass('open').addClass('closedp');
        $('.important_news_dropdown[data-action=' + data_action + ']').slideUp();
    }
});


$(document).on('click', '.option-news-important-select', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var important = elm.attr('data-important');
    var postData = [
        {name: 'news_id', value: news},
        {name: 'important', value: important},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: 'add'}
    ];
    jQuery.ajax(
    {
        url: option_news_important_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                $('.option-news-important-check[data-news=' + news + ']').fadeOut();
                if(value == 'add'){
                    $('.option-news-important-check[data-news=' + news + '][data-important= ' + important + ']').fadeIn();
                }
            }
        }
    });
});


$(document).on('click', '.option-news.read', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var postData = [
        {name: 'news_id', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: 'read'}
    ];
    jQuery.ajax(
    {
        url: option_news_read_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                if(value == 'read'){
                    elm.removeClass('fa-circle-o');
                    elm.addClass('colorGreen fa-circle');
                }else{
                    elm.removeClass('colorGreen fa-circle');
                    elm.addClass('fa-circle-o');
                }
            }
        }
    });
});


$(document).on('click', '.option-news.show-picture', function (e) {
    var elm = $(e.target);
    var has_thumbnail = elm.attr('data-has-thumbnail');
    var thumbnail = elm.attr('data-thumbnail');
    if(has_thumbnail == 'true'){
        $('.option_news_body').html('<img src="' + thumbnail + '" class="img-responsive" style="margin: 0 auto;">');
        $('#option_news').modal('toggle');
    }
});


$(document).on('click', '.option-news.news-report-broken', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var postData = [
        {name: 'news_id', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: 'add'}
    ];
    jQuery.ajax(
    {
        url: option_news_report_broken_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                if(value == 'add'){
                    elm.removeClass('fa-warning').addClass('fa-check-circle-o colorGreen');
                    setTimeout(function () {
                        elm.removeClass('fa-check-circle-o colorGreen').addClass('fa-warning');
                    }, 400);
                }
            }
        }
    });
});