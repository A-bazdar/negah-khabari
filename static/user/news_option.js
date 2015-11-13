/**
 * Created by Morteza on 11/13/2015.
 */


$(document).on('click', '.option-news.note', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    $('.option-news-show.note[data-news=' + news + ']').slideToggle();
});


$(document).on('keyup', 'input[name=option-news-note]', function (e) {
    if (e.keyCode == '13') {
        var elm = $(e.target);
        var news = elm.attr('data-news');
        var note = elm.val();
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
                        $('.option-news-note-success[data-news=' + news + ']').fadeIn().fadeOut();
                    }
                }
            });
        }
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
                    elm.addClass('colorYellow');
                }else{
                    elm.removeClass('colorYellow');
                }
            }
        }
    });
});


$(document).on('click', '.option-news.important', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    $('.option-news-show.important[data-news=' + news + ']').slideToggle();
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
                    elm.addClass('colorGreen');
                }else{
                    elm.removeClass('colorGreen');
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
                    $('.option-news-success[data-news=' + news + ']').fadeIn().fadeOut();
                }
            }
        }
    });
});