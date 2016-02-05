/**
 * Created by Morteza on 1/12/2016.
 */

//$(document).on('click', '.chart-content-analysis.chart-content-analysis-tabs', function (e) {
//    var data_action = $(this).attr('data-action');
//    $('.tab_content.chart-content-analysis').hide();
//    $('.tab_content.chart-content-analysis[data-action=' + data_action + ']').fadeIn();
//});


$(document).on('click', '#show_chart_content_analysis_modal', function (e) {
    $(".chart-content-date-picker").persianDatepicker();
    var chart_content_analysis = $('#chart_content_analysis');
    chart_content_analysis.modal('toggle');
    var elm = $(e.target).closest('.chart-content-analysis');
    var open = elm.attr('data-open');
    var action = $('.chart-content-analysis.chart-content-analysis-li.active').attr('data-action');
    var tab_content = $('.tab_content.chart-content-analysis[data-action=' + action + ']');
    if(open != "true"){
        jQuery.ajax(
            {
                url: chart_content_analysis_url,
                type: "post",
                data: [{name: '_xsrf', value: xsrf_token}, {name: 'action', value: action}],
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    if (status) {
                        tab_content.html(value['html']);
                        if(action == "content_format"){
                            create_pie_chart("pie_chart_content_format", value['contents']);
                            create_bar_chart("bar_chart_content_format", value['categories'], value['series']);
                        }
                        if(action == "performance_agency_number_news"){
                            create_pie_chart("pie_chart_performance_agency_number_news", value['contents']);
                            create_bar_chart("bar_chart_performance_agency_number_news", value['categories'], value['series']);
                        }
                        if(action == "daily_statistics_news"){
                            create_bar_chart("bar_chart_daily_statistics_news", value['categories'], value['series']);
                        }
                        if(action == "important_topic_news"){
                            create_bar_chart_2("bar_chart_2_important_topic_news", value['categories'], value['series']);
                        }
                        if(action == "important_keyword_news"){
                            create_bar_chart_2("bar_chart_2_important_keyword_news", value['categories'], value['series']);
                        }
                        if(action == "content_direction"){
                            create_pie_chart("pie_chart_content_direction", value['contents']);
                            create_bar_chart("bar_chart_content_direction", value['categories'], value['series']);
                        }
                        if(action == "agency_direction"){
                            create_pie_chart("pie_chart_agency_direction", value['contents']);
                            create_bar_chart("bar_chart_agency_direction", value['categories'], value['series']);
                        }
                        if(action == "important_news_maker"){
                            create_bar_chart_2("bar_chart_2_important_news_maker", value['categories'], value['series']);
                        }
                        $('.tab_content.chart-content-analysis').hide();
                        tab_content.fadeIn();
                        elm.attr('data-open', 'true');
                    }
                }
            });
    }
});


