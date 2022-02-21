let requestModal=`<div class="modal fade" id="requestModal" tabindex="-1" data-backdrop="static" data-keyboard="false" data-order_id="New">
        <div class="modal-dialog modal-dialog-centered modal-lg" role="document">
            <div class="modal-content">
                <div class="modal-body row">
                    <div class="col-12 col-lg-4 bg-water-gradient">
                        <div id="image_status" class="pt-5 animated zoomInDown faster">
                            <div class="text-center" id="imgage_dev">
                                <img>
                                <div class="mt-3 text-center mt-3 pl-4 pr-4" id="image_label_dev">
                                    <h3 class="text-bluegray font-weight-bold">Initialize request</h3>
                                    <p class="text-bluegray font-weight-bold">
                                        Progress status -- start -- </br>After initializing, it will be sent to your supervisors to review.
                                    </p>
                                    <div id="status_text">
                                        <!--<h6 class="text-secondary font-weight-bold">
                                            <small class="badge badge-light badge-pill">Initaiator</small>
                                            Leo Tu
                                            <strong>Initialized</strong>
                                        </h6>-->
                                    </div>
                                    <button type="button" class="btn btn-dark text-info" id="show_commentarea"><i class="far fa-comments mr-2"></i> Leave comments </button>
                                </div>
                            </div>
                            <div id="display_comment_area" style="display:none !important;">
                                <hr>
                                <div class="w-100 d-flex justify-content-end">
                                    <button type="button" id="hide_commentarea" class="btn btn-dark text-info position-absolute" data-toggle="button">
                                        <i class="fa fa-chevron-left mr-2"> Back </i>
                                    </button>
                                </div>
                                <!-- One comment content include:who/ avatar/ time/ comment content/ -->
                                <div class="col-12 mt-5" id="comment_area">
                                    <!-- Load comments history -->
                                </div>
                            </div>
                            <div id="edit_comment_area" style="display:none !important;">
                                <hr>
                                <textarea id="comment" class="summernote" data-postion="comment" placeholder="Comment ..."></textarea>
                                <button id="sendcomment_btn" type="button" class="btn btn-info btn-sm ml-2">
                                    <i class="fas fa-paper-plane mr-1"></i>Send
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="col-lg-8 px-5 py-3 bg-white" id="FormRequest_div">
                        <div class="d-inline-flex justify-content-between align-items-center w-100">
                            <div>
                                <h6 class="modal-title text-secondary text-center font-weight-bold"> Request
                                    <span class="badge badge-light badge-pill" id="order_id">Form id: - </span>
                                    <span class="badge badge-light badge-pill" id="parent_id">Parent form id: - </span>
                                </h6>
                            </div>
                            <button type="button" class="close" data-dismiss="modal">
                                <span> &times; </span>
                            </button>
                        </div>
                        <div class="bg-light bd-radius-8 p-1 d-inline-flex align-items-baseline w-100" id="form_breadcrumb" style="display:none !important;">
                            <span class="col-2 text-grey"> Assign </span>
                            <div class="font-bold-weight pt-2">
                                <!--<h6 class="badge badge-bluegray badge-pill" title="Request">Leo Tu/WHQ</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill" title="Team">DQMS &rsaquo;</h6>
                                <h6 class="badge badge-bluegray badge-pill" title="Account">WT-EBG</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill" title="Project">R360-EBG</h6> &rsaquo;
                                <h6 class="badge badge-bluegray badge-pill" title="Assigner">Luis Liao/WNH</h6>-->
                            </div>
                        </div>
                        <div class="bg-light bd-radius-8 w-100 mt-2" id="form_info" style="display:none !important;">
                            <div class="d-inline-flex align-items-center w-100 mt-2">
                                <span class="text-grey col-2"> Title </span>
                                <h6 class="text-bluegray ellipsis" id="request_title"></h6>
                            </div>
                            <div class="d-inline-flex align-items-top w-100 mt-2">
                                <span class="text-grey col-2"> Description </span>
                                <div class="mr-3 ellipsis" id="request_description" style="padding-top:0!important;"></div>
                            </div>
                        </div>
    <!-- authors initiator assigner developers -->
                        <div id="authors" class="mt-2 bg-light bd-radius-8 p-1">
                            <div class="d-inline-flex align-items-center w-100 author">
                                <span class="text-grey col-2"> Request </span>
                                <div class="d-inline-flex align-items-center" id="form_initiator">
                                    <img class="sticker mr-2" src="">
                                    <span class="text-grey"></span>
                                </div>
                            </div>
                            <div class="d-inline-flex align-items-center w-100 mt-2 author" style="display:none !important;">
                                <span class="text-grey col-2"> Assigner </span>
                                <div class="d-inline-flex align-items-center mr-3" id="form_assigner">
                                    <img class="sticker mr-2" src="">
                                    <span class="text-grey"></span>
                                </div>
                            </div>
                            <div class="d-inline-flex align-items-top w-100 mt-2 author" style="display:none !important;">
                                <span class="text-grey col-2 mt-1"> Developer </span>
                                <div id="form_owner">
                                    <img class="sticker mr-2" src="">
                                    <span class="text-grey mr-2" title="Contact window"></span>
                                    <strong class="ml-2">&#x22EF;</strong>
                                    <button class="btn btn-outline-secondary btn-sm toggle-dev-list" data-toggle="button"><i class="fa fa-list mr-1"></i></button>
                                    <button class="btn btn-info btn-sm" id="trigger_dev_modal" data-toggle="modal" data-target="#developersModal">
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
                                <span class="text-grey col-2 mt-1"> ReviewerList </span>
                                <div class="ReviewerList"></div>
                            </div>
                        </div>
    <!-- Form Request -->
                        <form id="FormRequest" enctype="multipart/form-data">
                            <hr>
                            <small class="position-absolute text-secondary" style="bottom: .7rem; right:3rem">
                                &#9733 is required field. Need to fill out before requesting.
                            </small>
                            <!-- Assign which team -->
                            <h6 class="text-secondary font-weight-bold"> Request which team</h6>
                            <div class="row align-items-center mt-3">
                                <label class="col-4"> &#9733 Dev Team </label>
                                <select type="select" class="selectpicker col-8" name="function" id="sel_function" data-width="auto" data-size="7" data-live-search="true" title="Select ..." required>
                                    <option value=""> Select... </option>
                                </select>
                            </div>
                            <div class="row align-items-center mt-3">
                                <label class="col-4"> &#9733 System </label>
                                <select type="select" class="selectpicker col-8" name="system_id" id="sel_system" data-width="auto" data-size="7" title="Select ..." data-live-search="true" required>
                                    <option value=""> Select... </option>
                                </select>
                            </div>
                            <div>
                                <label class="col-4 mt-3"> Dev Group/
                                    <span id="dev_group" class="pl-3" id="dev_group_name"> - </span>
                                </label>
                            </div>
                            <div>
                                <label class="col-4 mt-1"> Dev Leader/
                                    <span id="dev_leader" class="pl-3" id="dev_group_leader"> - </span>
                                </label>
                            </div>
                            <hr>
                            <!-- Assign content -->
                            <h6 class="text-secondary font-weight-bold mt-3"> Request content </h6>
                            <div class="row align-items-center mt-2" style="display: none!important;">
                                <label class="col-4"> &#9733 Title </label>
                                <div class="col-8 mb-2">
                                    <input type="text" class="field-style" name="title" id="title" placeholder="Develop what" required>
                                </div>
                            </div>

                            <div class="row align-items-top mt-2">
                                <label class="col-4 mt-2"> &#9733 Description </label>
                                <div class="col-8">
                                    <textarea type="text" class="field-style bd-radius-8" name="description" id="description" data-postion="requestform" placeholder="Develop deatail or purpose" required></textarea>
                                </div>
                            </div>
                            <small class="position-absolute text-secondary" style="bottom: .7rem; right:3rem">
                                &#9733 is required field. Need to fill out before requesting.
                            </small>
                            <hr>
                            <div class="d-flex justify-content-end mt-4 mb-4">
                                <button type="button" class="btn btn-info" id="initialize_btn">
                                    <i class="fa fa-paper-plane"></i>
                                    <span> Init request </span>
                                </button>
                            </div>
                        </form>
                        <div style="display : none !important;">
                            <div class="d-inline-flex align-items-top w-100 mb-4 file bg-light bd-radius-8 p-1 mt-2" id="show_file_div">
                                <h6 class="col-3 pt-1 text-secondary font-weight-bold"> Attached-file <i id="file_div_toggle" class="ml-2 fa fa-angle-up btn btn-light btn-sm" title="Expand"></i></h6>
                                <div class="col-9">
                                    <hr>
                                    <table class="w-100" id="filelist"></table>
                                    <hr>
                                    <small class="ml-3 text-secondary">Restrict number of files limit less than <strong id="restrict_file_num">100</strong>.
                                            and size of file limit less than <strong id="restrict_file_size"> 5GB </strong>.
                                    </small>
                                </div>
                            </div>
                            <div class="row align-items-center mt-2" id="tag_div">
                                <hr>
                                <h6 class="col-3 text-secondary font-weight-bold"> Depend on which form </h6>
                                <div class="mb-2 col-9 d-inline-flex align-items-baseline">
                                    <div class="input-group">
                                        <div class="input-group-prepend">
                                            <button class="btn btn-light ezinfoModal_trigger font-weight-bold" type="button">
                                                <i class="fa fa-file-alt"></i>
                                                <span></span>
                                            </button>
                                        </div>
                                        <div class="input-group-append">
                                            <button class="btn btn-info" type="button" data-toggle="modal" data-target="#tagModal" id="trigger_tagModal">
                                                <i class="fa fa-tag"></i> Edit tag
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <!-- Assign content -->
                            <form class="row align-items-top mt-2 file" id="FormUpload">
                                <div class="col-3">
                                    <h6 class="text-secondary font-weight-bold mt-3"> Attached files </h6>
                                    <span class="mt-1 text-danger font-weight-bold"><i class="fa fa-bullhorn mr-2"></i>Necessary file/
                                    <a class="btn btn-warning btn-sm" href="#" id="file_template_download" download><i class="fa fa-file-download mr-1"></i>Template</a>
                                    </span>
                                    <li class="text-danger">Systems architecture</li><li class="text-danger">Benefit assessment</li>
                                </div>
                                <div class="col-9">
                                    <label for="file" class="mt-2 upload-style form-control d-flex align-items-center justify-content-between bd-radius-8 bg-light">
                                        <input type="file" class="custom-file-input" id="files" name="files[]" multiple size="5" title="No file selected." required>
                                    </label>
                                    <h6 class="text-grey caption"> Drag&Drop or Click to choose your file.<i class="fa fa-cloud-upload-alt fa-lg ml-2"></i></h6>
                                    <span class="text-info caption" style="display: none;" id="selected_file"></span>
                                    <textarea class="form-control field-style bd-radius-8" rows="3" placeholder="File description..." name="description" id="file_description" required></textarea>

                                    <div class="d-flex justify-content-end mt-3 mb-4">
                                        <button type="button" class="btn btn-info" id="attached_file_btn"><i class="fa fa-paperclip"></i> Attached file </button>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="mb-4" id="Reinit_div" style="display:none !important;">
                            <hr>
                            <div class="d-flex justify-content-between">
                                <button type="button" class="btn btn-danger mr-3 text-left" id="close_init_btn" style="left:3em;">
                                    <i class="fa fa-stop"></i>
                                    <span> Close </span>
                                </button>
                                <button type="button" class="btn bg-primary" id="Reinitialize_btn">
                                    <i class="fa fa-paper-plane"></i>
                                    <span> Reinit request </span>
                                </button>
                            </div>
                        </div>
        <!-- Schedule -->
                        <div id="schedule_area" style="display:none !important;">
                            <hr>
                            <h6 class="text-secondary font-weight-bold mt-3"> Estimated schedule (Only for form receiver editing.) </h6>
                            <p class="text-danger"> <i class="fa fa-bullhorn text-danger mr-2"></i>Once applying schedule change, the whole request need to be approved by "initiator","developer contactor",and "reviewers(assigner supervisor)." </p>

                            <p class="text-danger"> Click "Submit schedule" button,the schedule will submit.</p>
                            <hr>
                            <div class="mt-2">
                                <table class="table table-borderless bg-light bd-radius-8 table-hover w-100" data-updatelist_obj="{}" data-del_id_arr="[]" id="schedulelist"></table>
                            </div>
                            <form id="FormSchedule" class="mt-2 bg-light bd-radius-8">
                                <table style="overflow:scroll;">
                                    <tbody>
                                        <tr class="d-flex align-items-top pt-2 pb-1">
                                            <td><input class="field-style mr-2" placeholder="Milestone..." name="event_name" required></td>
                                            <td style="max-width:150px;"><input class="field-style mr-2 date" placeholder="Estimated date" name="expected_time" required></td>
                                            <td style="min-width:320px;"><textarea class="form-control field-style bd-radius-8 mr-2" rows="2" name="description" placeholder="Description..." required></textarea></td>
                                            <td style="max-width:100px;">
                                                <div class="input-group mr-2">
                                                    <input type="text" class="form-control field-style" name="complete_rate" id="schedule_complete_rate" style="ime-mode:disabled" onkeyup="return ValidateNumber($(this),value)" placeholder="1~99 complete" required>
                                                    <div class="input-group-append">
                                                        <button class="btn btn-light font-weight-bold" type="button"> % </button>
                                                    </div>
                                                </div>

                                             </td>
                                            <td class="ml-2 pt-1"><button type="button" class="btn btn-info btn-sm" id="add_schedule_btn"><i class="fa fa-plus"></i>Add</button></td>
                                        </tr>
                                    </tbody>
                                </table>
                            </form>
                            <hr>
                            <div class="d-flex justify-content-between mt-2 mb-4">
                                <button type="button" class="btn btn-danger btn-sm" id="close_schedule_btn"><i class="fa fa-stop" title="WARNING: This is irreversible."></i> Close request </button>
                                <button type="button" class="btn btn-info btn-sm" id="update_schedule_btn"><i class="fa fa-calendar-day"></i> Submit schedule </button>
                            </div>
                        </div>
                        <div id="readonly_schedule_div" style="display:none !important;">
                            <div class="class="mt-2 bg-light bd-radius-8">
                                <h6 class="text-secondary font-weight-bold mt-3"> Estimated schedule (Only for form receiver editing.)
                                    <button class="btn btn-sm bg-cardDelay ml-2" type="button" id="show_shcedule_area" style="display:none !important;"> <i class="fa fa-pen"></i> Re-schedule </button>
                                </h6>
                                <table class="table table-borderless bg-light bd-radius-8 table-hover w-100" id="readonly_schedule"></table>
                            </div>
                        </div>
                        <div class="d-inline-flex justify-content-end bd-radius-8 bg-light p-1 w-100 mb-2 mt-2" style="display:none !important;">
                            <span class="text-secondary mr-2">Schedule pending status</span>
                            <div class="d-inline-flex" id="schedule_status">
                                <!--<div class="d-flex align-items-center mr-2 badge badge-light badge-pill" style="border:1px solid var(--info)">
                                    <img class="sticker mr-1" src="">
                                    <div>
                                        <span class="font-weight-bold">Luis Liao</span>
                                        <i class="fa fa-ellipsis-h text-info"></i>
                                    </div>
                                </div>-->
                            </div>
                        </div>
                        <div id="pend_schedule_div" class="w-100 bd-radius-8 bg-light p-2 mt-2" style="display:none !important;">
                            <h6 class="text-secondary font-weight-bold mr-2">Pend schedule</h6>
                            <P>Review the schedule, and check if the schedule is reasonble. Before submitting, you,as a contact,can discuss your members.</P>
                            <hr>
                            <div class="d-flex justify-content-end">
                                <button class="btn btn-success mr-3 btn-sm approve"><i class="fa fa-check-double mr-1"></i>Agree schedule</button>
                                <button class="btn btn-danger btn-sm return"> <i class="fa fa-reply mr-1"></i>Disagree</button>
                            </div>
                        </div>
        <!--progress-->
                        <div id="progress_area" class="mt-2" style="display:none !important;">
                            <hr>
                            <div class="pt-3 pb-3">
                                <div class="d-flex flex-column flex-sm-row justify-content-sm-between">
                                    <div class="mb-3 mb-sm-0">
                                        <span id="TimelimeTitle" class="h6 font-weight-bold text-secondary"></span>
                                        <span class="text-secondary cursor-pointer" data-toggle="modal" data-target="#TimelineHint">
                                            <i class="far fa-question-circle fa-fw align-text-top"></i>
                                        </span>
                                    </div>
                                    <div>
                                        <div class="btn-group">
                                            <!--<button id="TL-ScrollLeftFast" type="button" class="btn btn-sm btn-outline-secondary" title="Scroll left faster">
                                                <i class="fas fa-angle-double-left fa-fw"></i>
                                            </button>
                                            <button id="TL-ScrollLeft" type="button" class="btn btn-sm btn-outline-secondary" title="Scroll left">
                                                <i class="fas fa-chevron-left fa-fw"></i>
                                            </button>-->
                                            <button id="TL-ZoomOut" type="button" class="btn btn-sm btn-outline-secondary" title="Zoom-out">
                                                <i class="fas fa-search-minus fa-fw"></i>
                                            </button>
                                            <button id="TL-Reset" type="button" class="btn btn-sm btn-outline-secondary" title="Reset to default scale">
                                                <i class="fas fa-undo-alt fa-fw"></i>
                                            </button>
                                            <button id="TL-ZoomIn" type="button" class="btn btn-sm btn-outline-secondary" title="Zoom-in">
                                                <i class="fas fa-search-plus fa-fw"></i>
                                            </button>
                                            <!--<button id="TL-ScrollRight" type="button" class="btn btn-sm btn-outline-secondary" title="Scroll right">
                                                <i class="fas fa-chevron-right fa-fw"></i>
                                            </button>
                                            <button id="TL-ScrollRightFast" type="button" class="btn btn-sm btn-outline-secondary" title="Scroll right faster">
                                                <i class="fas fa-angle-double-right fa-fw"></i>
                                            </button>-->
                                        </div>
                                        <button type="button" class="btn btn-info btn-sm" id="add_milestone"><i class="fa fa-plus"></i> Add milestone</button>
                                    </div>
                                </div>
                                <table id="TL" class="table table-borderless mt-4"></table>
                            </div>
                            <hr>
                            <h6 class="text-secondary font-weight-bold"> Result link </h6>
                            <div class="row align-items-center mt-2">
                                <label class="col-3"> Result </label>
                                <div class="col-9 mb-2">
                                    <div class="input-group">
                                        <input type="text" class="form-control field-style" name="repository_url" id="repository_url" placeholder="http(s)://..." disabled required>
                                        <div class="input-group-append">
                                            <a class="btn btn-light" target="_blank">
                                                <i class="fa fa-link"></i>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="w-100 text-right mt-2" style="display:none;">
                                <button type="button" class="btn btn-info" id="submit_result"><i class="fa fa-paper-plane mr-1"></i>Submit result</button>
                            </div>
                        </div>
<!-- Signature -->
                        <div id="signature_func" style="display:none !important;">
                        <hr>
                            <div id="signature_alert_content">
                                <h5 class="text-center"> -- <i class="fa fa-user-check mr-1"></i> Please review/approve this leave application -- </h5>
                                <hr>
                                <p class="text-dark bd-radius-8 font-weight-bold">
                                    Please review the request form. Remember click the button on bottom of form and leave comments(required field). Once press the button,
                                    The information will record in the comments and process will go on.</br></br>
                                    <h6 class="badge badge-success badge-pill" style="width: 5.5rem;"><i class="fa fa-check-double mr-1"></i> Approve </h6> - You agree the form content totally.This form will be sent to another stage. </br>
                                    <h6 class="badge badge-warning badge-pill" style="width: 5.5rem;"><i class="fa fa-stop mr-1"></i> Close </h6> - You would like to stop this form,and the form will break</br>
                                    <h6 class="badge badge-danger badge-pill" style="width: 5.5rem;"><i class="fa fa-reply mr-1"></i> Return </h6> - There are some fields are wrong or ambiguous. The form will back to last stage.
                                </p>
                                <hr>
                            </div>
                            <h6 class="text-secondary font-weight-bold">Signature</h6>
                            <div class="row align-items-top mt-1">
                                <label class="col-2 text-grey"> Comment </label>
                                <div class="col-10 p-1">
                                    <textarea id="sign_comment" class="w-100 font-weight-bold bd-radius-8 bg-light p-1 bd-none" rows="5" placeholder="Required to leave comments..."></textarea>
                                </div>
                            </div>
                            <div id="assign_dev_func" class="d-flex align-items-baseline" style="display:none !important;">
                                <label class="col-2 text-grey"> Assign developers </label>
                                <div class="col-10">
                                    <button class="btn btn-info" data-toggle="modal" data-target="#developersModal">
                                        <i class="fa fa-users mr-1"></i>Edit
                                    </button>
                                </div>
                            </div>
                            <hr>
                            <div class="w-100 d-inline-flex justify-content-end">
                                <button type="button" class="btn btn-success mr-2" id="ApproveBTN"><i class="fa fa-check-double mr-1"></i> Approve </button>
                                <button type="button" class="btn btn-warning mr-5" id="ReturnBTN"><i class="fa fa-reply mr-1"></i> Return </button>

                                <button type="button" class="btn btn-danger" id="CloseBTN"><i class="fa fa-stop mr-1"></i> Close </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>`;





