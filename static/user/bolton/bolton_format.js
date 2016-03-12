/**
 * Created by Morteza on 3/1/2016.
 */


var highlight_phrases = [];
function empty_form_bolton_format(){
    var _form = $('form#BoltonFormat');
    _form.find('input[name=method]').val("AddBoltonFormat");
    _form.find('input[name=_id]').val('');
    _form.find('input[name=name]').val('');
    _form.find('input[name=show_summary][value=in_list]').prop('checked', true);
    _form.find('input[name=page_breake][value=after_group]').prop('checked', true);
    _form.find('input[type=checkbox]').val('');
    _form.find('input[name=title_1]').val('');
    _form.find('input[name=title_2]').val('');
    _form.find('input[name=title_3]').val('');
    _form.find('input[name=title_4]').val('');
    $('.fileupload-exists.remove-logo-btn').click();
    highlight_phrases = [];
    $('div.highlight_phrases').html('');
}

function make_bolton_format(item, type){
    var item_obj = $('#MakeBoltonFormatItem');
    item_obj.html($('#BoltonFormatItem').html());
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('[data-name]').attr('data-name', item['name']);
    item_obj.find('.bolton-format-name').html(item['name']);
    if(item['active']){
        item_obj.find('.bolton-format-active').addClass('red-turn-off-icon').attr('data-action', 'deactive');
    }else{
        item_obj.find('.bolton-type-active').addClass('green-turn-off-icon').attr('data-action', 'active');
    }
    if(type == "append")
        $('.bolton-format-list').append(item_obj.html());
    else
        $('.bolton-format-list').prepend(item_obj.html());
}
$(document).on('click', '.delete_highlight_phrase', function(e){
    $(e.target).closest('.highlight_phrase').remove();
    var temp_highlight_phrases = [];
    for(var i = 0; i < highlight_phrases.length; i++){
        if(highlight_phrases[i]['phrase'] != $(this).closest('.highlight_phrase').find('.phrase').html()){
            temp_highlight_phrases.push(highlight_phrases[i])
        }
    }
    highlight_phrases = temp_highlight_phrases;
});

$(document).on('click', '.add_highlight_phrase', function(e){
    var highlight_phrase = $('input[name=highlight_phrase]');
    var phrase = highlight_phrase.val();
    var color = $('input[name=highlight_phrase_color]').val();
    highlight_phrases.push({
        phrase: phrase,
        color: color
    });
    $('div.highlight_phrases').append('<div style="background-color: ' + color + '" class="highlight_phrase col-xs-2 text-center">\
                <div class="row">\
                    <div class="col-xs-3 cursor-pointer delete_highlight_phrase" style="border-left: 1px solid #000000"><i class="fa fa-times"></i></div>\
                    <div class="col-xs-9 phrase">' + phrase + '</div>\
                </div>\
            </div>');
    highlight_phrase.val("");
});

var __error = false;
var __message = false;
function check_value(__val, __msg){
    if((__val == "" || __val == " ") && !__error){
        __error = true;
        __message = __msg;
    }
    return __val
}

