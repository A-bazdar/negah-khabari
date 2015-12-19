/**
 * Created by Morteza on 12/18/2015.
 */

function make_news_column_detail_view(news) {
    var _make = $('#make_news_column_detail_view');
    _make.html($('#news_column_detail_view').html());
    _make.find('div#detail_row').attr('data-news', news['id']);
    if(news['thumbnail'] != null && news['thumbnail'] != ''){
        _make.find('img#thumbnail_news').attr('data-src', news['thumbnail']).attr('data-action', news['id']);
    }else{
        _make.find('img#thumbnail_news').attr('data-src', static_url_error_image_news);
    }
    _make.find('div#news_body').html(news['body']);
    $('#show_result_news #detail_first_news').append(_make.html());
    $('div.news_row[data-news=' + news['id'] + ']').fadeIn();
}