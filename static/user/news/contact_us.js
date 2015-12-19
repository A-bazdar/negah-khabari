/**
 * Created by Morteza on 12/19/2015.
 */

var __a = true;
$('#send_contact_us').submit(function (e) {
    if (__a) {
        __a = false;
        e.preventDefault();
        var btn = $('.send-contact-us-btn');
        btn.html(loader);
        var postData = $("#send_contact_us").serializeArray();
        jQuery.ajax(
                {
                    url: '',
                    type: "post",
                    data: postData,
                    success: function (response) {
                        var status = response['status'];
                        var value = response['value'];
                        var messages = response['messages'];
                        if (!status) {
                            var error = '';
                            for (var i = 0; i < messages.length; i++) {
                                error += messages[i] + '<br>';
                            }
                            if (error == '')
                                error = '„ «”›«‰Â œ— ”?” „ Œÿ«?? »Â ÊÃÊœ ¬„œÂ° ·ÿ›« œÊ»«—Â «„ Õ«‰ ò‰?œ.';
                            Alert.render(error, function () {
                                btn.html('«—”«·');
                                __a = true;
                            });
                        } else {
                            Alert.render('success', function () {
                                $('input[name=name]').val('');
                                $('input[name=email]').val('');
                                $('textarea[name=message]').val('');
                                btn.html('«—”«·');
                                __a = true;
                            });
                        }
                    },
                    error: function () {
                        Alert.render('error', function () {
                            btn.html('«—”«·');
                            __a = true;
                        });
                    }
                });
    }
});