$(document).on('submit', '#BoltonFormat', function(e){
    e.preventDefault();
    var btn =$('.add-bolton-form-btn') ;
    btn.html(loader);
    var data = new FormData();
    var _form = $('form#BoltonFormat');
    data.append('method', _form.find('input[name=method]').val());
    data.append('_id', _form.find('input[name=_id]').val());
    data.append('_xsrf', xsrf_token);
    data.append('name', check_value(_form.find('input[name=name]').val(), 'نام را وارد کنید.'));
    data.append('show_summary',  _form.find('input[name=show_summary]:checked').val());
    data.append('page_breake', _form.find('input[name=page_breake]:checked').val());
    data.append('note', _form.find('input[name=note]').prop('checked') ? 'true' : 'false');
    data.append('subject', _form.find('input[name=subject]').prop('checked') ? 'true' : 'false');
    data.append('direction', _form.find('input[name=direction]').prop('checked') ? 'true' : 'false');
    data.append('thumbnail', _form.find('input[name=thumbnail]').prop('checked') ? 'true' : 'false');

    var word_image = 'false';
    var word_image_size = 'false';
    if(_form.find('input[name=word_image]').prop('checked')){
        word_image = 'true';
        word_image_size = _form.find('select[name=word_image_size]').select2('val')
    }
    data.append('word_image', word_image);
    data.append('word_image_size', word_image_size);

    var html_image = 'false';
    var html_image_size = 'false';
    if(_form.find('input[name=html_image]').prop('checked')){
        html_image = 'true';
        html_image_size = _form.find('select[name=html_image_size]').select2('val')
    }
    data.append('html_image', html_image);
    data.append('html_image_size', html_image_size);

    var mobile_image = 'false';
    var mobile_image_size = 'false';
    if(_form.find('input[name=mobile_image]').prop('checked')){
        mobile_image = 'true';
        mobile_image_size = _form.find('select[name=mobile_image_size]').select2('val')
    }
    data.append('mobile_image', mobile_image);
    data.append('mobile_image_size', mobile_image_size);

    var rss_image = 'false';
    var rss_image_size = 'false';
    if(_form.find('input[name=rss_image]').prop('checked')){
        rss_image = 'true';
        rss_image_size = _form.find('select[name=rss_image_size]').select2('val')
    }
    data.append('rss_image', rss_image);
    data.append('rss_image_size', rss_image_size);
    data.append('highlight_phrases', JSON.stringify(highlight_phrases));

    data.append('logo', _form.find('input[type=file][name=logo]')[0].files[0]);
    data.append('format_cover', _form.find('select[name=format_cover]').select2('val'));
    data.append('format_pages', _form.find('select[name=format_pages]').select2('val'));
    data.append('title_1', check_value(_form.find('input[name=title_1]').val(), 'تیتر 1 را وارد کنید.'));
    data.append('title_2', check_value(_form.find('input[name=title_2]').val(), 'تیتر 2 را وارد کنید.'));
    data.append('title_3', check_value(_form.find('input[name=title_3]').val(), 'تیتر 3 را وارد کنید.'));
    data.append('title_4', check_value(_form.find('input[name=title_4]').val(), 'تیتر 4 را وارد کنید.'));
    data.append('place_insert_tables', _form.find('select[name=place_insert_tables]').select2("val"));
    data.append('place_insert_charts', _form.find('select[name=place_insert_charts]').select2("val"));

    data.append('content_format', _form.find('input[name=content_format]').prop('checked') ? 'true' : 'false');
    data.append('importance_news', _form.find('input[name=importance_news]').prop('checked') ? 'true' : 'false');
    data.append('performance_agency_number_news', _form.find('input[name=performance_agency_number_news]').prop('checked') ? 'true' : 'false');
    data.append('general_statistics_agency', _form.find('input[name=general_statistics_agency]').prop('checked') ? 'true' : 'false');
    data.append('daily_statistics_news', _form.find('input[name=daily_statistics_news]').prop('checked') ? 'true' : 'false');
    data.append('important_topic_news', _form.find('input[name=important_topic_news]').prop('checked') ? 'true' : 'false');
    data.append('important_keyword_news', _form.find('input[name=important_keyword_news]').prop('checked') ? 'true' : 'false');
    data.append('reflecting_news', _form.find('input[name=reflecting_news]').prop('checked') ? 'true' : 'false');
    data.append('importance_news_media_placement', _form.find('input[name=importance_news_media_placement]').prop('checked') ? 'true' : 'false');
    data.append('content_direction', _form.find('input[name=content_direction]').prop('checked') ? 'true' : 'false');
    data.append('agency_direction', _form.find('input[name=agency_direction]').prop('checked') ? 'true' : 'false');
    data.append('important_news_maker', _form.find('input[name=important_news_maker]').prop('checked') ? 'true' : 'false');
    data.append('main_sources_news_1', _form.find('input[name=main_sources_news_1]').prop('checked') ? 'true' : 'false');
    data.append('main_sources_news_2', _form.find('input[name=main_sources_news_2]').prop('checked') ? 'true' : 'false');

    if(__error){
        Alert.render(__message, function(){
            btn.html('ثبت');
            __error = false;
        });
        __error = false;
        return;
    }
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            async: true,
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                var messages = response['messages'];
                if (status) {
                    if(_form.find('input[name=method]').val() == "AddBoltonFormat"){
                        make_bolton_format(value, "prepend");
                        __bolton_formats.push(value);
                    }else{
                        var obj = $('.bolton_list_items[data-id=' + _form.find('input[name=_id]').val() + ']');
                        obj.find('.bolton-format-name').html(value['name']);
                        for(i = 0; i < __bolton_formats.length ; i++) {
                            if (__bolton_formats[i]['_id'] == _form.find('input[name=_id]').val()) {
                                value['_id'] = _form.find('input[name=_id]').val();
                                __bolton_formats[i] = value;
                            }
                        }
                    }
                        btn.html('ثبت');
                }else{
                    var error = '';
                    for(var i = 0; i < messages.length ; i++){
                        error += messages[i] + '<br>';
                    }
                    if(error == '')
                        error = 'error';
                    Alert.render(error, function(){
                        btn.html('ثبت');
                    });
                }
            },
            error: function () {
                Alert.render('error', function(){
                    btn.html('ثبت');
                });
            }
        });
});

