var majors = [];
var minors = [];

if(localStorage.getItem("aceObj") != null){
    var aces = JSON.parse(localStorage.getItem("aceObj"));
}
else {
    var aces = {
        ace1: [],
        ace2: [],
        ace3: [],
        ace4: [],
        ace5: [],
        ace6: [],
        ace7: [],
        ace8: [],
        ace9: [],
        ace10: []
    }
}


$(document).ready(function () {

    if(localStorage.getItem("schedule") != null){
        $("#years").html(localStorage.getItem("schedule"));
        $("#major-list").html(localStorage.getItem("major"));
        $("#minor-list").html(localStorage.getItem("minor"));
        $("#majorLink").html(localStorage.getItem("majorLink"));
        $("#minorLink").html(localStorage.getItem("minorLink"));
        $("#minor").html(localStorage.getItem("minorSel"));
        $("#major-minor").html(localStorage.getItem("majorSel"));
    }
    else {
        resetPlanner();
    }


    updateAce();

    if(localStorage.getItem("Sel") != null){
        $("#major-minor").html(localStorage.getItem("Sel"));
        majors = JSON.parse(localStorage.getItem("majors"));
        minors = JSON.parse(localStorage.getItem("minors"));
        return;
    }
    $.ajax({
        url: "majors.php",
        dataType: "json",
        type: 'post',
        success: function (response) {
            majors = response;
            var options = "";
            $.each(response, function (k, v) {

                if (k.length > 25) {
                    var str = k.substr(0, 24) + "...";
                }
                else {
                    var str = k;
                }
                options += "<option value='" + k + "'>" + str + "</option>";
            });
            $("#major").append(options);
        },
        error: function (error) {
            console.log(error);
        }
    });

    $.ajax({
        url: "minors.php",
        dataType: "json",
        type: 'post',
        success: function (response) {
            minors = response;
            var minorOptions = "";

            $.each(response, function (k, v) {
                if (k.length > 25) {
                    var str = k.substr(0, 24) + "...";
                }
                else {
                    var str = k;
                }
                minorOptions += "<option value='" + k + "'>" + str + "</option>";
            });
            $("#minor").append(minorOptions);
        },
        error: function (error) {
            console.log(error);
        }
    });

})

function getMajorCourses(value) {

    var arr = [];
    $.each(majors[value].subjects, function (k, v) {
        arr.push(v);
    });
    $("#maLink").remove();
    $("#majorLink").append("<a href='" + majors[value].uri + "' id='maLink' target='_blank'> Major Info </a>");

    arr.sort();

    $.ajax({
        url: "courses.php",
        dataType: "json",
        data: {
            codes: JSON.stringify(arr)
        },
        type: 'post',
        success: function (response) {

            majorCourses = response;
            var list = makeCourseList(response, "major");
            $("#major-list").empty();
            $("#major-list").append(list);

        },
        error: function (error) {
            console.log(error);
        }
    });
    var str = value;
    if (value.length > 25) {
        str = value.substr(0, 24) + "...";
    }
    $("#major option:first").attr('value',value).text(str);
}

function getMinorCourses(value) {

    var arr = [];
    $.each(minors[value].subjects, function (k, v) {
        arr.push(v);
    });

    $("#miLink").remove();
    $("#minorLink").append("<a href='" + minors[value].uri + "' id='miLink' target='_blank'>Minor Info</a>");

    arr.sort();
    $.ajax({
        url: "courses.php",
        dataType: "json",
        data: {
            codes: JSON.stringify(arr)
        },
        type: 'post',
        success: function (response) {
            minorCourses = response;
            var list = makeCourseList(response, "minor");
            $("#minor-list").empty();
            $("#minor-list").append(list);
        },
        error: function (error) {
            console.log(error);
        }
    });
    var str = value;
    if (value.length > 25) {
        str = value.substr(0, 24) + "...";
    }
    $("#minor option:first").attr('value',value).text(str);
}

