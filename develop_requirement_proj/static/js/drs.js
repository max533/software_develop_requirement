$(function(){
    //  Decode URL open coresponding to request
    let order_id=getUrlParameter('order');
    if(order_id!==undefined){
        let order_response=get_single_order(order_id);
        indentify_modal_show(order_response);
    }
    //  Press shift+mousewheel  <- -> 左右移動
    $(document).bind('mousewheel DOMMouseScroll','#table', function (event) {
        if(event.shiftKey === true) {
            $('#table').closest('.fixed-table-body').scrollLeft(
                $('#table').closest('.fixed-table-body').scrollLeft() - event.originalEvent.wheelDelta/4
            );
        }
    });

//  Add Request
    //  Reset modal
    $(document).on('click','#addRequestBtn',function(){
        append_New_requestModal();
        show_author('form_initiator',loginInfo);
    });
    //  Validate fields - init request
    $(document).on('click','#initialize_btn',function(){
        if($('#FormRequest').validate().form()){
            //  Add New request -- get order_id to upload file or tag past form
            let statusObj={"P0":{"initiator": "Approve"},"signed":false}
            let init_data=package_data('#FormRequest');
            init_data['status']=JSON.stringify(statusObj)

            init_data['initiator']=loginInfo.employee_id; 

            let order_data=post_order(init_data);
            let order_id=order_data['id'];
            //  Store order_id to requestModal
            $('#requestModal').data('order_id',order_id);
            //  Collapse Request which team info
            show_request_info(order_data);
            //  Show upload file
            afterInit(order_id);
            //  image_status
            request_image_module('waiting_signature');
        }else console.log('#FormRequest valid false');  
    });
    $(document).on('click','#Reinitialize_btn',function(){
        if($('#FormRequest').validate().form()){
            let signed=$('#requestModal').data('status')['signed'];
            let order_id=$('#requestModal').data('order_id');
            let statusObj={"P0":{"initiator": "Approve"},"signed":signed}
            let patch_data=package_data('#FormRequest');
            patch_data['status']=JSON.stringify(statusObj);
            $.when( patch_order(order_id,patch_data) ).then( refresh_requestModal(order_id) );
        }else console.log('#FormRequest valid false');  
    });
    $(document).on('click','#close_init_btn',function(){
        let signed=$('#requestModal').data('status')['signed'];
        let order_id=$('#requestModal').data('order_id');
        let statusObj={"P0":{"initiator": "Close"},"signed":signed}
        let patch_data={}
        patch_data['status']=JSON.stringify(statusObj);
        $.when( patch_order(order_id,patch_data) ).then( refresh_requestModal(order_id) );
    });



    $(document).on('hidden.bs.modal','#requestModal,#ezinfoModal', function () {
        $(this).remove();
    });

//  Schedule
    $(document).on('click','#add_schedule_btn',function(){
        let order_id=$('#requestModal').data('order_id');
        if($('#FormSchedule').validate().form()){
            let eventname=$('#FormSchedule').find('td').eq(0).find('input').val();
            let expdate=new Date($('#FormSchedule').find('td').eq(1).find('.date').val()).toISOString();
            let description=$('#FormSchedule').find('td').eq(2).find('textarea').val();
            let completerate=$('#FormSchedule').find('td').eq(3).find('input').val();
            let fake_id='New_'+$('#schedulelist').find('.Newschedule').length
            let newschedule={
                "id": fake_id,
                "event_name": eventname,
                "description": description,
                "timestamp": expdate,
                "complete_rate": completerate,
                "version": null,
                "update_time": " - ",
                "created_time": " - ",
                "order": order_id
            };

            $('#schedulelist').bootstrapTable('append',newschedule);
            $('#FormSchedule').find('input,textarea').val('');
        }
    });
    //  Restrict input directly from field
    $(document).on('input','#schedule_area .date',function(){
        $(this).val('');
    });
    $(document).on('click','#schedulelist tbody .delete',function(){
        let id=$(this).parents('tr').data('id');

        if(id.match('New')==null){
            let del_id_arr=$('#schedulelist').data('del_id_arr').concat(id);
            $('#schedulelist').data('del_id_arr',del_id_arr);
        }
        $('#schedulelist').bootstrapTable('remove',{field:'id',values:[id]});
    });
    //  Update schedule
    $(document).on('change','#schedulelist input,#schedulelist textarea',function(){
        let field=$(this).data('field');
        let value=$(this).val();
        let index=$(this).parents('tr').data('index');

        //  Update schedule cell date
        $('#schedulelist').bootstrapTable('updateCell',{
            index: index,
            field: field,
            value: value
        });
        
        //  Store change field into obj--> to sent ajax list
        let id=$(this).parents('tr').data('id');
        let update_obj=$('#schedulelist').data('updatelist_obj');
        if(field=='expected_time'&&value!=='') value=new Date(value).toISOString();

        if(id!=='New'){
            //  Store the update list into object {id:{field:value}}
            if(update_obj[id]==undefined){
                let row_obj={};
                row_obj[field]=value
                update_obj[id]=row_obj
            }else{               
                update_obj[id][field]=value
            }
            $('#schedulelist').data('updatelist_obj',update_obj);
        }
    });
    $(document).on('click','#close_schedule_btn',function(){
        let order_id=$('#requestModal').data('order_id');
        let status=$('#requestModal').data('status');
        status['P3']['assigner']='Close';
        let formdata={'status':JSON.stringify(status)};
        patch_order(order_id,formdata);
        $('#requestModal').modal('hide');
    });
    $(document).on('click','#update_schedule_btn',function(){
        let if_no_blank=1
        $('#schedulelist').find('input,textarea').each(function(){
            let value=$(this).val();
            if(value==''||value=='undefined'){
                if_no_blank=if_no_blank*0;
                $(this).addClass('border-danger');
            }else{
                $(this).removeClass('border-danger');
            }
        });
        if(if_no_blank){  // No blank field
            let update_list=[];
            let order_id=$('#requestModal').data('order_id');
            let del_id_arr=[];

            if($('#schedulelist').data('del_id_arr')==undefined||$('#schedulelist').data('del_id_arr')==''){}
            else del_id_arr=$('#schedulelist').data('del_id_arr');

            if($('#schedulelist').data('updatelist_obj')==undefined){}
            else update_list.push($('#schedulelist').data('updatelist_obj'));

            scheduleData=$('#schedulelist').bootstrapTable('getData',{useCurrentPage:true,includeHiddenRows:true});
                //  POST schedule
                $('#schedulelist').find('.Newschedule').each(function(){
                    let index=$(this).data('index');
                    //  Change time to ISO format
                    let fieldobj=scheduleData[index];
                    let date=fieldobj['timestamp']
                    fieldobj['timestamp']=new Date(date).toISOString();
                    post_schedule(fieldobj);
                })
                //  Patch schedule
                if(update_list==[]) console.log('No existed schedule update')
                else{
                    $.each(update_list[0],function(id,fieldobj){
                        if(Object.keys(fieldobj)[0]=='timestamp'){
                            let original_date=fieldobj['timestamp'] // 2020-01-01
                            fieldobj['timestamp']=new Date(original_date).toISOString(); // 2020-01-01 T00:00
                        }
                        patch_schedule(id,fieldobj);
                    });
                }
                //  Delete schedule
                if(del_id_arr==[]) console.log('No delete schedule update')
                else{
                    $.each(del_id_arr,function(i,id){
                        delete_schedule(id); 
                    });
                    $('#schedulelist').data('del_id_arr',[]);
                }
          
            //  Change order status
            // let order_response=get_single_order(order_id);
                let status=$('#requestModal').data('status');
                let signed=status['signed'];
                let newstatus={
                    'P3':{
                        'assigner':'Approve',
                        'initiator':'',
                        'developers':'',
                    },
                    'signed':signed
                }
            // status['P3']['assigner']='Approve';
                patch_order(order_id,{"status":JSON.stringify(newstatus)})
                //  Update schedule fields --> Modal refresh
                refresh_requestModal(order_id);
        }else{  console.log('Schedule list has blank'); }
    });
    //  Show schedule to edit
    $(document).on('click','#show_shcedule_area',function(){
        $('#schedule_area').fadeIn(0);
        $('#readonly_schedule_div').fadeOut(0);
    });
 
//  Global application
    $(document).on('click','.ezinfoModal_trigger',function(){
        let id=$(this).data('id');
        if(id==undefined||id==null||id==''){}
        else render_ezinfo(id);

        $('#ezinfoModal').modal('show');
    });



//  Click table fa-external-link-alt icon -- show the modal
    $(document).on('click','.fa-external-link-alt',function(){
        $('#ezinfoModal').modal('show');
    });

//  #requestModal    
    //  Form fields - Upload animation
    fileLists = [];
    let fileslimit = 5 //  Restrict file upload total number
    let file_size_limit = 10000000 //bites  file_size <= 10mb

    $('#restrict_file_num').text(fileslimit);  
    //  Upload file ui layout
        $(document).on('change','#files',function(event) {
            let tr_num=$('#filelist').find('tbody').find('tr').length;
            if(tr_num>=fileslimit) {
                //  upload file input disabled
                $('#selected_file').fadeOut(0);
                $('#files').prop('disabled',true);
                $('#files').parent('label').addClass('upload-style_disabled');
                $('#files').parent('label').siblings('h6').html('Uploaded number limited less than<span class="ml-2 font-weight-bold">'+fileslimit+'</span>.').fadeIn(0);
            }else{
                if($(this).val().length!==0){
                    let file=$('#files')[0].files[0];    //重新取得[input type='file']資料
                    let file_name=file['name'];
                    let file_size=bytesChange(file['size']);
                    if(file['size']<=file_size_limit){
                        let template='<i class="fa fa-file-alt fa-lg mr-1"></i>'+file_name+' - '+file_size

                        $('#selected_file').siblings('.caption').fadeOut(0);
                        $('#selected_file').html(template).fadeIn(0);
                    }else{
                        alertmodal_show();
                    }
                }else{
                    $('#selected_file').siblings('.caption').fadeIn(0);
                    $('#selected_file').html('').fadeOut(0);
                }
            }
        });       
        $(document).on('click','#attached_file_btn',function(){
            if($('#FormUpload').validate().form()){
                let tr_num=$('#filelist').find('tbody').find('tr').length;
                if(tr_num>=fileslimit) {
                    //  upload file input disabled
                    $('#files').prop('disabled',true);
                    $('#files').parent('label').addClass('upload-style_disabled');
                    $('#files').parent('label').siblings('h6').html('Uploaded number limited less than<span class="ml-2 font-weight-bold">'+fileslimit+'</span>.');
                }else{
                    if($('#files').val().length!==0){
                        let transmit_time_start;
                        let transmit_time_end;
                        let transmit_time_last = 0;
                        let transmit_loaded_last = 0;
                        let upload_start_time; // 開始上傳的時間(毫秒)

                        let file=$('#files')[0].files[0]; //重新取得[input type='file']資料
                        let file_name=file['name'];
                        let description=$('#file_description').val();
                        let order_id=$('#requestModal').data('order_id');

                        let formdata=new FormData;
                        formdata.append('path',file);
                        formdata.append('name',file_name);
                        formdata.append('description',description);
                        formdata.append('order',order_id);
                        let target;
                        $.ajax({
                            url:'/api/documents/',
                            method:'POST',
                            dataType: 'json',
                            data: formdata,
                            timeout:50000,
                            cache: false,
                            processData: false, 
                            contentType : false,
                            beforeSend: function ( XMLHttpRequest ){
                                formdata_console(formdata);
                                let newfile={
                                    "id": 'New',
                                    "name": file_name,
                                    "path": images.loadinggif_path,
                                    "order": order_id,
                                    "description": description,
                                    "size": file['size'],
                                    "update_time": ""
                                };
                                $('#filelist').bootstrapTable('append',newfile);
                                target=$('#filelist').find('tbody').find('tr').last().find('td').eq(1);
                                let loadinghtml=`<div class="loadingbar position-absolute">
                                                    <div class="progress mx-auto">
                                                        <div class="progress-bar progress-bar-striped bg-success font-weight-bold progress-bar-animated" style="width: 20%;"></div>
                                                    </div>
                                                    <div class="mr-2 mb-2 text-right font-weight-bold text-secondary loadedpercent"></div>
                                                </div>`;
                                target.append(loadinghtml);
                            },
                            error: function ( result, textStatus, XMLHttpRequest ){ 
                                console.log( result );  console.log( textStatus ); console.log('Uploading fail~') 
                            },
                            success: function ( result, textStatus, XMLHttpRequest ){ 
                                let id=result.id
                                let row_index=$('#filelist').find('tbody').find('tr').last().data('index');
                                $('#filelist').bootstrapTable('updateRow',{
                                    index: row_index, 
                                    row: {id: id},
                                });
                                let filename=result['name'];
                                let filetype=filename.split('.')[1];
                                let imgsrc=result['path'];
                                if(isImage(filetype)!==true) imgsrc=images['document'];

                                $('#filelist').find('tbody').find('tr').last().find('img').prop('src',imgsrc);
                                $('#filelist').find('tbody').find('tr').last().find('.filedownload').prop('href',result['path']);
                                $('#filelist').find('tbody').find('tr').last().find('.fileupdate').text(isotime_local(result['update_time']));
                            },
                            complete: function ( result, textStatus, XMLHttpRequest ){// 測試後請刪除
                                //  Remove progress bar and animation
                                target.find('.loadingbar').remove();
                                //  remove #files value --> so the change event can continue    
                                $('#files').val('');
                                $('#file_description').val('');
                                $('#files').trigger('change');
                                $('#FormUpload').find('.border-danger').removeClass('border-danger');
                            },
                            xhr: function() {
                                let xhr = $.ajaxSettings.xhr();
                                xhr.upload.onloadstart = function(e) {
                                    transmit_time_start = e.timeStamp;
                                    target.find('.loadedpercent').text('0%');
                                    upload_start_time = new Date().getTime();   //設置上傳開始時間(毫秒)
                                    upload_rate = 0; // 設置上傳速率(KB/秒)
                                    upload_file_loaded = 0;// 設置上傳開始時，以上傳的文件大小爲0%
                                    upload_estimate_time = 0; // 設置估算剩餘上傳完成的時間(秒)
                                };
                                xhr.upload.onloadend = function(e) {
                                    transmit_time_end = e.timeStamp;
                                    if( e.loaded == e.total ) {
                                        transmit_speed_avg = e.total / ((transmit_time_end - transmit_time_start) / 1000);
                                    } else {
                                        transmit_speed_avg = e.loaded / ((transmit_time_end - transmit_time_start) / 1000);
                                    }
                                };
                                xhr.upload.onprogress = function(e) {
                                    if( e.lengthComputable ) {
                                        let Percentage = Math.round((e.loaded * 100) / e.total);
                                        transmit_speed = (e.loaded - transmit_loaded_last) / 1024 / 1024 / ((e.timeStamp - transmit_time_last) / 1000);
                                        transmit_loaded_last = e.loaded;
                                        transmit_time_last = e.timeStamp;
                                        let upload_now_time = new Date().getTime(); // 獲取當前時間
                                        let time = (upload_now_time - upload_start_time) / 1000; // 毫秒 轉 秒
                                        let data = e.total - e.loaded; // 剩餘上傳的數據有多少B, 後面 轉 KB 轉 MB

                                        target.find('.progress-bar').css('width', Percentage + '%');
                                        target.find('.loadedpercent').numerator({
                                            toValue	: (Percentage <= 1 ? Percentage : Percentage-1),
                                            easing	: 'linear',
                                            duration: 100, //default 500
                                            onStart	: function() {
                                                target.find('.loadedpercent').text('0%');
                                            },
                                            onStep	: function() {
                                                target.find('.loadedpercent').text(Percentage + '%' );
                                            }
                                        });
                                    }
                                };
                                return xhr;
                            }
                        });
                    }
                }
            }

            
        });
    //  toggle file div // Close filediv or hide
        $(document).on('click','#file_div_toggle',function(){
            let file_div=$('#filelist').parents('.col-8');
            $(this).toggleClass('fa-angle-up fa-angle-down');
            if($(this).hasClass('fa-angle-down')) file_div.slideUp();   
            else file_div.slideDown();      
        });

    //  filelist table button action    
        $(document).on('click','#filelist button.btn-danger',function(){
            let id=$(this).parents('tr').data('id');

            $(this).parents('tr').addClass('animated zoomOutRight',function(){
                $(this).fadeOut(function(){
                    delete_document(id);
                    // comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
                    comment_area_height();
                    $('#filelist').bootstrapTable('remove',{field:'id',values:[parseInt(id)]});
                });
                if($('#files').prop('disabled')) {
                    //  upload file input cancel disabled
                    $('#files').prop('disabled',false);
                    $('#files').parent('label').removeClass('upload-style_disabled');
                    $('#files').parent('label').siblings('h6').html(' Drag&Drop or Click to choose your file.<i class="fa fa-cloud-upload-alt fa-lg ml-2"></i> ');
                }
            });
        });
        $(document).on('click','#filelist .description_edit,#schedulelist .description_edit',function(){
            let target=$(this).parents('.detail-view')
            //  Show Textarea allow to edit
            target.find('textarea').fadeIn(0);
            target.find('.description_alert').fadeIn(0);
            target.find('button').not('.description_edit').fadeIn(0);
            target.find('p').fadeOut(0);
            target.find('.description_edit').fadeOut(0);
        });
        function collapse_description(detail_view){
            detail_view.find('p').fadeIn(0);
            detail_view.find('.description_edit').fadeIn(0);
            detail_view.find('textarea').fadeOut(0);
            detail_view.find('button').not('.description_edit').fadeOut(0);
            detail_view.find('.description_alert').fadeOut(0);
        }
        $(document).on('click','#filelist .description_save',function(){
            let target=$(this).parents('.detail-view');
            let row_index=target.prev('tr').data('index');
            let id=$('#filelist').find('tr[data-index='+row_index+']').data('id');
            let filename=$('#filelist').find('tr[data-index='+row_index+']').find('.filename').text();
            let editcontent=$(this).parents('.detail-view').find('textarea').val();
            let update_file_data={
                'id':id,
                'name':filename,
                'description':editcontent,
            }
            if(update_document_detail(update_file_data)){
                $('#filelist').bootstrapTable('updateRow',{
                    index: row_index, 
                    row: {
                        description: editcontent,
                    },
                }); 
                $('#filelist').find('tr[data-index='+row_index+']').find('td').first().find('.detail-icon').trigger('click');
                collapse_description(target);
            }else console.log('Update fail~');
        });
        $(document).on('click','#filelist .description_cancel,#schedulelist .description_cancel',function(){
            let target=$(this).parents('.detail-view');
            collapse_description(target);
        });
        $(document).on('change','#filelist .detail-view textarea.bd-none,#schedulelist .detail-view textarea.bd-none',function(){
            let target=$(this).parents('.detail-view');
            let alerthtml=`<small class="pl-1 text-info font-weight-bold description_alert">Last edit not completed yet~</small>`;
            let cancelbtn=target.find('.description_cancel');
            cancelbtn.on('click',function(){
                target.find('textarea.bd-none').addClass('bd-info').removeClass('bd-none');
                if(target.find('.description_alert').length==0) $(alerthtml).insertAfter(target.find('textarea'));
            });
        });
 

    //  Comment area
        $(document).on('click','#hide_commentarea',function(){ comment_area_height();});  
        $(document).on('click','#show_commentarea',function(){ comment_area_height_expand();});
            
    //  Add comment
        $(document).on('click','#sendcomment_btn',function(){
            let order_id=$('#requestModal').data("order_id");
            if($('#comment').summernote('isEmpty')){         
            }else{  //  Comment content is not null
                let comment_html=$('#comment').summernote('code');
                let comment_obj={
                        "content":  comment_html,
                        "order": order_id
                };
                post_comment_history(comment_obj);
                let all_comments=get_comment_history(order_id);
                $('#comment_area').empty();
                $.each(all_comments,function(i,res){
                    append_comment_template('#comment_area',res);
                });
                let position_tar=$('#comment_area').find('div.mb-2').last();
                scrollToBottom($('#comment_area'),position_tar);
            }
        });

    
//  Submit result
        $(document).on('click','#submit_result',function(){
            let order_id=$('#requestModal').data('order_id');
            let status=JSON.stringify({'P5':{'developers':'Approve'}})
            let target=$('#repository_url');

            if( target.val().length==0 ){ // 是否為空值
                target.addClass('border-danger');
            }else if(target.val().trim().match(/^(?:http(s)?:\/\/)/)==null){ // 是否符合URL foramt
                target.addClass('border-danger');
            }else{
                target.removeClass('border-danger');
                let formdata={
                    'repository_url':target.val().trim(),
                    'status':status
                }
                $.when(patch_order(order_id,formdata)).then(
                    refresh_requestModal(order_id)
                );
                $('#repository_url').siblings('div').find('a').removeClass('btn-light').addClass('btn-success')
                                                    .prop('href',target.val().trim());
            }
        });


    // Searchbutton click 跳轉問題
    $('#search_tag').on('keypress',function(event) {
        if (event.keyCode == 13) { 
            $('#search_tag_btn').trigger('click');
            return false;
        }
    })
    $('#search_dev').on('keypress',function(event) {
        if (event.keyCode == 13) { 
            $('#search_dev_btn').trigger('click');
            return false;
        }
    })
});


