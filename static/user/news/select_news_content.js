/**
 * Created by Morteza on 1/12/2016.
 */

$(document).on('change', 'select.select-news-content', function(e){
    var elm = $(e.target).closest('.select-news-content');
    var _type = elm.attr('data-type');
    var _news = elm.attr('data-news');
    var _agency = $('.agency_btn[data-news=' + _news + ']').attr('data-agency');
    var _value = elm.select2('val');
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'type', value: _type},
        {name: 'news', value: _news},
        {name: 'agency', value: _agency},
        {name: 'value', value: _value}
    ];
    jQuery.ajax(
        {
            url: news_content_url,
            type: "post",
            data: postData
        });
});