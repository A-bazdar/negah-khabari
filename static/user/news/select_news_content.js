/**
 * Created by Morteza on 1/12/2016.
 */

$(document).on('change', 'select.select-news-content', function(e){
    var elm = $(e.target).closest('.select-news-content');
    var _type = elm.attr('data-type');
    var _news = elm.attr('data-news');
    var _value = elm.select2('val');
    var postData = [
        {name: '_xsrf', value: xsrf_token},
        {name: 'type', value: _type},
        {name: 'news', value: _news},
        {name: 'value', value: _value}
    ];
    jQuery.ajax(
        {
            url: news_content_url,
            type: "post",
            data: postData
        });
});