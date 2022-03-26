window.onscroll = function() {
    checkNavbar();
}
  
function checkNavbar() {
    if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        document.getElementById("navbar").style.boxShadow = "0px 4px 6px 0px rgba(0,0,0,0.49)";
        document.getElementById("navbar").style.mozBoxShadow = "0px 4px 6px 0px rgba(0,0,0,0.49)";
        document.getElementById("navbar").style.webkitBoxShadow = "0px 4px 6px 0px rgba(0,0,0,0.49)";
    } else {
        document.getElementById("navbar").style.boxShadow = "none";
        document.getElementById("navbar").style.mozBoxShadow = "none";
        document.getElementById("navbar").style.webkitBoxShadow = "none";
    }
}

function gotoDiv(div) {
    document.getElementById(div).scrollIntoView();
}

function getResources(clicked, name) {
    for(let i = 0; i < document.getElementsByClassName("c-rlt-button").length; i++) {
        document.getElementsByClassName("c-rlt-button")[i].classList.remove("c-r-selected");
    }

    clicked.classList.add("c-r-selected");
    document.getElementById("resourcesheader").innerText = clicked.innerText + " Resources";

    document.getElementById("resourcesbody").innerHTML = "Loading...";
    
    //connect to resource api with name as query and parse output
    //then add resources
}

function showQuizScores() {
    document.getElementById("showquizbtn").classList.add("c-sc-selected");
    document.getElementById("showcompbtn").classList.remove("c-sc-selected");

    document.getElementById("quizscoresarea").style.display = "block";
    document.getElementById("compscoresarea").style.display = "none";
}

function showCompScores() {
    document.getElementById("showcompbtn").classList.add("c-sc-selected");
    document.getElementById("showquizbtn").classList.remove("c-sc-selected");

    document.getElementById("quizscoresarea").style.display = "none";
    document.getElementById("compscoresarea").style.display = "block";
}
