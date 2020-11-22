$('.ticketbuy').on('click',function () {
    let tiid = $("input[name='ticketavailable']:checked").val();
    $.ajax({

        url: '',
        method: 'POST',
        type: 'Json',
        data : {
            tiid:tiid
        }
    });
    $('#'+ tiid +'').fadeOut(1000).delay(1000).remove();
    if($('.ticket-li').length === 0) {
        $('h4').show();
    }
    console.log($('.ticket-li').length);
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
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