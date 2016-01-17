/**
 * Created by Morteza on 12/7/2015.
 */

var pattern_search = '<tr class="pattern-search-row">\
                    <td data-id="__id__" class="pattern-search name">__name__</td>\
                    <td>\
                        <span data-id="__id__" class="cursor-pointer pattern-search edit"><i class="fa fa-pencil colorBlue"></i></span>\
                        <span data-id="__id__" class="cursor-pointer pattern-search delete"><i class="fa fa-times colorRed"></i></span>\
                    </td>\
                </tr>';


$(document).on('click', '.add-agency.pattern-search', function(){
    var agency_names = [];
    var agency_ids = [];
    var all = false;
    $.each($('input.pattern-search.agency:checked'), function(){
        if($(this).val() == 'all')
            all = true;
        agency_names.push({id: $(this).attr('data-name'), text: $(this).attr('data-name')});
        agency_ids.push($(this).val());
    });
    if(!all){
        $('input.pattern-search[name=agency]').val(agency_ids);
        $('input.pattern-search[name=agency_names]').select2("data", agency_names, true);
    }else{
        $('input.pattern-search[name=agency]').val("all");
        $('input.pattern-search[name=agency_names]').select2("data", [{'id': "همه منابع", text: 'همه منابع'}]);
    }
});


