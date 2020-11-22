let el1 = document.getElementsByClassName('game-container');
let el2 = document.getElementsByClassName('tube');
let el3 = document.getElementsByClassName('correctanswer')
let el4 = document.getElementsByClassName('answers');
let el5 = document.getElementsByClassName('timer');
let op1 = document.getElementsByClassName('op1');
let op2 = document.getElementsByClassName('op2');
let op3 = document.getElementsByClassName('op3');
let op4 = document.getElementsByClassName('op4');
let totalqst = el1.length;
let currentqst = 0;
let timr;
let lives = 3;
let gameover = false;

let startval = 30;

function starttimer() {
    startval = 30;
    playtimer();
}

function playtimer() {
    timr = setInterval(function () {
        if(startval === 0) {
            lives--;
            if ( lives === 0) {
                gameover = true;
            }
            clearInterval(timr);
            changequestion();
        }else {
            startval--;
            el5[currentqst - 1].innerHTML = startval;
        }
    },1000)
}

function getanswerfromyou(youranswer) {
    let ans = el3[currentqst - 1].value;
    if(youranswer === ans) {
        el2[currentqst - 1].style.background = 'green';
    }else {
        lives--;
        if ( lives === 0) {
            gameover = true;
        }
        el2[currentqst - 1].style.background = 'red';

        if(op1[currentqst - 1].innerHTML === ans) {
            op1[currentqst - 1].style.background = 'linear-gradient(to top,#9cff7a,#54ff55)';
            op1[currentqst - 1].style.boxShadow = '-2px -2px 5px #54ff55 inset, 5px 5px 10px #38c34d inset, 0 20px 10px rgba(0,0,0,0.1)';
            op1[currentqst - 1].style.color = '#333';
        }else if(op2[currentqst - 1].innerHTML === ans) {
            op2[currentqst - 1].style.background = 'linear-gradient(to top,#9cff7a,#54ff55)';
            op2[currentqst - 1].style.boxShadow = '-2px -2px 5px #54ff55 inset, 5px 5px 10px #38c34d inset, 0 20px 10px rgba(0,0,0,0.1)';
            op2[currentqst - 1].style.color = '#333';
        }else if(op3[currentqst - 1].innerHTML === ans) {
            op3[currentqst - 1].style.background = 'linear-gradient(to top,#9cff7a,#54ff55)';
            op3[currentqst - 1].style.boxShadow = '-2px -2px 5px #54ff55 inset, 5px 5px 10px #38c34d inset, 0 20px 10px rgba(0,0,0,0.1)';
            op3[currentqst - 1].style.color = '#333';
        }else if(op4[currentqst - 1].innerHTML === ans) {
            op4[currentqst - 1].style.background = 'linear-gradient(to top,#9cff7a,#54ff55)';
            op4[currentqst - 1].style.boxShadow = '-2px -2px 5px #54ff55 inset, 5px 5px 10px #38c34d inset, 0 20px 10px rgba(0,0,0,0.1)';
            op4[currentqst - 1].style.color = '#333';
        }

    }
    setTimeout(function () {
        clearInterval(timr);
        changequestion();
    },2000)
}


changequestion();
function changequestion() {
    
    if(gameover === false) {
        for(let i=0; i<totalqst; i++) {
            el1[i].style.display = 'none';
        }
    
        el1[currentqst].style.display = 'block';
        currentqst++;
        starttimer();
    
        if(currentqst === totalqst + 1){
            alert("All question are over over");
        }     
    }else {
        $('.game-container').fadeOut(1000).hide();
        playanima();

    }

}


function playanima() {
var animation = bodymovin.loadAnimation({
  container: document.getElementById('anima'),
  renderer: 'svg',
  loop: false,
  autoplay: true,
  path: '/static/javascript/data.json'
})
}
