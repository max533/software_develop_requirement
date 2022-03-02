function toggleSchedule (t){
    const target = $(t).parents('ul')
    console.log(target)
    $(t).toggleClass('fa-chevron-down').toggleClass('fa-chevron-up')
    target.find('.schedule-li').toggleClass('d-none')
}

$(function(){
//  General setting
    SCHEDULEstart='Estimated beginning';
    SCHEDULEend='Estimated end';

    $('#navSelectUser').find('img').data('employee_id',loginInfo['employee_id']);
    $.when( avatar_reload($('#navSelectUser').find('img')) ).then(function(){
        loginInfo['avatar']=$('#navSelectUser').find('img').prop('src');
    });

    //  modal basic setting mutli-modal
    $(document).on('hidden.bs.modal','.modal',function(){
        //  Focus the modal -css -ovwrflow-y
        // $('.modal.show').removeClass('blur');
        //  Show >=2 modals, one close, rest modal can scroll.
        let rest_show_modal_num=$('.modal.show').length;
        if(rest_show_modal_num>=1){
            if($('body').hasClass('modal-open')==false) $('body').addClass('modal-open');
        }
    });
    $(document).on('show.bs.modal', '.modal', function() {
        let zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex).data('index',$('.modal:visible').length).addClass('index-'+$('.modal:visible').length);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
        }, 0);
    });
    $(document).on('shown.bs.modal', '.modal', function() {
        if($('body').hasClass('modal-open')==false) $('body').addClass('modal-open');
    });


    // image prop path
    $('#navUser,#user').find('img').data('employee_id',loginInfo.employee_id).prop('src',images['defaultavatar']);
    $('#user').prop('href','http://10.32.48.118:50005/profile/'+loginInfo.employee_id);
    avatar_reload($('#navUser').find('img'));
    avatar_reload($('#user').find('img'));
    $('#user,#navUser').find('span').text(loginInfo.display_name.split('/Wistron')[0]);


    //  Toolbar Click #chart_list to call BI chart
    $(document).on('click','#chart_list',function(){
        let paginationUI = $(document).find('.fixed-table-pagination');
        $(this).find('i').toggleClass('fa-chart-bar fa-table');
        if($(this).find('i').hasClass('fa-table')){
            $(this).prop('title','Table');
            $('#table').fadeOut();
            paginationUI.fadeOut();
            //  Disable other button about table
            $(document).find('.fixed-table-toolbar').find('button').not('#chart_list').prop('disabled',true);
            // Change title
            $('#pagetitle').text('Development Requirement Chart');
        }else {
            $(this).prop('title','Chart');
            $(document).find('.fixed-table-toolbar').find('button').prop('disabled',false);
            $('#table').fadeIn();
            paginationUI.fadeIn();

            $('#pagetitle').text('Development Requirement List');
        }
    });


    //  假如開發者只有一人 不顯示這個按鈕和點點點
    //  .toggle-group-list
    $(document).on('click','.toggle-dev-list',function(){
        let dot = $('.toggle-dev-list').siblings('span').find('strong');
        $(this).siblings('.dev-list').slideToggle('fast',function(){
            if($(this).parents('#requestModal').length==1) comment_area_height();
        });
        dot.fadeToggle('fast');
    });

