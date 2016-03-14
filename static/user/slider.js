/**
 * Created by Morteza on 12/19/2015.
 */

$('.top-slider').slick({
    slidesToShow: 6,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 5000
});

$(document).on('click', '.slider_content', function (e) {
    var elm = $(e.target);
    var action = elm.closest('.slider_content').attr('data-action');
    location.href = show_news_url.replace(/__news__/g, action);
});