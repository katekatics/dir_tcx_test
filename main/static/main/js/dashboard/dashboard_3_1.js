$(document).ready(function () {
    sap_name();
    data();
    setInterval('data()', 180000);
    $('#open_close_business')[0].textContent = 'Свернуть';
    $('#open_close_products')[0].textContent = 'Свернуть';
    $('#sap').html('Бизнес показатели ' + ((window.location.pathname).split('-')[2]).slice(0, 4));
    $('#rto_traffic_check_theme')[0].clildNodes;
});

function sap_name() {
    $.post("/store/" + full_sap + "/sap_name/", { csrfmiddlewaretoken: getCookie('tcx_token') },
    function (data) {
        $('#sap_name').html(data);
    }
    )
}

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


function create_report_modal(body, head, block_name) {
    if (body.length > 0) {
        $("#" + block_name + "_body").attr('class', "card-body click_detect");
        $("#" + block_name + "_body").attr('data-target', "#" + block_name + "_modal");
        var table = '<table id="' + block_name + '_table" class="table table-striped table-bordered" cellspacing="0" width="100%"><thead><tr>';
        for (var i = 0; i < head.length; i++) {
            table += '<th>';
            table += head[i];
            table += '</th>';
        }
        table += '</tr></thead><tbody>';
        for (var i = 0; i < body.length; i++) {
            table += '<tr>';
            var line = body[i];
            for (var j = 0; j < line.length; j++) {
                table += '<td>';
                table += line[j];
                table += '</td>';
            }
            table += '</tr>';
        }
        table += '</tbody></table>';
        $("#" + block_name + "_modal_body").html(table);
        $("#" + block_name + "_table").DataTable();
        $('.dataTables_length').addClass('bs-select');
    }
}

function range_revenue(min, max, step) {
    lst = [];
    for (var i = min; i <= max;) {
        lst.push(i);
        i += step;        
    }
    return lst;
}

function create_revenue_report_modal(body, head, block_name, colors) {
    if (body.length > 0) {
        $("#" + block_name + "_body").attr('class', "card-body click_detect");
        $("#" + block_name + "_body").attr('data-target', "#" + block_name + "_modal");
        var table = '<table id="' + block_name + '_table" class="table table-striped table-bordered" cellspacing="0" width="100%"><thead><tr>';
        for (var i = 0; i < head.length; i++) {
            table += '<th>';
            table += head[i];
            table += '</th>';
        }
        table += '</tr></thead><tbody>';
        for (var i = 0; i < body.length; i++) {
            table += '<tr>';
            var line = body[i];
            for (var j = 0; j < line.length; j++) {
                for (k of range_revenue(1, line.length, 4)) {
                    if (j == k) {
                        table += '<td class="' + colors[i] + '">';
                    }
                    else {
                        table += '<td>';
                    }
                }
                
                table += line[j];
                table += '</td>';
            }
            table += '</tr>';
        }
        table += '</tbody></table>';
        $("#" + block_name + "_modal_body").html(table);
        $("#" + block_name + "_table").DataTable();
        $('.dataTables_length').addClass('bs-select');
    }

}

function block_errors(block, data) {
    var render = '';
    var delim = '';
    if (data.errors) {
        $.each(data.errors, function (index, error) {
            render += delim + error + " error";
            delim = "<br>";
        })
    }
    $("#" + block + "_footer_msg").html(render);
}

$(document).on("click", ".click_detect", function () {
    var action = $(this).attr('id');
    $.get("/click_detect/" + full_sap + "/" + action + "/")
})

var n = 0;
$(document).on("click", "#headingBusiness", function () {
    n += 1;
    res = n%2;
    if (res == 0) {
        $('#open_close_business')[0].textContent = 'Свернуть';
    }
    else {
        $('#open_close_business')[0].textContent = 'Развернуть';
    }
    
})

var k = 0;
$(document).on("click", "#headingProducts", function () {
    k += 1;
    res =k%2;
    if (res == 0) {
        $('#open_close_products')[0].textContent = 'Свернуть';
    }
    else {
        $('#open_close_products')[0].textContent = 'Развернуть';
    }
    
})

function data() {
    // Кассы
    pos();
    scale();
    kso();
    get_date_nps();

    // Бизнес
    business_revenue_new();
    business_rto();
    business_average_check();
    business_canceled_checks();
    nps_from_mongo();
    business_write_offs();
    business_sellers_perfom();
    business_open_documents();
    business_markdown();
    business_checks_traffic();
    business_old_price();


    products_overdue();
    products_low_saled();
    products_stoped_food();
    products_stoped_fresh();
    products_minus();
    products_top30();
    products_super_price();
    products_topvd();

    services_loyalty();
    services_cashless();
    services_net();
    services_alcohol();
}