let ezinfoModal=`<div class="modal fade" id="ezinfoModal" tabindex="-1" role="dialog">
<div class="modal-dialog modal-dialog-centered modal-lg pl-5" role="document">
    <div class="modal-content p-3">
        <div class="modal-body">
            <div class="col-12">
                <div class="d-flex justify-content-between align-items-start">
                    <h5> Form overview </h5>
                    <button type="button" class="close" data-dismiss="modal">
                        <span> &times; </span>
                    </button>
                </div>
                <hr>
                <div class="bg-light bd-radius-8 p-1 d-inline-flex align-items-baseline w-100">
                    <span class="ml-2 mr-2 text-grey"> Assign </span>
                    <div class="font-bold-weight pt-2" id="ez_breadcrumb">
                        <!--<h6 class="badge badge-bluegray badge-pill" title="Initiator"> - </h6> ›
                        <h6 class="badge badge-bluegray badge-pill mr-2" title="Team"> - </h6> ›
                        <h6 class="badge badge-bluegray badge-pill mr-2" title="Account"> - </h6> ›
                        <h6 class="badge badge-bluegray badge-pill mr-2" title="Project"> - </h6> ›
                        <h6 class="badge badge-bluegray badge-pill" title="Receiver"> - </h6>-->
                    </div>
                </div>
                <form class="w-100 py-4 bd-radius-8">
                    <h6 class="text-secondary font-weight-bold"> Basic info </h6>
                    <div class="row align-items-baseline mt-3">
                        <label class="col-3 text-grey"> Status </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold" name="status">Supervisor pending...</span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Form id </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold" name="id"> - </span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Parent form </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold" name="parent"> - </span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Request </label>
                        <div class="pl-2 col-9 bg-light bd-radius-8 p-1">
                            <img class="sticker">
                            <span class="text-secondary font-weight-bold ml-1" name="initiator"> - </span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Assigner </label>
                        <div class="pl-2 col-9 bg-light bd-radius-8 p-1">
                            <img class="sticker">
                            <span class=" text-secondary font-weight-bold ml-1" name="assigner"> - </span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Developers </label>
                        <div class="pl-2 col-9 bg-light bd-radius-8 p-1">
                            <img class="sticker">
                            <span class="text-secondary font-weight-bold mr-3" name="developers"> - <strong>...</strong></span>
                            <button type="button" class="btn btn-outline-secondary btn-sm toggle-dev-list" data-toggle="button">
                                <i class="fa fa-list"></i>
                            </button>
                            <div class="col-12 dev-list" style="display: none;">
                                <ul class="text-grey">
                                    <li class="mt-1"> - </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Signature list </label>
                        <div class="col-9 bg-light bd-radius-8 p-2" name="signature">
                            <!--<div class="mt-1">
                                <div class="d-inline-flex">
                                    <img class="sticker">
                                    <span class="pl-2 text-secondary font-weight-bold ml-1"> Leo tu/WNH/Wistron </span>
                                    <h6 class="badge badge-info badge-pill"> Approve <i class="fa fa-check-double ml-2"></i></h6>
                                </div>
                                <p class="ellipsis w-100 ml-5 bg-grey bd-radius-8"> what comments </p>
                            </div>-->
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Form initialized </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold ml-1" name="form_begin_time"> - </span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Form end </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold ml-1" name="form_end_time"> - </span>
                        </div>
                    </div>
                    <hr>
                    <h6 class="text-secondary font-weight-bold"> Form content </h6>
                    <div class="row align-items-baseline mt-3">
                        <label class="col-3 text-grey"> Title </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold" name="title" style="white-space: pre-wrap;"> - </span>
                        </div>
                    </div>
                    <div class="row align-items-baseline mt-1">
                        <label class="col-3 text-grey"> Description </label>
                        <div class="pl-2 col-9 bg-light bd-radius-8 p-1" name="description" style="white-space: pre-wrap;"> - </div>
                    </div>
                    <div class="row align-items-top mt-1">
                        <label class="col-3 text-grey"> Files </label>
                        <table class="table table-borderless col-9 bg-light bd-radius-8 table-hover" style="overflow:hidden;" name="files">
                            <thead>
                                <tr>
                                    <td> File name </td>
                                    <td> Size </td>
                                    <td> Description </td>
                                    <td class="text-center"> Download </td>
                                    <td> Created </td>
                                </tr>
                            </thead>
                            <tbody></tbody>
                          </table>
                    </div>
                    <div class="row align-items-center mt-1">
                        <label class="col-3 text-grey"> Result </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <a class="pl-2 p-1 font-weight-bold" name="repository_url" target="_blank"></a>
                        </div>
                    </div>
                    <hr>
                    <h6 class="text-secondary font-weight-bold"> Estimated schedule </h6>
                    <div class="row align-items-top mt-3">
                        <label class="col-3 text-grey"> Schedule plan </label>
                        <table class="table table-borderless col-9 bg-light bd-radius-8 table-hover" style="overflow:hidden;" name="schedule">
                            <thead>
                                <tr>
                                    <td>Milestone</td>
                                    <td>Estimated date</td>
                                    <td>Description</td>
                                    <td>Estimated complete rate(%)</td>
                                    <td>Created time</td>
                                </tr>
                            </thead>
                            <tbody></tbody>
                          </table>
                    </div>
                    <div class="row align-items-center mt-1">
                        <label class="col-3 text-grey"> Estimated developing time  </label>
                        <div class="col-9 bg-light bd-radius-8 p-1">
                            <span class="pl-2 text-secondary font-weight-bold" name="develop_time">
                                - <!--20 days (2020-05-06~2020-07-26)-->
                            </span>
                        </div>
                    </div>
                    <hr>
                    <h6 class="text-secondary font-weight-bold"> Devloping status </h6>
                    <div class="row align-items-center mt-3" name="est_rate">
                        <label class="col-3 text-grey"> Estimated complete rate </label>
                        <div class="col-9 p-1 d-inline-flex align-items-baseline">
                            <h6 class="text-grey mr-2" style="white-space: nowrap; width:10%;"> - </h6>
                            <div class="progress w-100 bg-light">
                                <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                    <div class="row align-items-center" name="act_rate">
                        <label class="col-3 text-grey"> Actual complete rate </label>
                        <div class="col-9 p-1 d-inline-flex align-items-baseline">
                            <h6 class="text-grey mr-2" style="white-space: nowrap; width:10%;"> - </h6>
                            <div class="progress w-100 bg-light">
                                <div class="progress-bar bg-success" role="progressbar" style="width: 0%"></div>
                            </div>
                        </div>
                    </div>
                    <div class="row align-items-center mt-2" name="progress_status">
                        <label class="col-3 text-grey"> Progress status </label>
                        <div class="col-9">
                            <h5 class="text-secondary mr-2"> - </h5>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</div>`;