$(document).on('submit', '#pattern_search_form', function(e){
    e.preventDefault();
    var postData = $(this).serializeArray();
    var btn = $('.pattern-search-btn') ;
    btn.html(loader);
    jQuery.ajax(
        {
            url: pattern_search_url,
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
                    Alert.render(error, function(){
                        btn.html('ثبت');
                        __a = true;
                    });
                    btn.html('ثبت');
                }else{
                    Alert.render('success', function(){
                        btn.html('ثبت');
                        var a = $('input.pattern-search[name=pattern-name]');
                        var b = $('input.pattern-search[name=action]');
                        $('input.pattern-search[type=checkbox]').prop('checked', false);
                        $('input.pattern-search[name=pattern_id]').val('');
                        $('select.pattern-search[name=period]').select2("val", "hour");
                        $('form#pattern_search_form .period-date').fadeOut();
                        $('table.table.pattern-search tr.empty').remove();
                        $('input.pattern-search.select2_keywords').select2("data", [], true);
                        $('input.pattern-search[name=exactly-word]').val('');
                        $('input.pattern-search[name=agency]').val("");
                        $('input.pattern-search[name=agency_names]').select2("data", [], true);
                        if(b.val() == 'edit'){
                            $('.pattern-search.name[data-id=' + value + ']').html(a.val());
                        }else{
                            $('table.table.pattern-search').append(pattern_search.replace(/__id__/g, value).replace(/__name__/g, a.val()));
                        }
                        b.val('add');
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


$(document).on('click', '.pattern-search.edit', function(e){
    var elm = $(e.target).closest('.pattern-search.edit');
    var btn_html =  elm.html();
    var pattern_id = elm.attr('data-id');
    elm.html(loader.replace(/20/g, '15'));
    var postData = {
        pattern_id: pattern_id,
        _xsrf: xsrf_token
    };
    jQuery.ajax(
        {
            url: pattern_search_url,
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
                }else{
                    $('input.pattern-search[type=checkbox]').prop('checked', false);
                    $('input.pattern-search[name=pattern-name]').val(value['name']);
                    $('select.pattern-search[name=period]').select2("val", value['period']);
                    if(value['period'] == 'period'){
                        $('input.pattern-search[name=start-date]').val(value['start_date']);
                        $('input.pattern-search[name=end-date]').val(value['end_date']);
                        $('form#pattern_search_form .period-date').fadeIn();
                    }else{
                        $('form#pattern_search_form .period-date').fadeOut();
                        $('input.pattern-search[name=start-date]').val("");
                        $('input.pattern-search[name=end-date]').val("");
                    }
                    $('select.pattern-search[name=key-words]').select2("data", [], true).select2("data", value["key_words"], true);
                    $('input.pattern-search[name=all-words]').select2("data", [], true).select2("data", value["all_words"], true);
                    $('input.pattern-search[name=exactly-word]').val(value["exactly_word"]);
                    $('input.pattern-search[name=each-words]').select2("data", [], true).select2("data", value["each_words"], true);
                    $('input.pattern-search[name=without-words]').select2("data", [], true).select2("data", value["without_words"], true);

                    $('select.pattern-search[name=direction-news]').select2('val', value["direction_news"]);
                    $('select.pattern-search[name=direction-agency]').select2('val', value["direction_agency"]);
                    $('select.pattern-search[name=main-source-news]').select2('val', value["main_source_news"]);
                    $('select.pattern-search[name=news-makers]').select2('val', value["news_makers"]);

                    $('input.pattern-search[name=picture]').prop('checked', value["picture"]);
                    $('input.pattern-search[name=video]').prop('checked', value["video"]);
                    $('input.pattern-search[name=voice]').prop('checked', value["voice"]);
                    $('input.pattern-search[name=doc]').prop('checked', value["doc"]);
                    $('input.pattern-search[name=pdf]').prop('checked', value["pdf"]);
                    $('input.pattern-search[name=archive]').prop('checked', value["archive"]);
                    $('input.pattern-search[name=tag_title]').prop('checked', value["tag_title"]);
                    $('input.pattern-search[name=bolton]').prop('checked', value["bolton"]);
                    $('input.pattern-search[name=note]').prop('checked', value["note"]);
                    $('input.pattern-search[name=unread]').prop('checked', value["unread"]);
                    $('input.pattern-search[name=star]').prop('checked', value["star"]);
                    $('input.pattern-search[name=important1]').prop('checked', value["important1"]);
                    $('input.pattern-search[name=important2]').prop('checked', value["important2"]);
                    $('input.pattern-search[name=important3]').prop('checked', value["important3"]);
                    $('input.pattern-search[name=agency]').val(value['agency']);
                    $('input.pattern-search[name=agency_names]').select2("data", [], true).select2("data", value['agency_names'], true);

                    $('input.pattern-search[name=action]').val('edit');
                    $('input.pattern-search[name=pattern_id]').val(value['_id']);
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


$(document).on('click', '.pattern-search.delete', function(e){
    var elm = $(e.target).closest('.pattern-search.delete');
    var btn_html =  elm.html();
    var pattern_id = elm.attr('data-id');
    elm.html(loader.replace(/20/g, '15'));
    var postData = {
        pattern_id: pattern_id,
        _xsrf: xsrf_token
    };
    jQuery.ajax(
        {
            url: pattern_search_url,
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
                    elm.closest('.pattern-search-row').remove();
                    empty_modal_pattern_search();
                }
            },
            error: function () {
                Alert.render('error', function(){
                    elm.html(btn_html);
                });
            }
        });
});

$('#pattern_search').on('hidden.bs.modal', function () {
    empty_modal_pattern_search();
});

$(document).on('click', '.empty-modal-pattern-search', function(){
    empty_modal_pattern_search();

});

function empty_modal_pattern_search(){
    $('input.pattern-search[name=pattern-name]').val('');
    $('input.pattern-search[name=action]').val('add');
    $('input.pattern-search[type=checkbox]').prop('checked', false);
    $('input.pattern-search[name=pattern_id]').val('');
    $('select.pattern-search[name=period]').select2("val", "hour");
    $('select.pattern-search[name=key-words]').select2('data', [], true);
    $('input.pattern-search[name=start-date]').val('');
    $('input.pattern-search[name=end-date]').val('');
    $('select.pattern-search[name=direction-news]').select2('val', "all");
    $('select.pattern-search[name=direction-agency]').select2('val', "all");
    $('select.pattern-search[name=main-source-news]').select2('val', "all");
    $('select.pattern-search[name=news-makers]').select2('val', "all");
    $('form#pattern_search_form .period-date').fadeOut();
    $('table.table.pattern-search tr.empty').remove();
    $('input.pattern-search.select2_keywords').select2("data", [], true);
    $('input.pattern-search[name=exactly-word]').val('');
    $('input.pattern-search[name=agency]').val("");
    $('input.pattern-search[name=agency_names]').select2("data", [], true);
}