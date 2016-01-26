/**
 * Created by Morteza on 1/26/2016.
 */

$(document).on('click', '.add-link-btn.agency', function(e){
    var elm = $(e.target).closest('.add-link-btn.agency');
    var _type = elm.attr('data-type');
    $('li.news-link-li[data-type=' + _type + ']').removeClass('active');
    $('.tab_content.add-link-con.agency[data-type=' + _type + ']').hide();
    var action = parseInt(Math.random() * 100000);
    $('.add-link-tabs.agency[data-type=' + _type + ']').append('<li role="presentation" data-type="' + _type + '" class="active news-link-li">\
        <a class="dir_tab tab-link-agency" data-type="' + _type + '" data-link="' + action + '" aria-controls="source" role="tab" data-toggle="tab">\
            <i class="fa fa-times remove-link-news agency colorRed" data-link="' + action + '"> </i> <span> لینک</span>\
            </a>\
    </li>');
    $('.add-link-contents.agency[data-type=' + _type + ']').append($("#links_content").html().replace(/__link__/g, action).replace(/__type__/g, _type).replace(/ temp/g, ''));
    $('.add-link-contents.agency[data-type=' + _type + '] .new_select').select2().removeClass('new_select').addClass('select');
    $('.tab_content.add-link-con.agency[data-type=' + _type + '][data-link=' + action + ']').fadeIn();
});

$(document).on('click', '.dir_tab.tab-link-agency', function(){
    var data_action = $(this).attr('data-link');
    var _type = $(this).attr('data-type');
    $('.tab_content.add-link-con.agency[data-type=' + _type + ']').hide();
    $('li.news-link-li[data-type=' + _type + ']').removeClass('active');
    $(this).closest('li.news-link-li').addClass('active');
    $('.tab_content.add-link-con.agency[data-type=' + _type + '][data-link=' + data_action + ']').fadeIn();
});

$(document).on('click', '.dir_tab.tab-address-agency', function(){
    var data_action = $(this).attr('data-action');
    var data_link = $(this).attr('data-link');
    $('.tab_content.add-address-con.agency[data-link=' + data_link + ']').hide();
    $('li.news-address-li[data-link=' + data_link + ']').removeClass('active');
    $(this).closest('li.news-address-li[data-link=' + data_link + ']').addClass('active');
    $('.tab_content.add-address-con.agency[data-action=' + data_action + '][data-link=' + data_link + ']').fadeIn();
});

$(document).on('click', '.remove-link-news.agency', function(){
    var data_action = $(this).closest('a').attr('data-action');
    $(this).closest('li.news-link-li').remove();
    $('.tab_content.add-link-con.agency[data-action=' + data_action + ']').remove();
});

$(document).on('change', 'select.link-news[name=subject]', function(){
    var s = $("option:selected", this).attr('data-name');
    if(s != "") {
        var action = $(this).closest('.add-link-con.agency').attr("data-link");
        $('.dir_tab.tab-link-agency[data-link=' + action + '] span').html(s);
    }
});

$(document).on('change', 'select.change-date-format', function(){
    var link = $(this).attr('data-link');
    var type = $('select[data-link=' + link + '] option:selected').attr('data-type');
    $('span.date-format[data-link=' + link + ']').hide();
    $('span.date-format[data-link=' + link + '][data-type=' + type + ']').fadeIn()
});

var html_exclude = '<div class="col-md-12 row-exclude">\
    <div class="row">\
        <div class="col-md-10">\
            <input type="text" class="form-control text-left" data-link="new-link-1" placeholder="Address" name="exclude">\
        </div>\
        <div class="col-md-2">\
            <div class="R_butt_red text-center test-address-agency delete-exclude" data-action="body" data-link="new-link-1"><i class="fa fa-times"></i></div>\
        </div>\
    </div>\
</div>';
$(document).on('click', '.add-exclude', function(e){
    var elm = $(e.target).closest('.add-exclude');
    var data_link = elm.attr('data-link');
    $('.excludes[data-link=' + data_link + ']').append(html_exclude);
});
$(document).on('click', '.delete-exclude', function(e){
    $(e.target).closest('.row-exclude').remove();
});