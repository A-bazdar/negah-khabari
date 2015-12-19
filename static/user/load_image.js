/**
 * Created by Morteza on 12/19/2015.
 */

function load_news() {
    $.each($("img.new_news_img"), function () {
        $(this).attr("src", $(this).attr("data-src")).removeClass('new_news_img');
    });
    $(".__scrolling").mCustomScrollbar({
        theme: "3d-dark"
    });
}