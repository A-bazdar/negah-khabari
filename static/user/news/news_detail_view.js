/**
 * Created by Morteza on 12/18/2015.
 */

function make_news_detail_view(news) {
    var _make = $('#make_news_detail_view');
    _make.html($('#news_detail_view').html());
    _make.find('div#news_row').attr('data-news', news['id']);
    _make.find('input.news-select').attr('id', news['id']).val(news['id']);
    _make.find('label#label_news_select').attr('for', news['id']);
    _make.find('div#title_news').html(news['title']);
    _make.find('div#summary_news').html(news['summary']);
    _make.find('span#date_news').html(news['_date']);
    _make.find('button#agency_info').css('background', news['agency_color']).html(news['agency_name']);
    $('#show_result_news').append(_make.html());
    $('div.news_row[data-news=' + news['id'] + ']').fadeIn();
}