$(document).on('click', ".bolton-format-edit", function(e){
    var elm = $(e.target).closest('.bolton-format-edit');
    var _id = elm.attr('data-id');
    for(var i = 0; i < __bolton_formats.length ; i++) {
        var _b = __bolton_formats[i];
        if(_b['_id'] == _id){
            var _form = $('form#BoltonFormat');
            _form.find('input[name=method]').val("EditBoltonFormat");
            _form.find('input[name=_id]').val(_id);
            _form.find('input[name=name]').val(_b['name']);
            _form.find('img.logo-image-format').attr('src', static_url_images_format + _b['logo']);
            _form.find('input[name=show_summary][value=' + _b['show_summary'] + ']').prop('checked', true);
            _form.find('input[name=page_breake][value=' + _b['page_breake'] + ']').prop('checked', true);
            _form.find('input[name=note]').prop('checked', _b['note'] ? true : false);
            _form.find('input[name=subject]').prop('checked', _b['subject'] ? true : false);
            _form.find('input[name=direction]').prop('checked', _b['direction'] ? true : false);
            _form.find('input[name=thumbnail]').prop('checked', _b['thumbnail'] ? true : false);
            _form.find('input[name=word_image]').prop('checked', _b['word_image'] ? true : false);
            _form.find('select[name=word_image_size]').select2('val', _b['word_image_size'] ? _b['word_image_size'] : 'small');
            _form.find('input[name=html_image]').prop('checked', _b['html_image'] ? true : false);
            _form.find('select[name=html_image_size]').select2('val', _b['html_image_size'] ? _b['html_image_size'] : 'small');
            _form.find('input[name=mobile_image]').prop('checked', _b['mobile_image'] ? true : false);
            _form.find('select[name=mobile_image_size]').select2('val', _b['mobile_image_size'] ? _b['mobile_image_size'] : 'small');
            _form.find('input[name=rss_image]').prop('checked', _b['rss_image'] ? true : false);
            _form.find('select[name=rss_image_size]').select2('val', _b['rss_image_size'] ? _b['rss_image_size'] : 'small');
            var highlight_phrases_html = '';
            for(var j = 0 ; j < _b['highlight_phrases'].length ; j++){
                highlight_phrases_html += '<div style="background-color: ' + _b['highlight_phrases'][j]['color'] + '" class="highlight_phrase col-xs-2 text-center">\
                    <div class="row">\
                        <div class="col-xs-3 cursor-pointer delete_highlight_phrase" style="border-left: 1px solid #000000"><i class="fa fa-times"></i></div>\
                        <div class="col-xs-9 phrase">' + _b['highlight_phrases'][j]['phrase'] + '</div>\
                    </div>\
                </div>';
            }
            _form.find('.highlight_phrases').html(highlight_phrases_html);
            _form.find('select[name=format_cover]').select2('val', _b['format_cover']);
            _form.find('select[name=format_pages]').select2('val', _b['format_pages']);
            _form.find('input[name=title_1]').val(_b['title_1']);
            _form.find('input[name=title_2]').val(_b['title_2']);
            _form.find('input[name=title_3]').val(_b['title_3']);
            _form.find('input[name=title_4]').val(_b['title_4']);
            _form.find('select[name=place_insert_tables]').select2('val', _b['place_insert_tables']);
            _form.find('select[name=place_insert_charts]').select2('val', _b['place_insert_charts']);
            _form.find('input[name=content_format]').prop('checked', _b['content_format'] ? true : false);
            _form.find('input[name=importance_news]').prop('checked', _b['importance_news'] ? true : false);
            _form.find('input[name=performance_agency_number_news]').prop('checked', _b['performance_agency_number_news'] ? true : false);
            _form.find('input[name=general_statistics_agency]').prop('checked', _b['general_statistics_agency'] ? true : false);
            _form.find('input[name=daily_statistics_news]').prop('checked', _b['daily_statistics_news'] ? true : false);
            _form.find('input[name=important_topic_news]').prop('checked', _b['important_topic_news'] ? true : false);
            _form.find('input[name=important_keyword_news]').prop('checked', _b['important_keyword_news'] ? true : false);
            _form.find('input[name=reflecting_news]').prop('checked', _b['reflecting_news'] ? true : false);
            _form.find('input[name=importance_news_media_placement]').prop('checked', _b['importance_news_media_placement'] ? true : false);
            _form.find('input[name=content_direction]').prop('checked', _b['content_direction'] ? true : false);
            _form.find('input[name=agency_direction]').prop('checked', _b['agency_direction'] ? true : false);
            _form.find('input[name=important_news_maker]').prop('checked', _b['important_news_maker'] ? true : false);
            _form.find('input[name=main_sources_news_1]').prop('checked', _b['main_sources_news_1'] ? true : false);
            _form.find('input[name=main_sources_news_2]').prop('checked', _b['main_sources_news_2'] ? true : false);
        }
    }
    $('.add-bolton-btn i').removeClass('fa-caret-down').addClass('fa-caret-up');
    $('.add-bolton-btn').removeClass('closebox').addClass('open');
    $('.add_bolton_form_con[data-id=5]').slideDown();
});

