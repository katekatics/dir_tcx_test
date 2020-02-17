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


$(document).on('click', '#kick_all_stores', function() {
    $.ajax({
        type: 'POST',
        url: '/kick_stores/', 
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
        },
        success: function(data) {  
        }
    });
})

$(document).on('click', '#kick_store', function() {
    $('#kick_store').attr("disabled", true);
    $('#kick_store').append('<span id="spiner" class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true" style="margin-left: 8px;"></span>');
    sap = $('#sap')[0].value;
    $.ajax({
        type: 'POST',
        url: '/kick_store/', 
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
            sap: sap
        },
        success: function(data) {
            if (data.errors) {
                $('#kick_store').html('Магазин не обновлен');
            }
            else {
                $('#kick_store').attr("class", "btn btn-sucess my-2");
                $('#kick_store').attr("disabled", false);
                $('#spiner').remove(); 
                $('#kick_store').html(data);
            }           
        }
    });
})