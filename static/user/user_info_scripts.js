/**
 * Created by Omid on 11/25/2015.
 */


$(document).on('click', '.change_pic_div', function () {
    $('input[name=input_upload_pic]').click();
});

$(document).on('change', 'input[name=input_upload_pic]', function () {
    $('.change_pic_div').html(loader.replace(/20/g, '10'));
    var data = new FormData();
    data.append('_xsrf', xsrf_token);
    data.append('pic', $("input[name=input_upload_pic]")[0].files[0]);
    $.ajax(
            {
                url: user_upload_pic_url,
                type: "post",
                cache: false,
                contentType: false,
                processData: false,
                async: true,
                data: data,
                success: function (data) {
                    var src = static_url_images_avatars;
                    $('.user_avatar').attr('src', src + data);
                    $('.change_pic_div').html('<span>تغییر عکس</span>');
                }
            });
});

jQuery.validator.addMethod("iran_mobiles", function (value, element) {
    return this.optional(element) || /^(09\d{9})$/.test(value);
}, "شماره موبایل را صحیح وارد کنید.");
jQuery.validator.addMethod("iran_phones", function (value, element) {
    return this.optional(element) || /^(0\d{10})$/.test(value);
}, "شماره تلفن را صحیح وارد کنید.");

$(document).on('click', '.general_settings_tab', function(){
    var data_action = $(this).attr('data-action');
    $('.tab_content').css('display','none');
    $('.tab_content[data-action=' + data_action + ']').fadeIn();
});

    var frm = $("#edit_general_info_user").validate({
        errorClass: "colorRed font-size-9",
        rules: {
            mobile: {
                required: true,
                iran_mobiles: true,
                minlength: 11
            },
            phone: {
                required: true,
                iran_phones: true,
                minlength: 11
            },
            username: {
                required: false
            },
            email: {
                required: false,
                email: true
            },
            name: "required",
            family: "required",
            organization: "required"
        },
        messages: {
            mobile: {
                required: "شماره موبایل خود را وارد کنید.",
                iran_mobiles: "شماره موبایل را به درستی وارد کنید.",
                minlength: "شماره موبایل باید 11 رقمی باشد."
            },
            phone: {
                required: "شماره تلفن خود را وارد کنید.",
                iran_phones: "شماره تلفن را به درستی وارد کنید.",
                minlength: "شماره تلفن باید 11 رقمی باشد."
            },
            email: {
                email: "ایمیل خود را به صورت صحیح وارد کنید."
            },
            name: "نام را وارد کنید.",
            family: "نام خانوادگی را وارد کنید.",
            organization: "سازمان را وارد کنید."
        }
    });

    var __a = true;
    $(document).on('submit', '#edit_general_info_user', function(e){
        if(__a){
            __a = false;
            e.preventDefault();
            var btn = $('.edit-general-info-user') ;
            btn.html(loader);
            var postData = $("#edit_general_info_user").serializeArray();
            jQuery.ajax(
                {
                    url: '',
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
                            Alert.render(error, function(){
                                btn.html('ذخیره');
                                __a = true;
                            });
                        }else{
                            Alert.render('success', function(){
                                btn.html('ذخیره');
                                __a = true;
                                $('.full-name-header').html(value['full_name']);
                                $('.username-header').html(value['username']);
                                $('.email-header').html(value['email']);
                                $('.errors').html('');
                            });
                        }
                    },
                    error: function () {
                        Alert.render('error', function(){
                            btn.html('ذخیره');
                            __a = true;
                        });
                    }
                });
        }
    });

var __d = true;
$(document).on('submit', '#edit_setting_user', function(e){
    if(__d){
        __d = false;
        e.preventDefault();
        var btn =$('.edit-setting-btn') ;
        btn.html(loader);
        var postData = $("#edit_setting_user").serializeArray();
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
                        Alert.render('success', function () {
                            btn.html('ذخیره');
                            __d = true;
                        });
                    }else{
                        var error = '';
                        for(var i = 0; i < messages.length ; i++){
                            error += messages[i] + '<br>';
                        }
                        if(error == '')
                            error = 'error';
                        Alert.render(error, function(){
                            btn.html('ذخیره');
                            __d = true;
                        });
                    }
                },
                error: function () {
                    Alert.render('error', function(){
                        btn.html('ذخیره');
                        __d = true;
                    });
                }
            });
    }
});

$(document).on('keyup', '#change_password input[name=new_password]', function(e){
    if($(this).val() != ""){
        var __strength_password = strength_password($(this).val());
        $('form#change_password .strength-password-status').html(__strength_password[1]);
        $('form#change_password .strength-password-error').html(__strength_password[2]);
        $('.progress-bar').attr('aria-valuenow', __strength_password[3]).css('width', __strength_password[3] + '%').css('background-color', __strength_password[0]).css('background-image', "linear-gradient(to bottom, " + __strength_password[0] + " 0%, " + __strength_password[0] + " 100%) !important").html(__strength_password[3] + '%');
    }else{
        $('.progress-bar').attr('aria-valuenow', 0).css('width', 0 + '%').html(0 + '%');
        $('form#change_password .strength-password-status').html('گذرواژه را وارد کنید');
        $('form#change_password .strength-password-error').html('حداقل طول گذرواژه باید بیشتر از 6 کاراکتر باشد');
    }
});

var __e = true;
$(document).on('submit', '#change_password', function(e){
    if(__e){
        __e = false;
        e.preventDefault();
        var btn =$('.change-password-btn') ;
        btn.html(loader);
        var postData = $("#change_password").serializeArray();
        jQuery.ajax(
            {
                url: change_password_url,
                type: "post",
                data: postData,
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    var messages = response['messages'];
                    if (status) {
                        Alert.render('success', function () {
                            btn.html('ذخیره');
                            __e = true;
                        });
                    }else{
                        var error = '';
                        for(var i = 0; i < messages.length ; i++){
                            error += messages[i] + '<br>';
                        }
                        if(error == '')
                            error = 'error';
                        Alert.render(error, function(){
                            btn.html('ذخیره');
                            __e = true;
                        });
                    }
                },
                error: function () {
                    Alert.render('error', function(){
                        btn.html('ذخیره');
                        __e = true;
                    });
                }
            });
    }
});
