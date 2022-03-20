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