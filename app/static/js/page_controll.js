var prevHeight = 0;
var prevWidth = 0;

var currentHeight;
var currentWidth;
var currentHeight = window.innerHeight;
var currentWidth = window.innerWidth;

var menu_button = document.getElementById("menu-button");
var nav_bar = document.getElementById("nav-bar");
var menu_li = document.getElementsByClassName("menu-li");

var mainbod = document.getElementById("mainbod");

function ShowLoop(loopject, sty=true) {
    var dispsty = (sty) ? '' : 'block';
   for (var i = 0; i < loopject.length; i++)
       loopject[i].style.display = dispsty;
}
function HideLoop(loopject) {
    for (var i = 0; i < loopject.length; i++)
       loopject[i].style.display = 'none';
 }
function OpenM() {
    menu_button.textContent = "🞬";
    nav_bar.style.height = "100vh";
    ShowLoop(menu_li, sty=false);
    mainbod.style.display = 'none'
}
function CloseM(hide=true) {
    menu_button.textContent = "☰";
    nav_bar.style.height = "";
    (hide === true) ? HideLoop(menu_li) : ShowLoop(menu_li);
    mainbod.style.display = ''
}

OpenCloseMenu = function(){
    if(menu_button.textContent == "☰"){
        OpenM();
    } else {
        CloseM();
    }
};

function resized() {

    // ApplyTopPadding();
    // prevHeight = currentHeight;
    // prevWidth = currentWidth;
    // currentHeight = $(window).height();
    // currentWidth = $(window).width();

    // if (currentWidth > 800){
    //     // console.log("A")
    //     $(".nav-bar").height(""); // unoverflow page
    //     $(".menu-li").show();
    //     $("#menu-button").text("🞬");
    // } else if (currentWidth <= 800 ) { // && prevWidth > 800
    //     // console.log("B")

    //     $(".menu-li").hide();
    //     $(".nav-bar").height(""); // unoverflow page
    //     $("#menu-button").text("☰");

    // }

    CloseM(hide=false);

}

function ApplyTopPadding(){

    tienda_nav = document.getElementById("tienda-nav");
    tienda_nav_height = tienda_nav.offsetHeight;
  
    document.getElementById("mainbod").style.paddingTop = tienda_nav_height + "px";
    console.log(tienda_nav_height);
  }
  
  

// EVENT LISTENERS

// https://gomakethings.com/how-to-convert-the-jquery-click-method-to-vanilla-js/
menu_button.addEventListener('click', OpenCloseMenu);
window.addEventListener('resize', resized);



function fn() {
    console.log('fn cat');
}

function ready() {
    if (document.readyState != 'loading') {
        // do something?;
    } else {
        // document.addEventListener('DOMContentLoaded', console.log("works"));
        document.addEventListener('DOMContentLoaded', fn());
    }
}


ready();






