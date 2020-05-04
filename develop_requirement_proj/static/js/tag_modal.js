
$(function(){
    $('#tagModal').on('hide.bs.modal',function(){
        if($('#requestModal').css('display')=='block'){
            $('#requestModal').removeClass('blur');
        };
    });


    $('#tagModal').on('shown.bs.modal',function(){
        if($('#requestModal').css('display')=='block'){
            $('#requestModal').addClass('blur');
        };
        let current_tag_list=get_tag_record()['rows'];
        $('#present_tag_table').bootstrapTable('destroy').bootstrapTable({
            data:current_tag_list, //severside 的網址
            pagination:false,
            fixedColumns: true,
            filterControl: true,
            cache: false,
            buttonsAlign:'right',
            // showColumns: true,
            buttonsClass: 'btn btn-outline-secondary float-right',
            pageSize:1,
            classes:'table-no-bordered',
            columns: [
                {
                    field:'id',
                    title:'Form id',
                    align:'left',
                    width:100,
                    formatter:function(value, row, index){
                        let html=`<h6>Form id: `+value+`</h6>
                                    <i class="fa fa-long-arrow-alt-down fa-lg"></i>`;
                        return html;
                    },
                },
                {
                    field:'develop_team_sub_function',
                    title:'Developer function',
                    width:100,
                },
                {
                    field:'assigner',
                    title:'Form receiver',
                    formatter:function(value, row, index){
                        let avatar=avatar_get(value.employee_id);
                        let html=`<div class="d-inline-flex align-items-top">
                                        <img class="sticker mr-2" src="`+avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
                                        <div>
                                            <small class="text-dark mb-1 mr-3">
                                                `+value.display_name.split('/Wistron')[0]+`
                                            </small>
                                        </div>
                                    </div>`
                        return html;
                    },
                },
                {
                    field:'title',
                    title:'Title',
                    formatter:function(value, row, index){
                        let html='<div class="ellipsis">'+value+'</div>';
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

            //  GET tags
            let url_select=randomnum(0,2);
            let urls=[fakedata_path+'tagtable.json',fakedata_path+'empty_table.json'][url_select];
        
            $('#result_tag_table').bootstrapTable('destroy').bootstrapTable({
                url:fakedata_path+'tagtable.json',
                pagination:false,
                fixedColumns: true,
                filterControl: true,
                cache: false,
                buttonsAlign:'right',
                buttonsClass: 'btn btn-outline-secondary float-right',
                sidePagination:'server',
                pageSize:50,
                classes:'table-no-bordered',
                columns: [
                    {
                        field:'id',
                        title:'Form id',
                        align:'center',
                    },
                    {
                        field:'develop_team_sub_function',
                        title:'Developer function',
                    },
                    {
                        field:'assigner',
                        title:'Form receiver',
                        formatter:function(value, row, index){
                            let avatar=avatar_get(value.employee_id);
                            let html=`<div class="d-inline-flex align-items-top">
                                            <img class="sticker mr-2" src="`+avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
                                            <div>
                                                <small class="text-dark mb-1 mr-3">
                                                    `+value.display_name.split('/Wistron')[0]+`
                                                </small>
                                            </div>
                                        </div>`
                            return html;
                        },
                    },
                    {
                        field:'title',
                        title:'Title',
                        formatter:function(value, row, index){
                            let html='<div class="ellipsis">'+value+'</div>';
                            return html;
                        },
                    },
                    {
                        field:'tag',
                        title:'Tag',
                        align:'center',
                        formatter:function(value, row, index){
                            let html=`<button class="btn btn-outline-info btn-sm pb-1" data-toggle="button">
                                        <i class="fa fa-tag"></i>
                                    </button>`;
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

//  Apply new tag
    $('#result_tag_table').on('click','button',function(){
        $(document).find('#result_tag_table button.active').removeClass('active');
        $(this).addClass('active');
    });




























});