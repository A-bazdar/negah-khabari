/**
 * Created by Morteza on 12/19/2015.
 */

function get_grouping() {
    var grouping_type = $('#news_grouping_type').attr('data-type');
    var _all = true;
    var _nothing = true;
    $.each($('input[type=checkbox][name=' + grouping_type + ']'), function () {
        if (!$(this).prop('checked')) {
            _all = false;
        } else {
            _nothing = false;
        }
    });
    if (_nothing)
        return [];
    var _grouping = [];
    if (grouping_type == 'subject') {
        _grouping = $("#form_grouping_news_subject").serializeArray();
    } else if (grouping_type == 'agency') {
        _grouping = $("#form_grouping_news_agency").serializeArray();
    } else if (grouping_type == 'keyword') {
        _grouping = $("#form_grouping_news_keyword").serializeArray();
    } else if (grouping_type == 'group') {
        _grouping = $("#form_grouping_news_group").serializeArray();
    } else if (grouping_type == 'geographic') {
        _grouping = $("#form_grouping_news_geographic").serializeArray();
    } else if (grouping_type == 'direction') {
        _grouping = $("#form_grouping_news_direction").serializeArray();
    }
    $('input.all-subjects[type=checkbox]').prop('checked', _all);
    if (_all) {
        _grouping = []
    }
    return _grouping
}

function get_searches() {
    var searches = [];
    if (search_type == "expert_search") {
        searches = $("#header_search_news").serializeArray();
    } else if (search_type == "exactly_search") {
        var search_news_header_input = $("#search_news_header_input").val();
        searches = [{name: "exactly-word", value: search_news_header_input}, {
            name: "type-search",
            value: 'exactly_search'
        }]
    } else if (search_type == "refinement_news") {
        searches = $("#refinement_news").serializeArray();
    } else {
        searches = [{name: "type-search", value: 'no_search'}]
    }
    return searches
}

function show_result_news(_page, _view, _grouping, _search, _sort) {
    $('body').removeClass('loaded');
    var news_type = $('.grouping.type-grouping.active').attr('data-type');
    var grouping_type = $('#news_grouping_type').attr('data-type');
    var _data = [
        {name: "_xsrf", value: xsrf_token},
        {name: "_page", value: _page},
        {name: "_view", value: _view},
        {name: "_news_type", value: news_type},
        {name: "_grouping_type", value: grouping_type},
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