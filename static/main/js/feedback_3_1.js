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

function get_feedback(){
    content = $('#feedback_input')[0].value;
    adress = window.location.pathname;
    if (adress.includes('Super')) {
        sap = ((adress.split('Super-')[1]).split('/')[0]).slice(-4);
    } 
    else {
        sap = 'home';
    }
    $.ajax({
        type: 'POST',
        url: '/get_feedback/',
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
            feedback: content,
            sap: sap,
        },
        success: function(data) {
            alert(data.msg);
            if (data.connect){
                $('#feedback_input')[0].value = '';
            }
        }
    })
}

$(document).on("click", "#feedback_send", function () {
    get_feedback();
})
