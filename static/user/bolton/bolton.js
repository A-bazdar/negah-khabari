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
    item_obj.find('.bolton-date').html(item['date']);
    item_obj.find('.bolton-type').html(item['type']['name']);
    item_obj.find('.bolton-count-section').html(item['sections'].length);
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
    item_obj.find('.bolton-type').html(item['type']['name']);
    item_obj.find('.bolton-count-section').html(item['sections'].length);
    item_obj.find('.show-bolton').attr('onclick', 'location.href="' + show_bolton_by_id_url.replace('__id__', item['_id']) + '"');
    if(type == "append")
        $('.bolton-list-list').append(item_obj.html());
    else
        $('.bolton-list-list').prepend(item_obj.html());
}

$(document).on('click', '.add-section-news', function(){
    $('.news-section-divs').append(news_section);
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
                        __a = true;
                    });
                }else{
                    Alert.render('success', function(){
                        btn.html('ثبت');
                        if($('form#BoltonForm input[name=method]').val() == "AddBolton"){
                            make_bolton(value, "prepend");
                            make_bolton_list(value, "prepend");
                        //}else{
                            //var obj = $('.bolton_list_items[data-id=' + value['_id'] + ']');
                            //obj.find('.bolton-type-name').html(value['name']);
                            //obj.find('.bolton-time-active').html(value['time_active']);
                            //obj.find('[data-name]').attr('data-name', value['name']);
                            //obj.find('[data-time-active]').attr('data-time-active', value['time_active']);
                            //obj.find('[data-unit]').attr('data-unit', value['unit']);
                            //obj.find('[data-from]').attr('data-from', value['from']);
                        }
                        empty_form_bolton();
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