function getSearchCourses(selectedValue) {

    if(selectedValue === null || selectedValue === ""){
        alert("Search Field Is Empty");
        return;
    }

    if (selectedValue.toUpperCase() == "ALPACA") {
        $("body").html("<img src='alpaca.jpg' height='100%'>");
    }
    var arr = selectedValue.split(" ");

    if (arr.length > 1 && !isNaN(arr[1].substring(0, 1))) {
        arr[1] = arr[1].toUpperCase();

        $.ajax({
            url: "searchCourse.php",
            dataType: "json",
            type: 'post',
            data: {
                search: JSON.stringify(arr)
            },
            success: function (response) {

                otherCourses = response;
                var list = makeCourseList(response, "search");
                $("#other-list").empty();
                $("#other-list").append(list);

            },
            error: function (error) {
                console.log(error);
            }
        });
    }
    else {
        $.ajax({
            url: "search.php",
            dataType: "json",
            type: 'post',
            data: {
                search: selectedValue
            },
            success: function (response) {

                var list = makeCourseList(response, "search");
                $("#other-list").empty();
                $("#other-list").append(list);

            },
            error: function (error) {
                console.log(error);
            }
        });
    }
}

function getCourseInfo(courseElement){
    var courseName1 = courseElement.id;
    var arr = courseName1.split(" ");

    $.ajax({
        url: "searchCourse.php",
        dataType: "json",
        type: 'post',
        data: {
            search: JSON.stringify(arr)
        },
        success: function (response) {
            console.log(response);
            var course = response[0].courseName + " " + response[0].courseNum;
            var title = response[0].title;
            var description = response[0].description;
            var prereqs = response[0].prerequisite;
            var hours = response[0].creditHours;
            var ace1 = response[0].ace1;
            var ace2 = response[0].ace2;
            if(ace2 === "0"){
                var aceStr = ace1;
            }
            if(ace1 === "0"){
                var aceStr = "";
            }
            if(ace1 != 0 && ace2 != 0){
                var aceStr = ace1 + ", " + ace2;
            }
            var str = " <h6>Course:</h6>" + " " + course + "<br>\n" +
                "                <h6>Title: </h6>" + " " + title + "<br>\n" +
                "                <h6>Credit Hours: </h6>" + " " + hours + "<br>\n" +
                "                <h6>ACE: </h6>" + " " + aceStr + "<br>\n" +
                "                <h6>Pre-Requisites: </h6><br>" + prereqs + "<br>\n" +
                "                <h6>Description: </h6><br>" + description + "<br>";

            $('#courseInfo').empty();
            $('#courseInfo').append(str).hide().fadeIn(2500);

        },
        error: function (error) {
            console.log(error);
        }
    });
}

function getAceInfo(courseElement){
    var courseName1 = courseElement.id;
    var arr = courseName1.split(" ");
    arr.splice(0,1);
    courseName1 = arr[0] + " " + arr[1];

    $.ajax({
        url: "searchCourse.php",
        dataType: "json",
        type: 'post',
        data: {
            search: JSON.stringify(arr)
        },
        success: function (response) {

            var ace = [response[0].ace1,response[0].ace2];
            handleAce(ace, courseName1);

        },
        error: function (error) {
            console.log(error);
        }
    });
}

function removeYear() {
    if ($('#years').children().last().children().children().children().length > 0) {
        return;
    }
    $('#years').children().last().fadeOut(1000, function () {
        this.remove();
    });
}

