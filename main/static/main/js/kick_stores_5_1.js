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
    $('#kick_all_stores').attr("disabled", true);
    $.ajax({
        type: 'POST',
        url: '/kick_stores/', 
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
        },
        success: function(data) {
            if (data.output) {
                setTimeout(function() 
                    {
                        $('#kick_all_stores').attr("disabled", false);
                    }, 1500000);
            }
        }
    });
})

$(document).on('click', '#kick_store', function() {
    $('#kick_store').attr("disabled", true);
    $('#kick_store').append('<span id="spiner" class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true" style="margin-left: 8px;"></span>');
    sap = $('#sap')[0].value;
    if (sap != ''){ 
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
                    alert(data.errors);
                    setTimeout(function() 
                        {
                            $('#kick_store').attr('class', 'btn btn-danger');
                            $('#kick_store').html('Пнуть магазин');
                            $('#kick_store').attr('disabled', false);
                        }, 10000);       
                }
                else {                
                    $('#kick_store').attr('disabled', false);
                    $('#spiner').remove();
                    if (data.output == "Data updated!\n") {
                        $('#kick_store').html('Магазин обновлен!');
                        $('#kick_store').attr('class', 'btn btn-success');
                    }
                    $('#sap')[0].value = '';
                    setTimeout(function() 
                        {
                            $('#kick_store').attr('class', 'btn btn-danger');
                            $('#kick_store').html('Пнуть магазин');
                        }, 10000);          
                }           
            }
        });
    }
})