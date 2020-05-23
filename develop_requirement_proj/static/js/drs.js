$(function(){
//  Add Request
    //  Reset modal
    $(document).on('click','#addRequestBtn',function(){
        $('body').append(requestModal);
        $('#image_status').find('img').first().prop('src',images.status);
        //  form sticker
        $('#form_initiator').data('id',loginInfo.employee_id);
        $('#form_initiator').find('img').prop('src',loginInfo.avatar);
        $('#form_initiator').find('span').text(loginInfo.dispaly_name.split('/Wistron')[0]);

        //  summernote
        $('.summernote').summernote({
            theme: 'journal',
            placeholder: '...',
            tabsize: 2,
            spellCheck: true,     
            minheight: 40,    // set editor height
            height: 'fitcontent', 
            lineHeights: '1.0',
            disableDragAndDrop: false,  
            focus: true, 
            hint: {
                mentions: ['jeff', 'peter'],
                    match: /\B@(\w*)$/,
                    search: function (keyword, callback) {
                    callback($.grep(this.mentions, function (item) {
                        return item.indexOf(keyword) == 0;
                    }));
                    },
                    content: function (item) {
                    return '@' + item;
                    },    
            },
            toolbar: [
                ['style', ['style']],
                ['font', ['bold', 'underline']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['insert', ['link', 'picture']],
                ['view', ['help']]
                // ['font', ['bold', 'underline', 'clear']],
                // ['table', ['table']],
                // ['insert', ['link', 'picture', 'video']],
                // ['view', ['fullscreen', 'codeview','help']]
            ],
            callbacks: {
                onInit: function() {
                    let placeholder=$(this).prop('placeholder');
                    let target=$(this).siblings('.note-editor').find('.note-placeholder')
                    target.text(placeholder);
                },
                onChange:function(contents, $editable) {},
                onKeydown: function(e) {
                    if(e.keyCode==13) console.log('Enter/Return key pressed');
                },
                onFocus: function() {
                    switch ($(this).data('position')) {
                        case 'comment':
                            if($('#toggle-commentarea.active').length==0) $('#toggle-commentarea').trigger('click');
                            break;
                        default:
                            break;
                    }
                },
            }
        });

        // Comment Area - Load comments history
        // let comments=get_record_history();
        // $('#comment_area').empty();
        // $.each(comments,function(){
        //     let comment_obj=$(this)[0];
        //     append_comment_template('#comment_area',comment_obj)
        // });

        





        $('#requestModal').data('order_id','New').modal('show');
        comment_area_height();
    });


    //  Request modal show
    $(document).on('shown.bs.modal','#requestModal', function () {


        //  gett filelist
        // let documents=get_documents('order_id');      
        // $('#filelist').bootstrapTable('destroy').bootstrapTable({
        //     data:documents,
        //     cache: false,
        //     classes:'table-no-bordered',
        //     iconsPrefix: 'fa',
        //     detailView:true,
        //     detailFormatter: 'filedetailFormatter',
        //     rowAttributes:function(row,index) {
        //         return {'data-id':row['id']};
        //     },
        //     icons: {
        //         detailOpen: 'fas fa-list',
        //         detailClose: 'fa-angle-up',
        //     },
        //     columns: [
        //         {   
        //             field:'id',
        //             width:100,
        //             formatter:function(value, row, index){
        //                 let filename=row['name'];
        //                 let filetype=filename.split('.')[1];

        //                 let imgsrc=row['path'];
        //                 if(isImage(filetype)!==true) imgsrc=images['document'];
                        
        //                 let html=`<img title="`+filename+`" src="`+imgsrc+`" /> `;
        //                 return html;
        //             }
        //         },
        //         {
        //             field:'path',
        //             align:'right',
        //             formatter:function(value, row, index){
        //                 let url=value;

        //                 let html=`<a class="btn btn-info btn-sm mt-2" href="`+url+`" download >
        //                             <i class="fa fa-cloud-download-alt "></i>
        //                         </a>`
        //                 return html;
        //             }
        //         },
        //         {
        //             field:'name',
        //             formatter:function(value, row, index){
        //                 let filesize=Number(row['size']);
        //                 let html=` <p class="font-weight-bold ellipsis pl-2 pr-2 mb-0 filename">`+value+`</p>
        //                             <small class="pl-2">`+bytesChange(filesize)+`</small>`;
        //                 return html;
        //             }
        //         },
        //         {
        //             align:'right',
        //             formatter:function(value, row, index){
        //                 let html=`<button type="button" class="btn btn-danger btn-sm mt-1">
        //                             <i class="fas fa-trash-alt"></i>
        //                         </buton>`
        //                 return html;
        //             }
        //         },
        //     ],
        //     formatNoMatches: function () {
        //         let html=NoMatches('No parent form record');
        //         return html;
        //     },
        //     formatLoadingMessage: function(){ 
        //         let html=LoadingMessage();
        //         return html;
        //     },
        //     onLoadError:function(status, jqXHR) {
        //         console.log(status);
        //         console.log(jqXHR);
        //     },
        //     onPostBody:function(name, args){
        //     }
        // });
        comment_area_height();
        


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
                        alertmodal_show();
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
                    // formdata.append('order',order_id);
                    formdata.append('order',1);
                    let target;
                    $.ajax({
                        // url:fakedata_path+'patch_files.json',測試用請刪除
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
                                "path": images['upload'],
                                "order": order_id,
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
                        error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); console.log('Uploading fail~') },
                        success: function ( result, textStatus, XMLHttpRequest ){ 
                            let id=result.id
                            $('#filelist').find('tbody').find('tr').last().data('id',id);
                        },
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
    //  toggle file div
        $('#file_div_toggle').find('i').off().on('click',function(){
            let file_div=$('#file_div_toggle').siblings('.file');
            console.log($('#file_div_toggle').siblings('.file'));
            $(this).toggleClass('fa-angle-up fa-angle-down');
            console.log('here');
            if($(this).hasClass('fa-angle-down')){
                // Close filediv
                file_div.slideUp();
            }else{
                file_div.slideDown();
            }
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
        $(document).on('click','#filelist .file_description_edit',function(){
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
        $(document).on('click','#filelist .file_description_save',function(){
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
        $(document).on('click','#filelist .file_description_cancel',function(){
            let target=$(this).parents('.detail-view');
            collapse_description(target);
        });
        $(document).on('change','#filelist .detail-view textarea.bd-none',function(){
            let target=$(this).parents('.detail-view');
            let alerthtml=`<small class="pl-1 text-info font-weight-bold description_alert">Last edit not completed yet~</small>`;
            let cancelbtn=target.find('.file_description_cancel');
            cancelbtn.on('click',function(){
                target.find('textarea.bd-none').addClass('bd-info').removeClass('bd-none');
                if(target.find('.description_alert').length==0) $(alerthtml).insertAfter(target.find('textarea'));
            });
        });


        $(document).on('input change','#complete_rate',function  (){
            limit0to100('#complete_rate');
        });
 




    //  Comment area
        $(document).on('click','#toggle-commentarea',function(){ 
            // if($(this).hasClass('active'))  comment_area_height_expand('imgage_dev','image_label_dev','authors','FormRequest','comment_area');
            if($(this).hasClass('active'))  comment_area_height_expand();
            else comment_area_height();
            // else comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
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


