/**
 * Created by Morteza on 11/13/2015.
 */

$(document).on('click','.show_option_news', function(){
    var data_news = $(this).attr('data-news');
    if($(this).hasClass('closedp')) {
        if($('.news_list_detail[data-news=' + data_news + ']').hasClass('closeBox')){
            $(this).removeClass('closedp').addClass('open');
            $('.show_option_news').css('background-position','-47px -130px');
            $(this).css('background-position','-29px -131px');
            $('.dropdown-option-container[data-news=' + data_news + ']').slideDown();
            $('.dropdown-option-container[data-news!=' + data_news + ']').slideUp();
        }
    }
    else {
        $(this).removeClass('open').addClass('closedp');
        $(this).css('background-position','-47px -130px');
        $('.dropdown-option-container[data-news=' + data_news + ']').slideUp();
    }
});

$(document).on('click','.second-header-dropdown', function(){
    var data_action = $(this).attr('data-action');
    if($(this).hasClass('closedp')) {
        $(this).removeClass('closedp').addClass('open');
        $('.my-dropdown[data-action=' + data_action + ']').slideDown();
        $('.my-dropdown[data-action!=' + data_action + ']').slideUp();
        $('.second-header-dropdown[data-action!=' + data_action + ']').removeClass('open').addClass('closedp');
    }
    else if($(this).hasClass('open')){
        $(this).removeClass('open').addClass('closedp');
        $('.my-dropdown[data-action=' + data_action + ']').slideUp();
    }
});


$(document).on('click', '.option-news.note', function (e) {
    var data_action = $(this).attr('data-action');
    var data_news = $(this).attr('data-news');
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

var html_note = '<div class="row margin-top-10" style="background-color: #BED0E2">\
                    <div class="col-md-1 col-sm-1 text-right"><i class="fa fa-comment"></i></div>\
                    <div class="col-md-11 col-sm-11">__note__</div>\
                </div>';
$(document).on('click', '.send-comment', function(e){
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var _type = elm.attr('data-type');
    var note = $('.comment-text[data-news='+ news +'][data-type=' + _type + ']').val();
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
                    $('.option-news.note[data-news=' + news + ']').addClass('colorBlue');
                    $('.comment-text[data-news='+ news +']').val(note);
                    $('.note-body-show.note-text[data-news=' + news + ']').html(note);
                    $('.note-body-contain[data-news=' + news + ']').show();
                }
            }
        });
    }
});


$(document).on('click', '.option-news.star', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var action = 'delete';
    if(elm.hasClass('fa-star-o')){
        action = 'add';
    }
    var postData = [
        {name: 'news_id', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: action}
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
                    $('.option-news.star[data-news=' + news + ']').removeClass('fa-star-o').addClass('colorOrange fa-star');
                }else{
                    $('.option-news.star[data-news=' + news + ']').removeClass('colorOrange fa-star').addClass('fa-star-o');
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
                    $('.option-news.important[data-news=' + news + ']').addClass('colorBeautyRed');
                }
            }
        }
    });
});


$(document).on('click', '.option-news.read', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var action = 'unread';
    if(elm.hasClass('fa-circle-o')){
        action = 'read';
    }
    var postData = [
        {name: 'news_id', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: action}
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
                    $('.option-news.read[data-news=' + news + ']').removeClass('fa-circle-o').addClass('colorGreen fa-circle');
                    $('.news_list_detail[data-news=' + news + ']').addClass('read').removeClass('unread');
                }else{
                    $('.option-news.read[data-news=' + news + ']').removeClass('colorGreen fa-circle').addClass('fa-circle-o');
                    $('.news_list_detail[data-news=' + news + ']').addClass('unread').removeClass('read');
                }
            }
        }
    });
});


$(document).on('click', '.option-news.news-report-broken', function (e) {
    var data_action = $(this).attr('data-action');
    if($(this).hasClass('closedp')){
        $('.news_report_broken_text').css('display','none');
        $(this).removeClass('closedp').addClass('open');
        $('.news_report_broken_text[data-action=' + data_action + ']').slideDown();
    }
    else{
        $(this).removeClass('open').addClass('closedp');
        $('.news_report_broken_text[data-action=' + data_action + ']').slideUp();
    }
});


$(document).on('click', '.send-news-report-broken', function(e){
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var text = $('.news-report-broken-text[data-news='+ news +']').val();
    var link = elm.attr('data-link');
    var title = elm.attr('data-title');
    if(text != ''){
        var postData = [
            {name: 'news_id', value: news},
            {name: 'text', value: text},
            {name: 'link', value: link},
            {name: 'title', value: title},
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
                    elm.removeClass('fa-paper-plane-o colorBlue').addClass('fa-check-circle-o colorGreen');
                    setTimeout(function () {
                        elm.removeClass('fa-check-circle-o colorGreen').addClass('fa-paper-plane-o colorBlue');
                    }, 400);
                    $('.news-report-broken-text').val('');
                }
            }
        });
    }
});


