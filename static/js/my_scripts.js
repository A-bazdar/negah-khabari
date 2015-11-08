/**
 * Created by Omid on 9/29/2015.
 */

$('.right_tabs').click(function(){
    $('.right_tabs.active').removeClass('active');
    $(this).addClass('active');
    var action = $(this).attr('data-action');
    $('.main_content').css('display','none');
    $('.main_content[data-action=' + action + ']').fadeIn();
});

$('.check_new').click(function(){
    var new_id = $(this).attr('data-id');
    if($(this).prop("checked")){
        $('.content_row[data-id=' + new_id + ']').css('background','#BFD0E4');
        var html = '<div class="col-md-5 col-sm-5 col-xs-5 additional_options" style="padding-top: 10px">' +
                '<div class="row">' +
                '<div class="col-md-3 col-sm-3 col-xs-3" style="padding-left: 5px; padding-right: 5px"><select style="width: 100%"><option>اصلی</option><option>اصلی</option></select></div>' +
                '<div class="col-md-3 col-sm-3 col-xs-3" style="padding-left: 5px; padding-right: 5px"><select style="width: 100%"><option>اصلی</option><option>اصلی</option></select></div>' +
                '<div class="col-md-3 col-sm-3 col-xs-3" style="padding-left: 5px; padding-right: 5px"><select style="width: 100%"><option>اصلی</option><option>اصلی</option></select></div>' +
                '<div class="col-md-3 col-sm-3 col-xs-3" style="padding-left: 5px; padding-right: 5px"><select style="width: 100%"><option>اصلی</option><option>اصلی</option></select></div>' +
                '</div>' +
                '</div>' +
                '<div class="col-md-1 col-sm-1 col-xs-1 additional_options" style="padding-left: 5px; padding-right: 5px" style="padding-top: 10px"><i class="fa fa-share-square-o cursor-pointer" style="vertical-align: -14px"></i><i class="fa fa-trash-o cursor-pointer" style="margin-right: 10px; vertical-align: -13px"></i> </div>';
        $('.content_row[data-id=' + new_id + '] .row').append(html);
    }
    else{
        $('.content_row[data-id=' + new_id + ']').css('background','#ffffff');
        $('.content_row[data-id=' + new_id + '] .row .additional_options').remove();
    }
});
