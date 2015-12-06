/**
 * Created by Morteza on 12/6/2015.
 */

$('body').delegate('input.parent[type=checkbox]', 'lcs-statuschange', function() {
    var parent_id = $(this).attr('data-id');
    if($(this).is(':checked')){
        $('input.child[type=checkbox][data-parent-id=' + parent_id + ']').lcs_on();
    }else{
        $('input.child[type=checkbox][data-parent-id=' + parent_id + ']').lcs_off();
    }
});

$('#media .R_butt_white_bordered').click(function(){
    var data_action = $(this).attr('data-action');
    $('#media .source_content').css('display','none');
    $('#media .source_content[data-action=' + data_action + ']').fadeIn();
});
$('#subject .R_butt_white_bordered').click(function(){
    var data_action = $(this).attr('data-action');
    $('#subject .source_content').css('display','none');
    $('#subject .source_content[data-action=' + data_action + ']').fadeIn();
});
$('#area .R_butt_white_bordered').click(function(){
    var data_action = $(this).attr('data-action');
    $('#area .source_content').css('display','none');
    $('#area .source_content[data-action=' + data_action + ']').fadeIn();
});