$(document).on('click', ".bolton-format-active", function(e){
    var elm = $(e.target).closest('.bolton-format-active');
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: elm.attr('data-action')},
        {name: 'method', value: "ActiveBoltonFormat"},
        {name: '_id', value: elm.attr('data-id')}
    ];
    var btn = $('.bolton-format-btn');
    jQuery.ajax(
        {
            url: '',
            type: "post",
            data: postData,
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                var messages = response['messages'];
                if (!status) {
                    var error = '';
                    for(var i = 0; i < messages.length ; i++){
                        error += messages[i] + '<br>';
                    }
                    if(error == '')
                        error = 'error';
                    Alert.render(error, function(){
                        btn.html('ثبت');
                    });
                }else{
                    if(elm.attr('data-action') == 'active'){
                        elm.addClass('red-turn-off-icon').removeClass('green-turn-off-icon').attr('data-action', 'deactive');
                    }else{
                        elm.addClass('green-turn-off-icon').removeClass('red-turn-off-icon').attr('data-action', 'active');
                    }
                }
            },
            error: function () {
                Alert.render('error', function(){
                    btn.html('ثبت');
                });
            }
        });
});

$(document).on('click', '.bolton-format-delete', function(e){
    Confirm.render(0, 0, 0, 0, 0, function(){
        var elm = $(e.target).closest('.bolton-format-delete');
        var _id = elm.attr('data-id');
        elm.html(loader.replace(/20/g, '15'));
        var postData = [
            {name: '_id', value: _id},
            {name: '_xsrf', value: xsrf_token},
            {name: 'method', value: 'DeleteBoltonFormat'}
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
                        Alert.render('success', function () {
                            elm.closest('.bolton_list_items').remove();
                        });
                    }else{
                        var error = '';
                        for(var i = 0; i < messages.length ; i++){
                            error += messages[i] + '<br>';
                        }
                        if(error == '')
                            error = 'error';
                        Alert.render(error, function(){
                            elm.html(trash);
                        });
                    }
                },
                error: function () {
                    Alert.render('error', function(){
                        elm.html(trash);
                    });
                }
            });
    }, function(){});
});

function show_search_format_result(){
    var search_box = $('.search-bolton-format-box');
    var name = search_box.find('input[name=name]').val();
    var postData = [
        {name: 'name', value: name},
        {name: '_xsrf', value: xsrf_token},
        {name: 'method', value: 'SearchBoltonFormat'}
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
                    $('.bolton-format-list').html('');
                    for(i = 0; i < value.length ; i++){
                        make_bolton_format(value[i], 'append');
                    }
                }else{
                    var error = '';
                    for(var i = 0; i < messages.length ; i++){
                        error += messages[i] + '<br>';
                    }
                    if(error == '')
                        error = 'error';
                    Alert.render(error, function(){});
                }
            },
            error: function () {
                Alert.render('error', function(){});
            }
        });
}

$(document).on('keyup', ".search-bolton-format-box input", function(e){
    show_search_format_result();
});