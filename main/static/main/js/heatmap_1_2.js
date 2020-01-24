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
    $('#heatmap_filter').on('change', function() {
        var option = $(this).children("option:selected")[0].id;
        if (option == 'day') {
            $('#day_div').css('display', '');
            $('#period_div').css('display', 'none');
            $('#month_div').css('display', 'none');

        } 
        else if (option == 'period') {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', '');
            $('#month_div').css('display', 'none');
        } 
        else if (option == 'month') {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', 'none');
            $('#month_div').css('display', '');
        }
        else {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', 'none');
            $('#month_div').css('display', 'none');
        }
    })
});

function get_date() {
    id = $("#heatmap_filter option:selected")[0].id;
    data = {'status': ''}
    if (id == 'day') {
        data.status = "day";
        data.date = $('#one_day')[0].value;
    }
    else if (id == 'period') {
        data.status = "period";
        data.start = $('#start_date')[0].value;
        data.end = $('#end_date')[0].value;
    } 
    else if (id == 'month') {
        data.status = "month";
        data.month = $('#one_month')[0].value;
    }
    else {
        data.status = "all";
    }
    return data;
}

$(document).on('click', '#get_heatmap_button', function() {
    result = get_date();
    $.ajax({
        type: 'POST',
        url: '/get_heatmap/', 
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
            data: JSON.stringify(result)
        },
        success: function(data) {
            $('#heatmap_img').html('<img src="/media/heatmap/heatmap_' + data.start + '_' + data.end + '.png">');
        }
    });
})