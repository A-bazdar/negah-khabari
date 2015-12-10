/**
 * Created by Morteza on 12/10/2015.
 */


$('.font-setting.font_setting_tabs').click(function(){
    var data_action = $(this).attr('data-action');
    $('.tab_content.font-setting').hide();
    $('.tab_content.font-setting[data-action=' + data_action + ']').fadeIn();
});

$(document).on('click', '.save-font-setting.form-font-setting', function(){
    var font = $(this).attr('data-font');
    $('.font-setting-btn.font-setting[data-font=' + font + ']').html(loader);
    var postData = $(this).serializeArray();
    jQuery.ajax(
    {
        url: font_setting_url,
        type: "post",
        data: postData,
        success: function (response) {
            var status = response['status'];
            var value = response['value'];
            if (status) {
                $('.font-setting-btn.font-setting[data-font=' + font + ']').html('ثبت');
            }
        }
    });
});