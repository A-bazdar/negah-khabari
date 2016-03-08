/**
 * Created by Morteza on 08/03/2016.
 */

function make_news(item){
    var item_obj = $('#MakeBoltonNewsItem');
    item_obj.html($('#BoltonNewsItem').html());
    item_obj.find('[data-id]').attr('data-id', item['_id']);
    item_obj.find('#agency_info').html(item['agency_name']);
    item_obj.find('.news-select').attr('id', item['_id']);
    item_obj.find('#label_news_select').attr('for', item['_id']);
    item_obj.find('#title_news').html(item['title']);
    $('#show_result_news').append(item_obj.html());
}

function show_news(section, name){
    $('.section-tab.active').removeClass('active');
    $('.section-tab[data-section=' + section + ']').addClass('active');
    $('#section_name').html(name);
    $('#show_result_news').html('');
    var postData = [
        {name: 'method', value: "ShowSectionNews"},
        {name: 'section', value: section},
        {name: '_xsrf', value: xsrf_token}
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
                    for(var i = 0; i < value.length ; i++){
                        make_news(value[i]);
                    }
                }
            }
        });
}