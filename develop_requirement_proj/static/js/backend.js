// Orders Operation
    // GET Fetch Order's Ancestor Collection by Order Id
    function get_tag_record(order_id){
        let res='';
        //  測試完請刪除
        let url_select=randomnum(0,2);
        let urls=[fakedata_path+'tagtable.json',fakedata_path+'empty_table.json'][url_select];
        let url='./api/orders/'+order_id+'/ancestors/';  
        urls=fakedata_path+'tagtable.json';
        $.ajax({
            url:urls, // {{service_url}}/api/orders/:id/ancestors/  
            method:"GET",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    //  POST Create an Orders
    function post_order(formdata){
        //  backend check field
        let field=backend_check_fields(formdata).join();
        formdata['field']=field;

        //  測試完請刪除
        $.ajax({
            // url:'./api/orders/',//{{service_url}}/api/orders/
            url:'#',//{{service_url}}/api/orders/
            method:"GET",
            data:formdata,
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
    }

    






// Histories Operation
    function append_comment_template(target,comment_obj){
        let editor_info=comment_obj['editor']
        let comment=comment_obj['comment'];
        let time=isotime_local(comment_obj['timestamp']);
        let comment_template='';

        if(editor_info['display_name']=='DQMS system'){
            comment_template=`<div class="mb-2">
                <div class="mx-auto">
                    <img class="sticker position-absolute" src="`+images['logoportrait']+`"></img>
                    <h3 class="ml-2 pl-4 pr-2 p-2 badge badge-dark badge-pill font-weight-bold">
                        `+editor_info["display_name"]+`
                        <span>`+comment+`</span>										
                    </h3>
                    <small class="text-secondary ml-1 font-weight-bold">`+time+`</small>
                </div>					
            </div>`;
        }else{
            comment_template=`<div class="mb-2">
               <div class="d-inline-flex align-items-top">
                   <img class="sticker mr-2" src="`+editor_info['avatar']+`">
                   <div><small class="text-dark mb-1 mr-3 font-weight-bold">`+editor_info["display_name"]+`</small></div>
               </div>
               <div class="bg-grey comments_shape">
                   <div class="text-dark p-2">`+comment+`</div>
               </div>
               <small class="text-secondary d-flex justify-content-end mr-2 font-weight-bold">`+time+`</small>
            </div>`;
        }
        $(target).append(comment_template);
    }


    // GET Filter Histories Collection by Order Id
    function get_record_history(orders_id){
        let res='';
        $.ajax({
            url:fakedata_path+'comment_history.json',
            method:'GET',
            dataType: "json",
            data: {'orders_id':orders_id},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }


    // POST Create User's Comment Histories
    function post_record_history(comment_obj){
        let res='';   
        // $.ajax({
        //     url:'histories/',
        //     method:"POST",
        //     dataType: "json",
        //     data: comment_obj,
        //     async: false,
        //     timeout: 5000,
        //     beforeSend: function ( XMLHttpRequest ){},
        //     error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
        //     success: function ( result, textStatus, XMLHttpRequest ){
        //         res=result;
        //         console.log(res);
        //     }    
        // });
        return res;
    }




//  Documents Operation
    function get_documents(){
        let res='';   
        $.ajax({
            url:fakedata_path+'files.json',
            method:"GET",
            dataType: "json",
            data: {},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    function patch_documents(){
        let res='';   
        $.ajax({
            url:fakedata_path+'patch_files.json',
            method:"GET",
            dataType: "json",
            data: {},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }





//  Developer Groups Operation
    function get_developers(){
        let res='';
        $.ajax({
            url:fakedata_path+'developers.json',
            method:'GET',
            dataType: 'json',
            data: '',
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
   


//  Employees Operation
    function get_employees(data){
        let res='';
        $.ajax({
            url:fakedata_path+'employees.json', //測試後請刪除
            // url:'/api/employees/',
            method:'GET',
            dataType: 'json',
            data: data,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }



 
//  Accounts Operation
    function get_accounts(data){
        let res='';
        $.ajax({
            url:fakedata_path+'accounts.json', //測試後請刪除
            method:'GET',
            dataType: 'json',
            data: data,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }    



//  Projects Operation
    function get_projects(acct_id){
        let res='';
        $.ajax({
            url:fakedata_path+'projects.json', //測試後請刪除
            method:'GET',
            dataType: 'json',
            data: {'acct_id':acct_id},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }  




//  Options Operation(function team)
    function get_options(){
        let res='';
        $.ajax({
            url:'/static/js/fakedata/options.json',
            method:"GET",
            dataType: "json",
            data: {},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }



//  Assigners Operation
    function get_assigners(sub_function,project_id){
        let assigners='';
        $.ajax({
            url:fakedata_path+'assigners.json',
            method:'GET',
            dataType: 'json',
            data: {
                'sub_function':sub_function,
                'project_id':project_id
            },
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                assigners=result;
            }    
        });
        return assigners;
    }




/*
    function patch_documents(key,file){
        let res='';   
        $.ajax({
            url:fakedata_path+'patch_files.json',
            method:"PATCH",
            dataType: "json",
            data: {},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( result, textStatus, XMLHttpRequest ){ console.log( result );  console.log( textStatus ); },
            success: function ( result, textStatus, XMLHttpRequest ){
                // res=result
            },
            xhr: function() {
                let xhr = $.ajaxSettings.xhr();
                xhr.upload.onloadstart = function(e) {
                    transmit_time_start = e.timeStamp;
                    $(".loadedpercent").text( "0%" );
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

                        upload_rate = Math.round(e.loaded / time); // 多少B/秒
                        upload_rate_unit = "B/s"; // 單位
                        upload_estimate_time = Math.round(data / upload_rate); // 估算剩餘上傳完成的時間(秒)
                        if (e.loaded / 1024 / 1024 > 1) {
                            upload_rate = (e.loaded / 1024 / 1024 / time).toFixed(2); // 多少MB/秒
                            upload_rate_unit = "MB/s"; // 單位
                        } else if (e.loaded / 1024 > 1) {
                            upload_rate = (e.loaded / 1024 / time).toFixed(2); // 多少KB/秒
                            upload_rate_unit = "KB/s"; // 單位
                        }
                        
                        if( upload_estimate_time > 300 ){
                            upload_estimate_time_unit = "minutes"
                            upload_estimate_time = upload_estimate_time/60;
                        }else{
                            upload_estimate_time_unit = "seconds"
                        }
                        //  UI render - progress 
                        //  (upload_estimate_time+" "+upload_estimate_time_unit) estimatedTime
                        //  (upload_rate+" "+upload_rate_unit) uploadRate
                         
                        // console.log(" + upload_rate + upload_rate_unit + " | " + upload_estimate_time + "秒");
                        $( ".progress-bar" ).css('width', Percentage + "%");
                        $( ".progress-bar" ).numerator({
                            toValue	: (Percentage <= 1 ? Percentage : Percentage-1),
                            easing	: 'linear',
                            duration: 100, //default 500
                            onStart	: function() {
                                $( ".loadedpercent" ).text( "0%" );
                            },
                            onStep	: function() {
                                $( ".loadedpercent" ).text( Percentage + " %" );
                            }
                        });
                    }
                };
                return xhr;
            },

        });
        return res;
    }
*/