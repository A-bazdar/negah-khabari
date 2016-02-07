/**
 * Created by Abolfazl on 03/02/2016.
 */

var copy_link = {
    links: "",
    has_ro_title: true,
    ro_title: "",
    title: "",
    has_summary: true,
    summary: "",
    thumbnail: "",
    body: "",
    date: "",
    __date: "",
    date_format: "",
    date_format_val: "تاریخ انتشار: %d %B %Y - %H:%"
};

$(document).on('click', '.copy-address', function(e){
    var elm = $(e.target);
    var row = elm.closest('.tab-content-row.agency');
    var date_format = row.find('select[name=date-format] option:selected').attr("data-type");
    var __date = date_format;
    if (date_format == "new_template") {
        date_format = row.find('input[name=new-template-date-format]').val();
    }
    var excludes = [];
    $.each(row.find('input[name=exclude]'), function(){
        excludes.push($(this).val());
    });
    var links = row.find('input[name=links]').val();
    if(links == undefined)
        links = row.find('input[name=comparatives]').val();
    copy_link = {
        links: links,
        has_ro_title: row.find('input[name=has-ro-title]').prop('checked'),
        ro_title: row.find('input[name=ro_title]').val(),
        title: row.find('input[name=title]').val(),
        has_summary: row.find('input[name=has-summary]').prop('checked'),
        summary: row.find('input[name=summary]').val(),
        thumbnail: row.find('input[name=thumbnail]').val(),
        body: row.find('input[name=body]').val(),
        date: row.find('input[name=date]').val(),
        __date: __date,
        excludes: excludes,
        date_format_val: row.find('select[name=date-format]').select2("val"),
        date_format: date_format
    };
});

$(document).on('click', '.paste-address', function(e){
    var elm = $(e.target);
    var row = elm.closest('.tab-content-row.agency');
    if (copy_link['__date'] == "new_template") {
        row.find('.date-format').hide();
        row.find('.date-format[data-type=new_template]').show();
        row.find('select[name=date-format]').select2("val", "new_template");
        row.find('input[name=new-template-date-format]').val(copy_link['date_format']);
    }else{
        row.find('.date-format').hide();
        row.find('.date-format[data-type=' + copy_link['__date'] + ']').show();
        row.find('select[name=date-format]').select2("val", copy_link['date_format_val']);
    }
    var excludes = "";
    for(var i = 0 ; i < copy_link['excludes'].length ; i++){
        excludes += html_exclude.replace(/__value__/g, copy_link['excludes'][i]);
    }
    row.find('.excludes').html(excludes);
    if(copy_link['links']){

    }
    row.find('input[name=links]').val(copy_link['links']);
    row.find('input[name=comparatives]').val(copy_link['links']);
    row.find('input[name=has-ro-title]').prop('checked', copy_link['has_ro_title']);
    if(!copy_link['has_ro_title'])
        row.find('input[name=ro_title]').val("").attr('disabled', 'disabled');
    row.find('input[name=ro_title]').val(copy_link['ro_title']);
    row.find('input[name=has-summary]').prop('checked', copy_link['has_summary']);
    if(!copy_link['has_summary'])
        row.find('input[name=summary]').val("").attr('disabled', 'disabled');
    row.find('input[name=summary]').val(copy_link['summary']);
    row.find('input[name=title]').val(copy_link['title']);
    row.find('input[name=summary]').val(copy_link['summary']);
    row.find('input[name=thumbnail]').val(copy_link['thumbnail']);
    row.find('input[name=body]').val(copy_link['body']);
    row.find('input[name=date]').val(copy_link['date']);
});