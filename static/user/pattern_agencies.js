/**
 * Created by Morteza on 12/6/2015.
 */

var pattern_agency = '<tr class="pattern-agency-row">\
                    <td data-id="__id__" class="pattern-agency name">__name__</td>\
                    <td>\
                        <span data-id="__id__" class="cursor-pointer pattern-agency edit"><i class="fa fa-pencil colorBlue"></i></span>\
                        <span data-id="__id__" class="cursor-pointer pattern-agency delete"><i class="fa fa-times colorRed"></i></span>\
                    </td>\
                </tr>';


$('.pattern-agencies.category').click(function(){
    var data_action = $(this).attr('data-action');
    $('.pattern-agencies.category-content').css('display','none');
    $('.pattern-agencies.category-content[data-action=' + data_action + ']').fadeIn();
});
$('.pattern-agencies.subject').click(function(){
    var data_action = $(this).attr('data-action');
    $('.pattern-agencies.subject-content').css('display','none');
    $('.pattern-agencies.subject-content[data-action=' + data_action + ']').fadeIn();
});
$('.pattern-agencies.geographic').click(function(){
    var data_action = $(this).attr('data-action');
    $('pattern-agencies.geographic-content').css('display','none');
    $('pattern-agencies.geographic-content[data-action=' + data_action + ']').fadeIn();
});


$(document).on('submit', '#pattern_agencies_form', function(e){
    e.preventDefault();
    var postData = $(this).serializeArray();
    var btn = $('.pattern-agencies-btn') ;
    btn.html(loader);
    jQuery.ajax(
        {
            url: pattern_agency_url,
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
                        error = 'متاسفانه در سیستم خطایی به وجود آمده، لطفا دوباره امتحان کنید.';
                    $('.errors').html(error);
                    btn.html('ثبت');
                    __a = true;
                }else{
                    Alert.render('success', function(){
                        btn.html('ثبت');
                        var a = $('input.pattern-agencies[name=pattern-name]');
                        var b = $('input.pattern-agencies[name=action]');
                        if(b.val() == 'edit'){
                            $('.pattern-agency.name').html(a.val());
                        }else{
                            $('table.table.pattern-agency').append(pattern_agency.replace(/__id__/g, value).replace(/__name__/g, a.val()));
                        }
                        $('input.pattern-agencies[type=checkbox]').lcs_off();
                        b.val('add');
                        $('input.pattern-agencies[name=pattern_id]').val('');
                        a.val('');
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


$(document).on('click', '.pattern-agency.edit', function(e){
    var elm = $(e.target).closest('.pattern-agency.edit');
    var btn_html =  elm.html();
    var pattern_id = elm.attr('data-id');
    elm.html(loader.replace(/20/g, '15'));
    var postData = {
        pattern_id: pattern_id,
        _xsrf: xsrf_token
    };
    jQuery.ajax(
        {
            url: pattern_agency_url,
            type: 'put',
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
                        error = 'متاسفانه در سیستم خطایی به وجود آمده، لطفا دوباره امتحان کنید.';
                    $('.errors').html(error);
                    elm.html(btn_html);
                    __a = true;
                }else{
                    $('input.pattern-agencies[type=checkbox]').lcs_off();
                    $('input.pattern-agencies[name=pattern-name]').val(value['name']);
                    for(var j = 0; j < value['agency'].length; j++){
                        $('input.pattern-agencies[name=agency][data-id=' + value['agency'][j] + ']').lcs_on()
                    }
                    for(j = 0; j < value['subject'].length; j++){
                        $('input.pattern-agencies[name=subject][data-id=' + value['subject'][j] + ']').lcs_on()
                    }
                    for(j = 0; j < value['geographic'].length; j++){
                        $('input.pattern-agencies[name=geographic][data-id=' + value['geographic'][j] + ']').lcs_on()
                    }
                    $('input.pattern-agencies[name=action]').val('edit');
                    $('input.pattern-agencies[name=pattern_id]').val(value['_id']);
                    elm.html(btn_html);
                }
            },
            error: function () {
                Alert.render('error', function(){
                    elm.html(btn_html);
                });
            }
        });
});


$(document).on('click', '.pattern-agency.delete', function(e){
    var elm = $(e.target).closest('.pattern-agency.delete');
    var btn_html =  elm.html();
    var pattern_id = elm.attr('data-id');
    elm.html(loader.replace(/20/g, '15'));
    var postData = {
        pattern_id: pattern_id,
        _xsrf: xsrf_token
    };
    jQuery.ajax(
        {
            url: pattern_agency_url,
            type: 'delete',
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
                        error = 'متاسفانه در سیستم خطایی به وجود آمده، لطفا دوباره امتحان کنید.';
                    $('.errors').html(error);
                    elm.html(btn_html);
                }else{
                    elm.closest('.pattern-agency-row').remove();
                    empty_modal_pattern_agency();
                }
            },
            error: function () {
                Alert.render('error', function(){
                    elm.html(btn_html);
                });
            }
        });
});

$('#pattern_agencies').on('hidden.bs.modal', function () {
    empty_modal_pattern_agency();
});

$(document).on('click', '.empty-modal-pattern-agency', function(){
    empty_modal_pattern_agency();

});
function empty_modal_pattern_agency(){
    $('.pattern-agencies-btn').html('ثبت');
    $('input.pattern-agencies[name=pattern-name]').val('');
    $('input.pattern-agencies[name=action]').val('add');
    $('input.pattern-agencies[type=checkbox]').lcs_off();
    $('input.pattern-agencies[name=pattern_id]').val('');
}