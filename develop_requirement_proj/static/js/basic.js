

$(function(){   

    var pressTimer;

    $('#table').mouseup(function(){
      clearTimeout(pressTimer);
      // Clear timeout
      return false;
    }).mousedown(function(){
      // Set timeout
      pressTimer = window.setTimeout(function() {
          alert('press too long');
      },1000);
      return false; 
    });

//  Global param
    // img_h = $('#image_status').find('img').first().css('height').split('px')[0];

//  General setting 
    //  modal basic setting mutli-modal
    $(document).on('hidden.bs.modal','.modal',function(){
            //  Focus the modal -css -ovwrflow-y
        $('.modal.show').removeClass('blur');
        //  Show >=2 modals, one close, rest modal can scroll.
        let rest_show_modal_num=$('.modal.show').length;
        if(rest_show_modal_num>=1){                
            if($('body').hasClass('modal-open')==false) $('body').addClass('modal-open');
        }
    });
    $(document).on('show.bs.modal', '.modal', function() {
        let zIndex = 1040 + (10 * $('.modal:visible').length);
        $(this).css('z-index', zIndex);
        setTimeout(function() {
            $('.modal-backdrop').not('.modal-stack').css('z-index', zIndex - 1).addClass('modal-stack');
            if($('.modal.show').length>=1){
                $('.modal.show').not(this).addClass('blur');
                $(this).removeClass('blur');
            }
        }, 0);
    });


    // image prop path
    $('#navUser,#user').find('img').prop('src',loginInfo.avatar);
    $('#user').find('span').text(loginInfo.dispaly_name);


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
            // if($(this).parents('#requestModal')) comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h)     
            if($(this).parents('#requestModal')) comment_area_height();     
        });
        dot.fadeToggle('fast');   
    });

