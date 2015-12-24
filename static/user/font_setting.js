/**
 * Created by Morteza on 12/10/2015.
 */


$(document).on('click', '.font-setting.font_setting_tabs', function(){
    var data_action = $(this).attr('data-action');
    $('.tab_content.font-setting').hide();
    $('.tab_content.font-setting[data-action=' + data_action + ']').fadeIn();
});

$(document).on('click', '.font-setting-btn.font-setting', function(){
    var font = $(this).attr('data-font');
    $('.font-setting-btn.font-setting[data-font-add=' + font + ']').html(loader);
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

$(document).on('click', '.font-default-setting-btn.font-setting', function(){
    var name = $(this).attr('data-name');
    var font, size;
    if(name == "menu"){
        font = $('.font-setting.menu-font.default-again').attr('data-default');
        size = $('.font-setting.menu-size.default-again').attr('data-default');
        $('select.font-setting[name=menu-font]').select2("val", font);
        $('select.font-setting[name=menu-size]').select2("val", size);
    }else if(name == "text"){
        font = $('.font-setting.text-font.default-again').attr('data-default');
        size = $('.font-setting.text-size.default-again').attr('data-default');
        $('select.font-setting[name=text-font]').select2("val", font);
        $('select.font-setting[name=text-size]').select2("val", size);
    }else if(name == "content"){
        font = $('.font-setting.content-font.default-again').attr('data-default');
        size = $('.font-setting.content-size.default-again').attr('data-default');
        $('select.font-setting[name=content-font]').select2("val", font);
        $('select.font-setting[name=content-size]').select2("val", size);
    }else if(name == "detail"){
        font = $('.font-setting.detail-font.default-again').attr('data-default');
        size = $('.font-setting.detail-size.default-again').attr('data-default');
        $('select.font-setting[name=detail-font]').select2("val", font);
        $('select.font-setting[name=detail-size]').select2("val", size);
    }else if(name == "print"){
        font = $('.font-setting.print-font-title.default-again').attr('data-default');
        size = $('.font-setting.print-size-title.default-again').attr('data-default');
        $('select.font-setting[name=print-font-title]').select2("val", font);
        $('select.font-setting[name=print-size-title]').select2("val", size);
        font = $('.font-setting.print-font-summary.default-again').attr('data-default');
        size = $('.font-setting.print-size-summary.default-again').attr('data-default');
        $('select.font-setting[name=print-font-summary]').select2("val", font);
        $('select.font-setting[name=print-size-summary]').select2("val", size);
        font = $('.font-setting.print-font-body.default-again').attr('data-default');
        size = $('.font-setting.print-size-body.default-again').attr('data-default');
        $('select.font-setting[name=print-font-body]').select2("val", font);
        $('select.font-setting[name=print-size-body]').select2("val", size);
    }
});

$(document).on('click', '.font-again-setting-btn.font-setting', function(){
    var name = $(this).attr('data-name');
    var font, size;
    if(name == "menu"){
        font = $('.font-setting.menu-font.default-again').attr('data-again');
        size = $('.font-setting.menu-size.default-again').attr('data-again');
        $('select.font-setting[name=menu-font]').select2("val", font);
        $('select.font-setting[name=menu-size]').select2("val", size);
    }else if(name == "text"){
        font = $('.font-setting.text-font.default-again').attr('data-again');
        size = $('.font-setting.text-size.default-again').attr('data-again');
        $('select.font-setting[name=text-font]').select2("val", font);
        $('select.font-setting[name=text-size]').select2("val", size);
    }else if(name == "content"){
        font = $('.font-setting.content-font.default-again').attr('data-again');
        size = $('.font-setting.content-size.default-again').attr('data-again');
        $('select.font-setting[name=content-font]').select2("val", font);
        $('select.font-setting[name=content-size]').select2("val", size);
    }else if(name == "detail"){
        font = $('.font-setting.detail-font.default-again').attr('data-again');
        size = $('.font-setting.detail-size.default-again').attr('data-again');
        $('select.font-setting[name=detail-font]').select2("val", font);
        $('select.font-setting[name=detail-size]').select2("val", size);
    }else if(name == "print"){
        font = $('.font-setting.print-font-title.default-again').attr('data-again');
        size = $('.font-setting.print-size-title.default-again').attr('data-again');
        $('select.font-setting[name=print-font-title]').select2("val", font);
        $('select.font-setting[name=print-size-title]').select2("val", size);
        font = $('.font-setting.print-font-summary.default-again').attr('data-again');
        size = $('.font-setting.print-size-summary.default-again').attr('data-again');
        $('select.font-setting[name=print-font-summary]').select2("val", font);
        $('select.font-setting[name=print-size-summary]').select2("val", size);
        font = $('.font-setting.print-font-body.default-again').attr('data-again');
        size = $('.font-setting.print-size-body.default-again').attr('data-again');
        $('select.font-setting[name=print-font-body]').select2("val", font);
        $('select.font-setting[name=print-size-body]').select2("val", size);
    }
});