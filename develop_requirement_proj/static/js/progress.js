//  Progress table param setting
const timelineConfig = {
    title: 'Dev Progress',
    defaultScale: '100%',
    height: 25, // px
    reduceAnimation: true,

    showCalendar: true,
    showTodayMark: true,
    showScheduleMark: true,
    
    scaleStep: '50%',
    scalerMin: 1,
    scalerMax: 5,
    currentTransform:0,

    scrollStep: 200, // px
    scrollStepFaster: 500, // px

    adaptiveLang: true,
};

function render_progress_schedule(progress_json,
                                    scheduleStart=$('#requestModal').data('schedule')['start'],
                                    scheduleEnd=$('#requestModal').data('schedule')['end']){
    $('#TL').empty();
    $('#TL').html(`<thead><tr></tr></thead><tbody></tbody>`);
    // Title
    $('#TimelimeTitle').text(timelineConfig.title);
        // Find min and max date of schedules
        let dates = [];
        
        if(scheduleStart==undefined||scheduleEnd==undefined){ console.log('WRONG SCHEDULE'); }


        dates.push(new Date(scheduleEnd));
        dates.push(new Date(scheduleStart));

        $.each(progress_json, function(){
            let row=$(this)[0]
            let Start=row['start_time']
            let End=row['end_time']
            dates.push(new Date(Start));
            dates.push(new Date(End));
        });
        let allScheduleStart = new Date(Math.min.apply(null, dates));
        let allScheduleEnd = new Date(Math.max.apply(null, dates));
        let allScheduleDuration = new Date(allScheduleEnd - allScheduleStart)/86400000 + 1;



        // Find min and max date of calendar
        let yearStart = allScheduleStart.getFullYear();
        let yearEnd = allScheduleEnd.getFullYear();
        let monthStart = allScheduleStart.getMonth() + 1;
        let monthEnd = allScheduleEnd.getMonth() + 1;

        function twoDigit(x) {
            x = x.toString();
            return x.length < 2 ? '0' + x : x;
        }
        function monthStartDate(year, month) {
            return year + '-' + twoDigit(month) + '-01';
        }
        function monthEndDate(year, month) {
            month = twoDigit(month);
            date = new Date(year, month, 0).getDate();
            return year + '-' + month + '-' + twoDigit(date);
        }

        let duration = new Date(new Date(monthEndDate(yearEnd, monthEnd)) - new Date(monthStartDate(yearStart, monthStart)))/86400000 + 1;

        // Make calendar bar
        if (timelineConfig.showCalendar) {
            let thead_html=`<tr><th class="align-baseline text-left"><i class="far fa-calendar-alt fa-lg"></i></th>
                                <th class="pl-2 pb-2""><h6>Editor</h6></th>
                                <th class="pl-2 pb-2""><h6>Milestone</h6></th>
                                <!--<th class="pl-2 pb-2""><h6>Description</h6></th>-->
                                <th class="pl-2 pb-2""><h6>Complete</h6></th>
                                <th class="w-100 px-0 pb-3">
                                    <div class="timeline-frame border border-grey rounded-lg" style="overflow-x: hidden;">
                                        <div id="TL-Calendar" class="timeline position-relative progress bg-transparent" style="width: ` + 
                                            timelineConfig.defaultScale + `; height: ` + timelineConfig.height + `px;">
                                        </div>
                                    </div></th>
                                </tr>`;
            $('#TL>thead').append(thead_html);

            let lastBarWidth = 0;
            for (y = yearStart; y <= yearEnd; y++) {
                for (m = (y == yearStart ? monthStart : 1); m <= (y == yearEnd ? monthEnd : 12); m++) {
                    let barStart = lastBarWidth;
                    let barWidth = new Date(y, m, 0).getDate() / duration * 100;
                    if (y == yearEnd && m == monthEnd) barWidth += 0.01; // Fix width of last month
                    lastBarWidth += barWidth;
                    let barColor = m%2 ? '#FEFEFE' : '#EEEEEE';
                    $('#TL-Calendar').append(
                        '<div class="position-absolute progress-bar h-100 calendar" title="' + monthStartDate(y, m) + ' ~ ' + monthEndDate(y, m) + '"' +
                        'style="width: 0; margin-left: 0; background-color: ' + barColor + '; z-index: 99;">' + 
                        ((m == 1 || m == 12) ? y + ' ' + monthNames[m-1].substring(0, 3) : monthNames[m-1]) + '</div>'
                    );
                    $('#TL-Calendar .calendar').last().data('width', barWidth + '%').data('margin-left', barStart + '%');
                }
            }
        }

        // Make timeline for individual function team
        $.each(progress_json, function(){
            let row=$(this)[0]
            let phase_index = 0;
            // let TL_ID = row['order'].replace(/ /g, '_');
            let TL_ID = row['order'];

            // let phaseStart = new Date(row['sta']);
            // let phaseEnd = new Date(Dates.End);
            let Start=new Date(row['start_time']);
            let End=new Date(row['end_time']);
            let today=new Date();
            let complete_percent=Number(row['complete_rate'])/100;
            let rowDuration = new Date(End - Start)/86400000 + 1;

            let barStart = new Date(Start - new Date(yearStart, monthStart-1, 1))/86400000/duration*100;
            let barWidth = rowDuration/duration*100;
            let completeWidth = Math.round(barWidth*complete_percent);
            let estimated_completeWidth;
            let estimated_completetRate;

            let schedule_start=new Date(scheduleStart);
            let schedule_end=new Date(scheduleEnd);
            let schedule_barStart = Math.round((schedule_start - new Date(yearStart, monthStart-1, 1))/86400000/duration*100);
            let schedule_barEnd = Math.round((schedule_end - new Date(yearStart, monthStart-1, 1))/86400000/duration*100);
            let schedule_width=Math.round(schedule_barEnd-schedule_barStart);
            let scheduleStart_date=scheduleStart.split('T')[0];
            let scheduleEnd_date=scheduleEnd.split('T')[0];
            let Start_date=row['start_time'].split('T')[0];
            let End_date=row['end_time'].split('T')[0];

            if(End.getTime() < today.getTime()){
                estimated_completeWidth=barWidth;
                estimated_completetRate=100;
            }else{ 
                // estimated_completeWidth=(new Date(today-Start)/new Date(new Date(monthEndDate(yearEnd, monthEnd)) - new Date(monthStartDate(yearStart, monthStart))))*100
                estimated_completeWidth=(today - new Date(yearStart, monthStart-1, 1))/86400000/duration*100-barStart;
                estimated_completetRate=Math.round(new Date(today-Start)/new Date(End - Start)*100)-Number(row['complete_rate']);

            }

            if (End.getTime() == allScheduleEnd.getTime()) barWidth += 0.01; // Fix width of last phase
            let barIndex = parseInt(100 - barWidth); // Shoter bar get higher z-index
            let row_html;
            if (rowDuration == 1) {
                row_html=` <tr><td class="align-middle pl-0">
                                <button class="btn bg-white text-info p-1 px-2 read_progress" type="bytton">
                                    <i class="fa fa-ellipsis-h"></i>
                                </button>
                                <button class="btn bg-white text-info p-1 mr-2 px-1 update_progress" type="bytton">
                                    <i class="fa fa-fw fa-pencil-alt mr-1"></i>
                                </button>
                                <button class="btn bg-white text-danger p-1 px-2 del_progress" type="bytton">
                                    <i class="fa fa-trash-alt"></i>
                                </button>
                            </td>
                            <td><img class="sticker" src="" data-employee_id="`+row['editor']['employee_id']+`" title="`+row['editor']['display_name']+`"></td>
                            <td><span class="text-secondary">`+row['name']+`</span></td>
                            <td><span class="text-secondary">`+row['complete_rate']+` %</span></td>
                            <td class="w-100 px-0">
                                <div class="timeline-frame border rounded-lg" style="overflow-x: hidden;">
                                    <div id="TL-` + TL_ID + `" class="timeline position-relative progress bg-secondary" 
                                        style="width:`+timelineConfig.defaultScale +`; height:` +timelineConfig.height+ `px;">
                                        <div class="position-absolute progress-bar h-100 milestone bg-transparent px-2" 
                                            data-width="`+barWidth+`%" data-margin-left="`+barStart+`%"
                                            style="width:0; margin-left:0; z-index: `+barIndex+`;">
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>`;
                        
            }else{
                // Phase
                let barRandomColor = 'rgba(' + 
                    Math.floor(Math.random()*180 + 50) + ',' + 
                    Math.floor(Math.random()*180 + 50) + ',' + 
                    Math.floor(Math.random()*180 + 50) + ', .5)';
                let scheduleObj={
                    "devloping_schedule":scheduleStart_date+" ~ "+scheduleEnd_date,
                    "milestone_period":Start_date+" ~ "+End_date,
                    "estimated_complete rate":estimated_completetRate,
                    "current_complete_rate":row['complete_rate']
                }
                row['schedule']=scheduleObj
                let description=' - ';
                if(row['description']==''||row['description']==null){}
                else description=row['description'];
                row_html=` <tr id="progress_`+row['id']+`" data-row=\'`+JSON.stringify(row)+`'\'>
                            <td data-field="id" data-value='`+row['id']+`' class="d-flex align-items-center text-nowrap pl-0">
                                <button class="btn bg-white text-info p-1 px-2 read_progress" type="bytton">
                                    <i class="fa fa-ellipsis-h"></i>
                                </button>
                                <button class="btn bg-white text-info p-1 px-1 mr-2 update_progress" type="bytton">
                                    <i class="fa fa-fw fa-pencil-alt mr-1"></i>
                                </button>
                                <button class="btn bg-white text-danger p-1 px-2 del_progress" type="bytton">
                                    <i class="fa fa-trash-alt"></i>
                                </button>
                            </td>
                            <td><img class="sticker" src="`+images['defaultavatar']+`" data-employee_id="`+row['editor']['employee_id']+`" title="`+row['editor']['display_name']+`/Update `+isotime_local(row['update_time'])+`"></td>
                            <td class="pt-2 ellipsis" data-field="name" data-value='`+row['name']+`'><span class="text-secondary">`+row['name']+`</span></td>
                            <!--<td data-field="description" data-value='`+row['description']+`'><p class="text-secondary">`+description+`</p></td>-->
                            <td class="pt-2" data-field="complete_rate" data-value='`+row['complete_rate']+`'><span class="text-secondary">`+row['complete_rate']+` %</span></td>
                            <td data-field="schedule" data-value=\'`+JSON.stringify(scheduleObj)+`'\' class="w-100 px-0">
                                <div class="timeline-frame rounded-lg pt-2" style="overflow-x: hidden;">
                                    <div id="TL-`+ TL_ID +`" class="timeline position-relative progress bg-light"
                                        style="width:`+timelineConfig.defaultScale +`; height:` +timelineConfig.height+ `px;">
                                        <div class="position-absolute progress-bar h-100 phase pt-1"
                                            data-width="`+schedule_width+`%" data-margin-left="`+schedule_barStart+`%"
                                            style="width: 0; margin-left: 0; background-color:rgba(0, 0, 0, 0.08); z-index:`+ barIndex +`;"
                                            title="Devloping schedule: `+scheduleStart_date+` ~ `+scheduleEnd_date+`">
                                        </div>
                                        <div class="position-absolute progress-bar h-100 phase"
                                            data-width="`+barWidth+`%" data-margin-left="`+barStart+`%"
                                            style="width: 0; margin-left: 0; background-color:var(--secondary); z-index:`+ barIndex +`;"
                                            title="Milestone period: `+Start_date+` ~ `+End_date+`">
                                        </div>
                                        <div class="position-absolute progress-bar h-100 phase"
                                            data-width="`+estimated_completeWidth+`%" data-margin-left="`+barStart+`%"
                                            style="width: 0; margin-left: 0; background-color:var(--danger); z-index:`+ barIndex +`;"
                                            title="Estimated complete rate: `+estimated_completetRate+`">
                                            <!-- <span>`+estimated_completetRate+` %</span>-->
                                        </div>
                                        <div class="position-absolute progress-bar h-100 phase"
                                            data-width="`+completeWidth+`%" data-margin-left="`+barStart+`%"
                                            style="width: 0; margin-left: 0; background-color:var(--success); z-index:`+ barIndex +`;"
                                            title="Current complete rate: `+row['complete_rate']+` %">
                                            <span>`+row['complete_rate']+` %</span>
                                        </div>
                                    </div>
                                </div>
                            </td>
                            </tr>`;
            }
            $('#TL>tbody').append(row_html);
            $('#TL .sticker').each(function(){
                target=$(this)                
                avatar_reload(target);
            })
        });
        function timeline_mark(time,markname){
            if (time >= new Date(yearStart, monthStart-1, 1) && time <= new Date(yearEnd, monthEnd-1, 0)) {
                let barStart = Math.round((time - new Date(yearStart, monthStart-1, 1))/86400000/duration*100);
                let barWidth = 1/duration*100;
                $('.timeline').append(
                    `<div class="position-absolute progress-bar h-100 timemark `+markname+` bg-transparent"
                            style="width: 0; margin-left: 0; z-index: 99;">
                    </div>`
                );
                $('.timeline .'+markname+'').data('width', barWidth+'%').data('margin-left', barStart+'%');
                $('.timeline .'+markname+'').tooltip({
                    html: true,
                    title: '<small>'+markname+'</small><br>' + 
                        time.getFullYear() + '-' + twoDigit(time.getMonth()+1) + '-' + twoDigit(time.getDate()) +
                        ' (' + dayNames[time.getDay()] + ')',
                    boundary: 'window'
                });
            }
        }
        // Make today mark
        if (timelineConfig.showTodayMark) {
            let today = new Date();
            timeline_mark(today,'todayline');
        }
        if (timelineConfig.showScheduleMark) {
            let schedule_start=new Date(scheduleStart);
            let schedule_end=new Date(scheduleEnd);
            timeline_mark(schedule_start,'Dev_start');
            timeline_mark(schedule_end,'Dev_end');
        }

    // Animate timeline
        $('#TL').find('.calendar, .phase, .milestone,.timemark').each(function() {
            if (timelineConfig.reduceAnimation) {
                $(this).css('margin-left', $(this).data('margin-left'));
            } else {
                $(this).animate({
                    'margin-left': $(this).data('margin-left')
                }, 'slow');
            }
            $(this).css('width', $(this).data('width'));
        });

    // Hover on phase will show border
        $('.phase').on('mouseenter', function() {
            $(this).addClass('phase-hovered');
        }).on('mouseleave', function() {
            $(this).removeClass('phase-hovered');
        });

    // Deal with tooltips of phase & milestone
        $('.phase, .milestone').on('mouseenter mouseup', function() {
            let barMiddleOffset = $(this).offset().left + $(this).width()/2;
            let frameOffset = $(this).closest('.timeline-frame').offset().left;
            let frameWidth = $(this).closest('.timeline-frame').width();
            if (barMiddleOffset > frameOffset && barMiddleOffset < frameOffset + frameWidth) {
                if ($(this).data('tooltip-shown') !== true) $(this).data('tooltip-shown', true).tooltip('show');
            }
        }).on('mouseleave', function() {
            if ($(this).data('tooltip-shown') !== false) $(this).data('tooltip-shown', false).tooltip('hide');
        });

        $('.phase, .milestone').on('mousemove', function() {
            if (curDown) {
                let barMiddleOffset = $(this).offset().left + $(this).width()/2;
                let frameOffset = $(this).closest('.timeline-frame').offset().left;
                let frameWidth = $(this).closest('.timeline-frame').width();
                if (barMiddleOffset > frameOffset && barMiddleOffset < frameOffset + frameWidth) {
                    if ($(this).data('tooltip-shown') !== true) $(this).data('tooltip-shown', true).tooltip('show');
                } else {
                    if ($(this).data('tooltip-shown') !== false) $(this).data('tooltip-shown', false).tooltip('hide');
                }
            }
        });

    // Drag to scroll timeline
        let curDown = false;
        let curXPos = 0;
        let lastXPos = 0;
        $(window).mousemove(function (e) {
            if (curDown) $('.timeline-frame').scrollLeft(lastXPos + curXPos - e.pageX);
        });
        $(document).on('mousedown','#TL tbody td:last-child',function (e) {
            e.preventDefault();
            curDown = true;
            curXPos = e.pageX;
            if(timelineConfig.currentTransform!==0)$(this).css('cursor', 'grabbing');
            else $(this).css('cursor', 'default');				
        });
        $(window).mouseup(function (e) {
            curDown = false;
            lastXPos = $('.timeline-frame').first().scrollLeft();
        });

    // Timeline Zoom-out
        $(document).on('click','#TL-ZoomOut', function () {
            let innerWidth = $('.timeline').first().width();
            let outerWidth = $('.timeline-frame').first().width();
            if ($('.timeline').queue().length == 0 && innerWidth > outerWidth * timelineConfig.scalerMin) {
                $('.timeline').animate({width: '-=' + timelineConfig.scaleStep}, {
                    start: function() {$('.timeline-frame').scrollLeft(lastXPos);}
                });
                timelineConfig.currentTransform--;
                if(timelineConfig.currentTransform==0) $('#TL tbody td:last-child').css('cursor', 'default');
            }
        });
    // Timeline Zoom-in
        $('#TL-ZoomIn').on('click', function () {
            let innerWidth = $('.timeline').first().width();
            let outerWidth = $('.timeline-frame').first().width();
            if ($('.timeline').queue().length == 0 && innerWidth <= outerWidth * timelineConfig.scalerMax) {
                $('.timeline').animate({width: '+=' + timelineConfig.scaleStep}, {
                    start: function() {$('.timeline-frame').scrollLeft(lastXPos);}
                });
                timelineConfig.currentTransform++;
                if(timelineConfig.currentTransform==0) $('#TL tbody td:last-child').css('cursor', 'default');
            }
        });
    // Timeline Zoom Back to default scale
        $('#TL-Reset').on('click', function () {
            if ($('.timeline').queue().length == 0) {
                $('.timeline').animate({width: timelineConfig.defaultScale}, {
                    start: function() {$('.timeline-frame').scrollLeft(lastXPos);}
                });
                timelineConfig.currentTransform=0;
                $('#TL tbody td:last-child').css('cursor', 'default');
            }
        });

    // Buttons to scroll timeline
        $(document).on('click','#TL-ScrollLeft', function () {
            if ($('.timeline-frame').queue().length == 0) {
                $('.timeline-frame').animate({scrollLeft: lastXPos -= timelineConfig.scrollStep}, 'normal');
            }
        });
        $(document).on('click','#TL-ScrollLeftFast', function () {
            if ($('.timeline-frame').queue().length == 0) {
                $('.timeline-frame').animate({scrollLeft: lastXPos -= timelineConfig.scrollStepFaster}, 'slow');
            }
        });
        $(document).on('click','#TL-ScrollRight', function () {
            if ($('.timeline-frame').queue().length == 0) {
                $('.timeline-frame').animate({scrollLeft: lastXPos += timelineConfig.scrollStep}, 'normal');
            }
        });
        $(document).on('click','#TL-ScrollRightFast', function () {
            if ($('.timeline-frame').queue().length == 0) {
                $('.timeline-frame').animate({scrollLeft: lastXPos += timelineConfig.scrollStepFaster}, 'slow');
            }
        });
}