//  Table
    //  Initiate Table
    $('#table').bootstrapTable('destroy').bootstrapTable({
        url:fakedata_path+'table.json', //severside 的網址
        // classes: 'table-striped',
        classes: 'table-borderless table-striped',
        pagination:true,
        paginationVAlign:'bottom',
        fixedColumns: true,
        filterControl: true,
        cache: false,
        sortOrder:'asc',
        contentType:'application/json',
        dataType:'json',
        showColumns: true,
        showRefresh: true,
        showToggle: true,
        detailView:true,
        // sidePagination:'server',
        sidePagination:'client',
        pageList:[10, 25, 50, 100],
        // searchOnEnterKey:true,
        clickToSelect: true,  //是否啟用點選選中行
        // trimOnSearch: true,
        buttonsClass: 'btn btn-outline-secondary float-right',
        detailFormatter: 'detailFormatter',
        queryParams:'queryParams',
        iconsPrefix: 'fa',
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
                align:'center',
                filterControlPlaceholder:'Search id',
                formatter:function(value, row, index){
                    let html=`<span class="ellipsis">`+value+`</span>`
                    return html;
                },
            },
            {
                field:'parent',
                title:'Parent form',
                align:'center',
                filterControl:'input',
                filterControlPlaceholder:'Search id',
                filterDataCollector:function(value, row, index){
                    return value;
                },
                formatter:function(value, row, index){
                    let html=''
                    if(value!==null||value!==''){
                        html = `<div class="ellipsis">
                                    <span class="col-6">`+value+`</span>
                                    <i class="ml-2 btn btn-success btn-sm fa fa-file-alt ezinfoModal_trigger"  data-id="`+value+`"></i>
                                </div>`;
                    }
                    return html;
                },
            },
            {
                field:'account',
                title:'Account',
                filterControl: 'select',
                filterControlPlaceholder:'Select Account',
                width:200,
                // filiterData:'var:accounts.id',
                filterDataCollector:function(value, row, index){
                    return (value.id+' _ '+value.code);
                },
                formatter:function(value, row, index){
                    let html=`<span class="ellipsis">`+value.code+`</span>`
                    return html;
                },
            },
            {
                field:'project',
                title:'Project',
                filterControl: 'select',
                filterControlPlaceholder:'Select project',
                width:200,
                filterDataCollector:function(value, row, index){
                    return (value.id+' _ '+value.code);
                },
                formatter:function(value, row, index){
                    let html=`<span class="ellipsis">`+value.code+`</span>`
                    return html;
                },
            },
            {
                field:'initiator',
                title:'Initiator',
                filterControl:'input',
                filterControlPlaceholder:'Search name',
                formatter:function(value, row, index){
                    let avatar=avatar_get(value.employee_id);
                    let html=`<div class="d-inline-flex align-items-top">
                                <img class="sticker mr-2" src="`+avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
                                <div>
                                    <small class="ellipsis text-dark mb-1 mr-1">
                                        `+value.display_name.split('/Wistron')[0]+`
                                    </small>
                                </div>
                            </div>`;
                    return html;
                },
            },
            {
                field:'develop_team_sub_function',
                title:'Developer function',
                filterControl: 'select',
                filterControlPlaceholder:'Select func',
                formatter:function(value, row, index){
                    let html=`<span class="ellipsis">`+value+`</span>`
                    return html;
                },
            },
            {
                field:'assigner',
                title:'Form receiver',
                filterControl:'input',
                filterControlPlaceholder:'Search name',
                formatter:function(value, row, index){
                    let avatar=avatar_get(value.employee_id);
                    let html=`<div class="d-inline-flex align-items-top">
                                    <img class="sticker mr-2" src="`+avatar+`" onerror="this.src='`+images['defaultavatar']+`'">
                                    <div>
                                        <small class="ellipsis text-dark mb-1 mr-1">
                                            `+value.display_name.split('/Wistron')[0]+`
                                        </small>
                                    </div>
                                </div>`;
                    return html;
                },
            },
            {
                field:'title',
                title:'Title',
                filterControl:'input',
                filterControlPlaceholder:'Search title',
                formatter:function(value, row, index){
                    let html='<div class="ellipsis">'+value+'</div>';
                    return html;
                },
            },
            {
                field:'description',
                title:'Description',
                filterControl:'input',
                filterControlPlaceholder:'Search',
                formatter:function(value, row, index){
                    let html='<div class="ellipsis">'+value+'</div>';
                    return html;
                },
            },
            {
                field:'form_begin_time',
                title:'Initial time',
                align:'left',
                sortable: true,
                filterControl:'input',
                formatter:function(value, row, index){
                    let localdate = new Date(value).toLocaleDateString({timeZone: 'Asia/Taipei'}).replace(/\//g, "-");
                    let localtime = new Date(value).toLocaleTimeString('en-US',{timeZone: 'Asia/Taipei', hour12: true});
                    let date = localdate+" "+localtime;
                    let html='<div class="ellipsis">'+date+'</div>';
                    return html;
                },
                filterControlPlaceholder:'2000-01-01 - 2000-01-01',
            },
            {
                field:'repository_url',
                title:'Result',
                hvalign: 'top',
                class:'pb-2',
                align:'center',
                formatter:function(value, row, index){
                    let html='';
                    if(value==''||value==null){
                        html='<a class="fa fa-link" title="nothing" disabled></a>'
                    }else{
                        html='<a href="'+value+'" class="fa fa-link" title="'+value+'"></a>'
                    }
                    return html;
                },
            }
        ],
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
                applyButtonClasses:'btn btn-info',
                cancelButtonClasses:'btn btn-warning',
                // autoApply:true,
                autoUpdateInput: false,
                locale: {
                    cancelLabel: 'Clear',
                    format: 'YYYY-MM-DD '
                }
            });
            target.on('apply.daterangepicker', function(ev, picker) {
                $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));    
                $('#table').bootstrapTable('triggerSearch');
            });
            target.on('cancel.daterangepicker', function(ev, picker) {
                $(this).val('');
                $('#table').bootstrapTable('triggerSearch');
            });
        },
        onDblClickRow:function(row,$element,field) {},
        onClickRow:function(row,$element,field) {
            console.log('click row');
            let authors=author_arr(result);
            console.log(row);
            console.log(authors);
            
        }
    });

    //  Create toolbar btn
    $(document).find('.fixed-table-toolbar').addClass('d-flex align-items-center justify-content-end');
    $('<button class="btn btn-warning text-secondary ml-2" id="addRequestBtn"><i class="fa fa-plus mr-1"></i>Add Request</button>').insertAfter($(document).find('.fixed-table-toolbar .btn-group')[0]);
    $('<button class="btn btn-outline-secondary" id="chart_list" title="Chart"><i class="fa fa-chart-bar"></i></button>').insertAfter($(document).find('.fixed-table-toolbar .btn-group').last()[0]);


    
    //  Delete upload image UI --> disabled upload img funciton
    $(document).find('.note-group-select-from-files').remove();
    $(document).find('.note-modal .close').remove();

});