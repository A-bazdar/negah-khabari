/**
 * Created by Morteza on 12/9/2015.
 */

$(".select2_keywords.key-words").select2({
    tags: []
});

$('.key-words.keyword_tabs').click(function(){
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

$(document).on('click', '.save-edit.key-words', function(e){
    var elm = $(e.target).closest('.save-edit.key-words');
    var key_id = elm.attr('data-key');
    var postData = $('.form-save-edit.key-words[data-key=' + key_id + ']').serializeArray();
    jQuery.ajax(
    {
        url: key_word_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                $('.keywords_box.key-words[data-key=' + key_id + ']').html(value).removeClass('display-none');
                $('.edit_keywords_box.key-words[data-key=' + key_id + ']').addClass('display-none');
            }
        }
    });
});