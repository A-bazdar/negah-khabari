/**
 * Created by Morteza on 12/24/2015.
 */


$(document).on('click', '.show-modal', function (e) {
    var elm = $(e.target);
    var _elm;
    var modal = elm.closest('.show-modal').attr('data-modal');
    var modal_id = elm.closest('.show-modal').attr('data-modal-id');
    var __modals = $('#modals');
    if(__modals.attr('data-' + modal) == 'true'){
        if(modal == "OptionNews"){
            _elm = $("div.option-news.div-images", e.target);
            var images = _elm.html().replace(/__src/g, 'src');
            $('#option_news_body').html(images);
        }
        if(modal == "PreParePrint"){
            _elm = $(e.target);
            var news = _elm.attr('data-news');
            $('#news_print_option_news').val(news);
        }
        if(modal == "UserInfo"){
            _elm = $(e.target);
            var tab = _elm.attr('data-modal-tab');
            $('.general_settings_tab[data-action=' + tab + ']').click();
        }
        if(modal == "FontSetting"){
            create_font_setting();
        }
        $('#' + modal_id).modal('toggle');
    }else{
        $.ajax({
            url: show_modal_url,
            type: 'post',
            data: [
                {name: '_xsrf', value: xsrf_token},
                {name: 'modal', value: modal}
            ],
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                if (status) {
                    __modals.append(value).attr('data-' + modal, 'true');
                    if(modal == "OptionNews"){
                        _elm = $("div.option-news.div-images", e.target);
                        var images = _elm.html().replace(/__src/g, 'src');
                        $('#option_news_body').html(images);
                    }
                    if(modal == "PreParePrint"){
                        _elm = $(e.target);
                        var news = _elm.attr('data-news');
                        $('#news_print_option_news').val(news);
                    }
                    if(modal == "UserInfo"){
                        _elm = $(e.target);
                        var tab = _elm.attr('data-modal-tab');
                        $('.general_settings_tab[data-action=' + tab + ']').click();
                    }
                    if(modal == "FontSetting"){
                        create_font_setting();
                    }
                    if(modal == "PatternSearch"){
                        $(".select2_keywords.pattern-search").select2({
                            tags: []
                        });
                        $('input.pattern-search.agency[type=checkbox]').lc_switch();

                        $("form#pattern_search_form .pattern-search[name=period]").select2({
                            placeholder: "?????? ????"
                        }).on("change", function () {
                            if ($(this).select2("val") == 'period') {
                                $('form#pattern_search_form .period-date').fadeIn();
                            } else {
                                $('form#pattern_search_form .period-date').fadeOut();
                            }
                        });
                    }
                    $('select.new_select').select2().removeClass('new_select');
                    $('#' + modal_id).modal('toggle');
                }
            }
        })
    }
});