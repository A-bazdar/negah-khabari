$(document).ready(function(){
	create_tooltip();
});

function create_tooltip(){
	$('.tooltip_create').each(function(){
		var text = $(this).attr('data-text');
		var type = $(this).attr('data-type');
		$(this).removeClass('tooltip_create').addClass('tooltip_show');
		$(this).append('<tooltip class="'+type+'" ><arrow><i></i></arrow><section>'+text+'</section></tooltip>');
	});
}
$(document).on('mouseover','.tooltip_show',function(){
    $('tooltip',this).stop().fadeIn();
});

$(document).on('mouseout','.tooltip_show',function(){
    $('tooltip',this).stop().fadeOut();
});