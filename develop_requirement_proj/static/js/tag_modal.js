
$(function(){
    $('#tagModal').on('shown.bs.modal',function(){

        let current_tag_list=get_tag_record();

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
                        let html=`<div class="ellipsis">`+value['code']+`<div>`;
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
        let keyword=$('#search_tag').val().length;
        let field=$('#search_tag_field').find('label.active').length;
        search_result_count=true;

        if(keyword==0&&field==0) $('#search_tag_btn').prop('title','fields required').tooltip('dispose').tooltip('show');
        else if(keyword==0&&field!==0) $('#search_tag_btn').prop('title','Search keyword required').tooltip('dispose').tooltip('show');
        else if(keyword!==0&&field==0) $('#search_tag_btn').prop('title','Search field required').tooltip('dispose').tooltip('show');
        else if(keyword!==0&&field!==0){

            //  GET tags 測試完請刪除
            // let url_select=randomnum(0,2);
            // let urls=[fakedata_path+'tagtable.json',fakedata_path+'empty_table.json'][url_select];
            let present_tag_id=$('#tag_div').find('.ezinfoModal_trigger').data('id');

            $('#result_tag_table').bootstrapTable('destroy').bootstrapTable({
                url:fakedata_path+'tagtable.json',
                pagination:true,
                fixedColumns: true,
                cache: false,
                buttonsAlign:'right',
                buttonsClass: 'btn btn-outline-secondary float-right',
                sidePagination:'server',
                pageList:[10,20,25],
                classes:'table-no-bordered',
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
                            let html=`<div class="ellipsis">`+value['code']+`<div>`;
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
                                            <img class="sticker mr-2" src="`+avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
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
                                            <img class="sticker mr-2" src="`+avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
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
                            if(value==present_tag_id){
                                html=`<button type="button" class="btn btn-outline-info btn-sm pb-1 active apply_tag" data-id="`+value+`">
                                        <i class="fa fa-tag"></i>
                                    </button>`;
                            }else{
                                html=`<button type="button" class="btn btn-outline-info btn-sm pb-1 apply_tag" data-id="`+value+`">
                                        <i class="fa fa-tag"></i>
                                    </button>`;
                            }
                                
                            return html;
                        }
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
                onLoadError:function(status, jqXHR) {
                    console.log(status);
                    console.log(jqXHR);
                },
                onPostBody:function(name, args){
                    $('.devsearch_fade').fadeIn();
                }
            });
        }
    });


    function apply_remove_tag(clickbtn){
        //  store id and title to dom
        let id=$(clickbtn).data('id');
        let formdata;
        //  store id and title to dom
        let target=$('#tag_div').find('.ezinfoModal_trigger')
        let show_form_target=target.find('span');
        // let id_target=$('#tag_div').find('button');
 
        if(id==undefined||id==''){
            formdata=[];
            target.data('id',null);
            show_form_target.text('');    
            target.addClass('btn-light').removeClass('btn-success');
            $('.apply_tag').removeClass('active');
        }else{
            formdata=get_tag_record(id);
            target.data('id',id);
            show_form_target.text('Tag Form : '+id+'');    
            target.removeClass('btn-light').addClass('btn-success');
        }    
        $('#present_tag_table').fadeOut().bootstrapTable('load',formdata).fadeIn();
    }

//  Apply new tag
    $('#result_tag_table').on('click','.apply_tag',function(){
        $('.apply_tag').removeClass('active').tooltip('dispose');
        $(this).tooltip({title:'Just apply tag !!'}).tooltip('show');
        $(this).addClass('active');
        apply_remove_tag('.apply_tag');
    });

//  Remove tag
    $('#remove_tag').on('click',function(){
        apply_remove_tag($(this)[0]);
    });




























});