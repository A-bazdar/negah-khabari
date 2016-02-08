/**
 * Created by Morteza on 12/18/2015.
 */

function make_show_news(news, body_news_font, news_content) {
    var _make = $('#make_show_news');
    $('.detail_news_scroll').attr('data-news', news['id']);
    _make.html($('#show_news').html());
    _make.find('div#option_news').attr('data-news', news['id']);
    _make.find('div#note_drop_down').attr('data-action', news['id']).attr('data-action', news['id']);
    _make.find('i#send_note_btn').attr('data-news', news['id']);
    if (news['options']['note'] != false) {
        _make.find('i#note_icon').addClass('colorBlue').attr('data-news', news['id']).attr('data-action', news['id']);
        _make.find('div#note_body_contain').attr('data-news', news['id']);
        _make.find('div#note_body_show').attr('data-news', news['id']).html(news['options']['note']);
        _make.find('textarea#send_note_text').attr('data-news', news['id']).text(news['options']['note']);
    }else{
        _make.find('i#note_icon').attr('data-news', news['id']).attr('data-action', news['id']);
        _make.find('div#note_body_contain').attr('data-news', news['id']).css('display', 'none');
        _make.find('div#note_body_show').attr('data-news', news['id']);
        _make.find('textarea#send_note_text').attr('data-news', news['id']);
    }
    if (news['options']['star']) {
        _make.find('i#star_icon').addClass('colorOrange fa-star').attr('data-news', news['id']);
        _make.find('div#sm_star_icon').removeClass('sm-star-icon').addClass('sm-yellow-star-icon').attr('data-news', news['id']);
    } else {
        _make.find('i#star_icon').addClass('fa-star-o').attr('data-news', news['id']);
        _make.find('div#sm_star_icon').removeClass('sm-yellow-star-icon').addClass('sm-star-icon').attr('data-news', news['id']);
    }
    var important = news['options']['important'];
    if (important == "Important1" || important == "Important2" || important == "Important3") {
        $('i#important_icon').addClass('colorBeautyRed').attr('data-news', news['id']).attr('data-action', news['id']);
    } else {
        $('i#important_icon').attr('data-news', news['id']).attr('data-action', news['id']);
    }
    _make.find('div#important_drop_down').attr('data-action', news['id']);
    _make.find('div.option-news-important-select').attr('data-news', news['id']);
    if (news['options']['important'] != "Important1") {
        $('i#important1_check').attr('data-news', news['id']).css('display', 'none');
    } else {
        $('i#important1_check').attr('data-news', news['id']);
    }
    if (news['options']['important'] != "Important2") {
        $('i#important2_check').attr('data-news', news['id']).css('display', 'none');
    } else {
        $('i#important2_check').attr('data-news', news['id']);
    }
    if (news['options']['important'] != "Important3") {
        $('i#important3_check').attr('data-news', news['id']).css('display', 'none');
    } else {
        $('i#important3_check').attr('data-news', news['id']);
    }
    if (news['options']['read']) {
        _make.find('i#read_unread').addClass('read').attr('data-news', news['id']);
        _make.find('i#read_icon').addClass('colorGreen fa-circle').attr('data-news', news['id']);
    } else {
        _make.find('i#read_unread').addClass('unread').attr('data-news', news['id']);
        _make.find('i#read_icon').addClass('fa-circle-o').attr('data-news', news['id']);
    }
    _make.find('i#site_link').attr('onclick', "window.open('" + show_news_url.replace(/__news__/g, news['id']) + "')");
    if (news['images'].length > 0) {
        var images = '';
        for (var i = 0; i < news['images'].length; i++)
            images += '<div class="col-md-6"><img __src="' + news['images'][i] + '" class="img-responsive"></div>';
        _make.find('div#news_images').html(images);
    } else {
        _make.find('i#image_icon').css('display', 'none');
    }
    if (news['video'] == null || news['video'] == '') {
        _make.find('i#video_icon').css('display', 'none');
    }
    if (news['sound'] == null || news['sound'] == '') {
        _make.find('i#sound_icon').css('display', 'none');
    }
    _make.find('i#base_news_link').attr('onclick', "window.open('" + news['link'] + "')");
    _make.find('i#print_icon').attr('data-news', news['id']);
    _make.find('i#save_icon').attr('data-news', news['id']);
    _make.find('i#report_broken_icon').attr('data-news', news['id']).attr('data-action', news['id']);
    _make.find('div#report_broken_drop_down').attr('data-action', news['id']);
    _make.find('i.news-zoom-in').attr('data-news', news['id']);
    _make.find('i.news-zoom-out').attr('data-news', news['id']);
    _make.find('i#report_broken_btn').attr('data-title', news['title']).attr('data-link', news['link']).attr('data-news', news['id']);
    _make.find('textarea#report_broken_text').attr('data-news', news['id']);
    _make.find('div#scroll_news').attr('data-news', news['id']);
    _make.find('div#summary_news').html(news['summary']);
    _make.find('div#body_news').html(news['body']).css({'font-size': body_news_font['size'] + 'pt', 'font-family': body_news_font['font']});
    _make.find('select#select_content_direction').addClass('new_select').attr('data-news', news['id']);
    _make.find('select#select_content_direction option[value=' + news_content['direction_select'] + ']').attr('selected', 'selected');
    _make.find('select#select_news_group').addClass('new_select').attr('data-news', news['id']);
    _make.find('select#select_news_group option[value=' + news_content['news_group_select'] + ']').attr('selected', 'selected');
    _make.find('select#select_main_source_news').addClass('new_select').attr('data-news', news['id']);
    _make.find('select#select_main_source_news option[value=' + news_content['main_source_news_select'] + ']').attr('selected', 'selected');
    _make.find('select#select_news_maker').addClass('new_select').attr('data-news', news['id']);
    _make.find('select#select_news_maker option[value=' + news_content['news_maker_select'] + ']').attr('selected', 'selected');
    images = '';
    if(news['thumbnail'] != null){
        images += '<img class="news_img new_news_img b-lazy new_news_img float-center" data-src="' + news['thumbnail'] + '" data-action="' + news['id'] + '" src="' + static_url_loading + '" onerror="this.onerror=null;this.src=\'' + static_url_error_image_news + '\';">';
    }
    for (i = 0; i < news['images'].length; i++)
        images += '<img class="news_img new_news_img b-lazy new_news_img float-center" data-src="' + news['images'][i] + '" data-action="' + news['id'] + '" src="' + static_url_loading + '" onerror="this.onerror=null;this.src=\'' + static_url_error_image_news + '\';">';
    _make.find('div#news_images_body').html(images);
    _make.find('div#note_body').attr('data-news', news['id']);
    $('.detail_news_container[data-news=' + news['id'] + ']').html(_make.html()).fadeIn();
    $(".__scrolling").niceScroll({
        cursorcolor: "#000",
        cursorwidth: "5px",
        railalign: "right",
        autohidemode: true,
        horizrailenabled: false
    });
}