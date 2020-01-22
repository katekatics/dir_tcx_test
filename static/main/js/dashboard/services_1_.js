function services_loyalty() {
    // Лояльность
    $.post("/store/" + full_sap + "/services_loyalty/", {csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            $("#services_loyalty").attr('class', data.theme);
            $("#services_loyalty").attr('data-original-title', data.tooltip);
        }
    );
}

function services_cashless() {
    // Безналичный расчет
    $.post("/store/" + full_sap + "/services_cashless/", {csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            $("#services_cashless").attr('class', data.theme);
            $("#services_cashless").attr('data-original-title', data.tooltip);
        }
    );
}


function services_net() {
    // Сеть
    $.post("/store/" + full_sap + "/services_net/", {csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            $("#services_net").attr('class', data.theme);
            $("#services_net").attr('data-original-title', data.tooltip);
        }
    );
}

function services_alcohol() {
    // ЕГАИС
    $.post("/store/" + full_sap + "/services_alcohol/", {csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            $("#services_alcohol").attr('class', data.theme);
            $("#services_alcohol").attr('data-original-title', data.tooltip);
        }
    );
}


