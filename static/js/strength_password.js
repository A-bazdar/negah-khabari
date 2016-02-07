/**
 * Created by Morteza on 2/6/2016.
 */


var strength_password_status = [
    "امنیت گذرواژه وارد شده بسیار ضعیف است",
    "امنیت گذرواژه وارد شده ضعیف است",
    "امنیت گذرواژه وارد شده شده متوسط است",
    "امنیت گذرواژه وارد شده شده قوی است"
];

var strength_password_colors = [
    "red",
    "yellow",
    "orange",
    "green"
];

var strength_password_errors = [
    "حداقل طول گذرواژه باید بیشتر از 6 کاراکتر باشد",
    "گذرواژه باید شامل حروف بزرگ و کوچک لاتین باشد",
    "گذرواژه باید ترکیبی از حروف لاتین و اعداد باشد"
];

function strength_password(password){
    if(!/^.{6,}$/.test(password)){
        return [strength_password_colors[0], strength_password_status[0], strength_password_errors[0], 25]
    }
    var error = "";
    var percent = 25;
    var status = 0;
    if(/(?=.*[a-z])/.test(password)){
        percent += 25;
        status += 1;
    }else{
        error = strength_password_errors[1];
    }
    if(/(?=.*\d)/.test(password)){
        percent += 25;
        status += 1;
    }else{
        error = strength_password_errors[2];
    }
    if(/(?=.*[A-Z])/.test(password)){
        percent += 25;
        status += 1;
    }else{
        error = strength_password_errors[1];
    }
    if(percent == 100)
        error = "";
    return [strength_password_colors[status], strength_password_status[status], error, percent]
}