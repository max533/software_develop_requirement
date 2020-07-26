# DJANGO_FORCE_LOGIN_USERNAME=10712714
# DJANGO_FORCE_LOGIN_USERNAME=9505005
# DJANGO_FORCE_LOGIN_USERNAME=9106015
# DJANGO_FORCE_LOGIN_USERNAME=8209089

MODULE
    refresh_requestModal(order_id);
    $('#table').bootstrapTable('refresh');

INFO
    Form request edit
        $('#FormRequest').fadeOut(0);
    Form breadcrumb
        show_request_info(order_reponse);
    ReviewerList
        signature_sign(id,signature_id);
    Developers

FILE
    File - Upload file div
        get_filelist(id);
        $('#tag_div').parent('div').fadeIn(0);
    File - list
        $('#FormUpload').prop('style','display:none !important;');

COMMENT
    edit
        $('#edit_comment_area').fadeOut(0);
    display
        $('#display_comment_area').fadeIn(0);



SIGNATURE
    signature btn
        $('#signature_func').fadeIn(0);

ASSIGN DEVELOPERS
        $('#assign_dev_func').fadeIn(0);

SCHEDULE
    edit
        $('#assign_dev_func').fadeIn(0);
    status
        let temp=schedule_status_template(order_reponse);
        $('#schedule_status').append(temp);
        $('#schedule_status').find('.sticker').each(function(){
            avatar_reload($(this));
        });
    show
        get_readonly_schedule(order_id)
        $('#readonly_schedule_div').fadeIn(0);
    pend
        $('#pend_schedule_div').fadeIn(0);

        get_schedulelist(order_reponse)  //有這個datepicker才可以


PROGRESS
    $('#FormAddMilestone').data('id');


IMAGE 
    instruction
        request_image_module();

    REQUEST IMAGE STATUS

    initialize_request
    Reinitialize_request
    signer_waiting_signature
    waiting_signature
    notify_signing
    waiting_receiver_accept_request
    receiver_assign_developers
    receiver_pending
    receiver_proposal_schedule
    pending_schedule
    developing

SHOW INTACT REQUIREMENT
        indentify_modal_show(row);


FLOW

Request flow
    當送出資料要刷新modal時
        let order_response=get_single_order(order_id);
        if(order_response){
            $.when( $('#requestModal').modal('hide') ).then(function(){
                indentify_modal_show(order_response);
            });
        }
    在開啟modal時候,存在dom會用到的值
        //  developer list
        $('#assign_dev_func').find('button').data('raw_dev_list',developers_object); -->show_author('form_owner',raw_dev_data);

        $('#requestModal').data('order_id')
        $('#requestModal').data('schedule')

    當modal hidden.bs.modal時，table會刷新資料
        $('#table').bootstrapTable('refresh');










Tag flow

ezinfo
    $('.ezinfoModal_trigger').data('id')-->觸發Modal