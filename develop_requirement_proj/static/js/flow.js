$(function(){

//  Form Vadlidate
    //  Form request validate setting
    $('#FormRequest').validate({
        rule:{
            description:{
                required: true,
                summernote_validated:true
            }
        }
    });
    //  Validate fields - init request
    $('#initialize_btn').on('click',function(){
        if($('#FormRequest').validate().form()){
            let statusObj={"p1_initiator": "Approve"}
            let init_data=package_data('#FormRequest');
            init_data['status']=JSON.stringify(statusObj)
            init_data['initiator']=$('#form_initiator').data('id');
            post_order(init_data);
        }else console.log('#FormRequest valid false');     
    });



//  Function 
    //  reset request modal
    function reset_requestModal(){
        $('#comment_area').empty();
        $('#filelist').find('tbody').empty();
        $('#toggle-commentarea').removeClass('active');
        $('#toggle-commentarea').find('i').removeClass('active fa-chevron-down').addClass('fa-chevron-up');
        $('#FormRequest_div').removeClass('col-lg-8');
    }
    function empty_data(){

    }





    function render_requestModal(status,role){
        







    }







    $('#requestModal').on('shown.bs.modal',function(){
        // reset_requestModal();
        // $('#toggle-commentarea').removeClass('active');
        // $('#toggle-commentarea').find('i').removeClass('active fa-chevron-down').addClass('fa-chevron-up');

        //  According Status and role to render different fields
        //  (If user=guest all btn display none;)
            //  Phase1  init approve
                //  After initializing request
                //  Show upload_area/ comment_area
                //  Show assigner 

                //  pop if user want to upload files

                //  Onlyif user==assigner,  Reject/ Accept btn pop
                //  Onlyif user==assigner, developer modal pop/  Cancel form btn pop


            //  Phase1  assigner reject
            
                //  Onlyif user==initiator,  Initialize/ Cancel form btn pop



            //  Phase1  assigner approve as same as phase2 initiator/assigner/developer ""
                //  Others waiting ...
                //  Only user=assigner, schedule modal pop/ Cancel form btn pop
                



            //  phase2 assigner approve initiator/developer ""
                // Waiting initiator, developer approve
                //  schedule modal pop/ At present, schedule condition



            //  phase2 assigner/initiator/developer approve
                //  if(user=developer) input result link pop(disabled none)  submit btn



            //  phase3 developer approve
                //  if(user=initiator) Reject btn/ Cancel form btn pop


        // Comment Area - Load comments history
        let comments=get_record_history();
        $.each(comments,function(){
            let comment_obj=$(this)[0];
            append_comment_template('#comment_area',comment_obj)
        });
        //  Files Area - Get fields
        let documents=get_documents('order_id');
        // documentkeys_exited=[];
        // $.each(documents,function(keyname,doc_obj){
        //     let url=doc_obj['link'];
        //     let filesize=Number(doc_obj['size_byte']);
        //     let filename=[...doc_obj['link'].split('/')].pop();
        //     let filetype=filename.split('.')[1];
        //     let imgsrc='';
        //     let keynum=Number(keyname.split('_')[1]);

        //     //  Store exited document key --> arrary
        //     documentkeys_exited.push(keynum);

        //     if(isImage(filetype)) imgsrc=url;
        //     else imgsrc=images['document'];

        //     let template = file_render_template(keyname,url,filesize);
        //     $('#filelist').find('tbody').append(template);
        //     $('#filelist').find('tr').last().find('img').prop('src',imgsrc);
        // });
/* modified */            
        $('#filelist').bootstrapTable('destroy').bootstrapTable({
            data:documents,
            cache: false,
            classes:'table-no-bordered',
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
                        let url=value;

                        let html=`<a class="btn btn-info btn-sm mt-2" href="`+url+`" download >
                                    <i class="fa fa-cloud-download-alt "></i>
                                </a>`
                        return html;
                    }
                },
                {
                    field:'name',
                    formatter:function(value, row, index){
                        let filesize=Number(row['size']);
                        let html=` <p class="font-weight-bold ellipsis pl-2 pr-2 mb-0 filename">`+value+`</p>
                                    <small class="pl-2">`+bytesChange(filesize)+`</small>`;
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
            }
        });












     










        // reset condition
        comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
    });






















});