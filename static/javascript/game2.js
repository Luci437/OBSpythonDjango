let usertotal = 0;
let computertotal = 0;
let whoisbatting = 'user';
let firsthalf = false;
let gameover = false;
let userwin = false;
let wincoin = 0;

function fullscreenagain() {
var elem = document.getElementById("bbdy");
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) { /* Firefox */
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari & Opera */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE/Edge */
    elem.msRequestFullscreen();
  }
}

function startups() {
    fullscreenagain();
    //$('.start1').fadeOut().hide();
    //$('.game-container').fadeIn().show();
    $('.toss-box-container').hide();
    $('.welcome-box').fadeOut().hide();
    $('.game-container').fadeIn().hide();
    setTimeout(function () {
        $('.start1').fadeOut().hide();
        $('.game-container').fadeIn().show();
        $('.welcome-box').fadeIn(100).show();
    },10000);
}

$(document).ready(function () {
    document.documentElement.webkitRequestFullscreen();
    $('.all-buttons').hide();
    $('.actual-game-container').hide();
    $('.result-main-box').hide();
    $('#out-img').hide();
    $('.nonstrikers').hide();
});

$('.toss-button').on('click', function () {
    $('.welcome-box').fadeOut().hide();
    let ranval = Math.floor(Math.random() * 2);
    let finalresult = '';

    let userval = $(this).val();

    if(ranval === 0) {
        finalresult = 'H';
    }else {
        finalresult = 'T';
    }

    if(userval === finalresult) {
        whoisbatting = 'user';
        $('#toss-result-text').html("You won the toss, and elected to bat.");
    }else {
        whoisbatting = 'computer';
        $('#toss-result-text').html("Computer won the toss and started to bat.");
    }

    $('#toss-result').html(finalresult);
    $('.toss-box-container').fadeIn().show();

    setTimeout(function () {
        $('.toss-box-container').fadeOut().hide();
        $('.all-buttons').fadeIn(200).show();
        $('.actual-game-container').fadeIn(200).show();
    }, 6000)
});

$('.btns').on('click', function () {

    if(gameover === false) {
        let clickedval = parseInt($(this).val());
        let computerval = Math.floor(Math.random() * 9 + 1);


        //wicket check
        if (computerval === clickedval) {

            if (whoisbatting === 'user') {
                $('#user-values').append('<li style="background: linear-gradient(#ffeb75,#ffcc58);color: #c8a044;padding: 0 12px;">OUT</li>');
                showball(computerval,'c');
            } else {
                $('#computer-values').append('<li style="background: linear-gradient(#ffeb75,#ffcc58);color: #c8a044;padding: 0 12px;">OUT</li>');
                showball(clickedval,'u');
            }

            //second half
            if (firsthalf) {

                if (whoisbatting === 'user') {
                    $('#user-values').append('<li style="padding: 0 45px;background: linear-gradient(#f9a23f,#f95f3c);color: #c34d31;">GAME.OVER</li>');
                    $('#computer-values').append('<li style="padding: 0 11px;background: linear-gradient(#baff94,#5dff77);color: #41ae53;">WIN</li>');
                } else {
                    $('#computer-values').append('<li style="padding: 0 45px;background: linear-gradient(#f9a23f,#f95f3c);color: #c34d31;">GAME.OVER</li>');
                    $('#user-values').append('<li style="padding: 0 11px;background: linear-gradient(#baff94,#5dff77);color: #41ae53;">WIN</li>');
                    userwin = true;
                }
                $('.all-buttons').hide();

                gameover = true;
                gamefinish();


            } else {
                firsthalf = true;

                if (whoisbatting === 'user') {
                    whoisbatting = 'computer';
                } else {
                    whoisbatting = 'user';
                }

            }
            setTimeout(function () {
                $('#out-img').hide();
            },2200);
        } else {

            if (whoisbatting === 'user') {
                usertotal += clickedval;
                $('#user-values').append('<li>' + clickedval + '</li>');
                $('#userscore').html(usertotal);
                showball(computerval,'c');


            } else {
                computertotal += computerval;
                $('#computer-values').append('<li>' + computerval + '</li>');
                $('#computerscore').html(computertotal);
                showball(clickedval,'u');
            }

            if(firsthalf) {
                if(whoisbatting === 'user') {
                    if(computertotal < usertotal) {
                        $('#user-values').append('<li style="padding: 0 10px;background: linear-gradient(#baff94,#5dff77);color: #41ae53;">WIN</li>');
                        gameover = true;
                        userwin = true;
                        gamefinish();
                    }
                }else {
                    if(computertotal > usertotal) {
                        $('#computer-values').append('<li style="padding: 0 10px;background: linear-gradient(#baff94,#5dff77);color: #41ae53;">WIN</li>');
                        gameover = true;
                        gamefinish();
                    }
                }
            }

        }
    }
});

function gamefinish() {
    $('.all-buttons').hide();
    if(userwin) {
        if (usertotal > 500) {
            wincoin = 200;
        }else if(usertotal > 200) {
            wincoin = 50;
        }else if(usertotal > 100) {
            wincoin = 20;
        }else if(usertotal > 50) {
            wincoin = 10;
        }
        $('#wincoin').val(wincoin)
        $('#userscored').val(usertotal)
        $('#result-text-h2').html("YOU WIN");
    }else {
        $('#wincoin').val("0")
        $('#userscored').val("0")
        $('#result-text-h2').html("YOU LOST");
    }
    $('#result-lcoin').html(wincoin);
    setTimeout(function () {
        $('.result-main-box').fadeIn(1000).show();
    },2000)
}

function showball(vals, usr) {
    if(usr === 'u') {
        $('.userstriker').show().fadeIn(1000).html(vals);
    }else {
        $('.computerstriker').show().fadeIn(1000).html(vals);
    }

    setTimeout(function () {
        $('.nonstrikers').fadeOut(1000).hide();
    },1000);

}