$(document).on('click', '.option-news-all', function(e){
    var elm = $(e.target);
    var option = elm.attr('data-option');
    var value = elm.attr('data-value');
    if(option == 'note' && value != "delete"){
        value = $('textarea.send-comment-all').val();
    }
    var postData = [
        {name: 'option', value: option},
        {name: 'value', value: value},
        {name: '_xsrf', value: xsrf_token}
    ];

    $.each($('input[type=checkbox][name=news-select]:checked'), function(){
        postData.push({name: "news", value: $(this).val()});
    });
    jQuery.ajax(
    {
        url: option_news_all_url,
        type: "post",
        data: postData,
        success: function (response) {
            var r = response['value'];
            if(option == 'read'){
                if(value == 'read'){
                    for(var i = 0; i < r.length; i++){
                        $('.option-news.read[data-news=' + r[i] + ']').removeClass('fa-circle-o').addClass('colorGreen fa-circle');
                        $('.news_list_detail[data-news=' + r[i] + ']').addClass('read').removeClass('unread');
                    }
                }else {
                    for (var i = 0; i < r.length; i++){
                        $('.option-news.read[data-news=' + r[i] + ']').removeClass('colorGreen fa-circle').addClass('fa-circle-o');
                        $('.news_list_detail[data-news=' + r[i] + ']').addClass('unread').removeClass('read');
                    }
                }
            }
            if(option == 'star'){
                if(value == 'add'){
                    for(var i = 0; i < r.length; i++){
                        $('.option-news.star[data-news=' + r[i] + ']').removeClass('fa-star-o').addClass('colorOrange fa-star');
                    }
                }else{
                    for(var i = 0; i < r.length; i++)
                        $('.option-news.star[data-news=' + r[i] + ']').removeClass('colorOrange fa-star').addClass('fa-star-o');
                }
            }
            if(option == 'important'){
                if(value != 'delete'){
                    for(var i = 0; i < r.length; i++){
                        $('.option-news-important-check[data-news=' + r[i] + ']').fadeOut();
                        $('.option-news-important-check[data-news=' + r[i] + '][data-important= ' + value + ']').fadeIn();
                        $('.option-news.important[data-news=' + r[i] + ']').addClass('colorBeautyRed');
                    }
                }else{
                    for(var i = 0; i < r.length; i++){
                        $('.option-news-important-check[data-news=' + r[i] + ']').fadeOut();
                        $('.option-news.important[data-news=' + r[i] + ']').removeClass('colorBeautyRed');
                    }
                }
            }
            if(option == 'note'){
                if(value != 'delete'){
                    for(var i = 0; i < r.length; i++){
                        $('.comment-text[data-news='+ r[i] +']').val(value);
                        $('.option-news.note[data-news=' + r[i] + ']').addClass('colorBlue');
                        $('.body-news-comment[data-news=' + r[i] + ']').html(html_note.replace(/__note__/g, value));
                    }
                }else{
                    for(var i = 0; i < r.length; i++){
                        $('.comment-text[data-news='+ r[i] +']').val('');
                        $('.option-news.note[data-news=' + r[i] + ']').removeClass('colorBlue');
                        $('.body-news-comment[data-news=' + r[i] + ']').html('');
                    }
                }
            }
        }
    });
});

$(document).on('click', '.option-news.news-report-broken', function (e) {
    var data_action = $(this).attr('data-action');
    if($(this).hasClass('closedp')){
        $('.news_report_broken_text').css('display','none');
        $(this).removeClass('closedp').addClass('open');
        $('.news_report_broken_text[data-action=' + data_action + ']').slideDown();
    }
    else{
        $(this).removeClass('open').addClass('closedp');
        $('.news_report_broken_text[data-action=' + data_action + ']').slideUp();
    }
});

$(document).on('click', '.font-print-option-news.font-print-option-news-tabs', function(){
    var data_action = $(this).attr('data-action');
    $('.tab_content.font-print-option-news').hide();
    $('.tab_content.font-print-option-news[data-action=' + data_action + ']').fadeIn();
});

$(document).on('click', '.print-option-news-btn.print-option-news', function(e){
    var btn = $(e.target).closest('.print-option-news-btn.print-option-news');
    var postData = $('#print_option_news').serializeArray();
    var news = $('#news_print_option_news').val();
    var _url = print_news_url.replace(/__news__/g, news);
    jQuery.ajax(
    {
        url: _url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                location.href = _url;
            }
        }
    });
})

;$(document).on('click', '.option-news.save', function (e) {
    var elm = $(e.target);
    var news = elm.attr('data-news');
    var _url = show_news_url.replace(/__news__/g, news);
    jQuery.ajax(
    {
        url: _url,
        type: "put",
        data: [{name: '_xsrf', value: xsrf_token}],
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                var a = document.body.appendChild(
                        document.createElement("a")
                    );
                a.download = value['title'] + ".html";
                a.href = "data:text/html;charset=utf-8, " + value['html'];
                a.innerHTML = "[Export conent]";
                a.click();
            }
        }
    });
});