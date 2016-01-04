/**
 * Created by Morteza on 12/19/2015.
 */

function load_news() {
    //var bLazy = new Blazy({
    //    breakpoints: [{
    //        width: 420, // max-width
    //        src: 'data-src-small'
    //    }]
    //    ,success: function(element){
    //        setTimeout(function(){
    //            var parent = element.parentNode;
    //            parent.className = parent.className.replace(/\bloading\b/,'');
    //        }, 200);
    //    }
    //});
    $.each($("img.new_news_img"), function () {
        $(this).attr("src", $(this).attr("data-src")).removeClass('new_news_img');
    });
}