function addYear() {
    var id = $('#years').children().last().attr('id');
    var numYears = $('#years').children().length;

    if (numYears > 5) {
        alert("Max number of years reached!");
        return;
    }
    if (isNaN(id)) {
        id = 2018;
    }
    else {
        id = parseInt(id) + 1;
    }


    var str = " <div class='row' id='" + id + "'>\n" +
        "                    <div class='outer col-md-4'>\n" +
        "                        <h6>Fall " + id + "</h6>\n" +
        "                        <div class='dropBox' ondrop='drop(event)' ondragover='allowDrop(event)'></div>\n" +
        "                    </div>\n" +
        "                    <div class='outer col-md-4'>\n" +
        "                        <h6>Spring " + (id + 1) + "</h6>\n" +
        "                        <div class='dropBox' ondrop='drop(event)' ondragover='allowDrop(event)'></div>\n" +
        "                    </div>\n" +
        "                    <div class='outer col-md-4'>\n" +
        "                        <h6>Summer " + (id + 1) + "</h6>\n" +
        "                        <div class='dropBox' ondrop='drop(event)' ondragover='allowDrop(event)'></div>\n" +
        "                    </div>\n" +
        "                </div>";

    $('#years').append(str);
    $('#' + id).hide().fadeIn(2000);
}


function makeCourseList(response, prefix) {
    var list = "";

    $.each(response, function (k, v) {
        var courseName = v.courseName + " " + v.courseNum;
        list += "<li draggable='true' class='courseList' ondragstart='drag(event)' id='" + prefix + " " + courseName + "' value='"+ courseName +"'>" +
            courseName + "<img draggable='false' id='" + courseName + "' class='info' src='Info.png' " +
            "onclick='getCourseInfo(this)'></li>\n";

    });

    return list;
}

//functions to allow drap and drop functionality on the courses
function allowDrop(ev) {
    ev.preventDefault();
}

function drag(ev) {
    ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
    ev.preventDefault();
    var data = ev.dataTransfer.getData("text");
    var element = document.getElementById(data);

    var courseName = element.getAttribute("value");

    if(ev.target.className === "dropBox"){
        if($(".dropBox").children.length > 5){
            return false;
        }
    }
    if (ev.target.className === "courseList") {
        if(ev.target.parentNode.className != "dropBox"){
            var dragElement = document.getElementById(data);
            ev.target.after(dragElement);
            sortList(ev.target.parentNode.id);

            var course = courseName;
            console.log("Drop course: " + course);
            removeFromAce(course);
        }
        else {
            getAceInfo(element);
        }
    }
    else if(ev.target.className === "drop1" || ev.target.className === "drop2"
            || ev.target.className === "drop3"){

        var dragElement = document.getElementById(data);
        ev.target.append(dragElement);
        sortList(ev.target.id);

        var course = courseName;
        console.log("Drop course: " + course);
        removeFromAce(course);
    }
    else {
        ev.target.appendChild(document.getElementById(data));
        getAceInfo(element);

    }
}

function sortList(id) {
    var list, i, switching, b, shouldSwitch;
    list = document.getElementById(id);
    switching = true;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
        // Start by saying: no switching is done:
        switching = false;
        b = list.getElementsByTagName("li");
        // Loop through all list items:
        for (i = 0; i < (b.length - 1); i++) {
            // Start by saying there should be no switching:
            shouldSwitch = false;
            /* Check if the next item should
            switch place with the current item: */
            if (b[i].innerHTML.toLowerCase() > b[i + 1].innerHTML.toLowerCase()) {
                /* If next item is alphabetically lower than current item,
                mark as a switch and break the loop: */
                shouldSwitch = true;
                break;
            }
        }
        if (shouldSwitch) {
            /* If a switch has been marked, make the switch
            and mark the switch as done: */
            b[i].parentNode.insertBefore(b[i + 1], b[i]);
            switching = true;
        }
    }
}

function updateAce(){

    for(var ace in aces){
        if(aces[ace].length > 0){
            var id = "#" + ace;
            $(id).css("background-color","rgba(39,255,28,0.69)");
        }
        if(aces[ace].length === 0){
            var id = "#" + ace;
            $(id).css("background-color","rgba(255,0,0,.8)");
        }
    }
}

