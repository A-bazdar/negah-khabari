/**
 * Created by Morteza on 3/1/2016.
 */

function empty_form_bolton(){
    $('form#BoltonForm input[name=method]').val("AddBolton");
    $('form#BoltonForm input[name=_id]').val('');
    $('form#BoltonForm input[name=name]').val('');
    $('form#BoltonForm select[name=type]').select2('val', '');
    $('.news-section-divs').html(news_section_base);
    $('form#BoltonForm select.new_select').select2().removeClass('new_select').addClass('select');
}

function make_bolton(item, type){
    var item_obj = $('#MakeBoltonItem');
    item_obj.html($('#BoltonItem').html());
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('.bolton-name').html(item['name']);
    if(item['manual']){
        item_obj.find('.bolton-is-manual').html('دستی');
    }else{
        item_obj.find('.bolton-is-manual').html('خودکار');
    }
    item_obj.find('.bolton-date').html(item['date']);
    item_obj.find('.bolton-type').html(item['type']['name']);
    item_obj.find('.bolton-count-section').html(item['sections'].length);
    if(item['active']){
        item_obj.find('.bolton-active').addClass('red-turn-off-icon').attr('data-action', 'deactive');
    }else{
        item_obj.find('.bolton-active').addClass('green-turn-off-icon').attr('data-action', 'active');
    }
    if(type == "append")
        $('.bolton-list').append(item_obj.html());
    else
        $('.bolton-list').prepend(item_obj.html());
}

function make_bolton_list(item, type){
    var item_obj = $('#MakeBoltonListItem');
    item_obj.html($('#BoltonListItem').html());
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('.bolton-name').html(item['name']);
    item_obj.find('.bolton-date').html(item['date']);
    if(item['manual']){
        item_obj.find('.bolton-is-manual').html('دستی');
    }else{
        item_obj.find('.bolton-is-manual').html('خودکار');
    }
    item_obj.find('.bolton-type').html(item['type']['name']);
    item_obj.find('.bolton-count-section').html(item['sections'].length);
    item_obj.find('.show-bolton').attr('onclick', 'location.href="' + bolton_by_id_url.replace('__id__', item['_id']) + '"');
    if(type == "append")
        $('.bolton-list-list').append(item_obj.html());
    else
        $('.bolton-list-list').prepend(item_obj.html());
}

