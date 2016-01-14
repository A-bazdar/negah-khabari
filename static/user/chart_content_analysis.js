/**
 * Created by Morteza on 1/12/2016.
 */

$(document).on('click', '.chart-content-analysis.chart-content-analysis-tabs', function (e) {
    var data_action = $(this).attr('data-action');
    $('.tab_content.chart-content-analysis').hide();
    $('.tab_content.chart-content-analysis[data-action=' + data_action + ']').fadeIn();
});


$(document).on('click', '#show_chart_content_analysis_modal', function (e) {
    var chart_content_analysis = $('#chart_content_analysis');
    $('.tab_content.chart-content-analysis').hide();
    $('.tab_content.chart-content-analysis[data-action=loader]').fadeIn();
    chart_content_analysis.modal('toggle');
    var elm = $(e.target).closest('.chart-content-analysis');
    var open = elm.attr('data-open');
    var tab_content = $('.tab_content.chart-content-analysis[data-action=content_format]');
    if(open == "true"){
        $('.tab_content.chart-content-analysis').hide();
        tab_content.fadeIn();
    }else{
        jQuery.ajax(
            {
                url: chart_content_analysis_url,
                type: "post",
                data: [{name: '_xsrf', value: xsrf_token}],
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    if (status) {
                        tab_content.html(value['html']);
                        create_pie_chart("pie_chart_content_format", value['contents']);
                        create_bar_chart("bar_chart_content_format", value['categories'], value['series']);
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
    if(open == "true"){
        $('.tab_content.chart-content-analysis').hide();
        $('.tab_content.chart-content-analysis[data-action=' + action + ']').show();
    }else{
        $('.tab_content.chart-content-analysis').hide();
        $('.tab_content.chart-content-analysis[data-action=loader]').show();
        jQuery.ajax(
            {
                url: chart_content_analysis_url,
                type: "post",
                data: [{name: '_xsrf', value: xsrf_token}, {name: 'action', value: action}],
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    if (status) {
                        var a = $('.tab_content.chart-content-analysis[data-action=' + action + ']');
                        a.html(value['html']);
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
                        $('.tab_content.chart-content-analysis').hide();
                        a.show();
                        elm.attr('data-open', 'true');
                    }
                }
            });
    }
});
