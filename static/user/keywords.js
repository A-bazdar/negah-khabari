/**
 * Created by Morteza on 12/9/2015.
 */

$(".select2_keywords.key-words").select2({
    tags: []
});

$(document).on('click', '.key-words.keyword_tabs', function(){
    var data_action = $(this).attr('data-action');
    var data_key = $(this).attr('data-key');
    $('.tab-content.key-words[data-key=' + data_key + ']').css('display','none');
    $('.tab-content.key-words[data-action=' + data_action + ']').fadeIn();
});

$(document).on('click', '.edit-keyword.key-words', function(e){
    var elm = $(e.target).closest('.edit-keyword.key-words');
    var key_id = elm.attr('data-key');
    $('.keywords_box.key-words[data-key=' + key_id + ']').addClass('display-none');
    $('.edit_keywords_box.key-words[data-key=' + key_id + ']').removeClass('display-none');
});

$(document).on('click', '.cancel-edit.key-words', function(e){
    var elm = $(e.target).closest('.cancel-edit.key-words');
    var key_id = elm.attr('data-key');
    $('.keywords_box.key-words[data-key=' + key_id + ']').removeClass('display-none');
    $('.edit_keywords_box.key-words[data-key=' + key_id + ']').addClass('display-none');
});

$(document).on('click', '#show_hide_add_keyword', function(e){
    var elm = $(e.target);
    var a = elm.attr('data-show');
    if(a == 'true'){
        $('#add_keyword_div').slideUp();
        elm.attr('data-show', 'false').html('+ افزودن');
    }else{
        $('#add_keyword_div').slideDown();
        elm.attr('data-show', 'true').html('- انصراف');
    }
});

$(document).on('click', '.save-edit.key-words', function(e){
    var elm = $(e.target).closest('.save-edit.key-words');
    var key_id = elm.attr('data-key');
    var org_html = elm.html();
    elm.html(loader);
    var postData = $('.form-save-edit.key-words[data-key=' + key_id + ']').serializeArray();
    postData.push({name: "action", value: "edit"});
    jQuery.ajax(
    {
        url: key_word_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            alert(status);
            var value = response['value'];
            if (status) {
                $('.keywords_box.key-words[data-key=' + key_id + ']').html(value['html']).removeClass('display-none');
                $('.edit_keywords_box.key-words[data-key=' + key_id + ']').addClass('display-none');
                var options = '';
                for (var i in value['keywords']) {
                    options += "<option value='" + value['keywords'][i]['id'] + "'>" + value['keywords'][i]['topic'] + "</option>";
                }
                $(".select.search-news[name=key-words]").select2("data", []).html(options);
                $(".select.refinement-news[name=key-words]").select2("data", []).html(options);
            }
            elm.html(org_html);
        }
    });
});

$(document).on('click', '.save-add.key-words', function(e){
    var elm = $(e.target);
    var org_html = elm.html();
    elm.html(loader);
    var postData = $('#form_add_keyword').serializeArray();
    postData.push({name: "action", value: "add"});
    jQuery.ajax(
    {
        url: key_word_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                $('#all_key_words').append(value['html']);
                $('#add_keyword_div').slideUp();
                $('#show_hide_add_keyword').attr('data-show', 'false').html('+ افزودن');
                $('#form_add_keyword input[type=text]').val('');
                var options = '';
                for (var i in value['keywords']) {
                    options += "<option value='" + value['keywords'][i]['id'] + "'>" + value['keywords'][i]['topic'] + "</option>";
                }
                $(".select.search-news[name=key-words]").select2("data", []).html(options);
                $(".select.refinement-news[name=key-words]").select2("data", []).html(options);
                elm.html(org_html);
            }
        }
    });
});

$(document).on('click', '.cancel-add.key-words', function(e){
    $('#add_keyword_div').slideUp();
    $('#show_hide_add_keyword').attr('data-show', 'false').html('+ افزودن');
});

var key_word_html = '<div class="key-word-row">\
                        <div class="row margin-top-10">\
                            <div class="col-md-1 col-sm-1 col-md-offset-1 col-sm-offset-1">\
                                <span>کلیدواژه : </span>\
                            </div>\
                            <div class="col-md-4 col-sm-4">\
                                <input class="form-control" type="text" name="keyword">\
                            </div>\
                            <div class="col-md-1 col-sm-1">\
                                <div class="R_butt_red key-words remove-key-word"><i class="fa fa-times"></i></div>\
                            </div>\
                        </div>\
                        <div class="row margin-top-10">\
                            <div class="col-md-1 col-sm-1 col-md-offset-2 col-sm-offset-2">\
                                <span>مترادف : </span>\
                            </div>\
                            <div class="col-md-9 col-sm-9">\
                                <input class="form-control select2_keywords key-words" type="text" name="synonyms">\
                            </div>\
                        </div>\
                        <div class="row margin-top-10">\
                            <div class="col-md-1 col-sm-1 col-md-offset-2 col-sm-offset-2">\
                                <span>نامترادف : </span>\
                            </div>\
                            <div class="col-md-9 col-sm-9">\
                                <input class="form-control select2_keywords key-words" type="text" name="no_synonyms">\
                            </div>\
                        </div>\
                    </div>';

$(document).on('click', '.add-key-word.key-words', function(e){
    $('#add_key_word_key_words').append(key_word_html);
});

$(document).on('click', '.edit-add-key-word.key-words', function(e){
    var elm = $(e.target).closest('.edit-add-key-word');
    var _key = elm.attr('data-key');
    $('.edit-keywords-div[data-key=' + _key + ']').append(key_word_html);
});

$(document).on('click', '.remove-key-word.key-words', function(e){
    $(e.target).closest('.key-word-row').remove();
});