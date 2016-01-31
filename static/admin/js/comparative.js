/**
 * Created by Abolfazl on 31/01/2016.
 */


$(document).on('click', '.add-comparative-btn.agency', function(e){
    var elm = $(e.target).closest('.add-comparative-btn.agency');
    var _type = elm.attr('data-type');
    $('.comparative-row-divs[data-type=' + _type + ']').append($('#comparative_content').html().replace(/__type__/g , _type));
    $('.comparative-row-divs[data-type=' + _type + '] .new_select').select2().removeClass('new_select').addClass('select');
});

$(document).on('click', '.delete-rss-btn.agency', function(e){
    $(e.target).closest('.rss-row').remove();
});