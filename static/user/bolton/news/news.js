/**
 * Created by Morteza on 08/03/2016.
 */

function make_news(item, section){
    var item_obj = $('#MakeBoltonNewsItem');
    item_obj.html($('#BoltonNewsItem').html());
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('[data-news]').attr('data-news', item['_id']);
    item_obj.find('#agency_info').css('background', item['agency_color']).html(item['agency_name']);
    item_obj.find('.news-select').attr('id', item['_id']);
    item_obj.find('#label_news_select').attr('for', item['_id']);
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

function show_news(section, name){
    $('.section-tab.active').removeClass('active');
    $('.section-tab[data-section=' + section + ']').addClass('active');
    $('#section_name').html(name);
    $('#show_result_news').html('');
    var postData = [
        {name: 'method', value: "ShowSectionNews"},
        {name: 'section', value: section},
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
                        $('select.select-news-content.new_select').select2().removeClass('new_select');
                    }
                }
            }
        });
}

$(document).on('change', 'select.select-news-content', function(e){
    var elm = $(e.target).closest('.select-news-content');
    var _type = elm.attr('data-type');
    var _news = elm.attr('data-news');
    var _section = elm.attr('data-section');
    var _value = elm.select2('val');
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
});

$(document).on('click', '.option-bolton-news.delete', function(e){
    Confirm.render(0, 0, 0, 0, 0, function(){
        var elm = $(e.target).closest('.option-bolton-news.delete');
        var elm_html = elm.html();
        elm.html(loader.replace(/20/g, '15'));
        var _news = elm.attr('data-news');
        var postData = [
            {name: '_xsrf', value: xsrf_token},
            {name: 'news', value: _news},
            {name: 'method', value: "DeleteBoltonNews"}
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
                        elm.closest('.news_row').remove();
                    }
                    elm.html(elm_html);
                }
            });
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
    var postData = [
        {name: 'news', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'bolton', value: bolton},
        {name: 'section', value: section},
        {name: 'method', value: method}
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
                    if(method == "MoveBoltonNews")
                        $('.news_row[data-news=' + news + ']').remove();
                }
                elm.html(btn_html);
                $('#add_to_bolton_modal').modal('toggle');
            }
        });
});

$(document).on('click', '.option-bolton-news.delete', function(e){
    Confirm.render(0, 0, 0, 0, 0, function(){
        var elm = $(e.target).closest('.option-bolton-news.delete');
        var elm_html = elm.html();
        elm.html(loader.replace(/20/g, '15'));
        var _news = elm.attr('data-news');
        var postData = [
            {name: '_xsrf', value: xsrf_token},
            {name: 'news', value: _news},
            {name: 'method', value: "DeleteBoltonNews"}
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
                        elm.closest('.news_row').remove();
                    }
                    elm.html(elm_html);
                }
            });
    }, function(){});
});