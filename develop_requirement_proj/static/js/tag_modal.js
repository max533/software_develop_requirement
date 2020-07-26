function render_tag_button(parent_id){
    //  store id and title to dom
    let target=$('#tag_div').find('.ezinfoModal_trigger')
    let show_form_target=target.find('span');

    if(parent_id==undefined||parent_id==''){
        target.data('id',null);
        show_form_target.text('No tag');    
        target.addClass('btn-light').removeClass('btn-success');
        $('.apply_tag').removeClass('active');
    }else{
        target.data('id',parent_id);
        show_form_target.text('Tag Form : '+parent_id+'');    
        target.removeClass('btn-light').addClass('btn-success');
    }   
}
//  選出的單號秀在按鈕上
function apply_remove_tag(parent_id){
    //  store id and title to dom
    let formdata=[];
    render_tag_button(parent_id)
    if(parent_id==undefined||parent_id==''){}
    else formdata=get_tag_record(parent_id);
    $('#present_tag_table').fadeOut().bootstrapTable('load',formdata).fadeIn();
}


$(function(){
    $('#tagModal').on('shown.bs.modal',function(){

        let order_id=$('#requestModal').data('order_id');
        let current_tag_list=get_tag_record(order_id);

        $('#present_tag_table').bootstrapTable('destroy').bootstrapTable({
            data:current_tag_list, //severside 的網址
            pagination:false,
            fixedColumns: true,
            cache: false,
            buttonsAlign:'right',
            buttonsClass: 'btn btn-outline-secondary float-right',
            pageSize:1,
            classes:'table-no-bordered',
            columns: [
                {
                    field:'id',
                    title:'Form id',
                    align:'left',
                    valign:'top',
                    width:100,
                    formatter:function(value, row, index){
                        let html=`<div class="mt-2 d-inline-flex align-items-baseline">
                                    <span class="font-weight-bold"> `+value+` </span>
                                    <i class="ml-2 btn btn-success btn-sm fa fa-file-alt ezinfoModal_trigger" data-id="`+value+`"></i>
                                </div>
                                <div class="w-100">
                                <i class="fa fa-long-arrow-alt-down fa-lg text-grey"></i></div>`;
                        return html;
                    },
                },
                {
                    field:'develop_team_sub_function',
                    title:'Developer team',
                    width:100,
                    valign:'top',
                    formatter:function(value, row, index){
                        let html=`<div class="ellipsis">`+value+`<div>`;
                        return html;
                    },
                },
                {
                    field:'project',
                    title:'Project',
                    width:100,
                    valign:'top',
                    formatter:function(value, row, index){
                        let html=`<div class="ellipsis">`+value['name']+`<div>`;
                        return html;
                    },
                },
                {
                    field:'title',
                    title:'Title',
                    valign:'top',
                    formatter:function(value, row, index){
                        let html='<div class="ellipsis">'+value+'</div>';
                        return html;
                    },
                }, 
                {
                    field:'description',
                    title:'Description',
                    valign:'top',
                    formatter:function(value, row, index){
                        let html='<div class="ellipsis">'+value+'</div>';
                        return html;
                    },
                },
                {
                    field:'form_end_time',
                    title:'Form end',
                    valign:'top',
                    formatter:function(value, row, index){
                        let localdate = new Date(value).toLocaleDateString({timeZone: 'Asia/Taipei'}).replace(/\//g, "-");
                        let localtime = new Date(value).toLocaleTimeString('en-US',{timeZone: 'Asia/Taipei', hour12: true});
                        let date = localdate+" "+localtime;
                        let html='<div class="ellipsis">'+date+'</div>';
                        return html;
                    },
                }
            ],
            formatNoMatches: function () {
                let html=NoMatches('No parent form record');
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
            onPostBody:function(){
                //  Tag the parent row
                let parent_tag=$('#present_tag_table').find('tbody').find('tr').not('.no-records-found').first().find('td').first().find('div').first();
                parent_tag.append('<h5 class="badge badge-info badge-pill">Parent form</h5>');
            }
        });
    });





//  Search parent form
    $('#search_tag_btn').on('click',function(){
        let keyword=$('#search_tag').val();
        let field=$('#search_tag_field').find('label.active');
        search_result_count=true;

        if(keyword.length==0&&field.length==0) $('#search_tag_btn').prop('title','fields required').tooltip('dispose').tooltip('show');
        else if(keyword.length==0&&field.length!==0) $('#search_tag_btn').prop('title','Search keyword required').tooltip('dispose').tooltip('show');
        else if(keyword.length!==0&&field.length==0) $('#search_tag_btn').prop('title','Search field required').tooltip('dispose').tooltip('show');
        else if(keyword.length!==0&&field.length!==0){

            //  GET tags 測試完請刪除
            // let url_select=randomnum(0,2);
            // let urls=[fakedata_path+'tagtable.json',fakedata_path+'empty_table.json'][url_select];
            let present_tag_id=$('#tag_div').find('.ezinfoModal_trigger').data('id');
            let filter_data={}
            let filter=field.find('input').val();
            filter_data[filter]=keyword

            let filter_orders=get_filter_orders(filter_data)['rows'];

            $('#result_tag_table').bootstrapTable('destroy').bootstrapTable({
                // url:fakedata_path+'tagtable.json',
                data:filter_orders,
                pagination:true,
                fixedColumns: true,
                cache: false,
                buttonsAlign:'right',
                buttonsClass: 'btn btn-outline-secondary float-right',
                sidePagination:'client',
                pageList:[10,20,25],
                classes:'table-no-bordered',
                queryParams:'queryParams',
                columns: [
                    {
                        field:'id',
                        title:'Form id',
                        align:'left',
                        valign:'center',
                        width:100,
                        formatter:function(value, row, index){
                            let html=`<div class="mt-1">
                                        <span class="font-weight-bold"> `+value+` </span>
                                        <i class="ml-2 btn btn-success btn-sm fa fa-file-alt ezinfoModal_trigger" data-id="`+value+`"></i>
                                    <div>`;
                            return html;
                        }
                    },
                    {
                        field:'develop_team_sub_function',
                        title:'Developer team',
                        width:100,
                        valign:'center',
                        formatter:function(value, row, index){
                            let html=`<div class="ellipsis">`+value+`<div>`;
                            return html;
                        }
                    },
                    {
                        field:'project',
                        title:'Project',
                        width:100,
                        valign:'center',
                        formatter:function(value, row, index){
                            let html=`<div class="ellipsis">`+value['name']+`<div>`;
                            return html;
                        }
                    },
                    {
                        field:'initiator',
                        title:'Initiator',
                        valign:'center',
                        formatter:function(value, row, index){
                            let avatar=avatar_get(value.employee_id);
                            let html=`<div class="d-inline-flex align-items-center">
                                            <img class="sticker mr-2" src="`+images['defaultavatar']+`" data-employee_id="`+value.employee_id+`">
                                            <div>
                                                <small class="text-dark mb-1 mr-3">
                                                    `+value.display_name.split('/Wistron')[0]+`
                                                </small>
                                            </div>
                                        </div>`
                            return html;
                        }
                    },
                    {
                        field:'assigner',
                        title:'Form receiver',
                        valign:'center',
                        formatter:function(value, row, index){
                            let avatar=avatar_get(value.employee_id);
                            let html=`<div class="d-inline-flex align-items-center">
                                            <img class="sticker mr-2" src="`+images['defaultavatar']+`" data-employee_id="`+value.employee_id+`">
                                            <div>
                                                <small class="text-dark mb-1 mr-3">
                                                    `+value.display_name.split('/Wistron')[0]+`
                                                </small>
                                            </div>
                                        </div>`
                            return html;
                        }
                    },
                    {
                        field:'title',
                        title:'Title',
                        valign:'center',
                        formatter:function(value, row, index){
                            let html='<div class="ellipsis">'+value+'</div>';
                            return html;
                        }
                    },
                    {
                        field:'form_end_time',
                        title:'Form end',
                        valign:'center',
                        formatter:function(value, row, index){
                            let localdate = new Date(value).toLocaleDateString({timeZone: 'Asia/Taipei'}).replace(/\//g, "-");
                            let localtime = new Date(value).toLocaleTimeString('en-US',{timeZone: 'Asia/Taipei', hour12: true});
                            let date = localdate+" "+localtime;
                            let html='<div class="ellipsis">'+date+'</div>';
                            return html;
                        }
                    },
                    {
                        field:'parent',
                        title:'Tag',
                        align:'center',
                        valign:'center',
                        formatter:function(value, row, index){
                            let html;
                            let order_id=$('#requestModal').data('order_id');

                            if(row['id']==order_id){
                                html=`<button type="button" class="btn btn-light btn-sm pb-1 apply_tag" data-order_id="`+row['id']+`" disabled>
                                        <i class="fa fa-lock"></i> Yourself
                                    </button>`;
                            }else if(value==present_tag_id&&present_tag_id!==order_id){
                                html=`<button type="button" class="btn btn-outline-info btn-sm pb-1 active apply_tag" data-order_id="`+row['id']+`">
                                        <i class="fa fa-tag"></i>
                                    </button>`;
                            }else{
                                html=`<button type="button" class="btn btn-outline-info btn-sm pb-1 apply_tag" data-order_id="`+row['id']+`">
                                        <i class="fa fa-tag"></i>
                                    </button>`;
                            }
                                
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
                onPostBody:function(name, args){
                    $('.devsearch_fade').fadeIn();
                    avatar_reload($('#result_tag_table').find('img.sticker'));
                }
            });
        }
    });


//  Apply new tag
    $('#result_tag_table').on('click','.apply_tag',function(){
        let order_id=$('#requestModal').data('order_id');
        let apply_parent_id=$(this).data('order_id');
        let formdata={'parent':apply_parent_id};
        $('.apply_tag').removeClass('active').tooltip('dispose');
        $(this).tooltip({title:'Just apply tag !!'}).tooltip('show');
        $(this).addClass('active');
        apply_remove_tag(apply_parent_id);
        patch_order(order_id,formdata);

        current_tag_list=get_tag_record(order_id);
        $('#present_tag_table').bootstrapTable('load', current_tag_list);
        $('#parent_id').text('Patent form id: '+parent_id);
    });

//  Remove tag
    $('#remove_tag').on('click',function(){
        let order_id=$('#requestModal').data('order_id');
        let formdata={'parent':''};
        apply_remove_tag('');
        patch_order(order_id,formdata);
        current_tag_list=[];
        $('#present_tag_table').bootstrapTable('load', current_tag_list);
    });




























});