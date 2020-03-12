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
function get_date_nps(){
    $('#nps_button').attr("disabled", true);
    $('#nps_button').append('<span id="spiner" class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true" style="margin-left: 8px;"></span>');
    $.ajax({
        type: 'POST',
        url: '/get_date_nps/', 
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
           
        },
        success: function(data) {
            start = data.start;
            end = data.end;

            var settings = {
                "url": "https://app.te-ex.ru/Perekrestok/api/nps?last_modified=" + start + "&last_modified_to=" + end + "",
                "method": "GET",
                "timeout": 0,
                "headers": {
                  "Authorization": "Basic cHJrbnBzMjpmZDNUZHM="
                },
              };
              
              $.ajax(settings).done(function (response) {
                $.ajax({
                    type: 'POST',
                    url: '/nps/', 
                    data: {
                        csrfmiddlewaretoken: getCookie('tcx_token'),
                        nps_records: JSON.stringify(response)
                    },
                    success: function(data) {
                        if (data) {
                            $('#nps_button').attr('disabled', false);
                            $('#spiner').remove();
                            $('#nps_button').html(data.output);
                            $('#nps_button').attr('class', 'btn btn-success');
                        }
                    }

                })
              });
        }
    });
}

  
$(document).ready(function() {
    $(document).on('click', '#nps_button', function(){
        get_date_nps();
    })
})