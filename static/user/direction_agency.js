/**
 * Created by Morteza on 12/7/2015.
 */
var check = '<i class="fa fa-check cursor-pointer"></i>';

var __w = true;
$(document).on('click', '.change-direction', function(e){
    if(__w){
        __w = false;
        var elm = $(e.target).closest('.change-direction');
        elm.html(loader.replace(/20/g, '15'));
        var agency = elm.attr('data-agency');
        var direction = $('select.user-direction[data-agency=' + agency + ']').select2("val");
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

$('.direction-agencies.category').click(function(){
    var data_action = $(this).attr('data-action');
    $('.direction-agencies.category-content').css('display','none');
    $('.direction-agencies.category-content[data-action=' + data_action + ']').fadeIn();
});