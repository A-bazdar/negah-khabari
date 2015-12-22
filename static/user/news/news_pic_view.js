/**
 * Created by Morteza on 12/18/2015.
 */

function make_news_pic_view(news) {
    var _make = $('#make_news_pic_view');
    _make.html($('#news_pic_view').html());
    _make.find('div#news_row').attr('data-news', news['id']);
    _make.find('div#news_img_container').attr('data-action', news['id']);
    if(news['thumbnail'] != null && news['thumbnail'] != ''){
        _make.find('img#thumbnail_news').attr('data-src', news['thumbnail']).attr('data-action', news['id']);
    }else{
        _make.find('img#thumbnail_news').attr('data-src', static_url_error_image_news);
    }
    _make.find('div#abstract_news').attr('data-action', news['id']);
    _make.find('input.news-select').attr('id', news['id']).val(news['id']);
    _make.find('label#label_news_select').attr('for', news['id']);
    _make.find('p#title_news').html(news['title']);
    _make.find('p#summary_news').html(news['summary']);
    _make.find('i#show_news_list_container').attr('data-news', news['id']);
    _make.find('div#option_news_drop_down').attr('data-news', news['id']);
    _make.find('div#note_drop_down').attr('data-action', news['id']);
    _make.find('i#send_note_btn').attr('data-news', news['id']);
    if (news['options']['note'] != false) {
        _make.find('i#note_icon').addClass('colorBlue').attr('data-news', news['id']).attr('data-action', news['id']);
        _make.find('textarea#send_note_text').attr('data-news', news['id']).text(news['options']['note']);
    }else{
        _make.find('i#note_icon').attr('data-news', news['id']).attr('data-action', news['id']);
        _make.find('textarea#send_note_text').attr('data-news', news['id']);
    }
    if (news['options']['star']) {
        _make.find('i#star_icon').addClass('colorOrange fa-star').attr('data-news', news['id']);
    } else {
        _make.find('i#star_icon').addClass('fa-star-o').attr('data-news', news['id']);
    }
    var important = news['options']['important'];
    _make.find('div#important_drop_down').attr('data-action', news['id']);
    if (important == "Important1" || important == "Important2" || important == "Important3") {
        _make.find('i#important_icon').addClass('colorBeautyRed').attr('data-news', news['id']).attr('data-action', news['id']);
    } else {
        _make.find('i#important_icon').attr('data-news', news['id']).attr('data-action', news['id']);
    }
    _make.find('div.option-news-important-select').attr('data-news', news['id']);
    if (news['options']['important'] != "Important1") {
        _make.find('i#important1_check').attr('data-news', news['id']).css('display', 'none');
    } else {
        _make.find('i#important1_check').attr('data-news', news['id']);
    }
    if (news['options']['important'] != "Important2") {
        _make.find('i#important2_check').attr('data-news', news['id']).css('display', 'none');
    } else {
        _make.find('i#important2_check').attr('data-news', news['id']);
    }
    if (news['options']['important'] != "Important3") {
        _make.find('i#important3_check').attr('data-news', news['id']).css('display', 'none');
    } else {
        _make.find('i#important3_check').attr('data-news', news['id']);
    }
    if (news['options']['read']) {
        _make.find('i#read_icon').addClass('colorGreen fa-circle').attr('data-news', news['id']);
    } else {
        _make.find('i#read_icon').addClass('fa-circle-o').attr('data-news', news['id']);
    }
    _make.find('i#site_link').attr('onclick', "window.open('" + show_news_url.replace(/__news__/g, news['id']) + "')");
    if (news['images'].length > 0) {
        var images = '';
        //for (var i = 0; i < news['images'].length; i++)
        //    images += '<div class="col-md-6"><img src="' + news['images'][i] + '" class="img-responsive"></div>';
        _make.find('div#news_images').html(images);
    } else {
        _make.find('i#image_icon').css('display-none');
    }
    if (news['video'] == null || news['video'] == '') {
        _make.find('i#video_icon').css('display', 'none');
    }
    if (news['sound'] == null || news['sound'] == '') {
        _make.find('i#sound_icon').css('display', 'none');
    }
    _make.find('i#base_news_link').attr('onclick', "window.open('" + news['link'] + "')");
    _make.find('i#print_icon').attr('data-news', news['id']);
    _make.find('a#save_icon').attr('download', news["title"] + '.html').attr('href', 'data:text/html;charset=utf-8, ' + news['download']);
    _make.find('i#report_broken_icon').attr('data-news', news['id']).attr('data-action', news['id']);
    _make.find('div#report_broken_drop_down').attr('data-action', news['id']);
    _make.find('i#report_broken_btn').attr('data-title', news['title']).attr('data-link', news['link']).attr('data-news', news['id']);
    _make.find('textarea#report_broken_text').attr('data-news', news['id']);
    $('#show_result_news').append(_make.html());
    $('div.news_row[data-news=' + news['id'] + ']').fadeIn();
}