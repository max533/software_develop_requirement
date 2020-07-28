$(function(){
//  Param    
    let undo_list=[]
    let undos_limit=10;
    let developers_limit=12;
    
    let developers=[];
    let developer_contacter=[];
    let original_dev_list=[];
    let current_dev_list=[];


//  function
    function undo_limit(){
        let limit=undos_limit+1    //limit=10
        if(undo_list.length>=limit){
            undo_list.splice(0,1);
        }
        //  Disabled undo btn or not
        switch (undo_list.length) {
            case 0:
                $('#developer_undo').prop('disabled',true);
                break;
            default:
                $('#developer_undo').prop('disabled',false);
                break;
        }
    }
    select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);


//  Select contact window
    $('#sel_devcontacter_div').find('.selectpicker').on('change',function(){
        developer_contacter=[];
        select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);
        if($(this).val()!==null){
            $(this).selectpicker('setStyle','btn-outline-danger','remove').selectpicker( 'refresh' );
        }
    });



    //  dev modal hide --> empty the developers list
    $('#developersModal').on('hide.bs.modal',function(){      
        //  Search fields empty
        $('#search_dev_site .selectpicker').selectpicker('val','');
        $('#search_dev').val('');
        $('#search_dev_field .active').removeClass('active');
    });



//  Developers table function    
    //  Reset developer list
    $('#developersModal').on('click','#developer_reset',function(){
        //  Store to undo list
        undo_list.push([...current_dev_list]);
        undo_limit();

        $('#present_dev_table').bootstrapTable('load',original_dev_list);
        current_dev_list=[...original_dev_list];

        let current_employee_id_list=current_id_arr(current_dev_list);
        if_employee_joined(current_employee_id_list,developers_limit,'#result_dev_table','#developers_limit');
   
        select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);
    });


    $('#developersModal').on('click','#developer_empty',function(){
        //  Store to undo list
        undo_list.push([...current_dev_list]);
        undo_limit();

        let data=[];
        $('#present_dev_table').bootstrapTable('load',data);
        current_dev_list=[];
        if_employee_joined([],developers_limit,'#result_dev_table','#developers_limit');
        select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);
    });


    $('#developersModal').on('click','#developer_undo',function(){
        let times=undo_list.length;
        let devdata=[];
        if(times>=1){
            devdata=undo_list[times-1];
            undo_list.splice(times-1,1);
            $('#present_dev_table').bootstrapTable('load',devdata);
            let current_employee_id_list=current_id_arr(devdata);
            if_employee_joined(current_employee_id_list,developers_limit,'#result_dev_table','#developers_limit');
        }else console.log('No undo!!');
        undo_limit();
        current_dev_list=devdata;
        select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);
    });
    $('#developersModal').on('shown.bs.modal',function(){
        let raw_dev_list=$('#assign_dev_func').find('button').data('raw_dev_list');
        developers=[];
        developer_contacter=[];
        original_dev_list=[];
        current_dev_list=[]
        if(raw_dev_list['member'].length==0&&raw_dev_list['contactor']!==''){
            developer_contacter.push(raw_dev_list['contactor']);
            original_dev_list=developer_contacter;
            current_dev_list=[...original_dev_list];
        }else if(raw_dev_list['member'].length!==0&&raw_dev_list['contactor']!==''){
            // if(raw_dev_list['member'].length!==0)developers=raw_dev_list['member'];
            developers=raw_dev_list['member']
            
            developer_contacter.push(raw_dev_list['contactor']);
            //  From backend developers list
            original_dev_list=developer_contacter.concat(developers);
            current_dev_list=[...original_dev_list];
        }

        $(this).find('.devsearch_fade').fadeOut(0);

        $('#present_dev_table').bootstrapTable('destroy').bootstrapTable({
            data:current_dev_list, //severside 的網址
            pagination:false,
            fixedColumns: true,
            filterControl: true,
            cache: false,
            buttonsAlign:'right',
            showColumns: true,
            buttonsClass: 'btn btn-outline-secondary float-right',
            classes:'table-no-bordered' ,
            columns: [
                {
                    field:'employee_id',
                    title:'Employee_id',
                    filterControl:'input',
                    width:'200',
                    align:'left',
                    filterControlPlaceholder:'Search id',
                },
                {
                    field:'display_name',
                    title:'Name',
                    filterControl:'input',
                    class:'ellipsis',
                    align:'left',
                    filterControlPlaceholder:'Search name',
                    filterDataCollector:function(value, row, index){
                        let rowlist = [];
                        let name=row['display_name'];
                        rowlist.push(name);
                        return rowlist;
                    },
                    formatter:function(value, row, index){ 
                        let name=row['display_name'];
                        let html = `<div class="d-inline-flex align-items-center"><img src="`+images['defaultavatar']+`" data-employee_id="`+row['employee_id']+`" class="mr-2 sticker"><span>`+name+`</span><div>`;
                        return html;
                    },
                },
                {
                    field:'job_title',
                    title:'Job title',
                    class:'ellipsis',
                    hvalign:'top',
                },
                {
                    field:'extension',
                    title:'Extension',
                    class:'ellipsis',
                    hvalign:'top',
                },
                {
                    field:'edit',
                    title:'Edit',
                    hvalign:'top',
                    formatter:function(value, row, index){
                        let html = `<button class="btn btn-danger btn-sm mt-1 del">
                                        <i class="fas fa-trash-alt"></i>
                                    </button>`;
                        return html;
                    },
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
            rowAttributes:function(row,index) {
                //  Store employee id in tr to selecte conviently
                return {'data-employee_id':row['employee_id']};
            },
            onPreBody:function(data){
                let html=LoadingMessage();
                return html;
            },
            onClickCell:function(field, value, row, $element) { 
                if(field=='edit'){
                    triggerRowDel = true;
                    $element.closest('tr').find('td').eq(0).trigger('click');
                    
                    //  Delete developer from present_dev_table
                    $('#present_dev_table_div').off().on('click','tbody .del',function(){
                        //  Store to undo list
                        undo_list.push([...current_dev_list]);
                        undo_limit();

                        let index=$(this).parents('tr').data('index');                       
                        current_dev_list.splice(index,1);

                        $(this).parents('tr').fadeOut('fast',function(){
                            //  會直接把current_dev_list的資料刪除 
                            $('#present_dev_table').bootstrapTable('remove',{field:'employee_id',values:[parseInt(row.employee_id)]});
                            $('#present_dev_table').bootstrapTable('load',current_dev_list);
     
                            //  Refresh search Table 刪除後可以重新加入 -> btn change
                            let current_employee_id_list=current_id_arr(current_dev_list);
                            if_employee_joined(current_employee_id_list,developers_limit,'#result_dev_table','#developers_limit');
                        });
                    });
                }
            },
            onPostBody:function(name,args){
                if(current_dev_list.length!==0) {
                    select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);
                    avatar_reload($('#present_dev_table').find('img.sticker'));
                }
            },
            onAll:function(name, args){},
        });
        
        let appendbtn_html=`<button type="button" class="btn btn-secondary btn-sm ml-2" id="developer_undo" disabled>
                                <i class="fas fa-undo-alt"></i> Undo
                            </button>
                            <button type="button" class="btn btn-warning btn-sm ml-2" id="developer_reset">
                                <i class="fas fa-thumbtack"></i> Reset last
                            </button>
                            <button type="button" class="btn btn-danger btn-sm ml-3" id="developer_empty">
                                <i class="fas fa-trash-alt"></i> Empty List
                            </button>`
        let undo_limit_alert=`<small class="d-flex justify-content-end text-grey mr-3">Undo limation up to `+undos_limit+`</small>`

        //  Create toolbar btn
        $('#present_dev_table_div').find('.fixed-table-toolbar').addClass('d-flex align-items-center justify-content-end');
        $(appendbtn_html).insertAfter($('#present_dev_table_div .fixed-table-toolbar .btn-group')[0]);
        $(undo_limit_alert).insertAfter($('#present_dev_table_div').find('.fixed-table-toolbar')[0]);

        //  Show count developers 
        let count_number=current_dev_list.length;
        cuunt_current_developers('#developers_limit',count_number,developers_limit);
    });
       



//  Search developers to add
    $('#search_dev_btn').on('click',function(){
        if($('#FormDevelopers').validate().form()){
            let data={};
            let paramkey=$('#search_dev_field').find('input:checked').val()
            data['site__exact']=$('#search_dev_site').find('select').val();
            data[paramkey+'__icontains']=$('#search_dev').val();

            let employees=get_employees(data);
            //  Ccurrent id list
            $('#result_dev_table').bootstrapTable('destroy').bootstrapTable({
                data:employees['rows'],
                fixedColumns: true,
                cache: false,
                contentType:'application/json',
                classes:'table-no-bordered',
                columns: [
                    {
                        field:'employee_id',
                        title:'Employee_id',
                    },
                    {
                        field:'display_name',
                        title:'Name',
                    },
                    {
                        field:'job_title',
                        title:'Job title',
                    },
                    {
                        field:'extension',
                        title:'Extension',
                    },
                    {
                        field:'plus',
                        title:'Plus',
                        width:'180',
                        formatter:function(value, row, index){
                            let employee_id=row['employee_id'];
                            let html;
                            let current_employee_id_list=current_id_arr(current_dev_list);
                            let current_devlopers_num=current_employee_id_list.length;
                            if(current_devlopers_num<developers_limit){
                                if(current_employee_id_list.includes(employee_id)){
                                    html = `<button type="button" class="btn btn-light mt-1 btn-sm" disabled>
                                                <i class="fas fa-signature mr-2"></i>Already joined
                                            </button>`;
                                }else{
                                    html = `<button type="button" class="btn btn-success mt-1 btn-sm add">
                                                <i class="fas fa-plus mr-2"></i>Plus
                                            </button>`;
                                }
                            }else{
                                html = `<button type="button" class="btn btn-light mt-1 btn-sm" disabled>
                                            <i class="fas fa-bullhorn mr-2"></i>Up to limitation <span>`+developers_limit+`<span>
                                        </button>`;
                            }
                            return html;
                        },
                    }
                ],  
                formatNoMatches: function () {
                    let html=NoMatches('Try to enter another keyword!');
                    return html;
                },
                formatLoadingMessage: function(){ 
                    let html=LoadingMessage();
                    return html;
                },
                rowAttributes:function(row,index) {
                    //  Store employee id in tr to selecte conviently
                    return {'data-employee_id':row['employee_id']};
                },
                onPreBody:function(data){
                    //  Show table
                    let html=LoadingMessage();
                    return html;
                },
                onPostBody:function(data){
                    //  Show table
                    $('#developersModal').find('.devsearch_fade').fadeIn(0);
                    let search_complete_html=`<div class="d-flex justify-content-center align-items-center bg-grey mt-2 p-2" style="border-radius:.8rem;">
                                        <h6 class="text-secondary font-weight-bold animated shake slower"> 
                                            - - -&emsp;Search complete&emsp;- - -
                                        </h6>
                                    </div>`;
                    $(search_complete_html).insertAfter('#result_dev_table'); 
                    
                },
                onClickCell:function(field, value, row, $element){  
                    if(field=='plus'){
                        $('#result_dev_table').off().on('click','.add',function(){
                            let addbtn=$(this);
    
                            addbtn.addClass('animated slideOutUpBig');//    位移的動畫
                            let btnhtml=`<button type="button" class="btn btn-light mt-1 btn-sm" style="display:none" disabled>
                                            <i class="fas fa-signature mr-2"></i>Already joined
                                        </button>`;
                            $(btnhtml).insertAfter(addbtn);
                            let disabledbtn=addbtn.siblings('button');
                            addbtn.fadeOut(300,function(){
                                disabledbtn.fadeIn(100);
                            });
    
                            addbtn.on('animationend webkitAnimationEnd', function () {
                                addbtn.remove();
                            });
                            $('#present_dev_table').bootstrapTable('append',row);
    
                            let targettr=$('#present_dev_table').find('tbody').find('tr').last();
                            targettr.fadeOut(0);
                            targettr.find('td').first().append('<h5 class="badge badge-alert badge-pill ml-1">Just joined</h5>')
                            targettr.fadeIn(800);
    
                            //  Store to undo list
                            undo_list.push([...current_dev_list]);
                            undo_limit();
    
                            //  current employee id list
                            current_dev_list.push(row);
                            let current_employee_id_list=current_id_arr(current_dev_list);
                            if_employee_joined(current_employee_id_list,developers_limit,'#result_dev_table','#developers_limit');
                            select_devcontacter('#sel_devcontacter_div','#present_dev_table',current_dev_list,developer_contacter);
                        });
                    }
                }
            });
        }
    });
    



//  Check present_dev_table_div is '' contactor is '' or before updating developers 
    $('#update_dev_btn').on('click',function(){
        let contactor_target=$('#sel_devcontacter_div').find('.selectpicker');
        if(developer_contacter.length==0){
            $(this).tooltip({title:'Assigne at least one developer contactor'}).tooltip('show');
            contactor_target.selectpicker('setStyle', 'btn-outline-danger');
            $('#developersModal').scrollTop(0);
        }else{
            $(this).tooltip('dispose');
            contactor_target.selectpicker('setStyle','btn-outline-danger','remove').selectpicker( 'refresh' );
            let member_arr=[];
            let developer_data={};
            let raw_dev_data={};
            let raw_member_arr=[]
            let contactor=developer_contacter[0]['employee_id'];
            let order_id=$('#requestModal').data('order_id');

            $.each(current_dev_list,function(i,devloper_info){
                if(devloper_info['employee_id']==contactor){
                }else{
                    member_arr.push(devloper_info['employee_id']);
                    raw_member_arr.push(devloper_info);
                } 
            });
            developer_data['member']=member_arr;
            developer_data['contactor']=contactor;
            raw_dev_data['member']=raw_member_arr;
            raw_dev_data['contactor']=developer_contacter[0];
            let respose_order=patch_order(order_id,{'developers':JSON.stringify(developer_data)})
            if(respose_order){    //  確認patch order正確傳到後端，接續執行
                $('#ApproveBTN').data('assigned',true);
                show_author('form_owner',raw_dev_data);
                $('#sel_devcontacter_div').find('.selectpicker').empty().selectpicker('refresh');
                
                //  把更新值存在btn-->在Show modal的值才可以正確
                $('#assign_dev_func').find('button').data('raw_dev_list',respose_order['developers'])
                $('#developersModal').modal('hide');
            }
        }
    });
});