//  Table
    //  Initiate Table
    $('#table').bootstrapTable('destroy').bootstrapTable({
        url:'/api/orders/', //severside 的網址
        classes: 'table-responsive table-bordered',
        theadClasses:'',
        pagination:true,
        paginationVAlign:'bottom',
        fixedColumns: true,
        filterControl: true,
        sortOrder:'asc',
        contentType:'application/json',
        dataType:'json',
        showColumns: true,
        showRefresh: true,
        showToggle: true,
        // detailView:true,
        sidePagination:'server',
        pageList:[10, 25, 50, 100],
        searchOnEnterKey:false,
        clickToSelect: true,  //是否啟用點選選中行
        buttonsClass: 'btn btn-outline-secondary float-right',
        detailFormatter: 'detailFormatter',
        queryParams:'queryParams',
        iconsPrefix: 'fa',
        rowStyle: function(row, index) {
            let status=Object.values(Object.values(row.status)[0])[0];
            if(status=='Close'){
                return {css:{'text-decoration':'line-through'}};
            }else{
                return {};
            }
        },
        icons: {
            paginationSwitchDown: 'fa-caret-down',
            paginationSwitchUp: 'fa-caret-up',
            refresh: 'fa-sync',
            toggleOff: 'fa-toggle-off',
            toggleOn: 'fa-toggle-on',
            columns: 'fa-th-list',
            detailOpen: 'fas fa-list',
            detailClose: 'fa-angle-left',
        },
        columns: [
            {
                field:'id',
                title:'Form id',
                filterControl:'input',
                filterControlPlaceholder:'Search id',
                formatter:function(value, row, index){
                    let html=`  <button type="button" class="btn btn-outline-primary btn-sm openOrder">
                                    Check ${value}
                                    <i class="fa fa-arrow-circle-right fa-sm ml-2"></i>
                                </button>`
                    return html;
                },
            },
            {
                field:'title',
                title:'Title',
                filterControl:'input',
                filterControlPlaceholder:'Search title',
                formatter:function(value, row, index){
                    let html = '-'
                    if(value){
                        html='<div class="ellipsis">'+value+'</div>';
                    }
                    return html;
                },
            },
            {
                field:'description',
                title:'Description',
                // visible: false,
                filterControl:'input',
                filterControlPlaceholder:'Search',
                formatter:function(value, row, index){
                    let html = '-'
                    if(value){
                        value=value.replace(/\\/g,'');
                        html='<div class="ellipsis">'+value+'</div>';
                    }
                    return html;
                },
            },
            {
                field:'schedule',
                title:'Schedule',
                hvalign: 'top',
                formatter:function(value, row, index){
                    if(!value.length) return '-'
                    value=value.reverse()
                    const htmlArr = $.map(value, (schedule, index)=>{
                        const {name, date_start, date_end}=schedule
                        return `<li class="${index!==0?'d-none schedule-li':''}">
                                    <span style="width:6rem; display:inline-block;">${name}</span>
                                    ${date_start} ~ ${date_end}
                                    ${index===0?'<i class="ml-2 text-primary fa fa-chevron-down" style="cursor:pointer;" onclick="toggleSchedule(this)"></i>':''}
                                </li>`
                    })
                    return `<ul class="m-1" style="list-style-type: none; padding-inline-start: 0;">
                                ${htmlArr.join('')}
                            </ul>`
                }
            },
            {
                field:'status',
                title:'Phase',
                class:'pb-2',
                visible:false,
                formatter:function(value, row, index){
                    let p=Object.keys(value)[0],
                        phase='';
                    switch (p) {
                        case 'P0':
                            phase='Initiatized order';
                            break;
                        case 'P1':
                            phase="Initiator's supervisor review"
                            break;
                        case 'P2':
                            phase="Receiver accept order"
                            break;
                        case 'P3':
                            phase="All participates negotiate schedule"
                            break;
                        case 'P4':
                            phase="Receiver's supervisor review"
                            break;
                        case 'P5':
                            phase="Developer develop"
                            break;
                        default:
                            break;
                    }
                    return phase;
                },
            },

            {
                field:'status_detail',
                title:'Status',
                hvalign: 'top',
                class:'pb-2',
                formatter:function(value, row, index){
                    function status_temp(d){
                        let employee_id=d.employee_id,
                            display_name=d.display_name,
                            role=d.role,
                            status=d.response,
                            status_color='text-info';
                        if(!display_name) display_name = "non-found"
                        else display_name = display_name.split('/')[0]

                        switch (status) {
                            case 'Approve':
                                status='approve';
                                status_color='text-success';
                                break;
                            case 'Return':
                                status='reject';
                                status_color='text-danger';
                                break;
                            case 'Close':
                                status='close';
                                status_color='text-light';
                                break;
                            case '':
                                status='in progress...';
                                break;
                            default:
                                break;
                        }
                        switch (role) {
                            case 'assigner':
                                role='Receiver';
                                break;
                            case 'signaturer':
                                role='Reviewer';
                                break;
                            case 'initiator':
                                role='Initiator';
                                break;
                            case 'developers':
                                role='Dev contact';
                                break;
                            default:
                                break;
                        }
                        html=`<div class="d-inline-flex align-items-top mt-1">
                                    <img class="sticker mr-2" src="`+images['defaultavatar']+`" data-employee_id="`+employee_id+`">
                                    <div class="d-inline-flex align-items-baseline" style="white-space: nowrap;">
                                        <small class="ellipsis text-dark mb-1 mr-1">`+role+`/ `+display_name+`</small>
                                        <small class="`+status_color+`" style="font-weight: 700;">`+status+`</small>
                                    </div>
                                </div>`;
                        return html;
                    }
                    let html=``
                    $.each(value.action,function(key,whoturn){
                        if( whoturn.response==='' ) html += status_temp(whoturn)
                    });
                    html=`<div>`+html+`</div>`
                    return html;
                },
            },
            // {
            //     field:'parent',
            //     title:'Parent form',
            //     visible: false,
            //     filterControl:'input',
            //     filterControlPlaceholder:'Search id',
            //     filterDataCollector:function(value, row, index){
            //         return value;
            //     },
            //     formatter:function(value, row, index){
            //         let html='<span class="text-grey font-weight-bold ml-3"> - </span>';
            //         if(value==null||value==''){
            //         }else{
            //             html = `<div class="ellipsis">
            //                         <span class="col-6">`+value+`</span>
            //                         <i class="ml-2 btn btn-success btn-sm fa fa-file-alt ezinfoModal_trigger"  data-id="`+value+`"></i>
            //                     </div>`;
            //         }
            //         return html;
            //     },
            // },
            // {
            //     field:'account',
            //     title:'Account',
            //     visible:false,
            //     filterControl: 'select',
            //     filterControlPlaceholder:'Select Account',
            //     width:200,
            //     filterDataCollector:function(value, row, index){
            //         return (value.id+' _ '+value.code);
            //     },
            //     formatter:function(value, row, index){
            //         let html = '-'
            //         if(value){
            //             html=`<span class="ellipsis">`+value.code+`</span>`
            //         }
            //         return html;
            //     },
            // },
            // {
            //     field:'project',
            //     title:'Project',
            //     filterControl: 'select',
            //     filterControlPlaceholder:'Select project',
            //     width:200,
            //     filterDataCollector:function(value, row, index){
            //         return (value.id+' _ '+value.name);
            //     },
            //     formatter:function(value, row, index){
            //         let html = '-'
            //         if(value){
            //             html=`<span class="ellipsis">`+value.name+`</span>`
            //         }
            //         return html;
            //     },
            // },
            {
                field:'develop_team_sub_function',
                title:'Developer function',
                visible:false,
                filterControl: 'select',
                filterControlPlaceholder:'Select func',
                filterDataCollector:function(value, row, index){
                    return value;
                },
                formatter:function(value, row, index){
                    let html = '-'
                    if(value){
                        html=`<span class="ellipsis">`+value+`</span>`
                    }
                    return html;
                },
            },
            {
                field:'initiator',
                title:'Request',
                filterControl:'input',
                filterControlPlaceholder:'Search name',
                formatter:function(value, row, index){
                    let html = '-'
                    if(typeof(value)=='string'&&value){
                        html = `<span>${value}(non-found)</span>`;
                    }else if(typeof(value)=='object'){
                        html = `<div class="d-inline-flex align-items-top mt-1">
                                    <img class="sticker mr-2" src="`+images['defaultavatar']+`" data-employee_id="`+value.employee_id+`">
                                    <div>
                                        <small class="ellipsis text-dark mb-1 mr-1">
                                            `+value.display_name.split('/Wistron')[0]+`
                                        </small>
                                    </div>
                                </div>`;
                    }
                    return html;
                },
            },
            {
                field:'assigner',
                title:'Assigner',
                visible: false,
                filterControl:'input',
                filterControlPlaceholder:'Search name',
                formatter:function(value, row, index){
                    let html = '-'
                    if(typeof(value)=='string'&&value){
                        html = `<span>${value}(non-found)</span>`;
                    }else if(typeof(value)=='object'){
                        html=`<div class="d-inline-flex align-items-top mt-1">
                                    <img class="sticker mr-2" src="`+images['defaultavatar']+`" data-employee_id="`+value.employee_id+`">
                                    <div>
                                        <small class="ellipsis text-dark mb-1 mr-1">
                                            `+value.display_name.split('/Wistron')[0]+`
                                        </small>
                                    </div>
                                </div>`;
                    }
                    return html;
                },
            },
            {
                field:'form_begin_time',
                title:'Initial time',
                align:'left',
                // sortable: true,
                filterControl:'input',
                formatter:function(value, row, index){
                    let html = '-'
                    if(value){
                        let date = isotime_local(value);
                        html='<div class="ellipsis">'+date+'</div>';
                    }
                    return html;
                },
                filterControlPlaceholder:'2000-01-01 - 2000-01-01',
            },
            {
                field:'repository_url',
                title:'Result',
                visible: false,
                hvalign: 'top',
                class:'pb-2',
                align:'center',
                formatter:function(value, row, index){
                    let html='<span class="text-grey font-weight-bold"> - </span>';
                    if(value==''||value==null){
                    }else{
                        html='<a href="'+value+'" class="fa fa-link" title="'+value+'" target="_blank"></a>'
                    }
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
        onLoadError:function(status, jqXHR) {
            console.log(status);
            console.log(jqXHR);
        },
        onPostBody:function(name, args){
            let target = $('#table').find('th[data-field="exp_date"],th[data-field="form_begin_time"]').find('input');
            target.daterangepicker({
                minYear: 1985,
                maxYear: parseInt(moment().format('YYYY'),10),
                autoUpdateInput: false,
                applyButtonClasses:'btn btn-info',
                cancelButtonClasses:'btn btn-warning',
                locale: {
                    cancelLabel: 'Clear',
                    format: 'YYYY-MM-DD '
                }
            });
            target.on('apply.daterangepicker', function(ev, picker) {
                target.trigger('cancel.daterangepicker');
                target.val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));
            });
            target.on('cancel.daterangepicker', function(ev, picker) {
                target.val("");
            });
            avatar_reload($('#table').find('img.sticker'));
        },
        onDblClickRow:function(row,$element,field) {},
        onClickCell:function(field, value, row, $element) {
            if(field == 'id') {
                    indentify_modal_show(row);
            }
        }
    });

    //  Create toolbar btn
    $(document).find('.fixed-table-toolbar').addClass('d-flex align-items-center justify-content-end');
    $('<button class="btn btn-warning text-secondary ml-2" id="addRequestBtn"><i class="fa fa-plus mr-1"></i>Add Request</button>').insertAfter($(document).find('.fixed-table-toolbar .btn-group')[0]);
    $('<button class="btn btn-outline-secondary" id="chart_list" title="Chart"><i class="fa fa-chart-bar"></i></button>').insertAfter($(document).find('.fixed-table-toolbar .btn-group').last()[0]);



});
