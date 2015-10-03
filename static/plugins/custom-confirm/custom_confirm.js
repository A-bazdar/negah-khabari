/**
 * Created by Morteza on 27/07/2015.
 */

var html = '<div id="dialog-overlay"></div>' +
           '<div id="dialog-box" style="z-index: 10000000000 !important">' +
               '<div id="dialog-box-head"></div>' +
               '<div id="dialog-box-body"></div>' +
               '<div id="dialog-box-footer"></div>' +
           '</div>';

function CustomConfirm(){
    this.render = function(text, accept_butt_txt, accept_butt_cls, reject_butt_txt, reject_butt_cls, SuccessCallback, RejectCallback){
        text = text || "آيا از انجام اين عميات اطمينان داريد ؟";
        accept_butt_txt = accept_butt_txt || "تاييد";
        accept_butt_cls = accept_butt_cls || "R_butt_green";
        reject_butt_txt = reject_butt_txt || "انصراف";
        reject_butt_cls = reject_butt_cls || "R_butt_red";
        var winW = window.innerWidth;
        var winH = window.innerHeight;
        var dialog_overlay = document.getElementById('dialog-overlay');
        var dialog_box = document.getElementById('dialog-box');
        dialog_overlay.style.display = "block";
        dialog_overlay.style.height = winH + "px";
        dialog_box.style.left = (winW/2) - (550 * .5) + "px";
        dialog_box.style.top = "100px";
        dialog_box.style.display = "block";
        document.getElementById('dialog-box-head').innerHTML = "پيام سيستم";
        document.getElementById('dialog-box-body').innerHTML = text;
        document.getElementById('dialog-box-footer').innerHTML = '<button style="margin-left:  20px !important" class="' + accept_butt_cls + ' accept_butt">' + accept_butt_txt + '</button><button class="' + reject_butt_cls + ' reject_butt" style="margin-right: 20px !important">' + reject_butt_txt + '</button>';
        $('.accept_butt').click(function() {
            document.getElementById('dialog-box').style.display = "none";
            document.getElementById('dialog-overlay').style.display = "none";
            SuccessCallback();
        });
        $('.reject_butt').click(function() {
            document.getElementById('dialog-box').style.display = "none";
            document.getElementById('dialog-overlay').style.display = "none";
            RejectCallback();
        });
    };
}

var bd = document.getElementsByTagName('body')[0];
bd.innerHTML += html;

var Confirm = new CustomConfirm();