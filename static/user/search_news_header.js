/**
 * Created by Morteza on 12/7/2015.
 */

function create_expert_search(){
    $('form#header_search_news .new_select').select2().removeClass('new_select');

    $("form#header_search_news .new_select2_keywords").select2({
        tags: []
    }).removeClass('new_select2_keywords');

    $("form#header_search_news .new_select_change[name=period]").select2({
        placeholder: "انتخاب کنید"
    }).on("change", function () {
        if ($(this).select2("val") == 'period') {
            $('.header-period-date').fadeIn();
        } else {
            $('.header-period-date').fadeOut();
        }
    }).removeClass('new_select_change');

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
                    for (var i = 0; i < output3['agency'].length; i++) {
                        options += "<option value='" + output3['agency'][i]['id'] + "'>" + output3['agency'][i]['text'] + "</option>";
                    }
                }
                $(".select.search-news[name=header-agency]").select2("data", []).html(options);
            }
        });
    });
}