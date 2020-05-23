let requestModal=`<div class="modal fade" id="requestModal" tabindex="-1" data-backdrop="static" data-keyboard="false">
        <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">						
                <div class="modal-body row">
                    <div class="col-12 col-lg-4 d-flex justify-content-center align-items-center bg-water-gradient">
                        <div id="image_status" class="d-flex justify-content-center align-items-center pt-5 animated zoomInDown faster">
                            <div class="text-center" id="imgage_dev">
                                <img>
                                <div class="text-center mt-3" id="image_label_dev">
                                <h3 class="text-bluegray font-weight-bold">Initialize request</h3>
                                <p class="text-bluegray font-weight-bold">
                                    Progress status -- start --
                                </p>
                            </div>
                            </div>
                            <hr>
                            <div style="display:none !important;">
                                <button type="button" id="toggle-commentarea" class="btn btn-secondary btn-sm position-absolute" data-toggle="button">
                                    <i class="fas fa-chevron-up"></i>
                                </button>
                                <!-- One comment content include:who/ avatar/ time/ comment content/ -->
                                <div class="col-12" id="comment_area">
                                    <!-- Load comments history -->
                                </div>
                            </div>
                            <div style="bottom:1rem; position: absolute; display:none !important;">
                                <hr>
                                <textarea id="comment" class="summernote" data-postion="comment" placeholder="Comment ..."></textarea>
                                <button id="sendcomment_btn" type="button" class="btn btn-info btn-sm ml-2">
                                    <i class="fas fa-paper-plane mr-1"></i>Send
                                </button>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-lg-8 px-5 py-3 bg-white" id="FormRequest_div">	
                        <div class="d-inline-flex justify-content-between align-items-baseline w-100">
                            <div>
                                <h6 class="modal-title text-secondary text-center font-weight-bold" id=""> New Request </h6>
                            </div>
                            <button type="button" class="close" data-dismiss="modal">
                                <span> &times; </span>
                            </button>
                        </div>
                        <div class="bg-light bd-radius-8 p-1 d-inline-flex align-items-baseline w-100" id="form_breadcrumb" style="display:none !important;">
                            <span class="mr-2 text-grey"> Assign who </span>
                            <div class="font-bold-weight">
                                <h6 class="badge badge-grey badge-pill" title="Initiator">Leo Tu/WHQ</h6> &rsaquo; 
                                <h6 class="badge badge-grey badge-pill" title="Team">DQMS &rsaquo;</h6>  
                                <h6 class="badge badge-grey badge-pill" title="Account">WT-EBG</h6> &rsaquo; 
                                <h6 class="badge badge-grey badge-pill" title="Project">R360-EBG</h6> &rsaquo; 
                                <h6 class="badge badge-grey badge-pill" title="Receiver">Luis Liao/WNH</h6>
                            </div>
                        </div>
    <!-- authors initiator assigner developers -->
                        <div id="authors" class="mt-2 bg-light bd-radius-8 p-1">			
                            <div class="d-inline-flex align-items-center w-100 author">
                                <span class="text-grey mr-2"> Initiator </span>
                                <div class="d-inline-flex align-items-center" id="form_initiator">
                                    <img class="sticker mr-2" src="">
                                    <span class="text-grey"></span>
                                </div>	
                            </div>
                            <div class="d-inline-flex align-items-center w-100 mt-2 author" style="display:none !important;">
                                <span class="text-grey mr-2"> Form receiver </span>
                                <div class="d-inline-flex align-items-center mr-3" id="form_assigner">
                                    <img class="sticker mr-2" src="">
                                    <span class="text-grey">
                                        <strong class="mr-2">
                                            DQMS/MMS
                                        </strong>
                                        Luis Liao/WHQ
                                    </span>
                                </div>
                            </div>
                            <div class="d-inline-flex align-items-top w-100 mt-2 author" style="display:none !important;">
                                <span class="text-grey mr-2 mt-1"> Assigned developer </span>
                                <div id="form_owner">
                                    <img class="sticker mr-2" src="">
                                    <span class="text-grey mr-2" title="Contact window">
                                        Jeff SH Wang/WHQ 
                                        <strong class="ml-2">&#x22EF;</strong>
                                    </span>
                                    <button class="btn btn-outline-secondary btn-sm toggle-dev-list" data-toggle="button"><i class="fa fa-list mr-1"></i></button>
                                    <button class="btn btn-info btn-sm" data-toggle="modal" data-target="#developersModal">
                                        <i class="fa fa-users"></i>
                                        Edit
                                    </button>
                                    <div class="dev-list">
                                        <ul class="text-grey">
                                            <!-- <li class="mt-1">Kevin SJ Huang/WHQ</li>
                                            <li class="mt-1">Leo Tu/WHQ</li>
                                            <li class="mt-1">Peter Hsien/WHQ</li> -->
                                        </ul>	
                                    </div>
                                </div>
                            </div>
                            <div class="d-inline-flex align-items-top w-100" style="display:none !important;">
                                <span class="text-grey mr-2 mt-1"> ReviewerList </span>
                                <div class="ReviewerList">
                                <!--<div class="mt-1">
                                        <img class="sticker mr-2" src="">
                                        <span class="text-success mr-2">
                                            Jeff SH Wang/WHQ  <i class="fa fa-check-double"></i>
                                        </span>
                                        <p class="bg-white bd-radius-8 p-1"></p>
                                    </div>-->
                                </div>
                            </div>
                        </div>	
                        <hr>
                        <small class="position-absolute text-secondary" style="bottom: .7rem; right:3rem">
                            &#9733 is required field. Need to fill out before requesting.
                        </small>
    <!-- Form Request -->
                        <form id="FormRequest" enctype="multipart/form-data">
                            <!-- Assign which team -->
                            <h6 class="text-secondary font-weight-bold"> Request which team </h6>
                            <div class="row align-items-center mt-3">
                                <label class="col-4"> &#9733 Assign which/ Team </label>
                                <select type="select" class="selectpicker col-8" name="function" id="sel_function" data-width="auto" data-size="7" data-live-search="true" title="Select..." required>
                                    <option value=""> Select... </option>
                                </select>
                            </div>
                            <div class="row align-items-center mt-3">
                                <label class="col-4"> &#9733 Account </label>
                                <select type="select" class="selectpicker col-8" name="account_id" id="sel_accounts" data-width="auto" data-size="7" data-live-search="true" title="Select..." required>
                                    <option value=""> Select... </option>
                                </select>
                            </div>				
                            <div class="row align-items-center mt-3">
                                <label class="col-4"> &#9733 Project </label>
                                <select type="select" class="selectpicker col-8" name="project_id" id="sel_projects" data-width="auto" data-size="7" title="Select account first" required>
                                    <option value=""> Select... </option>
                                </select>
                            </div>
                            <div class="row align-items-center mt-3">
                                <label class="col-4"> &#9733 Assign which/ Who </label>
                                <select type="select" class="selectpicker col-8" name="assigner"  data-width="auto" data-size="7" title="Select project & team first" id="sel_assigners" required>
                                    <option value=""> Select... </option>
                                </select>
                            </div>
                            <hr>
                            <!-- Assign content -->
                            <h6 class="text-secondary font-weight-bold mt-3"> Request content </h6>
                            <div class="row align-items-center mt-2">
                                <label class="col-4"> &#9733 Title </label>
                                <div class="col-8 mb-2">
                                    <input type="text" class="field-style" name="title" placeholder="Develop what" required>
                                </div>
                            </div>

                            <div class="row align-items-top mt-2">
                                <label class="col-4 mt-2"> &#9733 Request description </label>
                                <div class="col-8">
                                    <textarea type="text" class="summernote field-style bd-radius-8" name="description" data-postion="requestform" placeholder="Develop deatail or purpose" required></textarea>
                                </div>
                            </div>
                            <!-- Assign content -->
                            <div id="developer_report" style="display:none !important;">
                                <hr>
                                <h6 class="text-secondary font-weight-bold mt-3"> Developing proccess </h6>
                                <div class="row align-items-center mt-2">
                                    <label class="col-4"> Current completion rate </label>
                                    <div class="mb-2 col-8 d-inline-flex align-items-baseline">
                                        <div class="input-group">
                                            <input type="text" class="form-control field-style" name="complete_rate" id="complete_rate" style="ime-mode:disabled" onkeyup="return ValidateNumber($(this),value)" placeholder="0~100">
                                            <div class="input-group-append">
                                                <button class="btn btn-light font-weight-bold" type="button"> % </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            
                                <div class="row align-items-top mt-2">
                                    <label class="col-4 mt-2"> Note </label>
                                    <div class="col-8">
                                        <textarea class="form-control field-style bd-radius-8" rows="3" name="complete_rate_description" placeholder="Note..."></textarea>
                                    </div>
                                </div>
                                <div class="d-flex justify-content-end mt-2">
                                    <button class="btn btn-info btn-sm" id="update_status"><i class="fa fa-pen"></i> Update status </button>
                                </div>
                            </div>
                            
                            <small class="position-absolute text-secondary" style="bottom: .7rem; right:3rem">
                                &#9733 is required field. Need to fill out before requesting.
                            </small>
                            <hr>
                            <div class="d-flex justify-content-end mt-4 mb-4">
                                <button type="button" class="btn btn-info" id="initialize_btn">
                                    <i class="fa fa-paper-plane"></i>
                                    <span> Initialize request </span>
                                </button>
                            </div>
                        </form>	
                        <div style="display : none !important;">
                            <div class="row align-items-center mt-2" id="tag_div">
                                <hr>
                                <h6 class="col-4 text-secondary font-weight-bold"> Depend on which form </h6>
                                <div class="mb-2 col-8 d-inline-flex align-items-baseline">
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <button class="btn btn-light ezinfoModal_trigger font-weight-bold" type="button" data-id=""> 
                                                <i class="fa fa-file-alt"></i> 
                                                <span></span>
                                            </button>
                                        </div>
                                        <div class="input-group-append">
                                            <button class="btn btn-info" type="button" data-toggle="modal" data-target="#tagModal">
                                                <i class="fa fa-tag"></i> Edit tag
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Assign content -->
                            <h6 class="text-secondary font-weight-bold mt-3" id="file_div_toggle"> Attached files <i class="ml-2 fa fa-angle-up btn btn-light btn-sm" title="Expand"></i></h6>
                            <div class="row align-items-top mt-2 mb-4 file">
                                <div class="col-4 pt-4">
                                    <!-- <label> Upload Files<label> -->
                                </div>
                                <div class="col-8">
                                    <label for="file" class="mt-2 upload-style form-control d-flex align-items-center justify-content-between">											
                                        <input type="file" class="custom-file-input" id="files" name="files[]" multiple size="5" title="No file selected.">
                                    </label>
                                    <h6 class="text-grey caption"> Drag&Drop or Click to choose your file.<i class="fa fa-cloud-upload-alt fa-lg ml-2"></i></h6>
                                    <span class="text-info caption" style="display: none;" id="selected_file"></span>
                                    <textarea class="form-control field-style bd-radius-8" rows="3" placeholder="File description..." id="file_description"></textarea>
                                    <div class="d-flex justify-content-end mt-2">
                                        <button class="btn btn-info btn-sm" id="attached_file_btn"><i class="fa fa-paperclip"></i> Attached file </button>
                                    </div>
                                    <hr>
                                    <small class="ml-3 text-secondary">Restrict number of files limit less than <strong id="restrict_file_num"></strong>.
                                            and size of file limit less than <strong id="restrict_file_size">10 Mb</strong>.
                                    </small>
                                    <table class="w-100" id="filelist"></table>
                                </div>
                                <hr>
                            </div>
                        </div>
                    </div>
                </div>				
            </div>
        </div>
    </div>`;