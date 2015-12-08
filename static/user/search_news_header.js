/**
 * Created by Morteza on 12/7/2015.
 */

$('select.header-category.search-news').select2().on("change", function(){
    var options = "";
    $.ajax({
        data: {cid: $(this).select2("val"), _xsrf: xsrf_token},
        type: 'post',
        cache: true,
        url: get_agency_url,
        async: true,
        success: function (output3) {
            if (output3 != '0' && output3['agency'].length > 0) {
                for (var i in output3['agency']) {
                    options += "<option value='" + output3['agency'][i]['id'] + "'>" + output3['agency'][i]['name'] + "</option>";
                }
            }
            $(".select.search-news[name=header-agency]").select2("data", []).html(options);
        }, complete: function (output) {
        }
    });
});

$(".select[name=header-period]").select2({
    placeholder: "انتخاب کنید"
}).on("change", function () {
    if ($(this).select2("val") == 'period') {
        $('.header-period-date').fadeIn();
    } else {
        $('.header-period-date').fadeOut();
    }
});