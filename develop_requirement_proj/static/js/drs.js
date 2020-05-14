$(function(){
//  Add Request
    //  Reset modal
    $(document).on('click','#addRequestBtn',function(){
        $('#requestModal').data('order_id','New').modal('show');
    });

    $('#requestModal').find('.selectpicker').selectpicker('render');
//  Form fields - Select Options
    let Obj=get_options();
    let disabledarr=['BU','EE','ME'];
    let optionsValue=Object.values(Obj)[0];
    $.each(optionsValue,function(groupname,options){
        if(disabledarr.includes(groupname)){}
        else{
            $('#sel_function').append('<optgroup label="'+groupname+'"></optgroup>');
            $.each(options,function(i,subfunc){
                let el=$('#sel_function').find('optgroup').last()[0];
                let func_subfunc=groupname+"_"+subfunc;
                $("<option>").text(subfunc).val(func_subfunc).appendTo(el);            
            })
        }
    });
    $('#sel_function').selectpicker('refresh');



//  Global application
    $(document).on('click','.ezinfoModal_trigger',function(){
        let id=$(this).data('id');
        // $('#ezinfoModal').modal('show');

    });




//  Form fields - Select accounts
    $('#sel_function').on('change',function(){
        let sub_function=$('#sel_function').val();
        let accounts=get_accounts(sub_function);

        $('#sel_accounts').empty();
        $('#sel_accounts').append('<option value=""> Select... </option>');

        //  DQMS tricky rule
        if(sub_function=='QT_DQMS'){
            $.each(accounts,function(){
                let account_info=$(this)[0];
                if(account_info['code']=='WT-EBG') $('#sel_accounts').append('<option value="'+account_info['id']+'" selected>'+account_info['code']+'</option>'); 
            });
        }else{
            $.each(accounts,function(){
                let account_info=$(this)[0];
                $('#sel_accounts').append('<option value="'+account_info['id']+'">'+account_info['code']+'</option>');
            });
        }
       
        $('#sel_accounts').selectpicker('refresh');
    });




//  Form fields - Select projects
    $('#sel_accounts').on('change',function(){
        let sub_function=$('#sel_function').val();
        let acc_id=$('#sel_accounts').val();
        let projects=get_projects(acc_id);
        $('#sel_projects').empty();
        $('#sel_projects').append('<option value=""> Select... </option>');
        
        //  DQMS tricky rule
        if(sub_function=='QT_DQMS'){
            $.each(projects,function(){
                let project_info=$(this)[0];
                $('#sel_projects').append('<option value="'+project_info['id']+'">'+project_info['name']+'</option>');
            });
        }else{
            $.each(projects,function(){
                let project_info=$(this)[0];
                $('#sel_projects').append('<option value="'+project_info['id']+'">'+project_info['name']+'</option>');
            });
        }
        $('#sel_projects').selectpicker('refresh');        
    });


//  Form fields - Select assigners
    $('#sel_projects,#sel_function').on('change',function(){
        let project_id=$('#sel_projects').val();
        let sub_function=$('#sel_function').val().split('_')[1];
        if(project_id.length!==0 && sub_function!==0){
            let assigners=get_assigners(sub_function,project_id);
            $('#sel_assigners').empty();
            $('#sel_assigners').append('<option value=""> Select... </option>');
            $.each(assigners,function(){
                console.log($(this)[0]);
                let name=$(this)[0]['display_name'].split('/Wistron')[0];
                let phone_extension=$(this)[0]['extension'];
                let id=$(this)[0]['employee_id'];
                $('#sel_assigners').append('<option value="'+id+'" data-subtext=" #'+phone_extension+'">'+name+'</option>');
            });
            $('#sel_assigners').selectpicker('refresh');
        }
    });
  





//  Click table fa-external-link-alt icon -- show the modal
    $(document).on('click','.fa-external-link-alt',function(){
        $('#ezinfoModal').modal('show');
    });

//  #requestModal 
    //  Form fields - Select Assigners options
    $('#sel_assigners_dev').on('change',function(){
        // let dept_name=$(this).find('input:checked').val();
        // let assigners=get_assigners(dept_name);
        
        // $('#sel_assigners').empty();
        // $('#sel_assigners').append('<option value=""> Select '+dept_name+'...</option>');
        // $.each(assigners,function(i,v){
        //     $('#sel_assigners').append('<option value="'+v.display_name+'">'+v.display_name+'</option>');
        // });
        // $('#sel_assigners').selectpicker('refresh');
        // $('#sel_assigners').parents('div.row').slideDown();
    });

    
    //  Form fields - Upload animation
    fileLists = [];
    let fileslimit = 5 //  Restrict file upload total number
    let file_size_limit = 10000000 //bites  file_size <= 10mb

    $('#restrict_file_num').text(fileslimit);  
    //  Upload file ui layout
        $('#files').on('change', function(event) {
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
                        $('#alertModal').find('img').prop('src',images['404']);
                        $('#alertModal').modal('show');
                    }
                }else{
                    $('#selected_file').siblings('.caption').fadeIn(0);
                    $('#selected_file').html('').fadeOut(0);
                }
            }
        });       
        $('#attached_file_btn').off().on('click',function(){
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
                    formdata.append('order_id',order_id);
                    let target;
                    $.ajax({
                        url:fakedata_path+'patch_files.json',
                        method:'GET',
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
                                "path": images['upload'],
                                "order_id": order_id,
                                "description": description,
                                "size": file['size'],
                                "created_time": ""
                            };
                            $('#filelist').bootstrapTable('append',newfile);
                            target=$('#filelist').find('tbody').find('tr').last().find('td').eq(1);
                            let loadinghtml=`<div class="loadingbar">
                                                <div class="progress mx-auto">
                                                    <div class="progress-bar progress-bar-striped bg-success font-weight-bold progress-bar-animated" style="width: 20%;"></div>
                                                </div>
                                                <div class="mr-2 mb-2 text-right font-weight-bold text-secondary loadedpercent"></div>
                                            </div>`;
                            target.append(loadinghtml);
                        },
                        error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
                        // success: function ( result, textStatus, XMLHttpRequest ){ },
                        complete: function ( result, textStatus, XMLHttpRequest ){// 測試後請刪除
                            //  Remove progress bar and animation
                            target.find('.loadingbar').remove();
                            //  remove #files value --> so the change event can continue    
                            $('#files').val('');
                            $('#file_description').val('');
                            $('#files').trigger('change');
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
        });

    //  filelist table button action    
        $('#filelist').on('click','button.btn-danger',function(){
            let id=$(this).parents('tr').data('id');

            $(this).parents('tr').addClass('animated zoomOutRight',function(){
                $(this).fadeOut(function(){
                    delete_document(id);
                    comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
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
        $('#filelist').on('click','.file_description_edit',function(){
            let target=$(this).parents('.detail-view')
            //  Show Textarea allow to edit
            target.find('textarea').fadeIn(0);
            target.find('.description_alert').fadeIn(0);
            target.find('button').not('.file_description_edit').fadeIn(0);
            target.find('p').fadeOut(0);
            target.find('.file_description_edit').fadeOut(0);
        });
        function collapse_description(detail_view){
            detail_view.find('p').fadeIn(0);
            detail_view.find('.file_description_edit').fadeIn(0);
            detail_view.find('textarea').fadeOut(0);
            detail_view.find('button').not('.file_description_edit').fadeOut(0);
            detail_view.find('.description_alert').fadeOut(0);
        }
        $('#filelist').on('click','.file_description_save',function(){
            let target=$(this).parents('.detail-view');
            let row_index=target.prev('tr').data('index');
            // let contentTarget=$(this).parents('.detail-view').find('p');
            let editcontent=$(this).parents('.detail-view').find('textarea').val();
            $('#filelist').bootstrapTable('updateRow',{
                index: row_index, 
                row: {
                    description: editcontent,
                },
            }); 
            $('#filelist').find('tr[data-index='+row_index+']').find('td').first().find('.detail-icon').trigger('click');
            collapse_description(target);
        });
        $('#filelist').on('click','.file_description_cancel',function(){
            let target=$(this).parents('.detail-view');
            collapse_description(target);
        });
        $('#filelist').on('change','.detail-view textarea.bd-none',function(){
            let target=$(this).parents('.detail-view');
            let alerthtml=`<small class="pl-1 text-info font-weight-bold description_alert">Last edit not completed yet~</small>`;
            let cancelbtn=target.find('.file_description_cancel');
            cancelbtn.on('click',function(){
                target.find('textarea.bd-none').addClass('bd-info').removeClass('bd-none');
                if(target.find('.description_alert').length==0) $(alerthtml).insertAfter(target.find('textarea'));
            });
        });



 




    //  Comment area
        $(document).on('click','#toggle-commentarea',function(){ 
            if($(this).hasClass('active'))  comment_area_height_expand('imgage_dev','image_label_dev','authors','FormRequest','comment_area');
            else comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
            $(this).find('i').toggleClass('fa-chevron-down fa-chevron-up');
        });

        //  Add comment
        $('#sendcomment_btn').on('click',function(){
            if($('#comment').summernote('isEmpty')){         
            }else{  //  Comment content is not null
                let comment_html=$('#comment').summernote('code');
                let comment_obj={
                        "comment":  comment_html,
                        "orders_id": 10,
                        "editor": {
                            "employee_id": 10612704,
                            "display_name": "Jeff Sh Wang/WHQ/Wistron",
                            "avatar": images['defaultavatar'],
                        },
                        "timestamp": get_now_isotimeformat(),
                };
                //TODO POST comment
                // 測試完請刪除
                let res=post_record_history(comment_obj);
                append_comment_template('#comment_area',comment_obj);
                $('#comment').summernote('code', '');
                
                let position_tar=$('#comment_area').find('div.mb-2').last();
                scrollToBottom($('#comment_area'),position_tar);
            }
        });
});


