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
    $('#kpi_filter').on('change', function() {
        var option = $(this).children("option:selected")[0].id;
        if (option == 'day') {
            $('#day_div').css('display', '');
            $('#period_div').css('display', 'none');
            $('#month_div').css('display', 'none');

        } 
        else if (option == 'period') {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', '');
            $('#week_div').css('display', 'none');
            $('#month_div').css('display', 'none');

        } 
        else if (option == 'month') {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', 'none');
            $('#week_div').css('display', 'none');
            $('#month_div').css('display', '');
        }
        
        else if (option == 'week') {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', 'none');
            $('#month_div').css('display', 'none');
            $('#week_div').css('display', '');
        }
        else {
            $('#day_div').css('display', 'none');
            $('#period_div').css('display', 'none');
            $('#month_div').css('display', 'none');
            $('#week_div').css('display', 'none');
        }
    })
});

function get_date() {
    id = $("#kpi_filter option:selected")[0].id;
    data = {'status': ''}
    // if (id == 'day') {
    //     data.status = "day";
    //     data.date = $('#one_day')[0].value;
    // }
    if (id == 'period') {
        data.status = "period";
        data.start = $('#start_date')[0].value;
        data.end = $('#end_date')[0].value;
    } 
    else if (id == 'month') {
        data.status = "month";
        data.month = $('#one_month')[0].value;
    }
    else if (id == 'week') {
        data.status = "week";
        data.week = $('#one_week')[0].value;
    }
    else {
        data.status = "all";
    }
    return data;
}


$(document).on('click', '#get_kpi_button', function() {
    result = get_date();
    $('#get_kpi_button').attr("disabled", true);
    $('#get_kpi_button').append('<span id="spiner" class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true" style="margin-left: 8px;"></span>');
    $.ajax({
        type: 'POST',
        url: '/get_kpi_graph/', 
        data: {
            csrfmiddlewaretoken: getCookie('tcx_token'),
            data: JSON.stringify(result)
        },
        success: function(data) {
            $('#excel_active').attr('class', 'btn btn-dark text-white');
            $('#excel_active').attr('class', 'btn btn-dark text-white');
            if (data.text) {
                alert(data.text)
            } 
            else {
                
                $('#get_kpi_button').attr("disabled", false);
                $('#spiner').remove(); 
                $('#kpi_img').html('<img src="/media/kpi/kpi_' + data.start + '_' + data.end + '.png" style="width: 110%" class="mx-3">');
                $('#excel_all').attr('href', '/media/report_all_' + data.start + '_' + data.end + '.xlsx');
                $('#excel_all').attr('class', 'btn btn-success');
                $('#excel_active').attr('href', '/media/report_active_' + data.start + '_' + data.end + '.xlsx');
                $('#excel_active').attr('class', 'btn btn-success');
                $('#excel_kpi').attr('href', '/media/kpi_report_' + data.start + '_' + data.end + '.xlsx');
                $('#excel_kpi').attr('class', 'btn btn-success');
        }    
        }
    });
})

$(document).on('click', '#kpi_filter', function() {
    $('#excel_all').attr('class', 'btn btn-dark text-white');
    $('#excel_all').attr('href', '#');
    $('#excel_active').attr('class', 'btn btn-dark text-white');
    $('#excel_active').attr('href', '#');
    $('#excel_kpi').attr('class', 'btn btn-dark text-white');
    $('#excel_kpi').attr('href', '#');
})

$(document).on('click', '[id$="div"]', function() {
    $('#excel_all').attr('class', 'btn btn-dark text-white');
    $('#excel_all').attr('href', '#');
    $('#excel_active').attr('class', 'btn btn-dark text-white');
    $('#excel_active').attr('href', '#');
    $('#excel_kpi').attr('class', 'btn btn-dark text-white');
    $('#excel_kpi').attr('href', '#');
})