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







    // $('#requestModal').on('shown.bs.modal',function(){
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


        //  Files Area - Get fields
        












     










        // reset condition
        // comment_area_height('imgage_dev','image_label_dev','authors','FormRequest','comment_area',img_h);
        // comment_area_height();
    // });






















});