/**
 * Created by Abolfazl on 31/01/2016.
 */

var __test_html = '<div class="col-md-12 padding-10">\
                <div class="row"><div class="col-md-10"><a href="__link__">__link__</a></div><div class="col-md-2"></div>\
                <span data-links="__links__" data-base="__base_link__" data-link="__link__" class="refinement-news cursor-pointer">پالایش</span>\
                </div></div>';

$(document).on('click', '.test-address-agency', function(e){
    var elm = $(e.target).closest('.test-address-agency');
    elm.html(loader);
    var data_link = elm.attr('data-link');
    var link = $('input[name=link][data-link=' + data_link + ']').val();
    var address = $('input[name=links][data-link=' + data_link + ']').val();
    var base_link = elm.closest('form').find('input[name=base_link]').val();
    var postData = [
        {name: 'link', value: link},
        {name: 'address', value: address},
        {name: 'base_link', value: base_link},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: 'test_address'}
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
                    var html = '';
                    if(value.length > 0){
                        for(var i = 0; i < value.length ; i++){
                            html += __test_html.replace(/__link__/g, value[i]).replace(/__base_link__/g, base_link).replace(/__links__/g, data_link);
                        }
                        $('#result_test_address_div').html(html).show();
                        $('#result_test_news_link_div').hide();
                        elm.html('تست');
                    }else{
                        $('#result_test_address_div').html('موردی یافت نشد.');
                    }
                    $('#result_test_address').modal('toggle');
                    $('#result_test_address_div').show();
                    $('#result_test_news_link_div').hide();
                    elm.html('تست');
                }
            },
            error: function () {
                Alert.render('error', function(){
                    $('#result_test_address_div').show();
                    $('#result_test_news_link_div').hide();
                    elm.html('تست');
                });
            }
        });
});

$(document).on('click', '.refinement-news', function(e){
    var elm = $(e.target).closest('.refinement-news');
    elm.html(loader);
    var base_link = elm.attr('data-base');
    var data_link = elm.attr('data-link');
    var data_links = elm.attr('data-links');
    var format_date = $('select[name=date-format][data-link=' + data_links + ']').select2("val");
    var ro_title = $('input[name=ro_title][data-link=' + data_links + ']').val();
    var title = $('input[name=title][data-link=' + data_links + ']').val();
    var date = $('input[name=date][data-link=' + data_links + ']').val();
    var thumbnail = $('input[name=thumbnail][data-link=' + data_links + ']').val();
    var summary = $('input[name=summary][data-link=' + data_links + ']').val();
    var body = $('input[name=body][data-link=' + data_links + ']').val();
    var excludes = [];
    $.each($('input[name=exclude][data-link=' + data_links + ']'), function(){
        if($(this).val() != ""){
            excludes.push($(this).val());
        }
    });
    if(ro_title == "" || title == "" || date == "" || thumbnail  == "" || summary == "" || body == ""){
        Alert.render('همه آدرس ها را وارد کنید.', function(){
            elm.html('پالایش');
        });
    }
    var postData = [
        {name: 'address', value: data_link},
        {name: 'base_link', value: base_link},
        {name: 'ro_title', value: ro_title},
        {name: 'title', value: title},
        {name: 'date', value: date},
        {name: 'format_date', value: format_date},
        {name: 'thumbnail', value: thumbnail},
        {name: 'summary', value: summary},
        {name: 'body', value: body},
        {name: 'excludes', value: JSON.stringify(excludes)},
        {name: '_xsrf', value: xsrf_token},
        {name: 'action', value: 'refinement_news'}
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
                    var html = '<div class="col-md-12">\
                                    <div class="row">\
                                        <div class="col-md-12">\
                                            <div class="R_butt_blue back-result-test-address-div text-center">بازگشت</div>\
                                        </div>\
                                    </div>\
                                    <div class="row">\
                                        <div class="col-md-12"><h3 class="text-center">روتیتر</h3></div>\
                                        <div class="col-md-12">' + value['ro_title'] + '</div>\
                                    </div>\
                                    <div class="row">\
                                        <div class="col-md-12"><h3 class="text-center">تیتر</h3></div>\
                                        <div class="col-md-12">' + value['title'] + '</div>\
                                    </div>\
                                    <div class="row">\
                                        <div class="col-md-12"><h3 class="text-center">خلاصه</h3></div>\
                                        <div class="col-md-12">' + value['summary'] + '</div>\
                                    </div>\
                                    <div class="row">\
                                        <div class="col-md-12"><h3 class="text-center">عکس</h3></div>\
                                        <div class="col-md-12">' + value['thumbnail'] + '</div>\
                                        <div class="col-md-12"><img style="width: 200px;" src="' + value['thumbnail'] + '"></div>\
                                    </div>\
                                    <div class="row">\
                                        <div class="col-md-12"><h3 class="text-center">متن</h3></div>\
                                        <div class="col-md-12"><div class="text-center R_butt_blue show-continue-body-refinement">نمایش</div></div>\
                                        <div class="col-md-12 body-refinement" style="display: none">' + value['body'] + '</div>\
                                    </div>\
                                    <div class="row">\
                                        <div class="col-md-12"><h3 class="text-center">تاریخ</h3></div>\
                                        <div class="col-md-12">' + value['date'] + '</div>\
                                    </div>\
                                </div>';

                    elm.html('پالایش');
                    $('#result_test_address_div').hide();
                    $('#result_test_news_link_div').html(html).show();
                }
            },
            error: function () {
                Alert.render('error', function(){
                    elm.html('پالایش');
                });
            }
        });
});

$(document).on('click', '.back-result-test-address-div', function(e){
    $('#result_test_address_div').show();
    $('#result_test_news_link_div').hide();
});

$(document).on('click', '.show-continue-body-refinement', function(e){
    $('.body-refinement').slideToggle();
});

$(document).on('click', '.delete-comparative-news', function(e){
    $(e.target).closest('.comparative-row').remove();
});