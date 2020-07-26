// Orders Operation
    // GET Fetch Orders Collection


    // GET Fetch Order's Ancestor Collection by Order Id
    function get_tag_record(order_id){
        // let path=fakedata_path+'tagtable.json';//  測試完請刪除
        //  測試完請刪除 let urls=[fakedata_path+'tagtable.json',fakedata_path+'empty_table.json'][randomnum(0,2)];
        let path='/api/orders/'+order_id+'/ancestors/';
        let res='';
        $.ajax({
            url:path, 
            method:"GET",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    function get_filter_orders(filter_data){
        //  filter format->{"param":filter}
        let path='/api/orders/';
        let res='';
        $.ajax({
            url:path, 
            method:"GET",
            data:{"filter":JSON.stringify(filter_data)},
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }



    // GET Fetch a Specific Orders
    function get_single_order(id){
        // let path=fakedata_path+'singleform_info.json';//  測試完請刪除
        let path='/api/orders/'+id+'/';
        let res='';
        $.ajax({
            url:path,
            method:"GET",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }

    

    //  GET Fetch Order's Signature Collection by Order Id
    function get_signaturers(id){
        // let path=fakedata_path+'signaturers.json';//  測試完請刪除       
        let path='/api/orders/'+id+'/signatures/';       
        let res='';
        $.ajax({
            url:path,
            method:"GET",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }


    //  PUT Update Order's Signature Deatail by Order Id and Signature Id
    function put_signaturers(order_id,signature_id,formdata){
        // let path=fakedata_path+'signaturers.json';//  測試完請刪除
        let path='/api/orders/'+order_id+'/signatures/'+signature_id+'/'
        let res='';         
        $.ajax({
            url:path,
            method:"PUT",
            dataType: "json",
            data:formdata,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
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
        // formdata['fields']=field;
        //let path=fakedata_path+'singleform_info.json';  測試完請刪除
        let path='/api/orders/'; 
        let res='';
        $.ajax({
            url:path,
            method:"POST",
            data:formdata,
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }

    // PATCH Update Partially Specific Orders Detail
    function patch_order(order_id,formdata){
        // let field=backend_check_fields(formdata).join();
        // let path=fakedata_path+'singleform_info.json';//  測試完請刪除
        let path='/api/orders/'+order_id+'/';
        // formdata['fields']=field;
        let res='';
        $.ajax({
            url:path,
            method:"PATCH",
            data:formdata,
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }

    // PATCH Update Partially Specific Orders Detail
    function get_order_histories(order_id){
        let path='/api/orders/'+order_id+'/trackers/';
        // formdata['fields']=field;
        let res='';
        $.ajax({
            url:path,
            method:"GET",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }

    // GET Filter Histories Collection by Order Id
    function get_comment_history(order_id){
        // let path=fakedata_path+'comment_history.json';//  測試完請刪除
        let path='/api/comments/';
        let res='';
        $.ajax({
            url:path,
            method:'GET',
            dataType: "json",
            data: {'order':order_id},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }


    // POST Create User's Comment Histories
    function post_comment_history(comment_obj){
        let path='/api/comments/';
        let res='';   
        $.ajax({
            url:path,
            method:"POST",
            dataType: "json",
            data: comment_obj,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }




//  Documents Operation
    //  GET Filter Documents Collection by Order Id
    function get_documents(order_id){
        // let path=fakedata_path+'files.json';//  測試完請刪除
        let path='/api/documents/';
        let res='';
        if(order_id=='New'){
            console.log('Init New request -- get fileslist=[]');
        }else{
            $.ajax({
                url:path,
                method:"GET",
                dataType: "json",
                data: {
                    'order':order_id
                },
                async: false,
                timeout: 5000,
                beforeSend: function ( XMLHttpRequest ){},
                error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
                success: function ( result, textStatus, XMLHttpRequest ){
                    res=result;
                }    
            });
        }
        return res;
    }


    // PATCH Update Documents Detail
    function update_document_detail(update_file_data){
        // let path=fakedata_path+'patch_files.json';//  測試完請刪除
        let id=update_file_data['id'];
        let path='/api/documents/'+id+'/';
        let res=false;
        $.ajax({
            url:path,
            method:"PATCH",
            dataType: "json",
            data: update_file_data,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                console.log('Update file deatil successfully~');
                res=true;
            }    
        });
        return res;
    }

    // Delete Update Documents Detail
    function delete_document(id){
        // let path=fakedata_path+'patch_files.json';//  測試完請刪除
        let path='/api/documents/'+id+'/';
        $.ajax({
            url:path,
            method:"DELETE",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }



//  Schedules Operation
    //  GET Filter Schedules Collection by Order Id
    function get_current_schedule(order_id){
        // let path=fakedata_path+'schedule.json';//  測試完請刪除
        let path='/api/schedules/';
        let res='';
        $.ajax({
            url:path,
            method:'GET',
            data:{'order':order_id},
            dataType: 'json',
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    //  Filter Schedules History by Order Id
    function get_schedule_history(order_id){
        // let path=fakedata_path+'schedule.json';//  測試完請刪除
        let path='/api/schedules/group_tracker/'+order_id+'/';
        let res='';
        $.ajax({
            url:path,
            method:'GET',
            dataType: 'json',
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    //  POST Create a Schedules
    function post_schedule(add_schedule_data){
        // let path=fakedata_path+'schedule.json';//  測試完請刪除
        let path='/api/schedules/';
        let res='';
        $.ajax({
            url:path,
            method:'POST',
            dataType: 'json',
            data:add_schedule_data,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    //  PATCH Update Partially Schedules Detail
    function patch_schedule(id,update_schedule_data){
        // let path=fakedata_path+'schedule.json';//  測試完請刪除
        let path='/api/schedules/'+id+'/';
        let res='';
        $.ajax({
            url:path,
            method:'PATCH',
            dataType: 'json',
            data:update_schedule_data,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    //  PATCH Update Partially Schedules Detail
    function delete_schedule(id){
        // let path=fakedata_path+'schedule.json';//  測試完請刪除
        let path='/api/schedules/'+id+'/';
        let res='';
        $.ajax({
            url:path,
            method:'DELETE',
            dataType: 'json',
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }






//  Development Progress Operation
    //  GET Filter Development Progress Collection by Order Id
    function get_progress(order_id){
        // let path=fakedata_path+'progress.json';//  測試完請刪除
        let path='/api/progress/';
        let res='';
        $.ajax({
            url:path,
            method:'GET',
            data:{"order":order_id},
            dataType: 'json',
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    function post_progress(formdata){
        // let path=fakedata_path+'progress.json';//  測試完請刪除
        let path='/api/progress/';//  測試完請刪除
        let res='';
        $.ajax({
            url:path,
            method:"POST",
            data:formdata,
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    function patch_progress(id,formdata){
        let path='/api/progress/'+id+'/';
        let res='';
        $.ajax({
            url:path,
            method:'PATCH',
            dataType: 'json',
            data:formdata,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }
    function delete_progress(id){
        let path='/api/progress/'+id+'/';//  測試完請刪除
        let res='';
        $.ajax({
            url:path,
            method:"DELETE",
            dataType: "json",
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }





//  Developer Groups Operation
//  Employees Operation
    //  GET Search Employees with Site / Employee Id / English Name / Extension / Department ID
    function get_employees(data){
        // let path=fakedata_path+'developers.json';//  測試完請刪除
        let path='/api/employees/';
        let res='';
        $.ajax({
            url:path,
            method:'GET',
            dataType: 'json',
            data: data,
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }






// sub_function
//  Accounts Operation
    function get_accounts(sub_function){
        // let path=fakedata_path+'accounts.json';//  測試完請刪除
        let path='/api/accounts/';
        let res='';
        $.ajax({
            url:path, 
            method:'GET',
            dataType: 'json',
            data: {
                'sub_function':sub_function,
            },
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }    



//  Projects Operation
    function get_projects(acct_id){
        // let path=fakedata_path+'projects.json';//  測試完請刪除
        let path='/api/projects/';//  測試完請刪除

        let res='';
        $.ajax({
            url:path, 
            method:'GET',
            dataType: 'json',
            data: {'acct_id':acct_id},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }  




//  Options Operation(function team)
    function get_options(){
        // let path=fakedata_path+'options.json';//  測試完請刪除
        let path='/api/options/?field=dept_category';//  測試完請刪除

        let res='';
        $.ajax({
            url:path,
            method:"GET",
            dataType: "json",
            data: {},
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
            success: function ( result, textStatus, XMLHttpRequest ){
                res=result;
            }    
        });
        return res;
    }



//  Assigners Operation
    function get_assigners(sub_function,project_id){
        // let path=fakedata_path+'assigners.json';//  測試完請刪除
        let path='/api/assigners/';//  測試完請刪除

        let assigners='';
        $.ajax({
            url:path,
            method:'GET',
            dataType: 'json',
            data: {
                'sub_function':sub_function,
                'project_id':project_id
            },
            async: false,
            timeout: 5000,
            beforeSend: function ( XMLHttpRequest ){},
            error: function ( jqXHR, textStatus, errorThrown,exception ){ errormsg( jqXHR, textStatus, errorThrown,exception) },
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