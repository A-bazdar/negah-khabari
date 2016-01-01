/**
 * Created by Morteza on 12/18/2015.
 */

function make_news_column_list_view(news, font, size) {
    var _make = $('#make_news_column_list_view');
    _make.html($('#news_column_list_view').html());
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
    _make.find('div#news_row').attr('data-news', news['id']);
    _make.find('button#agency_info').css('background', news['agency_color']).html(news['agency_name']);
    _make.find('label#label_news_select').attr('for', news['id']);
    _make.find('div#title_news').html(news['title']).css({'font-size': size + 'pt', 'font-family': font});
    _make.find('span#date_news').html(news['_date']);
    _make.find('input.news-select').attr('id', news['id']).val(news['id']).attr(dict_select);
    $('#show_result_news #news_list').append(_make.html());
    $('div.news_row[data-news=' + news['id'] + ']').fadeIn();
    $(".__scrolling").niceScroll({
        cursorcolor: "#000",
        cursorwidth: "5px",
        railalign: "left",
        autohidemode: true,
        horizrailenabled: false
    });
}