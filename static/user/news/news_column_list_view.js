/**
 * Created by Morteza on 12/18/2015.
 */

function make_news_column_list_view(news) {
    var _make = $('#make_news_column_list_view');
    _make.html($('#news_column_list_view').html());
    _make.find('div#news_row').attr('data-news', news['id']);
    _make.find('button#agency_info').css('background', news['agency_color']).html(news['agency_name']);
    _make.find('input.news-select').attr('id', news['id']).val(news['id']);
    _make.find('label#label_news_select').attr('for', news['id']);
    _make.find('div#title_news').html(news['title']);
    _make.find('span#date_news').html(news['_date']);
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