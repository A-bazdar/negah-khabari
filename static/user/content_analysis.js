/**
 * Created by Morteza on 12/11/2015.
 */

$('.content-analysis.content-analysis-tab').click(function(){
    var data_action = $(this).attr('data-action');
    $('.tab_content.content-analysis').hide();
    $('.tab_content.content-analysis[data-action=' + data_action + ']').fadeIn();
});

var content_analysis_html = '<tr data-content="__content_id__">\
                            <td>__name__</td>\
                            <td><i data-content="__content_id__" class="fa fa-pencil"></i><i data-content="__content_id__" class="fa fa-trash-o"></i></td>\
                        </tr>';

$(document).on('submit', '.form-content-analysis', function(e){
    var btn = $('.content-analysis.content-analysis-btn', this);
    btn.html(loader);
    e.preventDefault();
    var postData = $(this).serializeArray();
    jQuery.ajax(
    {
        url: content_analysis_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                var __h = content_analysis_html.replace(/__name__/g, value['name']).replace(/__content_id__/g, value['_id']);
                if(value['action'] == "main_source_news"){
                    $('.table.content-analysis.main-source-news').append(__h);
                    $('.empty.content-analysis.main-source-news').remove();
                }else if(value['action'] == "news_group"){
                    $('.table.content-analysis.news-group').append(__h);
                    $('.empty.content-analysis.news-group').remove();
                }else if(value['action'] == "news_maker"){
                    $('.table.content-analysis.news-maker').append(__h);
                    $('.empty.content-analysis.news-maker').remove();
                }
                btn.html(plus);
            }
        }
    });
});

$(document).on('click', '.content-analysis.show-edit', function (e) {
    var elm = $(e.target).closest('.content-analysis.show-edit');
    var content = elm.attr('data-content');
    $('.edit-content.content-analysis').hide();
    $('.edit-content.content-analysis[data-content=' + content + ']').slideDown();
});

$(document).on('click', '.content-analysis.cancel-edit', function (e) {
    var elm = $(e.target).closest('.content-analysis.cancel-edit');
    var content = elm.attr('data-content');
    $('.edit-content.content-analysis[data-content=' + content + ']').hide();
});

$(document).on('click', '.content-analysis.save-edit', function (e) {
    var elm = $(e.target).closest('.content-analysis.save-edit');
    var content = elm.attr('data-content');
    var action = elm.attr('data-action');
    var name = $('input.content-analysis.name-edit[data-content=' + content + '][data-action=' + action + ']').val();
    var postData = [
        {name: 'content_id', value: content},
        {name: 'action', value: action},
        {name: 'name', value: name},
        {name: '_xsrf', value: xsrf_token}
    ];
    jQuery.ajax(
    {
        url: content_analysis_url,
        type: "put",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                $('.content-analysis.name-content[data-content=' + content + '][data-action=' + action + ']').html(name);
                $('.edit-content.content-analysis[data-content=' + content + ']').slideUp();
            }
        }
    });
});

$(document).on('click', '.content-analysis.delete', function (e) {
    var elm = $(e.target).closest('.content-analysis.delete');
    var content = elm.attr('data-content');
    var action = elm.attr('data-action');
    var postData = [
        {name: 'content_id', value: content},
        {name: 'action', value: action},
        {name: '_xsrf', value: xsrf_token}
    ];
    jQuery.ajax(
    {
        url: content_analysis_url,
        type: "delete",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                elm.closest('tr').remove();
                $('.edit-content.content-analysis[data-content=' + content + ']').remove();
            }
        }
    });
});