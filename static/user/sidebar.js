/**
 * Created by Morteza on 12/25/2015.
 */

var menuRight = document.getElementById('cbp-spmenu-s2');

function make_sortable(){
    $('.pr_drag').sortable({
        connectWith: '.pr_drag',
        handle: 'div.draggable',
        cursor: 'move',
        placeholder: 'placeholder',
        forcePlaceholderSize: true,
        opacity: 0.4,
        stop: function (event, ui) {
            $(ui.item).find('div.draggable').click();
            var grouping_type = $('#news_grouping_type').attr('data-type');
            var postData = [{name: '_xsrf', value: xsrf_token}, {name: 'grouping', value: grouping_type}];
            $.each($('form.pr_drag[data-grouping=' + grouping_type + '] div.drag'), function(){
                postData.push({name: 'item', value: $(this).attr('data-id')});
            });
            $.ajax({url: show_sidebar_url, type: 'put', data: postData});
        }
    })
}

$(document).on("click", ".open-side-menu.show-grouping", function (e) {
    var elm = $(e.target).closest('.open-side-menu.show-grouping');
    var grouping = elm.attr('data-grouping');
    var side_bar_grouping = $('#side_bar_grouping');
    if(side_bar_grouping.attr('data-' + grouping) == 'true'){
        $('.sidebar-items.grouping').hide();
        $('.sidebar-items.grouping.active').removeClass('active');
        $('.sidebar-items.grouping[data-grouping=' + grouping + ']').addClass('active').fadeIn();
        $('#news_grouping_type').attr('data-type', grouping);
        classie.add(this, 'active');
        classie.add(menuRight, 'cbp-spmenu-open');
        $(".__scrolling").niceScroll({
            cursorcolor: "#000",
            cursorwidth: "5px",
            railalign: "right",
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
                    $('.sidebar-items.grouping.active').removeClass('active');
                    $('.sidebar-items.grouping[data-grouping=' + grouping + ']').addClass('active').html(value).fadeIn();
                    $('#news_grouping_type').attr('data-type', grouping);
                    side_bar_grouping.attr('data-' + grouping, 'true');
                    make_sortable();
                }
            }
        });
        classie.add(this, 'active');
        classie.add(menuRight, 'cbp-spmenu-open');
        $(".__scrolling").niceScroll({
            cursorcolor: "#000",
            cursorwidth: "5px",
            railalign: "right",
            autohidemode: false,
            horizrailenabled: false
        });
    }
});

$(document).on('click','.close-chp-menu', function(){
    $('.cbp-spmenu.cbp-spmenu-open').removeClass('cbp-spmenu-open');
    $(".cbp-spmenu.__scrolling").getNiceScroll().remove();
});