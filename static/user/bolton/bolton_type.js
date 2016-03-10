/**
 * Created by Morteza on 3/1/2016.
 */

function empty_form_bolton_type(){
    $('form#BoltonTypeForm input[name=method]').val("AddBoltonType");
    $('form#BoltonTypeForm input[name=_id]').val('');
    $('form#BoltonTypeForm input[name=name]').val('');
    $('form#BoltonTypeForm input[name=time-active]').val('');
    $('form#BoltonTypeForm input[name=from]').val('');
}

function make_bolton_type(item, type){
    var item_obj = $('#MakeBoltonTypeItem');
    item_obj.html($('#BoltonTypeItem').html());
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('[data-name]').attr('data-name', item['name']);
    item_obj.find('[data-time-active]').attr('data-time-active', item['time_active']);
    item_obj.find('[data-unit]').attr('data-unit', item['unit']);
    item_obj.find('[data-from]').attr('data-from', item['from']);
    item_obj.find('.bolton-type-name').html(item['name']);
    item_obj.find('.bolton-time-active').html(item['time_active']);
    if(item['active']){
        item_obj.find('.bolton-type-active').addClass('red-turn-off-icon').attr('data-action', 'deactive');
    }else{
        item_obj.find('.bolton-type-active').addClass('green-turn-off-icon').attr('data-action', 'active');
    }
    if(type == "append")
        $('.bolton-type-list').append(item_obj.html());
    else
        $('.bolton-type-list').prepend(item_obj.html());
}

$(document).on('submit', "#BoltonTypeForm", function(e){
    e.preventDefault();
    var postData = $("#BoltonTypeForm").serializeArray();
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
                        __a = true;
                    });
                }else{
                    Alert.render('success', function(){
                        btn.html('ثبت');
                        if($('form#BoltonTypeForm input[name=method]').val() == "AddBoltonType"){
                            make_bolton_type(value, "prepend");
                        }else{
                            var obj = $('.bolton_list_items[data-id=' + value['_id'] + ']');
                            obj.find('.bolton-type-name').html(value['name']);
                            obj.find('.bolton-time-active').html(value['time_active']);
                            obj.find('[data-name]').attr('data-name', value['name']);
                            obj.find('[data-time-active]').attr('data-time-active', value['time_active']);
                            obj.find('[data-unit]').attr('data-unit', value['unit']);
                            obj.find('[data-from]').attr('data-from', value['from']);
                        }
                        empty_form_bolton_type();
                        __a = true;

                    });
                }
            },
            error: function () {
                Alert.render('error', function(){
                    btn.html('ثبت');
                    __a = true;
                });
            }
        });
});

$(document).on('click', ".bolton-type-active", function(e){
    var elm = $(e.target).closest('.bolton-type-active');
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: elm.attr('data-action')},
        {name: 'method', value: "ActiveBoltonType"},
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
                        __a = true;
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
                    __a = true;
                });
            }
        });
});

$(document).on('click', ".bolton-type-edit", function(e){
    var elm = $(e.target).closest('.bolton-type-edit');
    var _id = elm.attr('data-id');
    var name = elm.attr('data-name');
    var time_active = elm.attr('data-time-active');
    var unit = elm.attr('data-unit');
    var from = elm.attr('data-from');
    $('form#BoltonTypeForm input[name=method]').val("EditBoltonType");
    $('form#BoltonTypeForm input[name=_id]').val(_id);
    $('form#BoltonTypeForm input[name=name]').val(name);
    $('form#BoltonTypeForm input[name=time-active]').val(time_active);
    $('form#BoltonTypeForm select[name=unit]').select2("val", unit);
    $('form#BoltonTypeForm input[name=from]').val(from);
    $('.add-bolton-btn i').removeClass('fa-caret-down').addClass('fa-caret-up');
    $('.add-bolton-btn').removeClass('closebox').addClass('open');
    $('.add_bolton_form_con[data-id=2]').slideDown();
});

var trash = '<span class="icon-news trash-icon"></span>';

$(document).on('click', '.bolton-type-delete', function(e){
    Confirm.render(0, 0, 0, 0, 0, function(){
        var elm = $(e.target).closest('.bolton-type-delete');
        var _id = elm.attr('data-id');
        elm.html(loader.replace(/20/g, '15'));
        var postData = [
            {name: '_id', value: _id},
            {name: '_xsrf', value: xsrf_token},
            {name: 'method', value: 'DeleteBoltonType'}
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