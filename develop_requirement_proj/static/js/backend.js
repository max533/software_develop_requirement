// Orders Operation
    // GET Fetch Order's Ancestor Collection by Order Id
    function get_tag_record(order_id){
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
        let path='/api/orders/';
        let res='';
        $.ajax({
            // url:path,
            url:'path',
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
        let path='/api/orders/'+order_id+'/';
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
        let path='/api/progress/';
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
        let path='/api/progress/'+id+'/';
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
        let path='/api/projects/';
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
        let path='/api/options/?field=dept_category';
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
        let path='/api/assigners/';
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


//  Notifications Operation
    //  GET Fetch Notifications Collection by Current User
    function get_notifications_currentUser(){
        let path='/api/notifications/';
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
    //  PUT Update Notifications Detail
    function put_notifications_currentUser(id){
        let path='/api/notifications/'+id+'/';
        let res='';
        $.ajax({
            url:path,
            method:'PUT',
            dataType: 'json',
            data:{
                'id':id,
                'read_status':true
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
