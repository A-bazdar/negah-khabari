/**
 * Created by Morteza on 1/26/2016.
 */

$(document).on('click', '.add-rss-btn.agency', function(e){
    var elm = $(e.target).closest('.add-rss-btn.agency');
    var _type = elm.attr('data-type');
    $('li.news-rss-li[data-type=' + _type + ']').removeClass('active');
    $('.tab_content.add-rss-con.agency[data-type=' + _type + ']').hide();
    var action = parseInt(Math.random() * 100000);
    var __sort = 1;
    $.each($('.add-rss-tabs.agency[data-type=' + _type + '] li'), function(){__sort += 1});
    $('.add-rss-tabs.agency[data-type=' + _type + ']').append('<li role="presentation" data-rss="' + action + '" data-type="' + _type + '" data-sort="' + __sort + '" class="active news-rss-li drag">\
        <a class="dir_tab tab-rss-agency draggable" data-type="' + _type + '" data-rss="' + action + '" aria-controls="source" role="tab" data-toggle="tab">\
            <i class="fa fa-times remove-rss-news agency colorRed" data-rss="' + action + '"> </i> <span> لینک</span>\
            </a>\
    </li>');
    $('.add-rss-contents.agency[data-type=' + _type + ']').append($("#rss_content").html().replace(/__rss__/g, action).replace(/__type__/g, _type).replace(/ temp/g, ''));
    $('.add-rss-contents.agency[data-type=' + _type + '] .new_select').select2().removeClass('new_select').addClass('select');
    $('.tab_content.add-rss-con.agency[data-type=' + _type + '][data-rss=' + action + ']').fadeIn();
});

$(document).on('click', '.dir_tab.tab-rss-agency', function(){
    var data_action = $(this).attr('data-rss');
    var _type = $(this).attr('data-type');
    $('.tab_content.add-rss-con.agency[data-type=' + _type + ']').hide();
    $('li.news-rss-li[data-type=' + _type + ']').removeClass('active');
    $(this).closest('li.news-rss-li').addClass('active');
    $('.tab_content.add-rss-con.agency[data-type=' + _type + '][data-rss=' + data_action + ']').fadeIn();
});

$(document).on('click', '.dir_tab.tab-address-agency', function(){
    var data_action = $(this).attr('data-action');
    var data_rss = $(this).attr('data-rss');
    $('.tab_content.add-address-con.agency[data-rss=' + data_rss + ']').hide();
    $('li.news-address-li[data-rss=' + data_rss + ']').removeClass('active');
    $(this).closest('li.news-address-li[data-rss=' + data_rss + ']').addClass('active');
    $('.tab_content.add-address-con.agency[data-action=' + data_action + '][data-rss=' + data_rss + ']').fadeIn();
});

$(document).on('click', '.remove-rss-news.agency', function(){
    var data_action = $(this).closest('a').attr('data-rss');
    var data_type = $(this).closest('a').attr('data-type');
    $(this).closest('li.news-rss-li').remove();
    var __sort = 1;
    $.each($('.add-rss-tabs.agency[data-type=' + data_type + '] li'), function(){$(this).attr('data-sort', __sort);__sort += 1});
    $('.tab_content.add-rss-con.agency[data-rss=' + data_action + '][data-type=' + data_type + ']').remove();
});

$(document).on('change', 'select.rss-news[name=subject]', function(){
    var s = $("option:selected", this).attr('data-name');
    if(s != "") {
        var action = $(this).closest('.add-rss-con.agency').attr("data-rss");
        $('.dir_tab.tab-rss-agency[data-rss=' + action + '] span').html(s);
    }
});


$(document).on('change', 'select.rss-news[name=subject], select.rss-news[name=group]', function(e){
    var elm = $(e.target);
    elm = elm.closest('.tab_content.add-rss-con.agency');
    var __subject = elm.find("select.rss-news[name=subject] option:selected");
    var __group = elm.find("select.rss-news[name=group] option:selected");
    var subject_name = __subject.attr('data-name');
    var subject_parent_name = __subject.attr('data-parent-name');
    var group_name = __group.attr('data-name');
    var group_parent_name = __group.attr('data-parent-name');
    var subject_text = "";
    var group_text = "";
    if(subject_name != ""){
        subject_text += subject_name;
        if(subject_parent_name != ""){
            subject_text = subject_parent_name + " / " + subject_text
        }
    }
    if(group_name != ""){
        group_text += group_name;
        if(group_parent_name != ""){
            group_text = group_parent_name + " / " + group_text
        }
    }
    var tab_text = "";
    if(subject_text != ""){
        tab_text += subject_text;
    }
    if(group_text != "") {
        if (subject_text != "")
            tab_text += " | " + group_text;
        else
            tab_text += group_text;
    }
    var action = $(this).closest('.add-rss-con.agency').attr("data-rss");
    if(tab_text != "") {
        $('.dir_tab.tab-rss-agency[data-rss=' + action + '] span').html(tab_text);
    }else{
        $('.dir_tab.tab-rss-agency[data-rss=' + action + '] span').html('لینک');
    }
});

$(document).on('change', 'select.change-date-format', function(){
    var rss = $(this).attr('data-rss');
    var type = $('select[data-rss=' + rss + '] option:selected').attr('data-type');
    $('span.date-format[data-rss=' + rss + ']').hide();
    $('span.date-format[data-rss=' + rss + '][data-type=' + type + ']').fadeIn()
});

var html_exclude = '<div class="col-md-12 row-exclude">\
    <div class="row">\
        <div class="col-md-10">\
            <input type="text" class="form-control text-left" data-rss="new-rss-1" placeholder="Address" name="exclude">\
        </div>\
        <div class="col-md-2">\
            <div class="R_butt_red text-center delete-exclude" data-action="body" data-rss="new-rss-1"><i class="fa fa-times"></i></div>\
        </div>\
    </div>\
</div>';

$(document).on('click', '.add-exclude-rss', function(e){
    var elm = $(e.target).closest('.add-exclude-rss');
    var data_rss = elm.attr('data-rss');
    $('.excludes-rss[data-rss=' + data_rss + ']').append(html_exclude.replace(/__value__/g, ""));
});

$(document).on('click', '.delete-exclude', function(e){
    $(e.target).closest('.row-exclude').remove();
});