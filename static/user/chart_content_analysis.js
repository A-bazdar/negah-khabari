/**
 * Created by Morteza on 1/12/2016.
 */

$(document).on('click', '.chart-content-analysis.chart-content-analysis-tabs', function (e) {
    var data_action = $(this).attr('data-action');
    $('.tab_content.chart-content-analysis').hide();
    $('.tab_content.chart-content-analysis[data-action=' + data_action + ']').fadeIn();
});


$(document).on('click', '#show_chart_content_analysis_modal', function (e) {
    var elm = $(e.target).closest('.chart-content-analysis');
    var open = elm.attr('data-open');
    if(open == "true"){
        $('#chart_content_analysis').modal('toggle');
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
                        $('.tab_content.chart-content-analysis[data-action=content_format]').html(value['html']);
                        create_pie_chart("pie_chart_content_format", value['result']['contents']);
                        create_bar_chart("bar_chart_content_format", value['categories'], value['series']);
                        elm.attr('data-open', 'true');
                        $('#chart_content_analysis').modal('toggle');
                    }
                }
            });
    }
});
