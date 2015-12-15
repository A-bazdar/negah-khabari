/**
 * Created by Morteza on 12/7/2015.
 */
var check = '<i class="fa fa-check cursor-pointer"></i>';

$('.direction-agency.direction-agency-tabs').click(function(){
    var data_action = $(this).attr('data-action');
    $('.tab_content.direction-agency').hide();
    $('.tab_content.direction-agency[data-action=' + data_action + ']').fadeIn();
});

$(document).on('click', '.direction-agency.source-show.category', function(){
    var data_action = $(this).attr('data-action');
    $('.direction-agency.category-content.source-show').css('display','none');
    $('.direction-agency.category-content.source-show[data-action=' + data_action + ']').fadeIn();
});

$(document).on('click', '.direction-agency.direction-show.direction', function(){
    var direction = $(this).attr('data-direction');
    $('.direction-agency.category-content.direction-show').hide();
    $('.direction-agency.agency-content.direction-show').hide();
    $('.direction-agency.category-content.direction-show[data-direction=' + direction + ']').fadeIn();
});

$(document).on('click', '.direction-agency.direction-show.category', function(){
    var direction = $(this).attr('data-direction');
    var category = $(this).attr('data-category');
    $('.direction-agency.agency-content.direction-show').hide();
    $('.direction-agency.agency-content.direction-show[data-direction=' + direction + '][data-category=' + category + ']').fadeIn();
});

var __w = true;
$(document).on('click', '.change-direction', function(e){
    if(__w){
        __w = false;
        var elm = $(e.target).closest('.change-direction');
        elm.html(loader.replace(/20/g, '15'));
        var agency = elm.attr('data-agency');
        var show = elm.attr('data-show');
        var direction = $('select.user-direction[data-agency=' + agency + '][data-show=' + show + ']').select2("val");
        var postData = [
            {name: 'agency', value: agency},
            {name: 'direction', value: direction},
            {name: '_xsrf', value: xsrf_token},
            {name: 'action', value: 'change'}
        ];
        jQuery.ajax(
            {
                url: agency_direction_url,
                type: "post",
                data: postData,
                success: function (response) {
                    var status = response['status'];
                    var value = response['value'];
                    var messages = response['messages'];
                    if (status) {
                        Alert.render('success', function () {
                            elm.html(check);
                            var category = elm.attr("data-category");
                            var old_direction = elm.attr("data-direction");
                            $('.tab_content.direction-agency.source-show').html(value);
                            $('.direction-agency.agency-content.direction-show').hide();
                            $('.direction-agency.category-content.direction-show').hide();
                            $('.direction-agency.category-content.direction-show[data-direction=' + old_direction + ']').fadeIn();
                            $('.direction-agency.agency-content.direction-show[data-direction=' + old_direction + '][data-category=' + category + ']').fadeIn();
                            $('select.select.user-direction.direction-show').select2();
                            __w = true;
                        });
                    }else{
                        var error = '';
                        for(var i = 0; i < messages.length ; i++){
                            error += messages[i] + '<br>';
                        }
                        if(error == '')
                            error = 'error';
                        Alert.render(error, function(){
                            elm.html(check);
                            __w = true;
                        });
                    }
                },
                error: function () {
                    Alert.render('error', function(){
                        elm.html(check);
                        __w = true;
                    });
                }
            });
    }
});