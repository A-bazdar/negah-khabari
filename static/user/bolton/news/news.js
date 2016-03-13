/**
 * Created by Morteza on 08/03/2016.
 */

var user_actions = [];

function make_news(item, section){
    var item_obj = $('#MakeBoltonNewsItem');
    item_obj.html($('#BoltonNewsItem').html());
    var dict_select = {
        'data-news': item['id'],
        'data-read': item['read'] ? 'true' : 'false',
        'data-star': item['star'] ? 'true' : 'false',
        'data-note': item['note'] != false ? 'true' : 'false',
        'data-no-important': item['important'] != false ? 'true' : 'false',
        'data-important1': item['important'] == "Important1" ? 'true' : 'false',
        'data-important2': item['important'] == "Important2" ? 'true' : 'false',
        'data-important3': item['important'] == "Important3" ? 'true' : 'false'
    };
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('[data-news]').attr('data-news', item['_id']);
    item_obj.find('#agency_info').css('background', item['agency_color']).html(item['agency_name']);
    item_obj.find('.news-select').attr(dict_select).val(item['_id']);
    item_obj.find('#title_news').html(item['title']);
    item_obj.find('select#select_content_direction').addClass('new_select').attr('data-news', item['_id']).attr('data-section', section);
    item_obj.find('select#select_content_direction option[value=' + item['direction_content'] + ']').attr('selected', 'selected');
    item_obj.find('select#select_news_group').addClass('new_select').attr('data-news', item['_id']).attr('data-section', section);
    item_obj.find('select#select_news_group option[value=' + item['news_group'] + ']').attr('selected', 'selected');
    item_obj.find('select#select_main_source_news').addClass('new_select').attr('data-news', item['_id']).attr('data-section', section);
    item_obj.find('select#select_main_source_news option[value=' + item['main_source_news'] + ']').attr('selected', 'selected');
    item_obj.find('select#select_news_maker').addClass('new_select').attr('data-news', item['_id']).attr('data-section', section);
    item_obj.find('select#select_news_maker option[value=' + item['news_maker'] + ']').attr('selected', 'selected');
    $('#show_result_news').append(item_obj.html());
}

function show_news(section, name, sort, reverse){
    $('.section-tab.active').removeClass('active');
    $('.section-tab[data-section=' + section + ']').addClass('active');
    if(name != false)
        $('#section_name').html(name);
    $('#show_result_news').html('');
    var postData = [
        {name: 'method', value: "ShowSectionNews"},
        {name: 'section', value: section},
        {name: 'sort', value: sort},
        {name: 'reverse', value: reverse},
        {name: '_xsrf', value: xsrf_token}
    ];
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData,
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                var messages = response['messages'];
                if (status) {
                    for(var i = 0; i < value.length ; i++){
                        make_news(value[i], section);
                        $('.change-sort-news').attr('data-section', section);
                        $('select.select-news-content.new_select').select2().removeClass('new_select');
                    }
                }
            }
        });
}

function select_news_content(_type, _news, _section, _value){
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'type', value: _type},
        {name: 'news', value: _news},
        {name: 'section', value: _section},
        {name: 'value', value: _value},
        {name: 'method', value: "SelectNewsContent"}
    ];
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData
        });
}

function delete_news(_news){
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'news', value: _news},
        {name: 'method', value: "DeleteBoltonNews"}
    ];
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData
        });
}

function add_news_to_bolton(_news, _bolton, _section, _method){
    var postData = [
        {name: 'news', value: _news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'bolton', value: _bolton},
        {name: 'section', value: _section},
        {name: 'method', value: _method}
    ];
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData
        });
}

function move_news_to_bolton(_bolton, _section, _news){

    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'bolton', value: _bolton},
        {name: 'section', value: _section},
        {name: 'method', value: "MoveBoltonMultiNews"}
    ].add(_news);

    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData
        });
}

$(document).on('change', 'select.select-news-content', function(e){
    var elm = $(e.target).closest('.select-news-content');
    var _type = elm.attr('data-type');
    var _news = elm.attr('data-news');
    var _section = elm.attr('data-section');
    var _value = elm.select2('val');
    user_actions.push({
        function: 'select_news_content',
        _type: _type,
        _news: _news,
        _section: _section,
        _value: _value
    });
});

