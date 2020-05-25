//  Param rule
    // order_id will store requestModal datat-order_id >> $('#requestModal').data('order_id'


//  Global param
    loginInfo = {
        'employee_id' : Object.keys(profile)[0],
        'dispaly_name' : Object.values(profile)[0][ 'display_name' ],
        'role' : Object.values(profile)[0][ 'role' ],
        'projectRole': Object.values(profile)[0][ 'project' ]
    };
    loginInfo['avatar']=avatar_get(loginInfo.employee_id);  

    function alertmodal_show(img=images['404'],
        title='-- Upload Denied --',
        content='Upload file selected is oversize. Max-allowed-uploaded-file size is <strong>10 Mb</strong>.'){
        $('#alert_img').prop('src',img);
        $('#alert_title').text(title);
        $('#alert_content').html(content);
        $('#alertModal').modal('show');
    }

//  Basic
    function isImage(filetype){
        let imageFile=['tiff','tif','png','gif','jpg','jpeg']
        if( imageFile.includes(filetype) ) return true;
        else return false;
    }
    function get_now_isotimeformat(){
        let now=new Date().toISOString();
        return now;
    }
    function isotime_local(timestamp){
        let format_time = new Date(timestamp)
                .toLocaleString('zh', { hour12: false }) // 2020/3/21 04:26:38
                .replace(/\//g, '-') // 2020-3-21 04:26:38
                .slice(0,-3); // 2020-3-21 04:26
        return format_time;
    }
    function formdata_console(target){
        for(var pair of target.entries()) {
            console.log(pair[0]+ ', '+ pair[1]); 
        }
    }

    function limit0to100(e,v){    
        console.log(typeof(v))   
        let reg = /^(([1-9]\d?(\.\d?[1-9])?)|(0(\.\d?[1-9])?)|100)$/;
        if(v.match(reg)){
            return false;
        }else{
            return true;
        }
    }
    //  Restrict input number only
    function ValidateNumber(e, pnumber){
        let reg = /^(([1-9]\d?(\.\d?[1-9])?)|(0(\.\d?[1-9])?)|100)$/;

        if (!reg.test(pnumber))
        {
            $(e).val(reg.exec($(e).val()));
        }
        return false;
    }


    //  Modal package data
    function package_data(form){
        let formdata={};
        $(form).find('[name]').each( function () {
            if($(this).prop('required')){
                let field=$(this).prop('name');
                let value=$(this).val();
                
                switch( $(this).attr('type') ){
                    case 'radio':
                        if( $(this).prop('checked') ){
                            formdata[field]=value;
                        }
                        break;
                    case 'textarea':
                        if ($(this).val()!==null){
                            formdata[field]=value;
                        }
                        break;    
                    case 'select':
                        if ($(this).val()!==null){
                            let name=$(this).prop('name');
                            formdata[field]=value;

                            if(name=='function'){
                                let v=$(this).val() // EE_Power
                                let develop_team_function=v.split('_')[0];
                                let develop_team_sub_function=v.split('_')[1];
                                formdata['develop_team_function']=develop_team_function;
                                formdata['develop_team_sub_function']=develop_team_sub_function;
                                delete formdata['function']
                            }
                        }
                        break;
                    case 'file':
                        break;
                    default:
                        formdata[field]=value;
                        break;
                }
            }
            
        });
        return formdata;
    }
    function backend_check_fields(formdata){
        let fields=[];
        if(formdata!==undefined){
             $.each(Object.keys(formdata),function(i,field){
                fields.push(field);
            });
            return fields;
        }else console.log('Data is empty!!')
    }


//  UI Flow
    function author_arr(order_reponse){
        let initiator=order_reponse['initiator']['employee_id'];
        let assigner=order_reponse['assigner']['employee_id'];
        let contactor=order_reponse['developers']['contactor'];
        let arr=[{initiator:'initiator'},{assigner:'assigner'},{contactor:'contactor'}];
        return arr;
    }

    function indentify_user(employee_id,author_arr,){

    }

    function form_display(){

    }




//  Table setting 
    //  click btn to collapse down the more information
    function detailFormatter(index, row) {
        let last_comment_obj=[...get_record_history(row.id)].pop();
        let modifiedtime = isotime_local(last_comment_obj['timestamp']);
        let record = last_comment_obj['comment'];
        let editor_name = last_comment_obj['editor']['display_name'];
        let editor_avatar = avatar_get(last_comment_obj['employee_id']);
        let html = `<div class="ml-4">
                        <div class="d-inline-flex align-items-center">
                            <small class="font-weight-bold pt-1 mr-2">Last editor/ </small>
                                <img class="sticker mr-2" src="`+editor_avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
                                <h6 class="pt-1">`+editor_name+`</h6></div><div><p>
                            <small class="font-weight-bold">Last record/ </small>`+record+`</p
                            ><small class="text-secondary">Last modified time/ `+modifiedtime+`</small>
                        </div>`
        return html;
    }
    function filedetailFormatter(index, row) {
        let html = `<h6 class="badge badge-secondary badge-pill mt-2">
                        <i class="fas fa-sticky-note mr-2"></i>Description
                    </h6>
                    <p class="font-weight-bold bd-radius-8 p-1">`+row['description']+`</p>
                    <textarea class="w-100 font-weight-bold bd-radius-8 bg-white p-1 bd-none" palceholder="File desciption..." style="display:none;">`+row['description']+`</textarea>
                    <div class="text-right mb-2 mt-1">
                        <button type="button" class="btn btn-info btn-sm file_description_edit"><i class="fa fa-edit mr-1"></i>Edit</button>
                        <button type="button" class="btn btn-success btn-sm file_description_save" style="display:none;"><i class="fa fa-check-double mr-1"></i>Save</button>
                        <button type="button" class="ml-2 btn btn-secondary btn-sm file_description_cancel" style="display:none;"><i class="fa fa-times mr-1"></i>Cancel</button>
                    </div>`;
        return html;
    }

    //  Set the key and value sent to backend
    function queryParams(params) { 
        //這裡的鍵的名字和控制器的變量名必須一直，這邊改動，控制器也需要改成一樣的 
        var queryParams_temp = { 
            page_size: params.limit, //頁面大小 
            page_number: (params.offset / params.limit) + 1, //頁碼 
            sortOrder: params.order, //排位命令（desc，asc）

        };
        //  Redefine filter data
        if('filter' in params){
            let filterObj = $.parseJSON(params.filter);
            if( 'account' in filterObj){
                let account_id = filterObj['account'].split(' _ ')[0];
                filterObj['account_id'] = account_id;
                delete filterObj.account;
            }
            if( 'project' in filterObj){
                let project_id = filterObj['project'].split(' _ ')[0];
                filterObj['project_id'] = project_id;
                delete filterObj.project;
            }
            if( 'form_begin_time' in filterObj){
                
                let start = filterObj['form_begin_time'].split(' - ')[0];
                let end = filterObj['form_begin_time'].split(' - ')[1];
                console.log('here');
                let form_begin_time__before=new Date(start).toISOString();
                let form_begin_time__after=new Date(end).toISOString();
                filterObj['form_begin_time__before'] = form_begin_time__before;
                filterObj['form_begin_time__after'] = form_begin_time__after;
                delete filterObj.form_begin_time;
            }

            queryParams_temp['filter'] = JSON.stringify(filterObj);
        }
        return queryParams_temp; 
    }
    //  Format
    //  Table-formatNoMatches
    function NoMatches(messages) {
        let html=`<div class="d-flex justify-content-center bg-grey mt-2 tag_404_result">
                    <img src="`+images['404']+`" class="mt-3">
                    <h5 class="text-secondary position-absolute mt-3 bg-grey animated">FIND NOTHING!</h5>
                    <small class="text-secondary position-absolute mt-5 font-weight-bold">`+messages+`</small>
                </div>`;
        // let html=`<div class="d-flex justify-content-center bg-grey mt-2 tag_404_result">
        //             <img src="`+images['404']+`" class="mt-3">
        //             <h5 class="text-secondary position-absolute mt-3 bg-grey animated flash hingedown">FIND NOTHING!</h5>
        //             <small class="text-secondary position-absolute mt-5 font-weight-bold">`+messages+`</small>
        //         </div>`;
        return html;
    }
    //  Table-formatLoadingMessage
    function LoadingMessage() {
        let html=`<div class="text-center font-weight-bold mt-3 mb-2">
                    <h6>Loading<img class="ml-1" style="width: 30px;" src="`+images.loadinggif_path+`"></h6>
                </div>`;
        return html;
    }


    //  Timeline
    function loadTimeline(index,timelineTab,target,execTime) {

        let maxIndex=timelineTab.length;
        if(index < maxIndex) {
            addTimelineElement(index,timelineTab,target);
            setTimeout(function() {
            loadTimeline(index+=1,timelineTab,target);
            },execTime);
        }else{
            window.lineTime.style.height = 3.5 * (index) + "rem";
            window.lineTimePoint.classList.add("active");
        }
    }
    function addTimelineElement(index,timelineTab,target){
        var element = timelineTab[index];
        var blocTimeline = document.createElement("div");
        var blocTimelineLeft = document.createElement("div");
        var blocTimelineRight = document.createElement("div");
        blocTimeline.setAttribute("class", "bTimeline");
        blocTimelineLeft.setAttribute("class", "bLeft");
        blocTimelineRight.setAttribute("class", "bRight");
        var date = document.createElement("label");
        var para = document.createElement("p");
        var icon = document.createElement("i");
        var point = document.createElement("div");
        point.setAttribute("class", "bPoint");
        icon.setAttribute("class", "colorBlue fa fa-sm fa-" + element.icon);
        para.setAttribute("class", "colorBlue");
        date.setAttribute("class", "colorBlue");
        date.innerHTML = element.date;
        para.innerHTML = element.texte;
        blocTimelineLeft.appendChild(icon);
        blocTimelineRight.appendChild(date);
        blocTimelineRight.appendChild(para);
        blocTimeline.appendChild(point);
        blocTimeline.appendChild(blocTimelineLeft);
        blocTimeline.appendChild(blocTimelineRight);

        $(target).append(blocTimeline);
    }
    //  comment area height
    function comment_area_height_expand(){
        let image = $('#imgage_dev').find('img').first();
        let form_h=parseInt($('#FormRequest_div').css('height').split('px')[0]);
        let imgtext_h = parseInt($('#image_label_dev').css('height').split('px')[0]);
        let comment_h=parseInt($('#comment').parent('div').css('height').split('px')[0]);
        let h = (form_h-imgtext_h-comment_h-100)+'px';
        image.removeClass('animated zoomInDown').addClass('animated zoomOutUp').fadeOut(0);
        $('#comment_area').css('height',h).fadeIn(0);
    }

    function comment_area_height(){        
        let image = $('#imgage_dev').find('img').first();
        let imgtext_h = parseInt($('#image_label_dev').css('height').split('px')[0]);
        let formauthor_h = parseInt($('#authors').css('height').split('px')[0]);
        let global_img_h = parseInt($('#image_status').find('img').first().css('height').split('px')[0]);
        let form_h=parseInt($('#FormRequest_div').css('height').split('px')[0]);
        let comment_h=parseInt($('#comment').parent('div').css('height').split('px')[0]);  
        let h = (form_h-imgtext_h-global_img_h-comment_h-100)+'px';  
        $('#comment_area').css('height',h).fadeIn(0);
        image.removeClass('animated zoomOutUp').addClass('animated zoomInDown').fadeIn(0);
        console.log('HERE');
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


    //  bytes change to suitable num
    function bytesChange(bytes){
        let num ;
        if( typeof(bytes)=="number" && bytes>=0 ){
            if(bytes / 1024 / 1024 / 1024 > 1){
                num = (bytes / 1024 / 1024 / 1024).toFixed(2)+" GB"; //GB
            }else if (bytes / 1024 / 1024 > 1){
                num = (bytes / 1024 / 1024 ).toFixed(2)+"MB"; //MB
            }else if (bytes / 1024 > 1) {
                num = (bytes / 1024 ).toFixed(2)+" KB";; //KB
            }else if (bytes>=0) {
                num = (bytes).toFixed(2)+" B";; //B
            }
            return num;
        
        }else  console.log( bytes+"is not number. typeof "+typeof(bytes) );
    }
    //  TODO BUG Scroll to bottom 
    function scrollToBottom(scroll_tar,position_tar){
        let distance=position_tar.offset().top-Number(position_tar.css('height').slice(0,-2));
        $(scroll_tar).animate({ scrollTop: distance }, 1000);
    }
    //  Validate fields
    $.validator.setDefaults({
        validClass: 'is-valid', // Bootstrap valid class
        errorClass: 'is-invalid', // Bootstrap invalid class
        errorPlacement: function(error,element) {}, // Never show error message
        ignore: ':hidden:not(".summernote"),.note-editor *',
        debug: true, //只驗證  不提交
        invalidHandler: function() {},
        highlight: function(element, errorClass, validClass) {  
            invalidEffect( $(element) );
            callValidation ();
        },
        unhighlight: function(element, errorClass, validClass) {
            resetInvalid( $(element) );
        }
    });
    $.validator.addMethod('summernote_validated',function(element){
        let textareaIsEmpty=$(element).summernote('isEmpty');
        return textareaIsEmpty;
    });
    function callValidation (){
        $('input,.selectpicker').on('change input', function() {
            $(this).valid();
        });
        $(document).on('change keyup','.note-editable.border-danger',function() {
            $(this).parents('.note-editor').siblings('.summernote').valid();
        });
    }     
    function invalidEffect(field){
        switch( field.prop('type') ) {
            case 'radio':
                field.closest('.btn-group').find('label').addClass('border-danger');
                break;
            case 'select-one':
                field.selectpicker('setStyle', 'btn-outline-danger');
                break;
            case 'file':         
                field.parent('label').addClass('border-danger');
                break;
            case 'textarea':      
                field.siblings('.note-editor').find('.note-editable').addClass('border-danger');
                break;
            default:
                field.addClass('border-danger');
                break;
        } 
    }
    function resetInvalid(field){
        switch(field.prop('type')) {
            case 'radio':
                field.closest('.btn-group').find('label').removeClass('border-danger');
                break;
            case 'select-one':
                field.selectpicker('setStyle','btn-outline-danger','remove').selectpicker( 'refresh' );
                break;
            case 'file':
                field.parent( 'label' ).removeClass( 'border-danger' );    
                break;
            case 'textarea':      
                field.siblings('.note-editor').find('.note-editable').removeClass('border-danger');
                break;
            default:
                field.removeClass('border-danger');
                break;
        }
    }
    
    function avatar_get(employee_id){
        let teamroaster_path='http://10.32.20.124:50005/img/avatar/';
        let time=new Date;
        let timestamp=time.getTime();
        let src_path=teamroaster_path+employee_id+'?'+timestamp;
        return src_path.toString();
    }
    // function avatar_exchange(defaultimg,employee_id){
    //     let avatar=avatar_get(employee_id);
    //     let src=defaultimg;
    //     $.ajax({
    //         url:'http://10.32.20.124:50005/img/avatar/10712714?1590030586159',
    //         method:"GET",
    //         timeout: 5000,
    //         crossDomain: true,
    //         dataType: 'jsonp',
    //         async:false,
    //         error: function ( result, textStatus, XMLHttpRequest ){},
    //         success: function ( result, textStatus, XMLHttpRequest ){
    //             console.log('here');
    //         }    
    //     });
    //     return src;
    // }



//  dev_modal.js
    function current_id_arr(data_list){
        let arr=[]
        $(data_list).each(function(i,v){
            arr.push(v['employee_id']);
        });
        return arr;
    }
    function select_devcontacter(target,table,data){
        let sel=$(target).find('.selectpicker');
        let contactwindow=sel.val();
        sel.empty();
        
        sel.append('<option value=""> Select contact window... </option>');
        $.each(data,function(i,v){
            sel.append('<option value="'+v.employee_id+'">'+v.display_name+'</option>');
            if(i==data.length-1) {
                sel.selectpicker('refresh');
                sel.selectpicker('val',contactwindow);
            }
        });
        $('#windowbadge').remove();
        $(table).find('tr').each(function(){
            let id=$(this).data('employee_id');
            if(id==contactwindow){
                $(this).find('td').first().append('<h5 class="badge badge-info badge-pill ml-1" id="windowbadge"><i class="fa fa-user-check mr-1"></i>Contact window</h5>');
            }
        });
    }
    function if_employee_joined(currentIdList,limitation,table,show_count_Target){
        let count_number=currentIdList.length;
        $(table).find('tbody').find('tr').each(function(){
            let Id=$(this).data('employee_id');
            let target=$(this).find('td').last().find('button');
            if(count_number>=limitation){
                target.removeClass('btn-success add').addClass('btn-light');
                    target.html('<i class="fas fa-bullhorn mr-2"></i>Up to limitation <span>'+limitation+'<span>')
                            .prop('disabled',true);
            }else{
                if(currentIdList.includes(Id)){
                    target.removeClass('btn-success add').addClass('btn-light');
                    target.html('<i class="fas fa-signature mr-2"></i>Already joined')
                            .prop('disabled',true);
                }else{
                    target.addClass('btn-success add').removeClass('btn-light');
                    target.html('<i class="fas fa-plus mr-2"></i>Plus')
                            .prop('disabled',false);
                }
            }
        });
        cuunt_current_developers(show_count_Target,count_number,limitation)
    }
    function cuunt_current_developers(show_count_Target,count_number,limitation){
        $(show_count_Target).find('span').eq(0).html('<i class="fa fa-users mr-1 ml-2 text-secondary"></i>'+count_number+'');   
        $(show_count_Target).find('span').eq(1).html('Limitation '+limitation+'');   
        if(count_number>=limitation){
            $(show_count_Target).find('span').removeClass('badge-light').addClass('badge-danger');
            $(show_count_Target).find('span').eq(0).addClass('animated rubberBand infinite');
            $(show_count_Target).find('span').find('i').removeClass('text-secondary');
        }else{
            $(show_count_Target).find('span').removeClass('badge-danger').addClass('badge-light');
            $(show_count_Target).find('span').eq(0).removeClass('animated rubberBand infinite');
            $(show_count_Target).find('span').find('i').addClass('text-secondary');
        } 
    }