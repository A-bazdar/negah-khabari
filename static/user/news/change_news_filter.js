/**
 * Created by Morteza on 12/19/2015.
 */

function show_result_news(_page, _view, _search, _grouping, _sort) {
    $('body').removeClass('loaded');
    var news_type = $('.grouping.type-grouping.active').attr('data-type');
    var _data = [
        {name: "_xsrf", value: xsrf_token},
        {name: "_page", value: _page},
        {name: "_view", value: _view},
        {name: "_type", value: __type['type']},
        {name: "_action", value: __type['action']},
        {name: "_news_type", value: news_type},
        {name: "_sort", value: _sort}
    ];
    _data = $.merge(_data, _grouping);
    _data = $.merge(_data, _search);
    $.ajax({
        url: '',
        type: 'post',
        data: _data,
        success: function (response) {
            var status = response['status'];
            var messages = response['messages'];
            var value = response['value'];
            if (status) {
                set_news(value['news'], _view, value['font']['font'], value['size']);
                load_news();
                $('#pagination').html(value['pagination']);
                $('#nav_search').find('.expert-search-btn').slideUp().removeClass('open').addClass('close');
                $('button.c-menu__close').click();
                $('body').addClass('loaded');
                $('h1').css('color', '#222222');
                $('#news_update_show_time').attr('data-minute', "0");
                $('#news_update_show_time tooltip section b').html('بروز رسانی : هم اکنون');
            }
        }
    });
}

function get_news() {
    var _search = get_searches();
    var _view = $(".change-view-news.active").attr('data-view');
    var _sort = $(".change-sort-news.active").attr('data-sort');
    show_result_news(1, _view, _search, [], _sort);
}

var __type = {type: "ALL", action: "ALL"};

$(document).on('keyup', '#search_news_header_input', function (e) {
    if (e.keyCode == '13') {
        __type["type"] = "EXACTLY";
        __type["action"] = "SEARCH";
        get_news();
    }
});

$(document).on('click', '#search_news_header_btn', function (e) {
    __type["type"] = "EXACTLY";
    __type["action"] = "SEARCH";
    get_news();
});

$(document).on('click', '#refinement_news_search', function (e) {
    __type["type"] = "REFINEMENT";
    __type["action"] = "SEARCH";
    get_news();
});

$(document).on('click', '#search_news_complete_header_btn', function (e) {
    __type["type"] = "EXPERT";
    __type["action"] = "SEARCH";
    get_news();
});

$(document).on('change', 'input.grouping.grouping-checkbox[type=checkbox]', function () {
    __type['type'] = $('.sidebar-items.grouping.active').attr('data-grouping');
    __type['action'] = "GROUPING";
    var _view = $(".change-view-news.active").attr('data-view');
    var _sort = $(".change-sort-news.active").attr('data-sort');
    var _grouping = get_grouping();
    show_result_news(1, _view, [], _grouping, _sort);
});

$('a.grouping[data-toggle=tab]').on('shown.bs.tab', function (e) {
    __type['type'] = $('.sidebar-items.grouping.active').attr('data-grouping');
    __type['action'] = "GROUPING";
    var _view = $(".change-view-news.active").attr('data-view');
    var _sort = $(".change-sort-news.active").attr('data-sort');
    var _grouping = get_grouping();
    show_result_news(1, _view, [], _grouping, _sort);
});

$(document).on('change', 'input.all-grouping-checkbox', function () {
    if ($(this).prop('checked')) {
        __type["type"] = "ALL";
        __type["action"] = "ALL";
        var _type = $(this).attr('data-type');
        $('input.grouping[name=' + _type + ']').prop('checked', true);
        var _view = $(".change-view-news.active").attr('data-view');
        var _sort = $(".change-sort-news.active").attr('data-sort');
        show_result_news(1, _view, [], [], _sort);
    } else {
        $('input.subject').prop('checked', false);
    }
});

$(document).on('click', '#pagination .change-page', function (e) {
    var elm = $(e.target).closest('.change-page');
    var _page = elm.attr('data-page');
    var _search = get_searches();
    var _view = $(".change-view-news.active").attr('data-view');
    var _sort = $(".change-sort-news.active").attr('data-sort');
    var _grouping = get_grouping();
    show_result_news(_page, _view, _search, _grouping, _sort);
});

function update_news() {
    __type["type"] = "ALL";
    __type["action"] = "ALL";
    var _view = $(".change-view-news.active").attr('data-view');
    var _sort = $(".change-sort-news.active").attr('data-sort');
    show_result_news(1, _view, [], [], _sort);
}

$(document).on('click', '#news_update_show_time', function (e) {
    update_news();
});

