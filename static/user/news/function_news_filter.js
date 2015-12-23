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

function show_result_news(_page, _view, _grouping, _search, _filter, _sort) {
    $('body').removeClass('loaded');
    var news_type = $('.grouping.type-grouping.active').attr('data-type');
    var grouping_type = $('#news_grouping_type').attr('data-type');
    var _data = [
        {name: "_xsrf", value: xsrf_token},
        {name: "_page", value: _page},
        {name: "_view", value: _view},
        {name: "_news_type", value: news_type},
        {name: "_grouping_type", value: grouping_type},
        {name: "_sort", value: _sort},
        {name: "_filter", value: _filter}
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
                var _show_result_news = $('#show_result_news');
                _show_result_news.html("").attr('data-view', _view);
                var j = 0;
                if(_view == "list_view"){
                    for(j = 0; j < value['news'].length; j++){
                        make_news_list_view(value['news'][j]);
                    }
                }else if(_view == "column_list_view"){
                    var html = '<div id="news_list" class="col-md-6 col-sm-6 __scrolling" style="max-height: 500px"></div><div id="detail_first_news" class="col-md-6 col-sm-6 show-detail-main-con"></div>';
                    _show_result_news.html(html);
                    for(j = 0; j < value['news'].length; j++){
                        make_news_column_list_view(value['news'][j]);
                        if(j == 0)
                            make_news_column_detail_view(value['news'][j]);
                    }
                }else if(_view == "details_view"){
                    for(j = 0; j < value['news'].length; j++){
                        make_news_detail_view(value['news'][j]);
                    }
                }else if(_view == "details_pic_view"){
                    for(j = 0; j < value['news'].length; j++){
                        make_news_detail_pic_view(value['news'][j]);
                    }
                }else if(_view == "pic_view"){
                    for(j = 0; j < value['news'].length; j++){
                        make_news_pic_view(value['news'][j]);
                    }
                }
                $('#pagination').html(value['pagination']);
                $('#nav_search').find('.expert-search-btn').slideUp().removeClass('open').addClass('close');
                $('button.c-menu__close').click();
                load_news();
                $('body').addClass('loaded');
                $('h1').css('color', '#222222');
            }
        }
    });
}