let milestoneModal=`<div class="modal fade" id="milestoneModal" tabindex="-1" role="dialog">
<div class="modal-dialog modal-dialog-centered" role="document">
    <div class="modal-content modal-content-body">
        <div class="d-inline-flex justify-content-between align-items-baseline col-12 p-2">
            <h5 class="text-secondary" id="milestone_modal_title"> Add New milestone </h5>
            <button type="button" class="close" data-dismiss="modal">
                <span> &times; </span>
            </button>
        </div>
        <form id="FormAddMilestone" class="col-12">
            <div class="row align-items-center mt-2 editShow readShow" style="display: none;">
                <label class="col-4">Editor</label>
                <div class="mb-2 pl-3 col-8 d-inline-flex align-items-center">
                    <img class="sticker mr-2" src="../static/images/defaultsticker.png">
                    <span class="text-grey editor "></span>
                </div>
            </div>
            <div class="row align-items-center mt-2 editShow readShow" style="display: none;">
                <label class="col-4">Last Updated time</label>
                <div class="mb-2 pl-3 col-8 d-inline-flex align-items-baseline">
                    <span class="text-grey update_time"></span>
                </div>
            </div>
            <hr>
            <div class="row align-items-center mt-2">
                <label class="col-4"> &#9733 Milestone </label>
                <div class="mb-2 col-8 d-inline-flex align-items-baseline">
                    <input type="text" class="form-control field-style" name="name" placeholder="..." required>
                </div>
            </div>
            <div class="row align-items-top mt-2">
                <label class="col-4"> &#9733 Description </label>
                <div class="mb-2 col-8 d-inline-flex align-items-baseline">
                    <textarea type="text" class="form-control field-style bd-radius-8" name="description" placeholder="..." required></textarea>
                </div>
            </div>
            <div class="row align-items-center mt-2">
                <label class="col-4"> &#9733 Estimated developing period</label>
                <div class="mb-2 col-8 d-inline-flex align-items-baseline">
                    <div class="input-group">
                        <input type="text" class="form-control field-style" name="est_dev_period" id="est_dev_period" placeholder="YYYY-MM-DD - YYYY-MM-DD" required>
                    </div>
                </div>
            </div>
            <div class="row align-items-center mt-2">
                <label class="col-4"> &#9733 Complete rate</label>
                <div class="mb-2 col-8 d-inline-flex align-items-baseline">
                    <div class="input-group">
                        <input type="text" value="0" class="form-control field-style" name="complete_rate" id="progress_complete_rate" style="ime-mode:disabled" onkeyup="return ValidateNumber($(this),value)" placeholder="0~100" required>
                        <div class="input-group-append">
                            <button class="btn btn-light font-weight-bold" type="button"> % </button>
                        </div>
                    </div>
                </div>
            </div>
            <small class="text-secondary d-flex justify-content-end mb-2">
                ★ is required field. Need to fill out before requesting.
            </small>
            <hr>
            <div class="mb-2 d-flex justify-content-between">
                <div class="d-flex justify-content-start">
                    <button type="button" class="btn btn-danger editShow" id="delProgress" style="display: none;">
                        <i class="fa fa-trash-alt mr-2"></i>Delete
                    </button>
                </div>

                <div class="d-flex justify-content-end">
                    <button type="button" class="btn btn-info" id="addProgress">
                        <i class="fa fa-plus mr-2"></i>Add new milestone
                    </button>
                    <button type="button" class="btn btn-info ml-2 editShow" id="updateProgress" style="display: none;">
                        <i class="fa fa-check-double mr-2"></i>Save
                    </button>
                </div>
            </div>
        </form>
    </div>
</div>
</div>`