$(document).on('click', '.change-view-news', function (e) {
    var elm = $(e.target).closest('.change-view-news');
    $('.change-view-news.active').removeClass('active');
    elm.addClass('active');
    var _view = elm.attr('data-view');
    var _page = $('.pagination-container .change-page.active').attr('data-page');
    var _sort = $(".change-sort-news.active").attr('data-sort');
    var _search = get_searches();
    var _grouping = get_grouping();
    show_result_news(_page, _view, _search, _grouping, _sort);
});

$(document).on('click', '.change-sort-news', function (e) {
    var elm = $(e.target).closest('.change-sort-news');
    var _sort = elm.attr('data-sort');
    $('.change-sort-news.active').removeClass('active');
    elm.addClass('active');
    var _view = $(".change-view-news.active").attr('data-view');
    var _search = get_searches();
    var _grouping = get_grouping();
    show_result_news(1, _view, _search, _grouping, _sort);
});

function get_grouping() {
    if(__type['action'] == "GROUPING"){
        var _all = true;
        var _nothing = true;
        $.each($('input[type=checkbox][name=' + __type['type'] + ']'), function () {
            if (!$(this).prop('checked')) {
                _all = false;
            } else {
                _nothing = false;
            }
        });
        if (_nothing)
            return [];
        var _grouping = [];
        if (__type['type'] == 'subject') {
            _grouping = $("#form_grouping_news_subject").serializeArray();
        } else if (__type['type'] == 'agency') {
            _grouping = $("#form_grouping_news_agency").serializeArray();
        } else if (__type['type'] == 'keyword') {
            _grouping = $("#form_grouping_news_keyword").serializeArray();
        } else if (__type['type'] == 'group') {
            _grouping = $("#form_grouping_news_group").serializeArray();
        } else if (__type['type'] == 'geographic') {
            _grouping = $("#form_grouping_news_geographic").serializeArray();
        } else if (__type['type'] == 'direction') {
            _grouping = $("#form_grouping_news_direction").serializeArray();
        }
        $('input.all-subjects[type=checkbox]').prop('checked', _all);
        if (_all) {
            _grouping = []
        }
    }
    return _grouping
}

function get_searches() {
    var searches = [];
    if(__type["action"] == "SEARCH"){
        if (__type["type"] == "EXPERT") {
            searches = $("#header_search_news").serializeArray();
        } else if (__type["type"] == "EXACTLY") {
            var search_news_header_input = $("#search_news_header_input").val();
            searches = [{name: "exactly-word", value: search_news_header_input}, {
                name: "type-search",
                value: 'exactly_search'
            }]
        } else if (__type["type"] == "REFINEMENT") {
            searches = $("#refinement_news").serializeArray();
        }
    }
    return searches
}

$(document).on('click', 'ul#filter_news_header .filter-news-check', function(e){
    var elm = $(e.target).closest('.filter-news-check');
    if(elm.attr('data-filter') == 'all'){
        $('input[type=checkbox][name=news-select]').prop('checked', true);
    }else if(elm.attr('data-filter') == 'no-one'){
        $('input[type=checkbox][name=news-select]').prop('checked', false);
    }else{
        var filter = elm.attr('data-filter');
        var val = elm.attr('data-val');
        $('input[type=checkbox][name=news-select]').prop('checked', false);
        $('input[type=checkbox][name=news-select][data-' + filter + '=' + val + ']').prop('checked', true);
    }
});

var update_time = 0;
var start = false;
var _repeat_update_time = 0;
function news_update_show_time() {
    update_time += 60000;
    if(start && _repeat_update_time == update_time){
        update_news();
        update_time = 0;
    }else{
        var news_update_show_time = $('#news_update_show_time');
        var minute = news_update_show_time.attr('data-minute');
        minute = parseInt(minute) + 1;
        if (minute > 1)
            $('#news_update_show_time tooltip section b').html('بروز رسانی : ' + minute + ' دقیقه');
        else
            $('#news_update_show_time tooltip section b').html('بروز رسانی : هم اکنون');
        news_update_show_time.attr('data-minute', minute);
    }
}

var _timer_2;
_timer_2 = window.setInterval(function () {
    news_update_show_time();
}, 60000);

$(document).on('click', '#start_update_news', function () {
    clearInterval(_timer_2);
    var _time = $('select#news_update_set_time_change').select2("val");
    _repeat_update_time = parseInt(_time);
    start = true;
    update_time = 0;
    update_news();
    _timer_2 = window.setInterval(function () {
        news_update_show_time();
    }, 60000);
    $('#news_update_set_time_start').hide();
    $('#news_update_set_time_pause').show();
});

$(document).on('click', '#news_update_set_time_pause', function () {
    $('#news_update_set_time_start').show();
    $('#news_update_set_time_pause').hide();
    start = false;
});