function show_search_result(__type){
    var search_box = $('.search-bolton-box[data-type=' + __type + ']');
    var name = search_box.find('input[name=name]').val();
    var date = search_box.find('input[name=date]').val();
    var type = search_box.find('select[name=type] option:selected').attr("value");
    var manual = search_box.find('select[name=manual] option:selected').attr("value");
    var count_bolton_section = search_box.find('input[name=count-bolton-section]').val();
    if(name == "" && manual == "" && date == "" && type == "" && count_bolton_section == "")
        return;
    var postData = [
        {name: 'name', value: name},
        {name: 'date', value: date},
        {name: 'type', value: type},
        {name: 'manual', value: manual},
        {name: 'count_bolton_section', value: count_bolton_section},
        {name: 'show_type', value: __type},
        {name: '_xsrf', value: xsrf_token},
        {name: 'method', value: 'SearchBolton'}
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
                    if(__type == "list"){
                        $('.bolton-list-list').html('');
                        for(i = 0; i < value.length ; i++){
                            make_bolton_list(value[i], 'append');
                        }
                    }else if(__type == "topic"){
                        $('.bolton-list').html('');
                        for(i = 0; i < value.length ; i++){
                            make_bolton(value[i], 'append');
                        }
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

$(document).on('click', '.add-section-news', function(){
    var display = 'block';
    if($('input[name=manual]:checked').val() == "True"){
        display = 'none';
    }
    $('.news-section-divs').append(news_section.replace('__display__', display));
    $('.news-section-divs .new_select').select2().removeClass('new_select').addClass('select');
});

$(document).on('click', '.remove-section-news', function(e){
    $(e.target).closest('.news-section').remove();
});

$(document).on('submit', "#BoltonForm", function(e){
    e.preventDefault();
    var postData = $("#BoltonForm").serializeArray();
    var btn = $('.bolton-btn');
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
                    Alert.render('success', function(){
                        btn.html('ثبت');
                        if($('form#BoltonForm input[name=method]').val() == "AddBolton"){
                            make_bolton(value, "prepend");
                            make_bolton_list(value, "prepend");
                            __bolton_types.push(value);
                        }else{
                            var obj = $('.bolton_list_items[data-id=' + value['_id'] + ']');
                            obj.find('.bolton-name').html(value['name']);
                            obj.find('.bolton-type').html(value['type']['name']);
                            obj.find('.bolton-count-section').html(value['sections'].length);
                            for(var i = 0; i < __all_bolton.length ; i++) {
                                if (__all_bolton[i]['_id'] == value['_id']) {
                                    __all_bolton[i] = value;
                                }
                            }
                        }
                        empty_form_bolton();

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

$(document).on('click', ".bolton-active", function(e){
    var elm = $(e.target).closest('.bolton-active');
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: elm.attr('data-action')},
        {name: 'method', value: "ActiveBolton"},
        {name: '_id', value: elm.attr('data-id')}
    ];
    var btn = $('.bolton-type-btn');
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

$(document).on('click', '.bolton-delete', function(e){
    Confirm.render(0, 0, 0, 0, 0, function(){
        var elm = $(e.target).closest('.bolton-delete');
        var _id = elm.attr('data-id');
        elm.html(loader.replace(/20/g, '15'));
        var postData = [
            {name: '_id', value: _id},
            {name: '_xsrf', value: xsrf_token},
            {name: 'method', value: 'DeleteBolton'}
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

$(document).on('click', ".bolton-edit", function(e){
    var elm = $(e.target).closest('.bolton-edit');
    var _id = elm.attr('data-id');
    for(var i = 0; i < __all_bolton.length ; i++) {
        var _b = __all_bolton[i];
        if(_b['_id'] == _id){
            $('form#BoltonForm input[name=method]').val("EditBolton");
            $('form#BoltonForm input[name=_id]').val(_id);
            $('form#BoltonForm input[name=name]').val(_b['name']);
            $('form#BoltonForm select[name=format]').select2("val", _b['format']);
            var display = "block";
            if(_b['manual']){
                $('form#BoltonForm input[name=manual][value=True]').prop("checked", true);
                $('.bolton-type-div').hide();
                display = "none";
            }else{
                $('form#BoltonForm input[name=manual][value=False]').prop("checked", true);
                $('.bolton-type-div').show();
                display = "block";
            }
            $('form#BoltonForm select[name=type]').select2("val", _b['type']['_id']);
            $('form#BoltonForm input[name=section_id]').val(_b['sections'][0]['_id']);
            $('form#BoltonForm input[name=news_section]').val(_b['sections'][0]['section']);
            $('form#BoltonForm select[name=pattern_search]').select2("val", _b['sections'][0]['pattern']);
            for(var j = 1; j < _b['sections'].length ; j++) {
                var _c = _b['sections'][j];
                var temp = $('#Temp');
                temp.html(news_section.replace('__display__', display));
                temp.find('input[name=news_section]').attr('value', _c['section']);
                temp.find('input[name=section_id]').attr('value', _c['_id']);
                temp.find('select[name=pattern_search] option[data-val=' + _c['pattern'] + ']').attr('selected', 'selected');
                $('.news-section-divs').append(temp.html());
                $('.news-section-divs .new_select').select2().removeClass('new_select').addClass('select');
            }
        }
    }
    $('.add-bolton-btn i').removeClass('fa-caret-down').addClass('fa-caret-up');
    $('.add-bolton-btn').removeClass('closebox').addClass('open');
    $('.add_bolton_form_con[data-id=1]').slideDown();
});

$(document).on('keyup', ".search-bolton-box input", function(e){
    show_search_result($(this).closest('.search-bolton-box').attr('data-type'));
});

$(document).on('change', ".search-bolton-box select", function(e){
    show_search_result($(this).closest('.search-bolton-box').attr('data-type'));
});

$('.bolton-date-picker').persianDatepicker({
    onSelect: function () {
        var _type = "topic";
        if($('.right_tabs.active').attr('data-action') == "bolton_list")
            _type = "list";
        show_search_result(_type);
    }
});

$(document).on('change', "input[name=manual]", function(e){
    if($('input[name=manual]:checked').val() == "True"){
        $('.bolton-type-div').hide();
        $('.pattern-search-div').hide();
    }
    else{
        $('.bolton-type-div').show();
        $('.pattern-search-div').show();
    }
});