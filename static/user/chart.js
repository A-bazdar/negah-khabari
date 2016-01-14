/**
 * Created by Morteza on 1/12/2016.
 */

function create_pie_chart(__div_id, __data_provider){
    AmCharts.makeChart( __div_id, {
        "type": "pie",
        "theme": "light",
        "dataProvider": __data_provider,
        "titleField": "title",
        "valueField": "value",
        "labelRadius": 8,

        "radius": "42%",
        "innerRadius": "60%",
        "labelText": "[[title]]",
        "export": {
            "enabled": true
        }
    });
}

function create_bar_chart(__div_id, __categories, __series){
    $('#' + __div_id).highcharts({
        chart: {
            type: 'column'
        },
        xAxis: {
            categories: __categories,
            crosshair: true
        },
        tooltip: {
            headerFormat: '<span style="font-size:10px">{point.key}</span><table>',
            pointFormat: '<tr><td style="color:{series.color};padding:0">{series.name}: </td><td style="padding:0"><b>{point.y:.1f}</b></td></tr>',
            footerFormat: '</table>',
            shared: true,
            useHTML: true
        },
        plotOptions: {
            column: {
                pointPadding: 0.2,
                borderWidth: 0
            }
        },
        series: __series
    });

}

function create_bar_chart_2(__div_id, __categories, __series){
    $('#' + __div_id).highcharts({
        chart: {
            type: 'column'
        },
        xAxis: {
            categories: __categories
        },
        yAxis: {
            min: 0,
            stackLabels: {
                enabled: true,
                style: {
                    fontWeight: 'bold',
                    color: (Highcharts.theme && Highcharts.theme.textColor) || 'gray'
                }
            }
        },
        plotOptions: {
            column: {
                stacking: 'normal',
                dataLabels: {
                    enabled: true,
                    color: (Highcharts.theme && Highcharts.theme.dataLabelsColor) || 'white',
                    style: {
                        textShadow: '0 0 3px black'
                    }
                }
            }
        },
        series: __series
    });

}