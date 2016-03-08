/**
 * Created by Morteza on 3/7/2016.
 */

$(document).on('click', '.add-to-bolton', function(e){
    var elm = $(e.target).closest('.add-to-bolton');
    var news = elm.attr('data-news');
    $('.add-news-to-bolton').attr('data-news', news);
    $('#add_to_bolton_modal').modal('toggle');
});

$(document).on('click', '.add-news-to-bolton', function(e){
    var elm = $(e.target).closest('.add-news-to-bolton');
    var btn_html = elm.html();
    elm.html(loader);
    var bolton = elm.attr('data-bolton');
    var section = elm.attr('data-section');
    var news = elm.attr('data-news');
    var postData = [
        {name: 'news', value: news},
        {name: '_xsrf', value: xsrf_token},
        {name: 'bolton', value: bolton},
        {name: 'section', value: section}
    ];
    jQuery.ajax(
        {
            url: add_news_to_bolton_url,
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
                }
                elm.html(btn_html);
            }
        });
});