$(document).on('click', '.dir_tab.chart-content-analysis-tabs', function (e) {
    var elm = $(e.target).closest('.chart-content-analysis-tabs');
    var open = elm.attr('data-open');
    var action = elm.attr('data-action');
    $('.chart-content-analysis.chart-content-analysis-li.active').removeClass('active');
    $('.chart-content-analysis.chart-content-analysis-li[data-action=' + action + ']').addClass('active');
    $('.tab_content.chart-content-analysis').hide();
    $('.tab_content.chart-content-analysis[data-action=loader]').show();
    var _start = $('input.chart-content-date-picker[name=start]').val();
    var _end = $('input.chart-content-date-picker[name=end]').val();
    jQuery.ajax(
        {
            url: chart_content_analysis_url,
            type: "post",
            data: [{name: '_xsrf', value: xsrf_token}, {name: 'action', value: action},
                {name: '_start', value: _start}, {name: '_end', value: _end}],
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                if (status) {
                    var a = $('.tab_content.chart-content-analysis[data-action=' + action + ']');
                    a.html(value['html']);
                    if(action == "content_format"){
                        create_pie_chart("pie_chart_content_format", value['contents']);
                        create_bar_chart("bar_chart_content_format", value['categories'], value['series']);
                    }
                    if(action == "performance_agency_number_news"){
                        create_pie_chart("pie_chart_performance_agency_number_news", value['contents']);
                        create_bar_chart("bar_chart_performance_agency_number_news", value['categories'], value['series']);
                    }
                    if(action == "daily_statistics_news"){
                        create_bar_chart("bar_chart_daily_statistics_news", value['categories'], value['series']);
                    }
                    if(action == "important_topic_news"){
                        create_bar_chart_2("bar_chart_2_important_topic_news", value['categories'], value['series']);
                    }
                    if(action == "important_keyword_news"){
                        create_bar_chart_2("bar_chart_2_important_keyword_news", value['categories'], value['series']);
                    }
                    if(action == "content_direction"){
                        create_pie_chart("pie_chart_content_direction", value['contents']);
                        create_bar_chart("bar_chart_content_direction", value['categories'], value['series']);
                    }
                    if(action == "agency_direction"){
                        create_pie_chart("pie_chart_agency_direction", value['contents']);
                        create_bar_chart("bar_chart_agency_direction", value['categories'], value['series']);
                    }
                    if(action == "important_news_maker"){
                        create_bar_chart_2("bar_chart_2_important_news_maker", value['categories'], value['series']);
                    }
                    $('.tab_content.chart-content-analysis').hide();
                    a.show();
                    elm.attr('data-open', 'true');
                }
            }
        });
});


$(document).on('click', '.chart-content-analysis-change-date', function (e) {
    var elm = $(e.target).closest('.chart-content-analysis-tabs');
    var open = elm.attr('data-open');
    var action = $('.chart-content-analysis.chart-content-analysis-li.active').attr('data-action');
    $('.tab_content.chart-content-analysis').hide();
    $('.tab_content.chart-content-analysis[data-action=loader]').show();
    var _start = $('input.chart-content-date-picker[name=start]').val();
    var _end = $('input.chart-content-date-picker[name=end]').val();
    jQuery.ajax(
        {
            url: chart_content_analysis_url,
            type: "post",
            data: [{name: '_xsrf', value: xsrf_token}, {name: 'action', value: action},
                {name: '_start', value: _start}, {name: '_end', value: _end}],
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                if (status) {
                    var a = $('.tab_content.chart-content-analysis[data-action=' + action + ']');
                    a.html(value['html']);
                    if(action == "content_format"){
                        create_pie_chart("pie_chart_content_format", value['contents']);
                        create_bar_chart("bar_chart_content_format", value['categories'], value['series']);
                    }
                    if(action == "performance_agency_number_news"){
                        create_pie_chart("pie_chart_performance_agency_number_news", value['contents']);
                        create_bar_chart("bar_chart_performance_agency_number_news", value['categories'], value['series']);
                    }
                    if(action == "daily_statistics_news"){
                        create_bar_chart("bar_chart_daily_statistics_news", value['categories'], value['series']);
                    }
                    if(action == "important_topic_news"){
                        create_bar_chart_2("bar_chart_2_important_topic_news", value['categories'], value['series']);
                    }
                    if(action == "important_keyword_news"){
                        create_bar_chart_2("bar_chart_2_important_keyword_news", value['categories'], value['series']);
                    }
                    if(action == "content_direction"){
                        create_pie_chart("pie_chart_content_direction", value['contents']);
                        create_bar_chart("bar_chart_content_direction", value['categories'], value['series']);
                    }
                    if(action == "agency_direction"){
                        create_pie_chart("pie_chart_agency_direction", value['contents']);
                        create_bar_chart("bar_chart_agency_direction", value['categories'], value['series']);
                    }
                    if(action == "important_news_maker"){
                        create_bar_chart_2("bar_chart_2_important_news_maker", value['categories'], value['series']);
                    }
                    $('.tab_content.chart-content-analysis').hide();
                    a.show();
                    elm.attr('data-open', 'true');
                }
            }
        });
});
