$(function(){    
    $('#requestModal').modal('show');

    $('#requestModal').find('.selectpicker').selectpicker('render');
//  Form fields - Select Options
    let Obj=get_options();
    let optionsValue=Object.values(Obj)[0];
    $.each(optionsValue,function(groupname,options){
        $('#sel_function').append('<optgroup label="'+groupname+'"></optgroup>');
        $.each(options,function(i,subfunc){
            let el=$('#sel_function').find('optgroup').last()[0];
            let func_subfunc=groupname+"_"+subfunc;
            $("<option>").text(subfunc).val(func_subfunc).appendTo(el);            
        })
    });
    $('#sel_function').selectpicker('refresh');



//  Form fields - Select accounts
    let accounts=get_accounts();
    $('#sel_accounts').empty();
    $('#sel_accounts').append('<option value=""> Select... </option>');
    $.each(accounts,function(){
        let account_info=$(this)[0];
        $('#sel_accounts').append('<option value="'+account_info['id']+'">'+account_info['code']+'</option>');
    });
    $('#sel_accounts').selectpicker('refresh');

//  Form fields - Select projects
    $('#sel_accounts').on('change',function(){
        let acc_id=$('#sel_accounts').val();
        let projects=get_projects(acc_id);
        $('#sel_projects').empty();
        $('#sel_projects').append('<option value=""> Select... </option>');
        $.each(projects,function(){
            let project_info=$(this)[0];
            $('#sel_projects').append('<option value="'+project_info['id']+'">'+project_info['name']+'</option>');
        });
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
                let name=$(this)[0]['display_name'].split('/Wistron')[0];
                let id=$(this)[0]['employee_id'];
                $('#sel_assigners').append('<option value="'+id+'">'+name+'</option>');
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
            let files;
            files=$('#files')[0].files;    //重新取得[input type='file']資料
            files=Array.prototype.slice.call(files);  //將偽數組轉成陣列
            fileLists=fileLists.concat(files);   //重複的圖片還是會加在後面

            let fileindex = fileLists.length-1;
            let filename = fileLists[fileindex].name;
            let filesize = fileLists[fileindex].size;
            let filetype = files[0].type.split("/")[1].toLowerCase();
            let imgsrc = images['upload'];
            let template = file_downloading_template('new',filename,filesize);

            // if(filesize<=file_size_limit){
            if(true){
                $('#filelist').find('tbody').append(template);
                let thisrow=$(document).find('#filelist').find('tr').last();
                thisrow.find('img').prop('src',imgsrc).addClass('bg-grey animated flash infinite');
                comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h)
                
                //  document key name rule 測試中~等spec後會再更動
                let key;
                for(i=1;i<=fileslimit; i++){
                    if(documentkeys_exited.includes(i)) console.log(i+'exited');
                    else {
                        key='document_'+i;
                        break;
                    }
                }
                let formData = new FormData();
                formData.append(key,files);
    
                let transmit_time_start;
                let transmit_time_end;
                let transmit_time_last = 0;
                let transmit_loaded_last = 0;
                let upload_start_time; // 開始上傳的時間(毫秒)
    
                $.ajax({
                    url:fakedata_path+'patch_files.json',
                    method:'POST',
                    dataType: 'json',
                    data: formData,
                    timeout:310000,
                    cache: false,
                    processData: false, 
                    contentType : false,
                    beforeSend: function ( XMLHttpRequest ){
                        formdata_console(formData);
                    },
                    error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
                    // success: function ( result, textStatus, XMLHttpRequest ){
                    complete: function ( result, textStatus, XMLHttpRequest ){// 測試後請刪除
                        res=patch_documents();
    
                        let url=res['documents'][key]['link'];
                        let filename=res['documents'][key]['link'].split('/').pop();
                        let filetype=filename.split('.')[1];
                        let imgsrc='';
    
                        if(isImage(filetype)) imgsrc=url;
                        else imgsrc=images['document'];
                        //  Remove progress bar and animation
                        thisrow.find('.progress').remove();
                        thisrow.find('.loadedpercent').remove();
                        thisrow.find('img').prop('src',imgsrc).removeClass('bg-grey animated flash infinite');
                    },
                    xhr: function() {
                        let xhr = $.ajaxSettings.xhr();
                        xhr.upload.onloadstart = function(e) {
                            transmit_time_start = e.timeStamp;
                            thisrow.find('.loadedpercent').text('0%');
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
    
                                thisrow.find('.progress-bar').css('width', Percentage + '%');
                                thisrow.find('.loadedpercent').numerator({
                                    toValue	: (Percentage <= 1 ? Percentage : Percentage-1),
                                    easing	: 'linear',
                                    duration: 100, //default 500
                                    onStart	: function() {
                                        thisrow.find('.loadedpercent').text('0%');
                                    },
                                    onStep	: function() {
                                        thisrow.find('.loadedpercent').text(Percentage + '%' );
                                    }
                                });
                            }
                        };
                        return xhr;
                    }
                });
            }else{
                $('#alertModal').find('img').prop('src',images['404']);
                $('#alertModal').modal('show');
            }

            // not renove tr total
            let tr_num=$('#filelist').find('tr:not(.animated)').length;
            if(tr_num>=fileslimit) {
                //  upload file input disabled
                $('#files').prop('disabled',true);
                $('#files').parent('label').addClass('upload-style_disabled');
                $('#files').parent('label').siblings('h6').html('Uploaded number limited less than<span class="ml-2 font-weight-bold">'+fileslimit+'</span>.');
            }

            //  remove #files value --> so the change event can continue    
            $(this).val('');
        });
        $(document).on('click','#filelist button.btn-danger',function(){
            $(this).parents('tr').addClass('animated zoomOutRight',function(){
                $(this).fadeOut(function(){
                    comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
                });
                if($('#files').prop('disabled')) {
                    //  upload file input cancel disabled
                    $('#files').prop('disabled',false);
                    $('#files').parent('label').removeClass('upload-style_disabled');
                    $('#files').parent('label').siblings('h6').html(' Drag&Drop or Click to choose your file.<i class="fa fa-cloud-upload-alt fa-lg ml-2"></i> ');
                }
            });
        });






    $('#requestModal').on('shown.bs.modal',function(){
        $('#toggle-commentarea').removeClass('active');
        $('#toggle-commentarea').find('i').removeClass('active fa-chevron-down').addClass('fa-chevron-up');

        // Load comments history
        let comments=get_record_history();
        $.each(comments,function(){
            let comment_obj=$(this)[0];
            append_comment_template('#comment_area',comment_obj)
        });


        //  Get fields
        let documents=get_documents()['documents'];
        documentkeys_exited=[];
        $.each(documents,function(keyname,doc_obj){

            let url=doc_obj['link'];
            let filesize=Number(doc_obj['size_byte']);
            let filename=[...doc_obj['link'].split('/')].pop();
            let filetype=filename.split('.')[1];
            let imgsrc='';
            let keynum=Number(keyname.split('_')[1]);

            //  Store exited document key --> arrary
            documentkeys_exited.push(keynum);

            if(isImage(filetype)) imgsrc=url;
            else imgsrc=images['document'];

            let template = file_render_template(keyname,url,filesize);
            $('#filelist').find('tbody').append(template);
            $('#filelist').find('tr').last().find('img').prop('src',imgsrc);

        });

        // reset condition
        comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
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

    //  Form request validate setting
        $('#FormRequest').validate({
            rule:{
                description:{
                    required: true,
                    summernote_validated:true
                }
            }
        });

    //  Validate fields - init request
        $( "#initialize_btn" ).on( "click",function(){
            if($('#FormRequest').validate().form()){
                // let formData=new FormData();
                // let fields=$(this).find('[name]');
                // packageData('#FormRequest',formData);

                let statusObj={"p1_initiator": "Approve"}
                let init_data=package_data('#FormRequest');
                init_data['status']=JSON.stringify(statusObj)
                init_data['initiator']=$('#form_initiator').data('id');
                post_order(init_data);
            }else console.log('#FormRequest valid false');     
        });










    


});


