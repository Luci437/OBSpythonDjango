$('#community-form').on('submit', function (e) {
    e.preventDefault();

    let commessage = $('.community-input').val();

    if(commessage === '') {
        $('.community-error-message').css('opacity','1');
    }else {
        $('.community-error-message').css('opacity', '0');

        $.ajax({
            url: 'getchat/',
            type: 'post',
            data: {
                'message': commessage
            },
            success: function (data) {
                let totalmessages = data['totalchat'];
                let totalusers = data['totaluser'];


                $('#discussion-box').children().remove();
                $('.community-input').val('');
                let userid = 0;
                let username = '';
                let dt = '';

                for (let i = 0; i < totalmessages; i++) {

                    userid = data['chats'][i][1];
                    for (let j = 0; j < totalusers; j++) {
                        if (data['users'][j][0] === userid) {
                            username = data['users'][j][2];
                        }
                    }

                    $('#discussion-box').append('<div class="com-message-box"><h4 class="com-username">' + username + '</h4><h5 class="actual-com-message">' + data['chats'][i][2] + '</h5><h6 class="comm-message-tim">&#128337; ' + data['chats'][i][3] + '</h6></div>')
                }
                var chatlist = document.getElementById('discussion-box');
                chatlist.scrollTop = chatlist.scrollHeight;
            }
        });
    }
});

$(document).on('ready', function () {
    $('.community-message-box').hide();
});

$('.close-community').on('click', function () {
    $('.community-message-box').hide();
});
$('.community-btn').on('click', function () {
    $('.community-message-box').show();
});

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});