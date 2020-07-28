$(function(){
//  Form Vadlidate
    //  Form request validate setting
    $('#FormRequest').validate({
        rule:{
            description:{
                required: true,
                summernote_validated:true
            }
        }
    });
});