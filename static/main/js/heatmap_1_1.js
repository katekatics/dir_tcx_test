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

$(document).ready(function () {
    $('#filter').on('change', function() {
        var option = $(this).children("option:selected")[0].id;
        if (option == 'day') {
            $('#day_div').css('display', '');
            $('#period_div').css('display', 'none');
        } 
        else if (option == 'period') {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', '');
        } 
    })

});