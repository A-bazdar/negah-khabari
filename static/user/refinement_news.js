/**
 * Created by Morteza on 12/8/2015.
 */

function create_refinement_news(){
    var slideTop = new Menu({
        wrapper: '#o-wrapper',
        type: 'slide-top',
        menuOpenerClass: '.c-button',
        maskId: '#c-mask'
    });

    var slideTopBtn = document.querySelector('#c-button--slide-top');

    slideTopBtn.addEventListener('click', function (e) {
        e.preventDefault();
        slideTop.open();
    });
    $(".select2_keywords.refinement-news").select2({
        tags: []
    });

    $("form#refinement_news .refinement-news[name=period]").select2({
        placeholder: "انتخاب کنید"
    }).on("change", function () {
        if ($(this).select2("val") == 'period') {
            $('form#refinement_news .period-date').fadeIn();
        } else {
            $('form#refinement_news .period-date').fadeOut();
        }
    });

    $(document).on('click', '.filtration-news.show-slide', function (e) {
        var _data = [
            {name: "_xsrf", value: xsrf_token},
            {name: "action", value: 'get-all'}
        ];
        $.ajax({
            url: pattern_search_url,
            type: 'put',
            data: _data,
            success: function (response) {
                var status = response['status'];
                var messages = response['messages'];
                var value = response['value'];
                if (status) {
                    var html = '<li class="text-center"><input type="radio" checked name="pattern_search_show_refinement_news" value="nothing"><span style="vertical-align: 3px; margin-right: 10px">هیچ کدام</span><li>';
                    for (var i = 0; i < value.length; i++) {
                        html += '<input type="radio" name="pattern_search_show_refinement_news" value="' + value[i]['id'] + '"> ' + value[i]['name'];
                    }
                    $('.filtration-news-pattern-search').html(html);
                }
            }
        });
    });

    $(document).on('click', '.add-agency.refinement-news', function(){
        var agency_names = [];
        var agency_ids = [];
        var all = false;
        $.each($('input.refinement-news.agency:checked'), function(){
            if($(this).val() == 'all')
                all = true;
            agency_names.push({id: $(this).attr('data-name'), text: $(this).attr('data-name')});
            agency_ids.push($(this).val());
        });
        if(!all){
            $('input.refinement-news[name=agency]').val(agency_ids);
            $('input.refinement-news[name=agency_names]').select2("data", agency_names, true);
        }else{
            $('input.refinement-news[name=agency]').val("all");
            $('input.refinement-news[name=agency_names]').select2("data", [{'id': "همه منابع", text: 'همه منابع'}]);
        }
    });

    $(document).on('change', 'input[name=pattern_search_show_refinement_news]', function(){
        var pattern_id = $('input[name=pattern_search_show_refinement_news]:checked').val();
        if(pattern_id == 'nothing'){
            empty_refinement_news();
            return;
        }
        var postData = {
            pattern_id: pattern_id,
            _xsrf: xsrf_token
        };
        jQuery.ajax(
            {
                url: pattern_search_url,
                type: 'put',
                data: postData,
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    var messages = response['messages'];
                    if (!status) {
                        var error = '';
                        for(var i = 0; i < messages.length ; i++){
                            error += messages[i] + '<br>';
                        }
                        if(error == '')
                            error = 'متاسفانه در سیستم خطایی به وجود آمده، لطفا دوباره امتحان کنید.';
                        $('.errors').html(error);
                        __a = true;
                    }else{
                        $('input.refinement-news[type=checkbox]').prop('checked', false);
                        $('select.refinement-news[name=period]').select2("val", value['period']);
                        if(value['period'] == 'period'){
                            $('input.refinement-news[name=start-date]').val(value['start_date']);
                            $('input.refinement-news[name=end-date]').val(value['end_date']);
                            $('form#refinement_news .period-date').fadeIn();
                        }else{
                            $('form#refinement_news .period-date').fadeOut();
                            $('input.refinement-news[name=start-date]').val("");
                            $('input.refinement-news[name=end-date]').val("");
                        }

                        $('input.refinement-news[name=tags]').select2("data", value["tags"], true);
                        $('input.refinement-news[name=all-words]').select2("data", value["all_words"], true);
                        $('input.refinement-news[name=exactly-word]').val(value["exactly_word"]);
                        $('input.refinement-news[name=each-words]').select2("data", value["each_words"], true);
                        $('input.refinement-news[name=without-words]').select2("data", value["without_words"], true);
                        $('input.refinement-news[name=picture]').prop('checked', value["picture"]);
                        $('input.refinement-news[name=video]').prop('checked', value["video"]);
                        $('input.refinement-news[name=voice]').prop('checked', value["voice"]);
                        $('input.refinement-news[name=doc]').prop('checked', value["doc"]);
                        $('input.refinement-news[name=pdf]').prop('checked', value["pdf"]);
                        $('input.refinement-news[name=archive]').prop('checked', value["archive"]);
                        $('input.refinement-news[name=tag_title]').prop('checked', value["tag_title"]);
                        $('input.refinement-news[name=bolton]').prop('checked', value["bolton"]);
                        $('input.refinement-news[name=note]').prop('checked', value["note"]);
                        $('input.refinement-news[name=unread]').prop('checked', value["unread"]);
                        $('input.refinement-news[name=star]').prop('checked', value["star"]);
                        $('input.refinement-news[name=important1]').prop('checked', value["important1"]);
                        $('input.refinement-news[name=important2]').prop('checked', value["important2"]);
                        $('input.refinement-news[name=important3]').prop('checked', value["important3"]);
                        $('input.refinement-news[name=agency]').val(value['agency']);
                        $('input.refinement-news[name=agency_names]').select2("data", value['agency_names'], true);
                    }
                }
            });
    });

    $(document).on('click', '.empty-refinement-news', function() {
        empty_refinement_news();
    });
}

function empty_refinement_news(){
    $('input[name=pattern_search_show_refinement_news][value=nothing]').prop("checked", true);
    $('input.refinement-news[name=pattern-name]').val('');
    $('input.refinement-news[name=action]').val('add');
    $('input.refinement-news[type=checkbox]').prop('checked', false);
    $('input.refinement-news[name=pattern_id]').val('');
    $('select.refinement-news[name=period]').select2("val", "hour");
    $('form#refinement_news .period-date').fadeOut();
    $('input.refinement-news[name=start-date]').val('');
    $('input.refinement-news[name=end-date]').val('');
    $('table.table.refinement-news tr.empty').remove();
    $('input.refinement-news.select2_keywords').select2("data", [], true);
    $('input.refinement-news[name=exactly-word]').val('');
    $('input.refinement-news[name=agency]').val("");
    $('input.refinement-news[name=agency_names]').select2("data", [], true);
}