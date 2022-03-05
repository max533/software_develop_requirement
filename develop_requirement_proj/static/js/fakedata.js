//  Random date
    function randomDate(){
        var startDate = new Date(2012,0,1).getTime();
        var endDate = new Date(2021,0,1).getTime();
        var spaces = (endDate - startDate);
        var timestamp = Math.round(Math.random() * spaces);
        timestamp += startDate;
        return new Date(timestamp);
    }
    function formatDate(date){
        var month = randomDate().getMonth();
        var day = randomDate().getDate();
        if (month==0) month=1;
        month = month <10? '0' + month : month;
        day = day <10? '0' + day : day;
        return String(date.getFullYear()) +'-'+ month +'-'+ day;
    }
    function randomnum(start,end){
        let num = '';
        num = Math.floor((Math.random() * end) + start);
        return num;
    }
//  function end


//  fakedata
//  loginInfo
    // profile = {
    //     '10712714': {
    //         'dept':'ESQ200',
    //         'role':'Member',
    //         'project':{
    //             '11':'leader',
    //             '12':'member',
    //         },
    //         'domain': null,
    //         'avatar': '/static/images/minion.gif',
    //         'display_name': 'Leo Tu/WHQ/Wistron',
    //     },
    // };
    fakedata_path='/static/js/fakedata/' // 測試完請刪除

//  table data start
    data =[];

    let row = [];
    let title = [
        'New system develop about development requirement.',
        'Smartesting tool apply on the new website.',
        'Automatically test the sofware and update reqularly.'
        ];

    let name = [
        'Peter Hsien','Leo Tu','Jeff SH Wang','Steven CW Chen','Luis Liao',
        'Kevin SJ Huang','Bella Pan',
    ];

    let record = [
        'Initialize the request to TSC.',
        'Accept the request and assign Leo Tu as developer(contact window).',
        'Reject the request becaue <The description is too rough, and workoad is too heavy>.',
        'Complete the result.',
        'Reject the result because <the result is not fit the spec>.',
        'Cancel the request because the schedule can not arrive the same point.'
    ]
    let editor = [
        {'display_name':'Leo Tu/WHQ/Wistron','avatar':images['defaultavatar']},
        {'display_name':'Jeff SH Wang/WHQ/Wistron','avatar':images['defaultavatar']},
        {'display_name':'Peter Hsien/WHQ/Wistron','avatar':images['defaultavatar']},
    ]
    let teams = ['QT','EE','SW','TSC']
    let ids = ['9505005','10602719','9909200','10609704','10903703','10903704','10811707'];
    let html1 = '<h1><img src="https://s1.thcdn.com/productimg/1600/1600/11489653-1374492597223451.jpg" style="width: 25%; float: left;" class="note-float-left"><b>s<span style="background-color: rgb(255, 255, 0);">as</span>asa</b></h1><h4><b>a</b>adasdasd</h4>';
    let html2 = 'Consequat mauris nunc congue nisi vitae suscipit tellus. Pretium nibh ipsum consequat nisl vel pretium lectus quam id. Porttitor rhoncus dolor purus non enim praesent. Egestas fringilla phasellus faucibus scelerisque eleifend donec pretium. Eget lorem dolor sed viverra ipsum. Faucibus ornare suspendisse sed nisi lacus sed viverra. Dui accumsan sit amet nulla facilisi. Egestas egestas fringilla phasellus faucibus.';
    let descriptions =[html1,html2];

    let accounts=["Astro","Apollo","Irma","Cindy","Sami","L.E.A.D."]

    let projects=["Rack Grantly VR","Bamboo","Durant(5180M5)"];

    let repository_urls=['','https://www.google.com/'];

//TODO datakey will change
    let pdf =['','xx.pdf'];
    let xml =['','xx.xml'];
    let doc =['','xx.doc'];
    if(true){
        for( i=1; i<=50; i++ ){
            let dataObj = {};
            let namenum_1 = randomnum(0,8);
            let namenum_2 = randomnum(0,8);
            let titlenum = randomnum(0,3);

            dataObj['id']=i;
            dataObj['account'] = {"id":randomnum(0,10) ,"code":accounts[randomnum(0,6)]};
            dataObj['project'] = {"id":randomnum(0,50) ,"code":projects[randomnum(0,3)]};
            dataObj['develop_team_function'] = teams[titlenum];
            dataObj['develop_team_sub_function'] = 'DQMS';
            dataObj['status'] = {"p3_initiator_": "Approve"};
            dataObj['initiator'] = {"employee_id":ids[randomnum(0,7)] ,"display_name":name[namenum_1]+"/WNH/Wistron","extension": "85014815","job_title": "工程師"};
            dataObj['assigner'] = {"employee_id":ids[randomnum(0,7)] ,"display_name":name[namenum_2]+"/WNH/Wistron","extension": "85014815","job_title": "工程師"};
            dataObj['developers'] = {
                "mebmer":[
                    {"employee_id":ids[randomnum(0,7)] ,"display_name":name[namenum_2]+"/WNH/Wistron","extension": "85014815","job_title": "工程師"},
                    {"employee_id":ids[randomnum(0,7)] ,"display_name":name[namenum_2]+"/WNH/Wistron","extension": "85014815","job_title": "技術顧問"},
                    {"employee_id":ids[randomnum(0,7)] ,"display_name":name[namenum_2]+"/WNH/Wistron","extension": "85014815","job_title": "經理"}
                ],
                "contactor":{"employee_id":ids[randomnum(0,7)] ,"display_name":name[namenum_2]+"/WNH/Wistron","extension": "85014815","job_title": "工程師"}
            };
            dataObj['title'] = title[titlenum];
            dataObj['description'] = descriptions[randomnum(0,2)];
            dataObj['form_begin_time'] = randomDate().toISOString();
            dataObj['form_end_time'] = randomDate().toISOString();
            dataObj['expected_develop_duration_day'] = 10.5;
            dataObj['actual_develop_duration_day'] = 20.0;
            dataObj['repository_url'] = repository_urls[randomnum(0,2)];
            dataObj['parent']=(i*3)+7;


            data.push(dataObj);

            // dataObj['exp_date'] = formatDate(randomDate());
            // dataObj['initial_time'] = formatDate(randomDate())+" 下午00:00";
            // dataObj['initiator'] = name[namenum_1];
            // dataObj['assigner'] = name[namenum_2];
            // dataObj['last_modified'] = formatDate(randomDate())+" 下午00:00";
            // dataObj['last_modified'] = randomDate().toISOString();
            // dataObj['last_record'] = record[recordnum];
            // dataObj['last_editor'] = editor[titlenum];
            // dataObj['exp_date'] = randomDate().toISOString();
            // let file_1 = randomnum(0,2);
            // let file_2 = randomnum(0,2);
            // let file_3 = randomnum(0,2);
            // let file_4 = randomnum(0,2);
            // let file_5 = randomnum(0,2);
            // let recordnum = randomnum(0,6);
            // dataObj['file'] = {'mindmap':pdf[file_1],'process_flow':pdf[file_2],'feature_list':xml[file_3],'look&feel':pdf[file_4],'others':doc[file_5],};
        }
    }

//  table data end
