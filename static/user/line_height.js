/**
 * Created by Morteza on 1/1/2016.
 */

$(document).on('click','.set-line-height', function(e){
    var elm = $(e.target).closest('.set-line-height');

    var detail_news_container = $('.detail_news_container');
    if(elm.hasClass('low')){
        if(detail_news_container.hasClass('line-height-low')){
            return;
        }
        if(detail_news_container.hasClass('line-height-mid')){
            detail_news_container.removeClass('line-height-mid').addClass('line-height-low');
        }
        else if(detail_news_container.hasClass('line-height-high')){
            detail_news_container.removeClass('line-height-high').addClass('line-height-low');
        }
    }
    else if(elm.hasClass('middle')){
        if(detail_news_container.hasClass('line-height-mid')){
            return;
        }
        if(detail_news_container.hasClass('line-height-low')){
            detail_news_container.removeClass('line-height-low').addClass('line-height-mid');
        }
        else if(detail_news_container.hasClass('line-height-high')){
            detail_news_container.removeClass('line-height-high').addClass('line-height-mid');
        }
    }
    else if(elm.hasClass('high')){
        if(detail_news_container.hasClass('line-height-high')){
            return;
        }
        if(detail_news_container.hasClass('line-height-low')){
            detail_news_container.removeClass('line-height-low').addClass('line-height-high');
        }
        else if(detail_news_container.hasClass('line-height-mid')){
            detail_news_container.removeClass('line-height-mid').addClass('line-height-high');
        }
    }
    var line_height = elm.attr('data-line-height');
    $('.set-line-height.active').removeClass('active');
    elm.addClass('active');
    $.ajax({
        url: change_line_height_url,
        type: 'post',
        data: [
            {name: '_xsrf', value: xsrf_token},
            {name: 'line_height', value: line_height}
        ]
    });
});