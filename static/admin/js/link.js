/**
 * Created by Morteza on 1/26/2016.
 */

$(document).on('click', '.add-link-btn.agency', function(e){
    var elm = $(e.target).closest('.add-link-btn.agency');
    var _type = elm.attr('data-type');
    $('li.news-link-li[data-type=' + _type + ']').removeClass('active');
    $('.tab_content.add-link-con.agency[data-type=' + _type + ']').hide();
    var action = parseInt(Math.random() * 100000);
    var __sort = 1;
    $.each($('.add-link-tabs.agency[data-type=' + _type + '] li'), function(){__sort += 1});
    $('.add-link-tabs.agency[data-type=' + _type + ']').append('<li role="presentation" data-link="' + action + '" data-type="' + _type + '" data-sort="' + __sort + '" class="active news-link-li drag">\
        <a class="dir_tab tab-link-agency draggable" data-type="' + _type + '" data-link="' + action + '" aria-controls="source" role="tab" data-toggle="tab">\
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
    var data_action = $(this).closest('a').attr('data-link');
    var data_type = $(this).closest('a').attr('data-type');
    $(this).closest('li.news-link-li').remove();
    var __sort = 1;
    $.each($('.add-link-tabs.agency[data-type=' + data_type + '] li'), function(){$(this).attr('data-sort', __sort);__sort += 1});
    $('.tab_content.add-link-con.agency[data-link=' + data_action + '][data-type=' + data_type + ']').remove();
});

$(document).on('change', 'select.link-news[name=subject], select.link-news[name=group]', function(e){
    var elm = $(e.target);
    elm = elm.closest('.tab_content.add-link-con.agency');
    var __subject = elm.find("select.link-news[name=subject] option:selected");

    var __group = elm.find("select.link-news[name=group] option:selected");
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
    var action = $(this).closest('.add-link-con.agency').attr("data-link");
    if(tab_text != "") {
        $('.dir_tab.tab-link-agency[data-link=' + action + '] span').html(tab_text);
    }else{
        $('.dir_tab.tab-link-agency[data-link=' + action + '] span').html('لینک');
    }
});

$(document).on('change', 'select.change-date-format', function(){
    var link = $(this).attr('data-link');
    var type = $('select[data-link=' + link + '] option:selected').attr('data-type');
    $('span.date-format[data-link=' + link + ']').hide();
    $('span.date-format[data-link=' + link + '][data-type=' + type + ']').fadeIn()
});

$(document).on('click', '.add-exclude', function(e){
    var elm = $(e.target).closest('.add-exclude');
    var data_link = elm.attr('data-link');
    $('.excludes[data-link=' + data_link + ']').append(html_exclude.replace(/__value__/g, ""));
});
$(document).on('click', '.delete-exclude', function(e){
    $(e.target).closest('.row-exclude').remove();
});