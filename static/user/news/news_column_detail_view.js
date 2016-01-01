/**
 * Created by Morteza on 12/18/2015.
 */

function make_news_column_detail_view(news) {
    var _make = $('#make_news_column_detail_view');
    _make.html($('#news_column_detail_view').html());
    var dict_select = {
        'data-news': news['id'],
        'data-read': 'false',
        'data-star': 'false',
        'data-note': 'false',
        'data-no-important': 'false',
        'data-important1': 'false',
        'data-important2': 'false',
        'data-important3': 'false'
    };
    if (news['options']['read']) {
        dict_select['data-read'] = 'true';
    }
    if (news['options']['note'] != false) {
        dict_select['data-note'] = 'true'
    }
    if (news['options']['star']) {
        dict_select['data-star'] = 'true'
    }
    if (news['options']['important'] == "Important1") {
        dict_select['data-important1'] = 'true';
        dict_select['data-no-important'] = 'true'
    }
    if (news['options']['important'] == "Important2") {
        dict_select['data-important2'] = 'true';
        dict_select['data-no-important'] = 'true'
    }
    if (news['options']['important'] == "Important3") {
        dict_select['data-important3'] = 'true';
        dict_select['data-no-important'] = 'true'
    }
    _make.find('div#detail_row').attr('data-news', news['id']);
    if(news['thumbnail'] != null && news['thumbnail'] != ''){
        _make.find('img#thumbnail_news').attr('data-src', news['thumbnail']).attr('data-action', news['id']);
    }else{
        _make.find('img#thumbnail_news').attr('data-src', static_url_error_image_news);
    }
    _make.find('div#news_body').html(news['body']);
    _make.find('input.news-select').attr('id', news['id']).val(news['id']).attr(dict_select);
    $('#show_result_news #detail_first_news').html(_make.html());
    $('div.news_row[data-news=' + news['id'] + ']').fadeIn();
}