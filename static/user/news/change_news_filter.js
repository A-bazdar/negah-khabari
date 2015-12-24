/**
 * Created by Morteza on 12/19/2015.
 */


$('a.grouping[data-toggle=tab]').on('shown.bs.tab', function (e) {
    var _search = get_searches();
    var _show_news = $('#show_result_news');
    var _view = _show_news.attr('data-view');
    var _sort = _show_news.attr('data-sort');
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
});

$(document).on('click', '#pagination .change-page', function (e) {
    var elm = $(e.target).closest('.change-page');
    var _page = elm.attr('data-page');
    var _search = get_searches();
    var _show_news = $('#show_result_news');
    var _view = _show_news.attr('data-view');
    var _sort = _show_news.attr('data-sort');
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(_page, _view, _grouping, _search, _filter, _sort);
});

$(document).on('click', '#news_update_show_time', function (e) {
    update_news();
});

function update_news() {
    var _search = get_searches();
    var _show_news = $('#show_result_news');
    var _view = _show_news.attr('data-view');
    var _sort = _show_news.attr('data-sort');
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
}

$(document).on('click', '.change-view-news', function (e) {
    var elm = $(e.target).closest('.change-view-news');
    $('.change-view-news.active').removeClass('active');
    elm.addClass('active');
    var _view = elm.attr('data-view');
    var _sort = $('#show_result_news').attr('data-sort');
    var _search = get_searches();
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
});


$(document).on('click', '.change-sort-news', function (e) {
    var elm = $(e.target).closest('.change-sort-news');
    var _sort = elm.attr('data-sort');
    var _view = $('#show_result_news').attr('data-view');
    var _search = get_searches();
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
});

$(document).on('change', 'input.all-grouping-checkbox', function () {
    if ($(this).prop('checked')) {
        var _type = $(this).attr('data-type');
        $('input.grouping[name=' + _type + ']').prop('checked', true);
        var _search = get_searches();
        var _show_news = $('#show_result_news');
        var _view = _show_news.attr('data-view');
        var _sort = _show_news.attr('data-sort');
        var _grouping = [];
        var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
        show_result_news(1, _view, _grouping, _search, _filter, _sort);
    } else {
        $('input.subject').prop('checked', false);
    }
});

$(document).on('change', 'input.grouping.grouping-checkbox[type=checkbox]', function () {
    var _search = get_searches();
    var _show_news = $('#show_result_news');
    var _view = _show_news.attr('data-view');
    var _sort = _show_news.attr('data-sort');
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
});

function search_news_header() {
    var _search = get_searches();
    var _show_news = $('#show_result_news');
    var _view = _show_news.attr('data-view');
    var _sort = _show_news.attr('data-sort');
    var _grouping = get_grouping();
    var _filter = $('ul#filter_news_header .filter-news.active').attr('data-filter');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
}

$(document).on('keyup', '#search_news_header_input', function (e) {
    if (e.keyCode == '13') {
        search_type = "exactly_search";
        search_news_header();
    }
});

$(document).on('click', '#search_news_header_btn', function (e) {
    search_type = "exactly_search";
    search_news_header();
});

$(document).on('click', '#search_news_complete_header_btn', function (e) {
    search_type = "expert_search";
    search_news_header();
});

$(document).on('click', '#refinement_news_search', function (e) {
    search_type = "refinement_news";
    search_news_header();
});

$(document).on('click', 'ul#filter_news_header .filter-news', function (e) {
    var elm = $(e.target).closest('.filter-news');
    var _filter = elm.attr('data-filter');
    var _search = get_searches();
    var _show_news = $('#show_result_news');
    var _view = _show_news.attr('data-view');
    var _sort = _show_news.attr('data-sort');
    var _grouping = get_grouping();
    $('ul#filter_news_header .filter-news').removeClass('active');
    $('ul#filter_news_header .filter-news[data-filter=' + _filter + ']').addClass('active');
    show_result_news(1, _view, _grouping, _search, _filter, _sort);
});

function news_update_show_time() {
    var news_update_show_time_title = $('#news_update_show_time_title');
    var minute = news_update_show_time_title.attr('data-minute');
    minute = parseInt(minute) + 1;
    if (minute > 1)
        news_update_show_time_title.html('بروز رسانی : ' + minute + ' دقیقه');
    else
        news_update_show_time_title.html('بروز رسانی : هم اکنون');
    news_update_show_time_title.attr('data-minute', minute);
}

window.setInterval(function () {
    news_update_show_time();
}, 60000);

var _timer;
$(document).on('click', '#start_update_news', function () {
    var _time = $('select#news_update_set_time_change').select2("val");
    var _repeat_update_time = parseInt(_time);
    clearInterval(_timer);
    _timer = window.setInterval(function () {
        update_news()
    }, _repeat_update_time);
    update_news();
    $('#news_update_set_time_start').hide();
    $('#news_update_set_time_pause').show();
    $('#news_update_show_time_title').html('بروز رسانی : هم اکنون').attr('data-minute', 0);

});

$(document).on('click', '#news_update_set_time_pause', function () {
    $('#news_update_set_time_start').show();
    $('#news_update_set_time_pause').hide();
    clearInterval(_timer);
});