$(document).on('click', '.option-bolton-news.delete', function(e){
    Confirm.render(0, 0, 0, 0, 0, function(){
        var elm = $(e.target).closest('.option-bolton-news.delete');
        elm.html(loader.replace(/20/g, '15'));
        var _news = elm.attr('data-news');
        user_actions.push({
            function: 'delete_news',
            _news: _news
        });
        elm.closest('.news_row').remove();
    }, function(){});
});

$(document).on('click', '.option-bolton-news.copy, .option-bolton-news.move', function(e){
    var elm = $(e.target).closest('.option-bolton-news');
    var news = elm.attr('data-news');
    if(elm.hasClass('copy'))
        $('.add-news-to-bolton').attr('data-news', news).attr('data-action', 'copy');
    else
        $('.add-news-to-bolton').attr('data-news', news).attr('data-action', 'move');
    $('#add_to_bolton_modal').modal('toggle');
});

$(document).on('click', '.add-news-to-bolton', function(e){
    var elm = $(e.target).closest('.add-news-to-bolton');
    var btn_html = elm.html();
    elm.html(loader);
    var bolton = elm.attr('data-bolton');
    var section = elm.attr('data-section');
    var news = elm.attr('data-news');
    var method = "MoveBoltonNews";
    if(elm.attr('data-action') == 'copy')
        method = "CopyBoltonNews";

    user_actions.push({
        function: 'add_news_to_bolton',
        _news: news,
        _bolton: bolton,
        _section: section,
        _method: method
    });

    if(method == "MoveBoltonNews")
        $('.news_row[data-news=' + news + ']').remove();
    elm.html(btn_html);
    $('#add_to_bolton_modal').modal('toggle');
});

$(document).on('click', '.move-news-to-bolton', function(e){
    var elm = $(e.target).closest('.move-news-to-bolton');
    var bolton = elm.attr('data-bolton');
    var section = elm.attr('data-section');
    var news = [];
    $.each($('div#show_result_news input[type=checkbox][name=news-select]:checked'), function(){
        news.push({name: "news", value: $(this).val()});
    });
    user_actions.push({
        function: 'move_news_to_bolton',
        _bolton: bolton,
        _section: section,
        _news: news
    });

    $.each($('input[type=checkbox][name=news-select]:checked'), function(){
        $('.news_row[data-news=' + $(this).val() + ']').remove();
    });
});

$(document).on('click','.change-sort-news', function(e){
    var elm = $(e.target).closest('.change-sort-news');
    var sort = elm.attr('data-sort');
    var reverse = elm.attr('data-reverse');
    if(reverse == "True")
        elm.attr('data-reverse', "False");
    else
        elm.attr('data-reverse', "True");

    var section = elm.attr('data-section');
    $('.change-sort-news.active').removeClass('active');
    elm.addClass('active');
    show_news(section, false, sort, reverse);
});

$(document).on('click', '.filter-news-check', function(e){
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

$(document).on('click', '.user-actions-save', function(e){
    var elm = $(e.target).closest('.user-actions-save');
    var elm_html = elm.html();
    elm.html(loader);
    for(var i = 0; i < user_actions.length; i++){
        var action = user_actions[i];
        if(action['function'] == 'select_news_content'){
            select_news_content(action['_type'], action['_news'], action['_section'], action['_value']);
        }else if(action['function'] == 'delete_news'){
            delete_news(action['_news']);
        }else if(action['function'] == 'add_news_to_bolton'){
            add_news_to_bolton(action['_news'], action['_bolton'], action['_section'], action['_method']);
        }else if(action['function'] == 'move_news_to_bolton'){
            move_news_to_bolton(action['_bolton'], action['_section'], action['_news']);
        }
    }
    var bolton_news = [];
    $.each($('.news_list_detail[data-is-show=true]'), function(){
        var news = $(this).attr('data-news');
        var news_container = $('.detail_news_container[data-news=' + news + ']');
        bolton_news.push({
            _id: news,
            ro_title: news_container.find('.ro-title').html(),
            title: news_container.find('.title').html(),
            summary: news_container.find('.summary').html(),
            body: news_container.find('.body').html(),
            image: news_container.find('.image').html(),
            images: news_container.find('.images').html()
        });
    });
    bolton_news = JSON.stringify(bolton_news);
    if(bolton_news.length){
        var postData = [
            {name: '_xsrf', value: xsrf_token},
            {name: 'bolton_news', value: bolton_news},
            {name: 'method', value: "EditBoltonNews"}
        ];
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData
        });
    }
    elm.html(elm_html);

});