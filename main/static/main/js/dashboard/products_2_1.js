function products_overdue() {
    // Товары без движения
    $.post("/store/" + full_sap + "/products_overdue/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_overdue_theme").attr('class', data.theme);                
                $("#products_overdue_body_text").html(data.body_text);
                $("#products_overdue_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_overdue');
                $("#products_overdue_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("products_overdue", data);
        }
    );
}


function products_low_saled() {
    // Товары с низкими продажами
    $.post("/store/" + full_sap + "/products_low_saled/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_low_saled_theme").attr('class', data.theme);
                $("#products_low_saled_body_text").html(data.body_text);
                $("#products_low_saled_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_low_saled');
                $("#products_low_saled_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("products_low_saled", data);
        }
    );
}


function products_stoped_food() {
    // Товары без движения FOOD
    $.post("/store/" + full_sap + "/products_stoped_food/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_stoped_food_theme").attr('class', data.theme);
                $("#products_stoped_food_body_text").html(data.body_text);
                $("#products_stoped_food_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_stoped_food');
                $("#products_stoped_food_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
                
            }
            block_errors("products_stoped_food", data);
        }
    );
}

function products_stoped_fresh() {
    // Товары без движения FRESH
    $.post("/store/" + full_sap + "/products_stoped_fresh/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_stoped_fresh_theme").attr('class', data.theme);
                $("#products_stoped_fresh_body_text").html(data.body_text);
                $("#products_stoped_fresh_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_stoped_fresh');
                $("#products_stoped_fresh_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("products_stoped_fresh", data);
        }
    );
}

function products_minus() {
    // Товары с отрицательными остатками
    $.post("/store/" + full_sap + "/products_minus/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_minus_theme").attr('class', data.theme);
                $("#products_minus_body_text").html(data.body_text);
                $("#products_minus_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_minus');
                $("#products_minus_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("products_minus", data);
        }
    );
}

function products_top30() {
    // Топ 30
    $.post("/store/" + full_sap + "/products_top30/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_top30_theme").attr('class', data.theme);
                $("#products_top30_body_text").html(data.body_text);
                $("#products_top30_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_top30');
                $("#products_top30_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("products_top30", data);
        }
    );
}

function products_topvd() {
    // Топ ВД
    $.post("/store/" + full_sap + "/products_topvd/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#products_topvd_theme").attr('class', data.theme);
                $("#products_topvd_body_text").html(data.body_text);
                $("#products_topvd_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'products_topvd');
                $("#products_topvd_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
                
            }
            block_errors("products_topvd", data);
        }
    );
}