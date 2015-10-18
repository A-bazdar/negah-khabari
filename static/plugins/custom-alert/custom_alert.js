/**
 * Created by Morteza on 27/07/2015.
 */

var html = '<div id="dialog-overlay"></div>' +
           '<div id="dialog-box" style="z-index: 10000000000 !important">' +
               '<div id="dialog-box-head"></div>' +
               '<div id="dialog-box-body"></div>' +
               '<div id="dialog-box-footer"></div>' +
           '</div>';

var dialogs = {
    error: {txt: 'متاسفانه در سیستم خطایی به وجود آمده، لطفا دوباره امتحان کنید.', btn: 'R_butt_red', icn: 'fa-times colorRed'},
    success: {txt: 'عملیات با موفقیت انجام شد.', btn: 'R_butt_green', icn: 'fa-check colorGreen'},
    message_send: {txt: 'پیام با موفقیت ارسال شد.', btn: 'R_butt_green', icn: 'fa-check colorGreen'},
    empty: {txt: 'لطفا همه فیلدها را وارد کنید.', btn: 'R_butt_yellow', icn: 'fa-exclamation-triangle  colorYellow'},
    report_password: {txt: 'حساب کاربری با موفقیت ایجاد شد و تلفن همراه کابر به عنوان گذرواژه انتخاب شد.', btn: 'R_butt_green', icn: 'fa-check colorGreen'}
};

function CustomAlert(){
    this.render = function(__key, OkCallback){
        if(__key in dialogs){
            __key = dialogs[__key];
        }else{
            __key = {txt: __key, btn: 'R_butt_red', icn: 'fa-times colorRed'}
        }
        var winW = window.innerWidth;
        var winH = window.innerHeight;
        var dialog_overlay = document.getElementById('dialog-overlay');
        var dialog_box = document.getElementById('dialog-box');
        dialog_overlay.style.display = "block";
        dialog_overlay.style.height = winH + "px";
        dialog_box.style.left = (winW/2) - (550 * .5) + "px";
        dialog_box.style.top = "100px";
        dialog_box.style.display = "block";
        document.getElementById('dialog-box-head').innerHTML = "پیام سیستم";
        document.getElementById('dialog-box-body').innerHTML = '<i style="margin-left: 10px" class="fa ' + __key['icn'] + '"></i>' + __key['txt'];
        document.getElementById('dialog-box-footer').innerHTML = "<button class='" + __key['btn'] + " ok-alert'>تایید</button>";
        $('.ok-alert').click(function() {
            document.getElementById('dialog-box').style.display = "none";
            document.getElementById('dialog-overlay').style.display = "none";
            OkCallback();
        });
    };
}

var bd = document.getElementsByTagName('body')[0];
bd.innerHTML += html;

var Alert = new CustomAlert();