function fillin_milestone(rowdata){
    $('#FormAddMilestone').find('[name]').each(function(){
        let key=$(this).prop('name');
        if(rowdata[key]!==undefined){ $(this).val(rowdata[key]);}
        if(key=='est_dev_period'){
            let start=rowdata['start_time'].split('T')[0];
            let end=rowdata['end_time'].split('T')[0];
            let value=start+' ~ '+end;
            $(this).val(value);
        }

    });
    let target=$('#FormAddMilestone').find('img.sticker');
    target.data('employee_id',rowdata['editor']['employee_id']);
    $('#FormAddMilestone').find('.editor').html(rowdata['editor']['display_name']);
    $('#FormAddMilestone').find('.update_time').html(isotime_local(rowdata['update_time']));
}

// Languages for date
const userLang = navigator.language || navigator.userLanguage;
let monthNames = ['Ja', 'Fe', 'Mr', 'Ap', 'My', 'Jn', 'Jl', 'Au', 'Se', 'Oc', 'Nv', 'De'];
let dayNames = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];

let scheduleStart='2019-05-20T08:26:38.093183Z';
let scheduleEnd='2020-08-20T08:26:38.093183Z';

progress_json=get_progress();

$(function(){
    // render_progress_schedule(progress_json,scheduleStart,scheduleEnd);
    //	Add Milestone
        $(document).on('click','#add_milestone',function(){
            $('#FormAddMilestone').data('id','New');
            //	Show button
            $('#milestoneModal .editShow').fadeOut(0);
            $('#addProgress').fadeIn(0);

            $('#milestone_modal_title').text('Add new milestone');
            //	Reset the modal value
            $('#FormAddMilestone').find('input,textarea').each(function(){
                $(this).val('');
            });	
            // $('.daterangepicker').find('.cancelBtn').trigger('click');
            // $('#est_dev_period').trigger('cancel.daterangepicker');
            $('#milestoneModal').modal('show');
        });
    
    
    //	Init Daterangepicker
        $('#est_dev_period').daterangepicker({
            applyButtonClasses:'btn btn-info',
            cancelButtonClasses:'btn btn-warning',
            autoUpdateInput: false,
            locale: {
                cancelLabel: 'Clear',
                format: 'YYYY-MM-DD '
            }
        });
        $('#est_dev_period').on('apply.daterangepicker', function(ev, picker) {
            $(this).val(picker.startDate.format('YYYY-MM-DD') + ' - ' + picker.endDate.format('YYYY-MM-DD'));   
            $('#est_dev_period').valid();
            $(this).trigger('change');
        });
        $('#est_dev_period').on('cancel.daterangepicker', function(ev, picker) {
            $(this).val('');
        });

        $(document).on('click','#addProgress,.update_progress,.read_progress',function (){
            $('body').append(milestoneModal);
            $('#milestoneModal').on('hidden.bs.modal',function(){
                $(this).remove();
            });
        });
        
    //	Click add milestone button
        $('#addProgress').on('click',function(){
            if($('#FormAddMilestone').validate().form()){
                $('#milestoneModal .editShow').fadeOut(0);
                let formdata=package_data('#FormAddMilestone');
                let start_time=new Date(formdata['est_dev_period'].split(' - ')[0]).toISOString();
                let end_time=new Date(formdata['est_dev_period'].split(' - ')[1]).toISOString();
                let order_id=$('#requestModal').data('order_id');
                let ROWS;
                formdata['start_time']=start_time;
                formdata['end_time']=end_time;
              
                formdata['order']=order_id;
                delete formdata['est_dev_period'];
                $.when(post_progress(formdata)).then(
                    ROWS=get_progress(order_id)
                );
                render_progress_schedule(ROWS);

                $('#milestoneModal').modal('hide');
            }
            $('#FormAddMilestone').find('input textarea').prop('disabled',false);
        });
        $('#delProgress').on('click',function(){
            let id=$('#FormAddMilestone').data('id');
            delete_progress(id);
            $('#milestoneModal').modal('hide');
            $('#progress_'+id).fadeOut(300,function(){
                $(this).remove();
            });
        });
    //	Update milestone button
        $(document).on('click','.update_progress',function (){
            let row=$(this).parents('tr').data('row');
            fillin_milestone(row);
            //	Show button 
            $('#milestoneModal .editShow').fadeIn(0);
            $('#addProgress').fadeOut(0);

            $('#FormAddMilestone').data('id',row['id']);
            $('#FormAddMilestone').find('input textarea').prop('disabled',false);

            $('#milestone_modal_title').text('Edit milestone');
            avatar_reload($('#milestoneModal').find('.sticker'));
            $('#milestoneModal').modal('show');
        });
    //	Update milestone button
        $(document).on('click','.read_progress',function (){
            let row=$(this).parents('tr').data('row');
            fillin_milestone(row);
            //	Show button 
            $('#milestoneModal .editShow').not('.readShow').fadeOut(0);
            $('#milestoneModal .readShow').fadeIn(0);
            $('#addProgress').fadeOut(0);

            $('#FormAddMilestone').data('id',row['id']);
            $('#FormAddMilestone').find('input,textarea').prop('disabled',true);

            $('#milestone_modal_title').text('Milestone detail');
            avatar_reload($('#milestoneModal').find('.sticker'));
            $('#milestoneModal').modal('show');
        });
        //  存下變更過的值
        let patch_progress_field=[];
        $('#FormAddMilestone').find('input,textarea').on('change',function(){
            let target=$(this).prop('name');
  
            if(patch_progress_field.includes(target)==false)patch_progress_field.push(target);
        });
        $(document).on('click','#updateProgress',function (){
            if($('#FormAddMilestone').validate().form()){
                let formdata={}
                let id=$('#FormAddMilestone').data('id');
                let order_id=$('#requestModal').data('order_id');
                let ROWS;
                $.each(patch_progress_field,function(i,key){
                    let value=$('#FormAddMilestone').find('[name='+key+']').val()
                    if(key=='est_dev_period'){
                        let start_time=new Date(value.split(' - ')[0]).toISOString();
                        let end_time=new Date(value.split(' - ')[1]).toISOString();
                        formdata['start_time']=start_time;
                        formdata['end_time']=end_time;
                    }else formdata[key]=value;
                });
                patch_progress_field=[];
                $.when(patch_progress(id,formdata)).then(ROWS=get_progress(order_id));
                render_progress_schedule(ROWS);
                $('#milestoneModal').modal('hide');
            }
        });
    //	Delete milestone button		
        $(document).on('click','.del_progress',function (){
            $('#FormAddMilestone').removeData('id');
            let id=$(this).parents('tr').data('row')['id'];
            delete_progress(id);
            $(this).parents('tr').fadeOut(300,function(){
                $(this).remove();
            });	
        });
    
        $('#milestoneModal').on('hide.bs.modal',function(){
            $('#FormAddMilestone').find('input,textarea').removeClass('border-danger');
        });


});