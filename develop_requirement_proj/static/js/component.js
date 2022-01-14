//  Global param
    //  Get url param
    function getUrlParameter(sParam) {
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;
        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : decodeURIComponent(sParameterName[1]);
            }
        }
    };


//  GET Fetch Current Employee
    function get_profile(){
        let path='/api/employees/me/';
        let res='';
        $.ajax({
            url:path,
            method:'GET',
            dataType: 'json',
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
    profile=get_profile();
    loginInfo = {
        'employee_id' : profile['employee_id'],
        'display_name' : profile['display_name'],
    };

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
        if(timestamp==null||timestamp=='') return timestamp
        else{
            let format_time = new Date(timestamp)
                .toLocaleString('zh', { hour12: false }) // 2020/3/21 04:26:38
                .replace(/\//g, '-') // 2020-3-21 04:26:38
                .slice(0,-3); // 2020-3-21 04:26
            return format_time;
        }
    }
    function isodate_local(timestamp){
        if(timestamp==null||timestamp=='') return timestamp
        else{
            let format_date = new Date(timestamp)
                    .toLocaleString('zh', { hour12: false }) // 2020/3/21 04:26:38
                    .replace(/\//g, '-') // 2020-3-21 04:26:38
                    .slice(0,-9); // 2020-3-21 04:26
            return format_date;
        }
    }
    function daysCalculate (begin,end){// Formate:"2020-01-20T08:59:38.093183Z"
        begin=new Date(begin).getTime();
        end=new Date(end).getTime();
        let day = 24*60*60*1000;
        let diffDays = Math.round( Math.abs((begin - end )/(day)) );
        return diffDays;
    }
    function formdata_console(target){
        for(var pair of target.entries()) {
            console.log(pair[0]+ ', '+ pair[1]);
        }
    }

    function limit0to100(e,v){
        let reg = /^(([1-9]\d?(\.\d?[1-9])?)|(0(\.\d?[1-9])?)|100)$/;
        if(v.match(reg)){
            return false;
        }else{
            return true;
        }
    }
    //  Ajax error
    function alertmodal_show(img=images['404'],
					title='-- Upload Denied --',
                    content='Upload file selected is oversize. Max-allowed-uploaded-file size is <strong>10 Mb</strong>.',
                    detail=''){
					$('#alert_img').prop('src',img);
					$('#alert_title').text(title);
					$('#alert_content').html(content);
					$('#alert_detail').html(detail);
					$('#alertModal').modal('show');
				}
    function errormsg( jqXHR, textStatus, errorThrown,exception){
        let message=''
        let code=jqXHR.status
        if (code == 401 || code==403) {
            // window.location.reload();
            message = 'Permission deny.';
        }else if( code == 500 ) {
            message = 'Server error. Please connect devloper.';
        }else if( textStatus === 'timeout' ) {
            message = 'Time out error. Check if your network connecting condition or transitting speed.';
        } else if (exception === 'abort') {
            message = 'Ajax request aborted.';
        }else{
            message=jqXHR['responseText'];
        }
        detail=jqXHR['responseText']
        console.log('ERROR------------------------------------------------------');
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
        console.log('-----------------------------------------------------------')
        let title=code+" / "+errorThrown;
        alertmodal_show(images['ajaxfail'],title,message,detail);
    }
    //  Restrict input number only
    function ValidateNumber(e, pnumber){
        let reg = /^(([1-9]\d?(\.\d?[1-9])?)|(0(\.\d?[1-9])?)|100)$/;
        // let reg = /^(0?[1-9]|[1-9][0-9])$/;
        if (!reg.test(pnumber)){
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
    // function backend_check_fields(formdata){
    //     let fields=[];
    //     if(formdata!==undefined){
    //          $.each(Object.keys(formdata),function(i,field){
    //             fields.push(field);
    //         });
    //         return fields;
    //     }else console.log('Data is empty!!')
    // }
//  Table setting
    //  click btn to collapse down the more information
    function detailFormatter(index, row) {
        let order_history_track=get_order_histories(row.id);
        let html=''
        $.each(order_history_track,function(i,row){
            let status=Object.values(Object.values(row.status)[0])[0];
            let who=Object.keys(Object.values(row.status)[0])[0];
            switch (who) {
                case 'initiator':
                    who='Intiator'
                    break;
                case 'assigner':
                    who='Form receiver'
                    break;
                case 'developer':
                    who='Developer'
                    break;
                default:
                    who='Reviewer'
                    break;
            }
            if(status==''){
                status='pending...'
            }
            let status_html=`<span class="ellipsis">`+who+` `+status+`</span>`

            let dev='';
            if(row.developers.member!==[]){
                $.each(row.developers.member,function(i,info) {
                    let person_name=info.display_name;
                    dev+=person_name+'/ '
                })
            }
            let developers_html=`<span class="ellipsis">`+dev+`</span>`;
            function empty_value(value){
                if(value==null||value==undefined||value=='') return ' - ';
                else return value;
            }
            let link_color='';
            if(row.repository_url==''||row.repository_url==null) link_color='text-grey';
            let row_html=`<tr>
                            <td>`+status_html+`</td>
                            <td>`+empty_value(row.account.code)+`</td>
                            <td>`+empty_value(row.project.name)+`</td>
                            <td class="text-center">`+empty_value(row.develop_team_function)+`</td>
                            <td class="text-center">`+empty_value(row.develop_team_sub_function)+`</td>
                            <td>`+empty_value(row.initiator.display_name)+`</td>
                            <td>`+empty_value(row.assigner.display_name)+`</td>
                            <td class="text-center">`+empty_value(row.developers.contactor.display_name)+`</td>
                            <td>`+empty_value(developers_html)+`</td>
                            <td>`+empty_value(row.title)+`</td>
                            <td>`+empty_value(row.description)+`</td>
                            <td class="text-center">`+empty_value(row.expected_develop_duration_day)+`</td>
                            <td class="text-center">`+empty_value(row.actual_develop_duration_day)+`</td>
                            <td class="text-center"><a class="fa fa-link `+link_color+`" href="`+row.repository_url+`" title="`+row.repository_url+`"></a></td>
                            <td class="text-center">`+empty_value(row.parent)+`</td>
                            <td class="text-center">`+empty_value(row.update_staff)+`</td>
                            <td>`+empty_value( isotime_local(row.update_time) )+`</td>
                          </tr>`;
            html+=row_html;
        });
        let table_html=`<div class="bd-radius-8">
                            <table class="table-bordered table-sm" style="max-height:20em;overflow:scroll;display:block;">
                            <thead>
                            <tr>
                                <th nowrap="nowrap" class="align-top">Status</th>
                                <th nowrap="nowrap" class="align-top">Account</th>
                                <th nowrap="nowrap" class="align-top">Project</th>
                                <th nowrap="nowrap" class="align-top">Dev fn team</th>
                                <th nowrap="nowrap" class="align-top">Dev Sub fn team</th>
                                <th nowrap="nowrap" class="align-top">Initiator</th>
                                <th nowrap="nowrap" class="align-top">Form receiver</th>
                                <th nowrap="nowrap" class="align-top">Contact</th>
                                <th nowrap="nowrap" class="align-top">Developers</th>
                                <th nowrap="nowrap" class="align-top">Title</th>
                                <th nowrap="nowrap" class="align-top">Description</th>
                                <th nowrap="nowrap" class="align-top">Est dev day</th>
                                <th nowrap="nowrap" class="align-top">Act dev day</th>
                                <th nowrap="nowrap" class="align-top">Result</th>
                                <th nowrap="nowrap" class="align-top">Parent form</th>
                                <th nowrap="nowrap" class="align-top">Editor</th>
                                <th nowrap="nowrap" class="align-top">Update time</th>
                            </tr>
                            </thead>
                            <tbody>
                                `+html+`
                            </tbody>
                        </table></div>`
        return table_html;
    }
    function filedetailFormatter(index, row) {
        let html = `<div style="max-width:29rem;">
                        <h6 class="badge badge-secondary badge-pill mt-2">
                            <i class="fas fa-sticky-note mr-2"></i>Description
                        </h6>
                        <p class="w-100" style="word-wrap: break-word; word-break: normal; ">`+row['description']+`</p>
                        <textarea class="w-100 font-weight-bold bd-radius-8 bg-white p-1 bd-none" palceholder="File desciption..." style="display:none;">`+row['description']+`</textarea>
                        <div class="text-right mb-2 mt-1">
                            <button type="button" class="btn btn-info btn-sm description_edit"><i class="fa fa-edit mr-1"></i>Edit</button>
                            <button type="button" class="btn btn-success btn-sm description_save" style="display:none;"><i class="fa fa-check-double mr-1"></i>Save</button>
                            <button type="button" class="ml-2 btn btn-secondary btn-sm description_cancel" style="display:none;"><i class="fa fa-times mr-1"></i>Cancel</button>
                        </div>
                    </div>`;
        return html;
    }

    //  Set the key and value sent to backend
    function queryParams(params) {
        //  這裡的鍵的名字和控制器的變量名必須一直，這邊改動，控制器也需要改成一樣的
        let queryParams_temp = {
            page_size: params.limit, //頁面大小
            page: (params.offset / params.limit) + 1, //頁碼
            sort_order: '-form_begin_time', //排位命令（desc，asc）
        };
        //  Redefine filter data
        if('filter' in params){
            let filterObj = $.parseJSON(params.filter);
            if( 'account' in filterObj){
                let account_id = filterObj['account'].split(' _ ')[0];
                filterObj['account'] = account_id;
            }
            if( 'project' in filterObj){
                let project_id = filterObj['project'].split(' _ ')[0];
                filterObj['project'] = project_id;
            }
            if( 'form_begin_time' in filterObj){
                let start = filterObj['form_begin_time'].split(' - ')[0];
                let end = filterObj['form_begin_time'].split(' - ')[1];
                let form_begin_time_after=new Date(start).toISOString();
                let form_begin_time_before=new Date(end).toISOString();
                filterObj['form_begin_time_after'] = form_begin_time_after;
                filterObj['form_begin_time_before'] = form_begin_time_before;
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
        return html;
    }
    //  Table-formatLoadingMessage
    function LoadingMessage() {
        let html=`<div class="text-center font-weight-bold mt-3 mb-2">
                    <h6>Loading<img class="ml-1" style="width: 30px;" src="`+images.loadinggif_path+`"></h6>
                </div>`;
        return html;
    }

    //  comment area height
    function comment_area_height_expand(){
        let image_dev = $('#imgage_dev');
        let form_h=parseInt($('#FormRequest_div').css('height').split('px')[0]);
        let comment_h=parseInt($('#comment').parent('div').css('height').split('px')[0]);
        let h = (form_h-comment_h-100)+'px';
        image_dev.removeClass('animated zoomInDown').addClass('animated zoomOutUp').fadeOut(0);
        $('#display_comment_area').css('height',h)
        $('#comment_area,#edit_comment_area,#display_comment_area').fadeIn(0);

        let status=$('#requestModal').data('status');
        let phase=Object.keys(status)[0]
        let ifClose=Object.values(Object.values(status)[0])[0];

        if(ifClose=='Close'||(ifClose=='Approve'&&phase=='P5')){//  關單或完成單子時,劉訊息的區塊消失
            $('#comment_area,#display_comment_area').fadeIn(0);
            $('#edit_comment_area').fadeOut(0);
        }else{
            $('#comment_area,#edit_comment_area,#display_comment_area').fadeIn(0);
        }
    }

    function comment_area_height(){
        let img_dev = $('#imgage_dev');
        let form_h=parseInt($('#FormRequest_div').css('height').split('px')[0]);
        let comment_h=parseInt($('#comment').parent('div').css('height').split('px')[0]);
        let img_dev_h=parseInt($('#imgage_dev').css('height').split('px')[0]);
        let h = (form_h-img_dev_h-comment_h-100)+'px';
        $('#display_comment_area,#edit_comment_area').prop('style','display:none!important;')
        img_dev.removeClass('animated zoomOutUp').addClass('animated zoomInDown').fadeIn(0);
    }
    // Histories Operation
    function append_comment_template(target,comment_obj){
        let editor=comment_obj['editor']
        let comment=comment_obj['content'];

        let created_time=isotime_local(comment_obj['created_time']);
        let comment_template='';
        comment_template=`<div class="mb-2">
            <div class="d-inline-flex align-items-top">
                <img class="sticker mr-2 talker" data-employee_id="`+editor['employee_id']+`" src="">
                <div><small class="text-dark mb-1 mr-3 font-weight-bold">`+editor["display_name"]+`</small></div>
            </div>
            <div class="bg-grey comments_shape">
                <div class="text-dark p-2">`+comment+`</div>
            </div>
            <small class="text-secondary d-flex justify-content-end mr-3 font-weight-bold">`+created_time+`</small>
        </div>`;
        $(target).append(comment_template);
        let img_path=avatar_get(editor['employee_id']);
        let path=avatar_default_get(editor['employee_id']);
        //  Update image
        $(target).find('img.talker').last().prop('src',img_path);
        $(target).find('img.talker').last().one('error',function(){$(this).prop('src',path)});
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
    function scrollToBottom(){
        let moveto = Number($('#comment_area').css('height').slice(0,-2));
        $('#display_comment_area').stop(true, true).animate({ scrollTop: moveto }, 500);
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
        $('input,.selectpicker,textarea').on('change input', function() {
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
                field.addClass('border-danger');
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
                field.removeClass('border-danger');
                break;
            default:
                field.removeClass('border-danger');
                break;
        }
    }
    // let time=new Date;
    // let timestamp=time.getTime();
    function avatar_get(employee_id,timestamp=(new Date).getHours()){
        let teamroaster_path='http://10.32.48.118:50005/img/avatar/';
        let src_path=teamroaster_path+employee_id+'?'+timestamp;
        return src_path.toString();
    }
    function avatar_default_get(employee_id){
        let teamroaster_path='http://10.32.48.118:50005/img/avatar/default-1.svg';
        if(employee_id!==undefined){
            employee_id=employee_id.toString();
            let num=(Number(employee_id.substr(-2,2))+Number(employee_id.substr(-4,2)))%100;
            teamroaster_path='http://10.32.48.118:50005/img/avatar/default-'+num+'.svg';
        }else{
            console.warn('employee_id undefined');
        }
        return teamroaster_path;
    }
    function avatar_reload(target){
        target.prop('src',images['defaultavatar']);
        target.one('load',function(){
            let employee_id=$(this).data('employee_id');
            let avatar=avatar_get(employee_id);
            $(this).prop('src',avatar);
            $(this).one('error',function(){
                let path=avatar_default_get(employee_id);
                $(this).prop('src',path);
            });
        });
    }
//  render list signaturer
    function render_signaturer_list(id,target){
        let signature_data=get_signaturers(id);
        if(signature_data==null||signature_data==''||signature_data==[]){}
        else{
            target.empty();
            $.each(signature_data,function(i,info){
                let name=info['signer']['display_name'];
                let employee_id=info['signer']['employee_id'];
                let comment=info['comment'];
                let status=info['status'];
                let job_title=info['signer']['job_title'];
                let department=info['sign_unit'];
                let status_html='';
                let comment_html='';
                let time='';
                if(info['signed_time']==null||info['signed_time']==''||info['signed_time']==[]) {}
                else time=isotime_local(info['signed_time']);

                switch (status) {
                    case 'Approve':
                        status_html='<small class="badge badge-success badge-pill p-1 ml-1"> <i class="fa fa-check-double"></i> Approve </small>';
                        break;
                    case 'Return':
                        status_html='<small class="badge badge-danger badge-pill p-1 ml-1"> <i class="fa fa-reply"></i> Reject </small>';
                        break;
                    case 'Close':
                        status_html='<small class="badge badge-warning badge-pill p-1 ml-1"> <i class="fa fa-stop"></i> Close </small>';
                        break;
                    case '':
                        status_html='<small class="badge badge-info badge-pill p-1 ml-1"> <i class="fa fa-pen"></i> Pending... </small>';
                        break;
                    default:
                        break;
                }
                if(comment==null||comment==''){}
                else{ comment_html='<p class="ellipsis bg-grey bd-radius-8">'+comment+'</p>'; }

                let html=`<div class="mt-1">
                            <div class="d-inline-flex align-items-center">
                                <img class="sticker mr-2" src="`+images['defaultavatar']+`" data-employee_id="`+employee_id+`">
                                <span class="text-secondary font-weight-bold">`+name+`</span>
                                <small class="badge badge-light badge-pill p-1 ml-1">`+department+`/ `+job_title+`</small>
                                `+status_html+`
                                <small class="text-grey ml-1 pt-1">`+time+`</small>
                            </div>
                            `+comment_html+`
                        </div>`;
                target.append(html);
                avatar_reload(target.find('img').last());
            });
        }
    }

//  requestModal
    //  selectpicker(When status==p0/p1)
    function request_selectpicker(){
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
        //  Form fields - Select accounts
            $('#sel_function').on('change',function(){
                let sub_function=$('#sel_function').val();
                let accounts=get_accounts(sub_function);

                $('#sel_accounts').empty().selectpicker('refresh');
                $('#sel_projects').empty().selectpicker('refresh');
                $('#sel_assigners').empty().selectpicker('refresh');
                reset_author('form_assigner');

                $('#sel_accounts').append('<option value="" selected> Select... </option>');

                //  DQMS tricky rule
                if(sub_function=='DSPA_DS'){
                    $.each(accounts,function(){
                        let account_info = $(this)[0];
                        if(account_info['code']=='WT-EBG') $('#sel_accounts').append('<option value="'+account_info['id']+'">'+account_info['code']+'</option>');
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
                let acc_id=$('#sel_accounts').val();
                let projects=get_projects(acc_id);
                $('#sel_projects').empty().selectpicker('refresh');
                $('#sel_assigners').empty().selectpicker('refresh');
                reset_author('form_assigner');

                $('#sel_projects').append('<option value="" selected> Select... </option>');

                //  DQMS tricky rule
                $.each(projects,function(){
                    let project_info = $(this)[0];
                    $('#sel_projects').append('<option value="'+project_info['id']+'">'+project_info['name']+'</option>');
                });

                $('#sel_projects').selectpicker('refresh');
            });
        //  Form fields - Select assigners
            let assigners='';
            $('#sel_projects').on('change',function(){
                let project_id=$('#sel_projects').val();
                let sub_function='';
                if($('#sel_function').val().length!==0){
                    sub_function=$('#sel_function').val().split('_')[1];
                }
                reset_author('form_assigner');
                $('#sel_assigners').empty().selectpicker('refresh');
                $('#sel_assigners').append('<option value="" selected> Select... </option>');
                if(project_id.length!==0 && sub_function!==0){
                    assigners=get_assigners(sub_function,project_id);
                    console.log(assigners)
                    $.each(assigners,function(index,v){
                        let name=$(this)[0]['display_name'].split('/Wistron')[0];
                        let phone_extension=$(this)[0]['extension'];
                        let id=$(this)[0]['employee_id'];
                        $('#sel_assigners').append('<option value="'+id+'" data-index="'+index+'" data-subtext=" #'+phone_extension+'">'+name+'</option>');
                    });
                    $('#sel_assigners').selectpicker('refresh');
                }
            });
        //  Show assigner is who
        $('#sel_assigners').on('change',function(){
            let assigners_index=$(this).find('option:selected').data('index');
            let assigner_info=assigners[assigners_index];
            reset_author('form_assigner');
            show_author('form_assigner',assigner_info);
        });
    }
    function show_author(form_role,info){
        let roleinfo;
        let target=$('#'+form_role);

        if(form_role=='form_owner') {
            roleinfo=info['contactor'];
            if(info['member']==''||info['member']==null||info['member']==[]){
                target.find('.toggle-dev-list').fadeOut(0);
            }else{
                target.find('.dev-list ul').empty();
                target.find('.toggle-dev-list').fadeIn(0);
                $.each(info['member'],function(i,member){
                let html='<li class="mt-1">'+member['display_name']+'</li>'
                target.find('.dev-list ul').append(html);
                });
            }
        }else roleinfo=info;

        let img_path=avatar_get(roleinfo.employee_id);
        let path=avatar_default_get(roleinfo.employee_id);
        let name=roleinfo['display_name'];
        //  Update image
        target.find('img').prop('src',img_path);
        target.find('img').one('error',function(){$(this).prop('src',path)});

        //  Update name
        target.find('span').text(name);
        target.parents('.author').fadeIn(0);
    }
    function reset_author(form_role){
        let target=$('#'+form_role);
        if(target.parents('.author').css('display')!=='none'){
            target.find('img').prop('src',images['defaultavatar']);
            target.find('span').text('');
            target.parents('.author').prop('style','display:none !important;');
        }
    }
    function show_request_info(order_data){
        let id=order_data['id'];
        let parent=' - ';
        if(order_data['parent']==''||order_data['parent']==null){}
        else parent=order_data['parent'];

        $('#form_breadcrumb').find('div').empty();
        $('#request_title,#request_description').empty();
        let breadcrumb_html=` <h6 class="badge badge-bluegray badge-pill" title="Initiator">`+order_data['initiator']['display_name']+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill mr-2" title="Team">`+order_data['develop_team_function']+`_`+order_data['develop_team_sub_function']+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill mr-2" title="Account">`+order_data['account']['code']+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill mr-2" title="Project">`+order_data['project']['name']+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill" title="Receiver">`+order_data['assigner']['display_name']+`</h6>`;
        let title=order_data['title'];
        let description_html=order_data['description'].replace(/\\/g,'');
        let signaturer_target=$('#authors').find('.ReviewerList');
        $('#order_id').text('Form id: '+id);
        $('#parent_id').text('Patent form id: '+parent);
        //  get signaturer List
        render_signaturer_list(id,signaturer_target);
        signaturer_target.parent('div').fadeIn(0);
        //  show assigner
        let assigner_img=$('#form_assigner').find('img');
        let assigner_info=order_data['assigner'];
        assigner_img.data('employee_id',assigner_info['employee_id']).prop('src',images['defaultavatar']);
        avatar_reload(assigner_img);
        $('#form_assigner').find('span').text(assigner_info['display_name']);

        $('#form_assigner').parent('div').fadeIn(0);

        $('#form_breadcrumb').find('div').append(breadcrumb_html);
        $('#request_title').text(title);
        $('#request_description').append(description_html);
        $('#form_breadcrumb,#form_info').fadeIn(0);
    }
    function hide_request_info(){
        if($('#form_breadcrumb').css('display')!=='none'){
            $('#form_breadcrumb').find('div').empty();
            $('#form_breadcrumb ').prop('style','display:none !important;');
            $('#request_title,#request_description').empty();
            $('#form_info').prop('style','display:none !important;');
        }
    }
    function request_image_status(image_path=images.status,title='Initialize request',detail='Progress status -- start --'){
        $('#imgage_dev').find('img').first().prop('src',image_path);
        $('#image_label_dev').find('h3').html(title);
        $('#image_label_dev').find('p').text(detail);
        //  Refresh #table
        $('#table').bootstrapTable('refresh');
    }
    function request_image_module(keyword){//initialize_request/waiting_signature/notify_signing/waiting_receiver_accept_request/receiver_assign_developers
        let image_path;
        let title;
        let detail;
        switch (keyword) {
            case 'Reinitialize_request':
                image_path=images.reject;
                title='Reject request !!';
                detail=`Your request is rejected.Will reinitialize or close the request?`;
                break;
            case 'initialize_request':
                image_path=images.status;
                title='Initialize request';
                detail='Progress status -- start --';
                break;
            case 'signer_waiting_signature':
                image_path=images.pending;
                title='Reviewer\'s pending <img src="'+images['loadinggif_path']+'" style="width:2rem;">';
                detail=`When it's your turn, the system will notify you by email or the notification btn on the top.`;
                break;
            case 'waiting_signature':
                image_path=images.pending;
                title='Reviewer\'s pending <img src="'+images['loadinggif_path']+'" style="width:2rem;">';
                detail=`You can upload files, tag form derived from. System already email to your supervisor.`;
                break;
            case 'notify_signing':
                image_path=images.approve;
                title='Review this request,please~';
                detail=`You need to review the request now.`;
                break;
            case 'waiting_receiver_accept_request':
                image_path=images.assigndev;
                title='Form receiver\'s pending <img src="'+images['loadinggif_path']+'" style="width:2rem;">';
                detail='If receiver agree to accept this request, the request will go on.';
                break;
            case 'receiver_assign_developers':
                image_path=images.assigndev;
                title='Assign developers, estimate schedule for the request,please~';
                detail='You need to review request now.';
                break;
            case 'receiver_pending':
                image_path=images.approve;
                title='Will you accept the rquest?';
                detail='If you accept,you need to assigner developers at least two,and press "Approve" button. Initiator\'s supervisors already approved before.';
                break;
            case 'receiver_proposal_schedule':
                image_path=images.schedule;
                title='Plan schedule';
                detail='You already accept the request and need to discuss with your team members and initator to plan schedule.';
                break;
            case 'pending_schedule':
                image_path=images.pend_schedule;
                title='Pending Schedule <img src="'+images['loadinggif_path']+'" style="width:2rem;">';
                detail='If Initiator and developer contactor approve this schedule proposal, the request will go on.';
                break;
            case 'developing':
                image_path=images.developing;
                title='Developing...';
                detail='Developers can regularly update progress, and participates also track by progress data.';
                break;
            case 'waiting_result_approve':

                break;
            case 'form_closed':
                image_path=images.closed;
                title='Request Closed';
                detail='If your future request need to link the request info, you can tag the form as parent.';
                break;
            case 'initiator_pend':
                image_path=images.finalcheck;
                title='Initiator checking <img src="'+images['loadinggif_path']+'" style="width:2rem;">';
                detail='Initiator check if the result fit the original expection.';
                break;
            case 'form_completed':
                image_path=images.completed;
                title='Request Completed';
                detail='The request is already completed! If you want to extend the request(ex:2.0),and you initialize create a new request and tag this form.';
                break;
            case 'processing':
                break;
            default:
                break;
        }
        request_image_status(image_path,title,detail);
    }
    function get_filelist(order_id){
        let documents=get_documents(order_id);
        $('#filelist').bootstrapTable('destroy').bootstrapTable({
            data:documents,
            cache: false,
            classes:'',
            iconsPrefix: 'fa',
            detailView:true,
            detailFormatter: 'filedetailFormatter',
            rowAttributes:function(row,index) {
                return {'data-id':row['id']};
            },
            icons: {
                detailOpen: 'fas fa-list',
                detailClose: 'fa-angle-up',
            },
            columns: [
                {
                    field:'id',
                    width:100,
                    formatter:function(value, row, index){
                        let filename=row['name'];
                        let filetype=filename.split('.')[1];

                        let imgsrc=row['path'];
                        if(isImage(filetype)!==true) imgsrc=images['document'];

                        let html=`<img title="`+filename+`" src="`+imgsrc+`" /> `;
                        return html;
                    }
                },
                {
                    field:'path',
                    align:'right',
                    formatter:function(value, row, index){
                        let path=value;
                        let html=`<a class="btn btn-info btn-sm mt-2 filedownload" href="`+path+`" download="`+row['name']+`" >
                                    <i class="fa fa-cloud-download-alt "></i>
                                </a>`
                        return html;
                    }
                },
                {
                    field:'name',
                    formatter:function(value, row, index){
                        let filesize=Number(row['size']);
                        let html=` <p class="ellipsis pl-2 pr-2 mb-0 filename" style="width:10rem;">`+value+`</p>
                                    <small class="pl-2">`+bytesChange(filesize)+`</small>`;
                        return html;
                    }
                },
                {
                    field:'update_time',
                    formatter:function(value, row, index){
                        let time=isotime_local(value);
                        let html=`<small class="text-grey fileupdate">Update/ `+time+`</small>`
                        return html;
                    }
                },
                {
                    align:'right',
                    formatter:function(value, row, index){
                        let html=`<button type="button" class="btn btn-danger btn-sm mt-1">
                                    <i class="fas fa-trash-alt"></i>
                                </buton>`
                        return html;
                    }
                },
            ],
            formatNoMatches: function () {
                let html=NoMatches('No file uploaded.');
                return html;
            },
            formatLoadingMessage: function(){
                let html=LoadingMessage();
                return html;
            },
            onLoadError:function(status, jqXHR) {
                console.log(status);
                console.log(jqXHR);
            },
            onPostBody:function(name, args){
            }
        });
    }
    function afterInit(order_id){
        $('#FormRequest').fadeOut(0);
        $('#tag_div').parent('div').fadeIn(0);
        get_filelist(order_id);
    }

    function get_schedulelist(schedule_data){
        // let schedule=get_current_schedule(order_id);
        $('#schedulelist').bootstrapTable('destroy').bootstrapTable({
            data:schedule_data,
            cache: false,
            classes:'',
            iconsPrefix: 'fa',
            rowAttributes:function(row,index) {
                let time=row['expected_time']
                return {'data-id':row['id'],'data-time':time,'data-update_fields_obj':'{}'};
            },
            icons: {
                detailOpen: 'fas fa-list',
                detailClose: 'fa-angle-up',
            },
            columns: [
                {
                    field:'id',
                    visible:false,
                },
                {
                    field:'event_name',
                    title:'Milestone',
                    valign:'top',
                    width:250,
                    formatter:function(value, row, index){
                        let html=`<span class="ellipsis">`+value+`</span>`
                        if(row.complete_rate==0||row.complete_rate==100){}
                        else {html=`<input class="field-style mr-2" data-field="event_name" placeholder="Milestone..." value="`+value+`" required>`;}
                        return html;
                    }
                },
                {
                    field:'timestamp',
                    title:'Exp date',
                    width:100,
                    valign:'top',
                    sortable:true,
                    formatter:function(value, row, index){
                        let date;
                        if(value==null|value==''){
                            console.log('Estimated Date null or ""')
                            date="";
                        }else{date=new Date(value).toLocaleString('zh', { hour12: false })
                                                    .replace(/\//g, '-')
                                                    .split(' ')[0];}
                        let html=`<input class="field-style mr-2 date" data-field="timestamp" placeholder="Estimated date" value="`+date+`" required>`;
                        return html;
                    }
                },
                {
                    field:'description',
                    title:'Description',
                    valign:'top',
                    width:250,
                    formatter:function(value, row, index){
                        let html=`<textarea class="field-style bd-radius-8" data-field="description">`+value+`</textarea>`;
                        return html;
                    }
                },
                {
                    field:'complete_rate',
                    title:'Exp complete(%)',
                    align:'center',
                    valign:'top',
                    width:50,
                    formatter:function(value, row, index){
                        let html=value;
                        if(value==0||value==100){}
                        else{
                            html=`<div class="input-group mr-2">
                                <input type="text" value="`+value+`" class="form-control field-style" name="complete_rate" data-field="complete_rate" style="ime-mode:disabled" onkeyup="return ValidateNumber($(this),value)" placeholder="1~99 complete">
                                <div class="input-group-append">
                                    <button class="btn btn-light font-weight-bold" type="button"> % </button>
                                </div>
                            </div>`;
                        }
                        return html;
                    }
                },
                {
                    field:'update_time',
                    title:'Updated time',
                    align:'center',
                    valign:'top',
                    width:50,
                    formatter:function(value, row, index){
                        let html=value;
                        if(value==' - '){}
                        else html=`<span>`+isotime_local(value)+`</span>`
                        return html;
                    }
                },
                {
                    field:'delete',
                    title:'Delete',
                    align:'center',
                    valign:'top',
                    formatter:function(value, row, index){
                        let html='';
                        if(row.complete_rate==0||row.complete_rate==100){}
                        else {
                            html=`<button data-event_name="`+row['event_name']+`" type="button" class="btn btn-danger btn-sm mt-1 delete">
                                    <i class="fas fa-trash-alt"></i>
                                </button>`;
                        }
                        return html;
                    }
                },
            ],
            formatNoMatches: function () {
                let html=NoMatches('No file uploaded.');
                return html;
            },
            formatLoadingMessage: function(){
                let html=LoadingMessage();
                return html;
            },
            onLoadError:function(status, jqXHR) {
                console.log(status);
                console.log(jqXHR);
            },
            onPostBody:function(name, args){
                $('#schedule_area').find('.date')
                            .datepicker({ dateFormat: 'yy-mm-dd',
                                            beforeShowDay: $.datepicker.noWeekends,
                                        });
                $('#schedulelist').find('tbody tr').each(function(){
                    let id=$(this).data('id')
                    if(typeof(id)!=='number'){
                        $(this).find('td').first().append('<h5 class="badge badge-alert badge-pill mt-2 position-absolute showedit" style="left:-20px;"> New </h5>');
                        $(this).addClass('Newschedule');
                    }
                });
            }
        });
    }
    function get_readonly_schedule(order_id){
        let schedule_data=get_current_schedule(order_id);
        $('#readonly_schedule').bootstrapTable('destroy').bootstrapTable({
            data:schedule_data,
            classes:'',
            iconsPrefix: 'fa',
            rowAttributes:function(row,index) {
                let time=row['expected_time']
                return {'data-id':row['id'],'data-time':time,'data-update_fields_obj':'{}'};
            },
            icons: {
                detailOpen: 'fas fa-list',
                detailClose: 'fa-angle-up',
            },
            columns: [
                {
                    field:'event_name',
                    title:'Milestone',
                    valign:'top',
                    width:250,
                    formatter:function(value, row, index){
                        let html=`<span class="ellipsis">`+value+`</span>`
                        return html;
                    }
                },
                {
                    field:'timestamp',
                    title:'Exp date',
                    width:100,
                    valign:'top',
                    sortable:true,
                    formatter:function(value, row, index){
                        let date;
                        if(value==null|value==''){console.log('Estimated Date null or ""')}
                        else{date=new Date(value).toLocaleString('zh', { hour12: false })
                                                    .replace(/\//g, '-')
                                                    .split(' ')[0];}
                        let html=`<span class="ellipsis hideedit">`+date+`</span>`;
                        return html;
                    }
                },
                {
                    field:'description',
                    title:'Description',
                    valign:'top',
                    width:250,
                    formatter:function(value, row, index){
                        let html=`<span class="ellipsis hideedit">`+value+`</span>`;
                        return html;
                    }
                },
                {
                    field:'complete_rate',
                    title:'Exp complete(%)',
                    align:'center',
                    valign:'top',
                    width:50,
                    formatter:function(value, row, index){
                        let html=value;
                        if(value==' - '){}
                        else{
                            html=`<span class="ellipsis hideedit">`+value+`% </span>`;
                        }
                        return html;
                    }
                },
                {
                    field:'created_time',
                    title:'Created time',
                    align:'center',
                    valign:'top',
                    formatter:function(value, row, index){
                        let html=value;
                        if(value==' - '){}
                        else html=`<span>`+isotime_local(value)+`</span>`
                        return html;
                    }
                }
            ],
            formatNoMatches: function () {
                let html=NoMatches('...');
                return html;
            },
            formatLoadingMessage: function(){
                let html=LoadingMessage();
                return html;
            },
            onLoadError:function(status, jqXHR) {
                console.log(status);
                console.log(jqXHR);
            },
            onPostBody:function(name, args){}
        });
    }




//  dev_modal.js
    function current_id_arr(data_list){
        let arr=[]
        $(data_list).each(function(i,v){
            arr.push(v['employee_id']);
        });
        return arr;
    }
    function select_devcontacter(target,table,data,developer_contacter){
        let sel=$(target).find('.selectpicker');
        let contactwindow=null;
        if(developer_contacter.length!==0) {
            sel.selectpicker('val',developer_contacter[0]['employee_id']);
            contactwindow=developer_contacter[0]['employee_id'];
        }else{
            contactwindow=sel.val();
        }
        sel.empty();
        sel.append('<option value=""> Select contact window... </option>');
        $.each(data,function(i,v){
            sel.append('<option value="'+v.employee_id+'">'+v.display_name+'</option>');
            if(i==data.length-1) {
                sel.selectpicker('refresh');
                sel.selectpicker('val',contactwindow);
            }
            if(v['employee_id']==contactwindow){
                developer_contacter.length=0;
                developer_contacter.push(v);
            }
        });
        $('#windowbadge').remove();
        if(contactwindow!==null){
            $(table).find('tr').each(function(){
                let id=$(this).data('employee_id');
                if(id==contactwindow){
                    $(this).find('td').first().append('<h5 class="badge badge-info badge-pill ml-1" id="windowbadge"><i class="fa fa-user-check mr-1"></i>Contact window</h5>');
                    return;
                }
            });
        }

    }
    function if_employee_joined(currentIdList,limitation,table,show_count_Target){
        let count_number=currentIdList.length;
        $(table).find('tbody').find('tr').each(function(){
            let Id=$(this).data('employee_id');
            if(typeof($(this).data('employee_id'))=="number"){Id=JSON.stringify($(this).data('employee_id'));}

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



//  ezinfo_modal.js
    function render_ezinfo(id){
        $('body').append(ezinfoModal);
        let form_data=get_single_order(id);
        let signature_data=get_signaturers(id);
        let schedule_data=get_current_schedule(id);
        let files_data=get_documents(id);
        let progress_data=get_progress(id);

        let initiator=form_data.initiator.display_name;
        let assigner=form_data.assigner.display_name;
        let team=form_data.develop_team_function+'_'+form_data.develop_team_sub_function;
        let account=form_data.account.code;
        let project=form_data.project.name;
        let begin;
        let end;
        let days;
        let b_day;
        let e_day;
        let now;
        let b;
        let e;
        let est_rate=0;
        let progress_info;
        let created_date='-';
        let develop_date='-';
        let current_rate=0;

        if(schedule_data[0].timestamp==null){
        }else {
            begin=schedule_data[0].timestamp
            end=schedule_data[schedule_data.length-1].timestamp
            days=daysCalculate(begin,end);
            b_day=isodate_local(begin);
            e_day=isodate_local(end);
            now=new Date().getTime();
            b=new Date(b_day).getTime();
            e=new Date(e_day).getTime();

            est_rate=100;
            if(now<e) est_rate=Math.round((now-b)/(e-b)*100);
        }
        if(progress_data==null||progress_data==''||progress_data==[]){}
        else{
            progress_info=progress_data[progress_data.length-1]
            created_date=isodate_local(progress_info['created_time']);
            develop_date=isodate_local(progress_info['develop_time']);
            current_rate=progress_info['complete_rate'];
        }

        let breadcrumb_html=` <h6 class="badge badge-bluegray badge-pill" title="Initiator">`+initiator+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill mr-2" title="Team">`+team+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill mr-2" title="Account">`+account+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill mr-2" title="Project">`+project+`</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill" title="Receiver">`+assigner+`</h6>`;
        $('#ez_breadcrumb').append(breadcrumb_html);

        $('#ezinfoModal').find('form').find('[name]').each(function(){
            let field_name=$(this).attr('name');
            let field=$(this);
            switch (field_name) {
                case 'account':
                case 'project':
                    field.text(form_data[field_name]['code']);
                    break;
                case 'initiator':
                case 'assigner':
                    const name = form_data[field_name]
                    field.siblings('img').prop('src',images['defaultavatar'])
                    if(!name){
                        field.text('-');
                    }else if(typeof(name)=='string'&&name){
                        field.text(form_data[field_name]+'(non-found)')
                    }else if(typeof(name)=='object'){
                        field.text(form_data[field_name]['display_name']);
                        field.siblings('img').data('employee_id',form_data[field_name]['employee_id']);
                        avatar_reload(field.siblings('img'))
                    }
                    break;
                case 'developers':
                    if(form_data['developers']['contactor']==''){
                        //  Default value={"member":[],"contactor":""}
                        field.parent('div').html('<span class="pl-2 text-secondary font-weight-bold ml-1" name="developers"> - </span>');
                    }else if(form_data['developers']['contactor']==''&& form_data['developers']['member'].length!==0){
                        field.siblings('img').prop('src',images['defaultavatar']);
                        alertmodal_show(img=images['assigndev'],'-- NO Developer Contact --','WARNING!! NO assigned developer contact but exited member !!(Unexpected stituation)')
                        field.text('-');
                    }else{
                        field.html(form_data[field_name]['contactor']['display_name']+'<strong>...</strong>');
                        field.siblings('img').prop('src',images['defaultavatar']).data('employee_id',form_data[field_name]['contactor']['employee_id']);
                        avatar_reload(field.siblings('img'));
                        let target=field.siblings('.dev-list').find('ul');
                        target.empty()
                        if(form_data[field_name]['member']==null||form_data[field_name]['member']==''){
                            target.text(' - ');
                        }else{
                            $.each(form_data[field_name]['member'],function(i,info){
                                let name=info['display_name'];
                                target.append('<li class="mt-1">'+ name +'</li>');
                            });
                        }
                    }
                    break;
                case 'form_begin_time':
                case 'form_end_time':
                    if(form_data[field_name]==null||form_data[field_name]==''){
                        field.html(' - ');
                    }else field.html(isotime_local(form_data[field_name]));
                    break;
                case 'repository_url':
                    if(form_data[field_name]==null||form_data[field_name]==''){
                        field.html(' - ');
                    }else field.prop('href',form_data[field_name]).html('<i class="mr-2 fa fa-link"></i>'+form_data[field_name]);
                    break;
                    case 'signature':
                        if(signature_data==null||signature_data==''||signature_data==[]){
                            field.html(' - ');
                        }else render_signaturer_list(id,field);
                        break;
                case 'files':
                    let file_html=`<tr>
                                        <td> - </td>
                                        <td> - </td>
                                        <td> - </td>
                                        <td class="text-center"> - </td>
                                        <td> - </td>
                                    </tr>`;
                    if(files_data==null||files_data==''||files_data==[]){
                        field.find('tbody').append(file_html);
                    }else {
                        $.each(files_data,function(i,info){
                            file_html=`<tr data-id=`+info.id+`>
                                            <td class="ellipsis">`+info.name+`</td>
                                            <td class="ellipsis">`+bytesChange(Number(info.size))+`</td>
                                            <td class="ellipsis">`+info.description+`</td>
                                            <td class="text-center"><a href="`+info.path+`" class="fa fa-cloud-download-alt btn btn-info btn-sm p-1 text-light" style="cursor: pointer;" download></a></td>
                                            <td class="ellipsis">`+isotime_local(info.update_time)+`</td>
                                        </tr>`;
                            field.find('tbody').append(file_html);
                        });
                    }
                    break;
                case 'schedule':
                    let schedule_html=`<tr>
                                            <td> - </td>
                                            <td> - </td>
                                            <td> - </td>
                                            <td> - </td>
                                            <td> - </td>
                                        </tr>`;

                    if(schedule_data[0].timestamp==null){
                        field.find('tbody').append(schedule_html);
                    }else {
                        $.each(schedule_data,function(i,info){
                            schedule_html=`<tr data-id=`+info.id+`>
                                                <td class="font-weight-bold text-secondary ellipsis">`+info.event_name+`</td>
                                                <td class="ellipsis">`+isodate_local(info.timestamp)+`</td>
                                                <td class="ellipsis">`+info.description+`</td>
                                                <td class="text-center">`+info.complete_rate+`%</td>
                                                <td class="ellipsis">`+isotime_local(info.created_time)+`</td>
                                            </tr>`;
                            field.find('tbody').append(schedule_html);
                        });
                    }
                    break;
                case 'develop_time':
                    if( schedule_data[0].timestamp==null ) field.text(' - ');
                    else {
                        field.text(days+' days ('+b_day+'~'+e_day+')');
                    }
                    break;
                case 'est_rate':
                    field.find('h6').text(est_rate+' %');
                    field.find('.progress-bar').css('width',est_rate+'%');
                    break;
                case 'act_rate':
                    field.find('h6').html(current_rate+' %');
                    field.find('h6').tooltip({title:'Record date/ '+develop_date+' Created Date/ '+created_date});
                    field.find('.progress-bar').css('width',current_rate+'%');
                    break;
                case 'progress_status':
                    let target=field.find('h5');
                    if(progress_data==null||progress_data==''||progress_data==[]){
                        target.addClass('text-secondary');
                        target.html('<em>Uninitiated - </em>');
                    }else{
                        if(current_rate>est_rate){
                            target.addClass('text-success');
                            target.html('<em>Advanced +'+Number(current_rate)-Number(est_rate)+'%</em>');
                        }else if(current_rate==est_rate){
                            target.addClass('text-success');
                            target.html('<em>On schedule</em>');
                        }else if(current_rate<est_rate){
                            target.addClass('text-warning');
                            target.html('<em>Delayed -'+(Number(est_rate)-Number(current_rate))+'%</em>');
                        }
                    }
                    break;
                case 'status':
                    let value=form_data[field_name];
                    let status=Object.values(Object.values(value)[0])[0];
                    let who=Object.keys(Object.values(value)[0])[0];
                    switch (who) {
                        case 'initiator':
                            who='Intiator'
                            break;
                        case 'assigner':
                            who='Form receiver'
                            break;
                        case 'developer':
                            who='Developer'
                            break;
                        default:
                            who='Reviewer'
                            break;
                    }
                    if(status==''){
                        status='pending...'
                    }
                    let html=`<span class="ellipsis">`+who+` `+status+`</span>`
                    field.html(who+` `+status);
                    break;
                default:
                    if(form_data[field_name]==undefined || form_data[field_name]==null){
                        field.html(' - ');
                    }else field.html(form_data[field_name]);
                    break;
            }
        });

        $('#ezinfoModal').modal('show');

    }




//  UI Flow
    function signature_sign(order_id,signature_id){
        $('#signature_func').fadeIn(0);
        //  Review btn
        $('#ApproveBTN,#ReturnBTN,#CloseBTN').off().on('click',function(){
            let status=$(this).prop('id').slice(0,-3);
            let comment=$('#sign_comment').val();
            // let order_id=$('#requestModal').data('order_id');
            let formdata={};
            if(comment.length==0){
                $('#sign_comment').addClass('border-danger').removeClass('bd-none');
            }else{
                $('#sign_comment').addClass('bd-none').removeClass('border-danger');
                formdata={
                    'id':signature_id,
                    'status':status,
                    'comment':comment
                }
                $.when(put_signaturers(order_id,signature_id,formdata)).done(refresh_requestModal(order_id));
            }

            // put_signaturers(order_id,signature_id,formdata)
        });
    }
    function pend_sign(order_id,status,phase,role){
        $('#signature_func').fadeIn(0);
        //  Review btn
        $('#ApproveBTN,#ReturnBTN,#CloseBTN').off().on('click',function(){
            let decide=$(this).prop('id').slice(0,-3);
            status[phase][role]=decide
            let formdata={
                'status':JSON.stringify(status),
            }
            $.when(patch_order(order_id,formdata)).done(refresh_requestModal(order_id));
        });
    }
    function refresh_requestModal(order_id){
        let order_response=get_single_order(order_id);
        $('#requestModal').modal('hide');
        indentify_modal_show(order_response);
    }
    function append_New_requestModal(order_id='New'){
        $('body').append(requestModal);
        $('#image_status').find('img').first().prop('src',images.status);
        $('#file_template_download').prop('href',file_template_path)
        //  summernote
        $('.summernote').summernote({
            dialogsInBody: true,
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
                ['insert', ['link','picture']],
                ['view', ['help']]
            ],
            callbacks: {
                onInit: function() {
                    let placeholder=$(this).prop('placeholder');
                    let target=$(this).siblings('.note-editor').find('.note-placeholder')
                    target.text(placeholder);

                    //  Delete upload image UI --> disabled upload img funciton
                    $(document).find('.note-group-select-from-files').remove();
                    $(document).find('.note-modal .close').remove();
                },
                onChange:function(contents, $editable) {},
                onKeydown: function(e) {
                    if(e.keyCode==13) console.log('Enter/Return key pressed');
                },
                onFocus: function() {},
            }
        });
        //  selectpicker_option_render
        request_selectpicker();
        if(order_id!=='New'){
             // Comment Area - Load comments history
            let comments=get_comment_history(order_id);
            $('#comment_area').empty();
            $.each(comments,function(){
                let comment_obj=$(this)[0];
                append_comment_template('#comment_area',comment_obj)
            });
            comment_area_height();
        }else {
            console.log('The order_id is '+order_id);
            $('#show_commentarea').fadeOut(0);
        }

        $('#requestModal').modal('show');
    }
    function schedule_status_template(order_data){
        //  user_role=='initiator','contactor', 其他沒有功能
        let color='info';
        let icon='ellipsis-h';
        let author_arr=['initiator','developers'];
        let temp='';
        let template='';
        let title='pending...'
        let whoclass='';
        $.each(author_arr,function(i,author){
            let author_data='';
            if(author=='developers'){
                author_data=order_data[author]['contactor'];
                author_data['role']='Contact';
            }else{
                author_data=order_data[author];
                author_data['role']='Initiator';
            }
            let name=author_data['display_name'].split('/Wistron')[0];
            switch (order_data['status']['P3'][author]) {
                case 'Approve':
                    color='success';
                    icon='check-double'
                    title='Approve'
                    break;
                case 'Return':
                    color='danger';
                    icon='reply'
                    title='Reject'
                    break;
                case '':
                    color='info';
                    icon='ellipsis-h'
                    title='Pending...'
                    break;
                default:
                    break;
            }
            template=`<div class="d-flex align-items-center mr-2 badge badge-light badge-pill" style="border:1px solid var(--`+color+`)" title="`+title+`">
                        <img class="sticker mr-1" src="`+images['defaultavatar']+`" data-employee_id="`+author_data['employee_id']+`">
                        <div>
                            <span class="font-weight-bold"><span class="text-grey">`+author_data['role']+`/ &nbsp </span>`+name+`</span>
                            <i class="fa fa-`+icon+` text-`+color+`"></i>
                        </div>
                    </div>`;
            temp+=template
        });
        return temp;
    }
    function pend_schedule(order_id,status,role_arr){
        let formdata=''
        $(document).on('click','#pend_schedule_div button',function(){
            let decide='';
            if($(this).hasClass('approve')){      decide='Approve'
            }else if($(this).hasClass('return')){ decide='Return' }
            console.log(role_arr)
            role_arr=JSON.parse(role_arr);
            $.each(role_arr,function (i,role){
                if(role=='contactor'){role='developers'}
                console.log(status['P3'])
                console.log(role)
                status['P3'][role]=decide;
            })
            formdata=JSON.stringify(status);
            $.when( patch_order(order_id,{'status':formdata})).then(refresh_requestModal(order_id));
        });
    }


    function indentify_user(login_id,order_reponse){
        let singnature_response=get_signaturers(order_reponse.id);

        let initiator=order_reponse['initiator']['employee_id'];
        let assigner=order_reponse['assigner']['employee_id'];
        let author_obj={};
        author_obj[initiator]=['initiator'];
        //  假如initiator和addigner或contactor 為同一人  -->{9505005:['initiator','assigner','contactor']}
        if(author_obj[assigner]==undefined)author_obj[assigner]=['assigner'];
        else if(author_obj[assigner].length!==0)author_obj[assigner].push('assigner');

        let members=order_reponse['developers']['member'];
        let member_obj={};
        if(order_reponse['developers'].length!==0){
            let contactor=order_reponse['developers']['contactor']['employee_id'];
            // author_obj[contactor]='contactor';
            if(author_obj[contactor]==undefined) author_obj[contactor]=['contactor'];
            else if(author_obj[contactor].length!==0) author_obj[contactor].push('contactor');

            $.each(members,function(index,member_info){
                let employee_id=member_info.employee_id;
                member_obj[employee_id]=index;
            });
        }
        let signaturer_obj={};
        let Indentification='';

        $.each(singnature_response,function(index,signaturer_info){
            let employee_id=signaturer_info.signer.employee_id;
            signaturer_obj[employee_id]=signaturer_info.id; //signature_id
        });
        let status=singnature_response[singnature_response.length-1]['status']

        if(login_id in signaturer_obj){
            Indentification={'identity':['signature'],'index':signaturer_obj[login_id]};
            if(login_id in author_obj){
                Indentification={'identity':['signature','assigner'],'index':signaturer_obj[login_id]};
            }
        }else if(login_id in author_obj){
            let role_arr=[];
            $.each(author_obj,function( employee_id,role ){
                if(employee_id==login_id) role_arr=role;
            });
            // Indentification={'identity':author_obj[login_id],'index':0};
            Indentification={'identity':JSON.stringify(role_arr),'index':0};
        }else if(login_id in member_obj){       Indentification={'identity':['member'],'index':member_obj[login_id]};
        }else{                                  Indentification={'identity':['guest'],'index':0};
        }
        Indentification['singnature_status']=status;
        return Indentification;
    }
    // function indentify_modal_show(indentify_user,order_reponse){
    function indentify_modal_show(order_response){
        let userobj=indentify_user(loginInfo.employee_id,order_response);

        //  identify_user format {'identity':'guest'.'index':0}
        //  'identity' initiator/ assigner/ contactor/ member/ signaturer/
        let status=order_response['status'];
        let phase=Object.keys(order_response['status'])[0];
        let id=order_response.id;
        let signed=order_response['status']['signed'];
        let actor=Object.keys(order_response['status'][phase])[0];
        let loginId=loginInfo.employee_id;
        let signature_id=userobj['index'];
        let role=userobj['identity'];
        let raw_dev_data=order_response['developers'];

        //  確認是否因為signer return 造成phase退回的(因為status清空，所以光看status無法得知)
        let singnature_status=userobj['singnature_status'];
        //  Example {'staus':{'P0':{ 'initiataor':'Close' },'signed':flase }} 解析後結果--> 'Closed'
        //  但如果有多人(Phase3 則會有bugs),目前流程多人時，不能Closed
        let oringinal_status=Object.values(Object.values(status)[0])[0];

        //  schedule list
        let schedule_data=get_current_schedule(id);

        //initialize_request/waiting_signature/notify_signing/waiting_receiver_accept_request/receiver_assign_developers
        if(role=='guest'){
            render_ezinfo(id);
        }else{
            append_New_requestModal(id);
            $('#requestModal').data('order_id',id);
            $('#requestModal').data('status',status)
            show_request_info(order_response);
            show_author('form_initiator',order_response['initiator']);

            switch (phase) {
//  Initiator initialize request...
                case 'P0':
                    if(role.includes('initiator')){
                        if(singnature_status=='Return'||signed==true){
                            request_image_module('Reinitialize_request');
                            //  把過去的值填上
                            reinit_value(order_response);
                            $('#initialize_btn,#form_breadcrumb,#form_info').fadeOut(0);
                            $('#Reinit_div').fadeIn(0);
                            get_filelist(id);
                            $('#tag_div').parent('div').fadeIn(0);
                            // $('#FormUpload').fadeIn(0);
                            $('#initialize_btn').siblings('button').fadeIn(0);
                        }else if(singnature_status==''){}
                    }else{
                        request_image_module('initialize_request');
                        $('#FormRequest').fadeOut(0);
                    }
                    break;
//  Initiator supervisor signing...
                case 'P1':
                    $('#FormRequest').fadeOut(0);
                    //  Store order_id to requestModal
                    if(loginId==actor){
                        //  image_status
                        request_image_module('notify_signing');
                        signature_sign(id,signature_id);
                    }else if(role.includes('initiator')||role.includes('assigner')){
                        //  image_status
                        request_image_module('waiting_signature');
                        $('#tag_div').parent('div').fadeIn(0);
                        get_filelist(id);
                    }else{
                        request_image_module('waiting_signature');
                        get_filelist(id);
                        //  Show upload files
                        $('#tag_div').fadeOut(0);
                        $('#FormUpload').fadeOut(0);
                        $('#tag_div').parent('div').fadeIn(0);
                    }
                    break;
//  Assigner assign developers
                case 'P2':
                    $('#FormRequest').fadeOut(0);
                    $('#FormUpload').prop('style','display:none !important;');
                    get_filelist(id);
                    $('#tag_div').parent('div').fadeIn(0);
                    if(role.includes('assigner')){
                        request_image_module('notify_signing');
                        $('#signature_func').fadeIn(0);
                        $('#sign_comment').parent().parent('.row').prop('style','display:none !important;');
                        $('#assign_dev_func').fadeIn(0);

                        $('#ApproveBTN,#ReturnBTN,#CloseBTN').off().on('click',function(){
                            let action=$(this).prop('id').split('BTN')[0];
                            if(action=='Approve'&&$(this).data('assigned')!==true){
                                $('#developersModal').modal('show');
                                return false;
                            }
                            $('#signature_func').fadeOut(0);
                            let status_obj=JSON.stringify({'P2':{'assigner':action,"signed":signed}})
                            let formdata={'status':status_obj}
                            $.when(patch_order(id,formdata)).then(refresh_requestModal(id));
                        });
                    }else if(role.includes('signature')){
                        request_image_module('waiting_receiver_accept_request');
                        $('#trigger_tagModal').prop('disabled',true);

                    }else request_image_module('waiting_receiver_accept_request');
                    break;
//  Assigner plan schedule
//  Initiator, contactor pend schedule
                case 'P3':
                    let assigner_status=status['P3']['assigner'];
                    $('#FormRequest').fadeOut(0);
                    get_schedulelist(schedule_data);
                    get_filelist(id);
                    $('#tag_div').parent('div').fadeIn(0);
                    show_author('form_owner',raw_dev_data);
                    let temp=schedule_status_template(order_response);
                    $('#schedule_status').empty().append(temp);
                    $('#schedule_status').parent('div').fadeIn(0);
                    $('#FormUpload').prop('style','display:none !important;');
                    switch (assigner_status) {
                        case 'Close':
                            $('#schedule_status').parent('div').prop('style','display:none !important;');
                        case '':
                            if(role.includes('assigner')){
                                request_image_module('receiver_proposal_schedule');
                                $('#schedule_area').fadeIn(0);
                            }else{
                                request_image_module('pending_schedule');
                                $('#FormUpload').fadeIn(0);
                            }
                            break;
                        case 'Approve':
                            $('#schedule_status').find('.sticker').each(function(){
                                avatar_reload($(this));
                            });
                            $('#schedule_area').fadeOut(0);
                            get_readonly_schedule(id);
                            $('#readonly_schedule_div').fadeIn(0);
                            request_image_module('pending_schedule');

                            if(role.includes('initiator')&&role.includes('contactor')){
                                console.log('自己發起自己做的狀況');
                                $('#FormUpload').fadeIn(0);
                                let status_arr=Object.values(status['P3']);
                                let ifsigned=1
                                $.each(status_arr,function(i,v){
                                    ifsigned=ifsigned*(v.length);
                                });
                                if(ifsigned==0) {
                                    $('#pend_schedule_div').fadeIn(0);
                                    pend_schedule(id,status,role)
                                };
                            }else if(role.includes('initiator')||role.includes('contactor')){
                                $('#FormUpload').fadeIn(0);
                                let r=role
                                if(role.includes('contactor')) r='developers'
                                else if(role.includes('initiator')) r='initiator'

                                let ifreviewed=status['P3'][r].length
                                if(ifreviewed==0){
                                    $('#pend_schedule_div').fadeIn(0);
                                    pend_schedule(id,status,role);
                                }
                            }else if(role.includes('assigner')){
                                $('#show_shcedule_area').fadeIn(0);
                            }
                            break;
                        default:
                            break;
                    }
                    break;
//  Assigner sypervisor signing...
                case 'P4':
                    $('#FormRequest').fadeOut(0);
                    $('#FormUpload').prop('style','display:none !important;');
                    get_schedulelist(schedule_data);
                    get_filelist(id);
                    $('#tag_div').parent('div').fadeIn(0);
                    show_author('form_owner',raw_dev_data);

                    $('#FormRequest').fadeOut(0);
                    if(loginId==actor){
                        //  image_status
                        request_image_module('notify_signing');
                        signature_sign(id,signature_id);
                    }else if(role.includes('initiator')||role.includes('assigner')){
                        //  image_status
                        request_image_module('waiting_signature');
                    }else{
                        request_image_module('waiting_signature');
                        //  Show upload files
                        $('#tag_div').fadeOut(0);
                        $('#FormUpload').fadeOut(0);
                    }
                    break;
//  Developers submit result...
//  Initiator pending...
                case 'P5':
                    $('#FormRequest').fadeOut(0);
                    // $('#FormUpload').prop('style','display:none !important;');
                    get_schedulelist(schedule_data);
                    get_filelist(id);
                    $('#tag_div').parent('div').fadeIn(0);
                    show_author('form_owner',raw_dev_data);
                    //  schedule list
                    let scheduleStart=schedule_data[0]['timestamp'];
                    let scheduleEnd=schedule_data[schedule_data.length-1]['timestamp'];
                    let schedule={'start':scheduleStart,'end':scheduleEnd};
                    $('#requestModal').data('schedule',schedule);

                    $('#schedule_area').fadeOut(0);
                    get_readonly_schedule(id);
                    $('#readonly_schedule_div').fadeIn(0);
                    $('#schedule_status').parent('div').prop('style','display:none !important;');

                    let progress_json=get_progress(id);
                    render_progress_schedule(progress_json,scheduleStart,scheduleEnd);
                    $('#progress_area').fadeIn(0);
                    if(order_response['repository_url']==null||order_response['repository_url']==''){}
                    else {
                        $('#repository_url').val(order_response['repository_url']);
                        $('#repository_url').siblings('div').find('a').removeClass('btn-light').addClass('btn-success')
                                                                        .prop('href',order_response['repository_url']);
                    }
                    if(actor=='developers') request_image_module('developing');
                    else if(actor=='initiator'&&oringinal_status==''){}
                    if(actor=='initiator'&&oringinal_status=='Approve'){
                        request_image_module('form_completed');
                        $('#tag_div,#trigger_dev_modal,.update_progress,.del_progress,#add_milestone').prop('style','display:none !important;');
                    }else{

                        if(role.includes('initiator')||role.includes('contactor')){
                            $('#progress_area').find('.read_progress').fadeOut(0);
                            if(actor=='developers'){
                                $('#repository_url').prop('disabled',false);
                                $('#submit_result').parent('div').fadeIn(0);
                            }else if(actor=='initiator'&&oringinal_status==''){
                                request_image_module('notify_signing');
                                $('#signature_func').fadeIn(0);
                                $('#sign_comment').parent('div').parent('div').fadeOut(0);
                                $('#sign_comment').parent('div').parent('div').siblings('h6').fadeOut(0);

                                pend_sign(id,status,'P5','initiator');
                            }
                        }else if(role.includes('initiator')){
                            $('#progress_area').find('.update_progress,.del_progress,#add_milestone').fadeOut(0);
                            if(actor=='developers'){
                            }else if(actor=='initiator'&&oringinal_status==''){
                                request_image_module('notify_signing');
                                $('#signature_func').fadeIn(0);
                                $('#sign_comment').parent('div').parent('div').fadeOut(0);
                                $('#sign_comment').parent('div').parent('div').siblings('h6').fadeOut(0);

                                pend_sign(id,status,'P5','initiator');
                            }
                        }else if(role.includes('contactor')){
                            $('#progress_area').find('.read_progress').fadeOut(0);
                            if(actor=='developers'){
                                $('#repository_url').prop('disabled',false);
                                $('#submit_result').parent('div').fadeIn(0);
                            }else if(actor=='initiator'&&oringinal_status==''){
                                request_image_module('initiator_pend');
                                $('#repository_url').prop('disabled',true);
                                $('#submit_result').parent('div').fadeOut(0);
                            }
                        }else if(role.includes('member')){
                            $('#progress_area').find('.read_progress').fadeOut(0);
                            if(actor=='developers'){
                            }else if(actor=='initiator'&&oringinal_status==''){
                                request_image_module('initiator_pend');
                            }
                        }else{
                            $('#tag_div').fadeOut(0);
                            $('#progress_area').find('.update_progress,.del_progress,#add_milestone').fadeOut(0);
                            if(actor=='developers'){
                            }else if(actor=='initiator'&&oringinal_status==''){
                                request_image_module('initiator_pend');
                            }
                        }
                        if(role.includes('assigner')) $('#show_shcedule_area').fadeIn(0);
                    }
                    break;
                default:
                    break;
            }

        }
        if($('#tag_div').parent('div').css('display')!=='none'){
            render_tag_button(order_response['parent']);
        }
        if(oringinal_status=='Close'){
            $('#FormRequest,#FormUpload,#schedule_area,#schedule_status,#signature_func,#trigger_dev_modal').prop('style','display:none !important;');
            $('.update_progress,.del_progress,#add_milestone,#show_shcedule_area').prop('style','display:none !important;');
            $('#progress_area').find('.read_progress').fadeIn(0);
            request_image_module('form_closed');
        }

        if(role.includes('signature')&&role.length==1){$('#tag_div').fadeOut(0);$('#FormUpload').fadeOut(0);}
        //  Store developers list to assign_dev_func>btn
        $('#assign_dev_func').find('button').data('raw_dev_list',order_response['developers']);
        $('.toggle-dev-list').trigger('click')
    }


    function reinit_value(order_reponse){
        let option=order_reponse['develop_team_function']+'_'+order_reponse['develop_team_sub_function'];
        $('#sel_function').selectpicker('val',option).trigger('change').selectpicker('render');
        $('#sel_accounts').selectpicker('val',order_reponse['account']['id']).trigger('change').selectpicker('render');
        $('#sel_projects').selectpicker('val',order_reponse['project']['id']).trigger('change').selectpicker('render');
        $('#sel_assigners').selectpicker('val',order_reponse['assigner']['employee_id']).trigger('change').selectpicker('render');
        $('#title').val(order_reponse['title']);
        $('#description').summernote('code',order_reponse['description']);
    }
