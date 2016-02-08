/**
 * Created by Morteza on 1/26/2016.
 */

$(document).on('click', '.add-comparative-btn.agency', function(e){
    var elm = $(e.target).closest('.add-comparative-btn.agency');
    var _type = elm.attr('data-type');
    $('li.news-comparative-li[data-type=' + _type + ']').removeClass('active');
    $('.tab_content.add-comparative-con.agency[data-type=' + _type + ']').hide();
    var action = parseInt(Math.random() * 100000);
    var __sort = 1;
    $.each($('.add-comparative-tabs.agency[data-type=' + _type + '] li'), function(){__sort += 1});
    $('.add-comparative-tabs.agency[data-type=' + _type + ']').append('<li role="presentation" data-comparative="' + action + '" data-type="' + _type + '" data-sort="' + __sort + '" class="active news-comparative-li drag">\
        <a class="dir_tab tab-comparative-agency draggable" data-type="' + _type + '" data-comparative="' + action + '" aria-controls="source" role="tab" data-toggle="tab">\
            <i class="fa fa-times remove-comparative-news agency colorRed" data-comparative="' + action + '"> </i> <span> لینک</span>\
            </a>\
    </li>');
    $('.add-comparative-contents.agency[data-type=' + _type + ']').append($("#comparatives_content").html().replace(/__comparative__/g, action).replace(/__type__/g, _type).replace(/ temp/g, ''));
    $('.add-comparative-contents.agency[data-type=' + _type + '] .new_select').select2().removeClass('new_select').addClass('select');
    $('.tab_content.add-comparative-con.agency[data-type=' + _type + '][data-comparative=' + action + ']').fadeIn();
});

$(document).on('click', '.dir_tab.tab-comparative-agency', function(){
    var data_action = $(this).attr('data-comparative');
    var _type = $(this).attr('data-type');
    $('.tab_content.add-comparative-con.agency[data-type=' + _type + ']').hide();
    $('li.news-comparative-li[data-type=' + _type + ']').removeClass('active');
    $(this).closest('li.news-comparative-li').addClass('active');
    $('.tab_content.add-comparative-con.agency[data-type=' + _type + '][data-comparative=' + data_action + ']').fadeIn();
});

$(document).on('click', '.dir_tab.tab-address-agency', function(){
    var data_action = $(this).attr('data-action');
    var data_comparative = $(this).attr('data-comparative');
    $('.tab_content.add-address-con.agency[data-comparative=' + data_comparative + ']').hide();
    $('li.news-address-li[data-comparative=' + data_comparative + ']').removeClass('active');
    $(this).closest('li.news-address-li[data-comparative=' + data_comparative + ']').addClass('active');
    $('.tab_content.add-address-con.agency[data-action=' + data_action + '][data-comparative=' + data_comparative + ']').fadeIn();
});

$(document).on('click', '.remove-comparative-news.agency', function(){
    var data_action = $(this).closest('a').attr('data-comparative');
    var data_type = $(this).closest('a').attr('data-type');
    $(this).closest('li.news-comparative-li').remove();
    var __sort = 1;
    $.each($('.add-comparative-tabs.agency[data-type=' + data_type + '] li'), function(){$(this).attr('data-sort', __sort);__sort += 1});
    $('.tab_content.add-comparative-con.agency[data-comparative=' + data_action + '][data-type=' + data_type + ']').remove();
});

$(document).on('change', 'select.comparative-news[name=subject], select.comparative-news[name=group]', function(e){
    var elm = $(e.target);
    elm = elm.closest('.tab_content.add-comparative-con.agency');
    var __subject = elm.find("select.comparative-news[name=subject] option:selected");

    var __group = elm.find("select.comparative-news[name=group] option:selected");
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
    var action = $(this).closest('.add-comparative-con.agency').attr("data-comparative");
    if(tab_text != "") {
        $('.dir_tab.tab-comparative-agency[data-comparative=' + action + '] span').html(tab_text);
    }else{
        $('.dir_tab.tab-comparative-agency[data-comparative=' + action + '] span').html('لینک');
    }
});

$(document).on('change', 'select.change-date-format', function(){
    var comparative = $(this).attr('data-comparative');
    var type = $('select[data-comparative=' + comparative + '] option:selected').attr('data-type');
    $('span.date-format[data-comparative=' + comparative + ']').hide();
    $('span.date-format[data-comparative=' + comparative + '][data-type=' + type + ']').fadeIn()
});

$(document).on('click', '.add-exclude-comparative', function(e){
    var elm = $(e.target).closest('.add-exclude-comparative');
    var data_comparative = elm.attr('data-comparative');
    $('.excludes-comparative[data-comparative=' + data_comparative + ']').append(html_exclude.replace(/__value__/g, ""));
});

$(document).on('click', '.delete-exclude', function(e){
    $(e.target).closest('.row-exclude').remove();
});

$(document).on('click', '.add-comparative-rss-btn.agency', function(e){
    var elm = $(e.target).closest('.add-comparative-rss-btn.agency');
    var _type = elm.attr('data-type');
    $('.comparative-row-divs[data-type=' + _type + ']').append($('#comparative_rss_content').html().replace(/__type__/g , _type));
    $('.comparative-row-divs[data-type=' + _type + '] .new_select').select2().removeClass('new_select').addClass('select');
});

$(document).on('click', '.delete-rss-btn.agency', function(e){
    $(e.target).closest('.rss-row').remove();
});
