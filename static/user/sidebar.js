/**
 * Created by Morteza on 12/25/2015.
 */

var menuRight = document.getElementById('cbp-spmenu-s2');

$(document).on("click", ".open-side-menu.show-grouping", function (e) {
    var elm = $(e.target).closest('.open-side-menu.show-grouping');
    var grouping = elm.attr('data-grouping');
    var side_bar_grouping = $('#side_bar_grouping');
    if(side_bar_grouping.attr('data-' + grouping) == 'true'){
        $('.sidebar-items.grouping').hide();
        $('.sidebar-items.grouping[data-grouping=' + grouping + ']').fadeIn();
        $('#news_grouping_type').attr('data-type', grouping);
        classie.add(this, 'active');
        classie.add(menuRight, 'cbp-spmenu-open');
        $(".__scrolling").niceScroll({
            cursorcolor: "#000",
            cursorwidth: "5px",
            railalign: "left",
            autohidemode: false,
            horizrailenabled: false
        });
    }else{
        var _loader = '<div class="text-center" style="margin-top: 210px;">' + loader.replace(/20/g, '50') + '</div>';
        $('.sidebar-items.grouping[data-grouping=' + grouping + ']').html(_loader);
        $.ajax({
            url: show_sidebar_url,
            type: 'post',
            data: [
                {name: '_xsrf', value: xsrf_token},
                {name: 'grouping', value: grouping}
            ],
            success: function (response) {
                var status = response['status'];
                var value = response['value'];
                if (status) {
                    $('.sidebar-items.grouping').hide();
                    $('.sidebar-items.grouping[data-grouping=' + grouping + ']').html(value).fadeIn();
                    $('#news_grouping_type').attr('data-type', grouping);
                    side_bar_grouping.attr('data-' + grouping, 'true');
                }
            }
        });
        classie.add(this, 'active');
        classie.add(menuRight, 'cbp-spmenu-open');
        $(".__scrolling").niceScroll({
            cursorcolor: "#000",
            cursorwidth: "5px",
            railalign: "left",
            autohidemode: false,
            horizrailenabled: false
        });
    }
});