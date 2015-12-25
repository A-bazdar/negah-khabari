/**
 * Created by Morteza on 12/25/2015.
 */

function set_news(__news, __view){
    var _show_result_news = $('#show_result_news');
    _show_result_news.html("").attr('data-view', __view);
    var j = 0;
    if(__view == "list_view"){
        for(j = 0; j < __news.length; j++){
            make_news_list_view(__news[j]);
        }
    }else if(__view == "column_list_view"){
        var html = '<div id="news_list" class="col-md-6 col-sm-6 __scrolling __new_scrolling" style="max-height: 500px"></div><div id="detail_first_news" class="col-md-6 col-sm-6 show-detail-main-con"></div>';
        _show_result_news.html(html);
        for(j = 0; j < __news.length; j++){
            make_news_column_list_view(__news[j]);
            if(j == 0)
                make_news_column_detail_view(__news[j]);
        }
    }else if(__view == "details_view"){
        for(j = 0; j < __news.length; j++){
            make_news_detail_view(__news[j]);
        }
    }else if(__view == "details_pic_view"){
        for(j = 0; j < __news.length; j++){
            make_news_detail_pic_view(__news[j]);
        }
    }else if(__view == "pic_view"){
        for(j = 0; j < __news.length; j++){
            make_news_pic_view(__news[j]);
        }
    }
}