function handleAce(aceOptions, courseName) {
    var aceOne = aceOptions[0];
    var aceTwo = aceOptions[1];

    if(aceOne != 0){
        var param = aces["ace" + aceOne];
        for(var i = 0; i < param.length; i++){
            if(param[i] === courseName){
                return;
            }
        }
        if(aceTwo != 0){
            param = aces["ace" + aceTwo];
            for(var i = 0; i < param.length; i++){
                if(param[i] === courseName){
                    return;
                }
            }
            var choice = prompt("Which Ace should this count towards " + aceOne + " or " + aceTwo).trim();

            while(choice != aceOne && choice != aceTwo){
                choice = prompt("Incorrect input please type either " + aceOne + " or " + aceTwo);
            }
            var aceOne = "ace" + choice;
        }
        else {
            var aceOne = "ace" + aceOne;
        }
        aces[aceOne].push(courseName);
        updateAce();
    }
}

function removeFromAce(course){
    console.log("Remove from ace: " + course);
    for(var ace in aces){
        for(var i = 0; i < aces[ace].length; i++){
            if(aces[ace][i] === course){
                aces[ace].splice(i,1);
                updateAce();
            }
        }
    }
}

function saveSchedule(){
    var schedule = $("#years").html();
    var major = $("#major-list").html();
    var minor = $("#minor-list").html();
    var majlink = $("#majorLink").html();
    var minlink = $("#minorLink").html();
    var majorSel = $("#major-minor").html();

    // Store Content
    localStorage.setItem("aceObj", JSON.stringify(aces));
    localStorage.setItem("schedule", schedule);
    localStorage.setItem("major", major);
    localStorage.setItem("minor", minor);
    localStorage.setItem("majorLink", majlink);
    localStorage.setItem("minorLink", minlink);
    localStorage.setItem("Sel", majorSel);
    localStorage.setItem("majors", JSON.stringify(majors));
    localStorage.setItem("minors", JSON.stringify(minors));
}

function resetPlanner(){
    var string = "<div class=\"row\" id=\"2018\">\n" +
        "<div class=\"outer col-md-4\">\n" +
        "<h6>Fall 2018</h6>\n" +
        "<div class=\"dropBox\" ondrop=\"drop(event)\" ondragover=\"allowDrop(event)\"></div>\n" +
        "</div>\n" +
        "<div class=\"outer col-md-4\">\n" +
        "<h6>Spring 2019</h6>\n" +
        "<div class=\"dropBox\" ondrop=\"drop(event)\" ondragover=\"allowDrop(event)\"></div>\n" +
        "</div>\n" +
        "<div class=\"outer col-md-4\">\n" +
        "<h6>Summer 2019</h6>\n" +
        "<div class=\"dropBox\" ondrop=\"drop(event)\" ondragover=\"allowDrop(event)\"></div>\n" +
        "</div>\n" +
        "</div>";

    $("#years").empty();
    $("#years").append(string);

    aces = {
        ace1: [],
        ace2: [],
        ace3: [],
        ace4: [],
        ace5: [],
        ace6: [],
        ace7: [],
        ace8: [],
        ace9: [],
        ace10: []
    }

    updateAce();
}


function exportPDF(){

    $("#years").css("background-color", "white");
    $("#years").css("width", "1000px");



    var pdf = new jsPDF();
    pdf.internal.scaleFactor = .5;
    var elements = $("#years");


    var i = 0;
    var recursiveAddHtml = function () {
        if (i < elements.length) {
            var x = 0, y = i * 20;
            pdf.addHTML(elements.get(i), x, y, function () {
                i++;
                recursiveAddHtml();
            });
        } else {
            pdf.save("Schedule.pdf");
        }
    }

    recursiveAddHtml();
    $("#years").css("background-color", "");
    $("#years").css("width", "");

}


function searchForAce(aceNum){
    $.ajax({
        url: "aceSearch.php",
        dataType: "json",
        type: 'post',
        data: {
            search: aceNum
        },
        success: function (response) {

            var courseList = makeCourseList(response, "search");
            $("#other-list").empty();
            $("#other-list").append(courseList);

        },
        error: function (error) {
            console.log(error);
        }
    });
}