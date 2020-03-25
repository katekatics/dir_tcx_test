function business_revenue_new() {
    // Продажи
    $.post("/store/" + full_sap + "/business_revenue_new/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                revenue = (data.body_text).split('|');
                $("#business_revenue_new_theme").attr('class', data.theme);
                $("#business_revenue_new_body_text").html(data.body_text);
                $('#today_revenue').html(revenue[0]);
                $('#lw_revenue').html(revenue[1]);
                $('#ly_revenue').html(revenue[2]);
                $("#business_revenue_new_tooltip").attr('data-original-title', data.tooltip);
                $("#business_revenue_new_footer_time").html(data.date);
                create_revenue_report_modal(data.tbody, data.thead, 'business_revenue_new', data.colors);
                $("#business_revenue_new_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("business_revenue_new", data);
        }

    );
}


function business_rto() {
    //РТО 
    $.post("/store/" + full_sap + "/business_rto/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                text = (data.body_text).split('<br>');
                plan_fact = text[0].split('|');
                plan_fact_percent = text[1].split('|');
                plan_fact_predict = text[2].split('|');
                $("#business_rto_theme").attr('class', data.theme);
                $("#business_rto_body_text").html(data.body_text);
                $("#business_rto_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
                $("#business_bar_footer_time").html(data.date);
                $("#business_rto_footer_time").html(data.date_rto);
                $("#percent_and_saled").html(data.sales_today + ' ₽ (' + data.percent_today_fact + '%) / ' + data.plan_sales_today + ' ₽');
                $("#myBar").css('width', data.percent_today_fact + '%');
                $('#rto_plan').html(plan_fact[0]);
                $('#rto_fact').html(plan_fact[1]);
                $('#rto_plan_percent').html(plan_fact_percent[0]);
                $('#rto_fact_percent').html(plan_fact_percent[1]);
                $('#predict_sum').html(plan_fact_predict[0]);
                $('#predict_percent').html(plan_fact_predict[1]);
                if (data.percent_today_fact>100)
                    {
                        $("#myBar").css('width', 100 + '%');
                    }
                else
                    {
                        $("#myBar").css('width', data.percent_today_fact + '%');
                    }
                
            }
            block_errors("business_rto", data);
        }
    );
}


function business_average_check() {
    // Средний чек

    $.post("/store/" + full_sap + "/business_average_check/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                av_check = (data.body_text).split('|');
                $("#business_average_check_theme").attr('class', data.theme);
                $("#business_average_check_body_text").html(data.body_text);
                $("#today_av_check").html(av_check[0]);
                $("#lw_av_check").html(av_check[1]);
                $("#ly_av_check").html(av_check[2]);
                $("#business_average_check_footer_time").html(data.date);
                $("#business_average_check_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("business_average_check", data);
        }
    );
}


function business_canceled_checks() {
    // Количество аннулированных чеков
    $.post("/store/" + full_sap + "/business_canceled_checks/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#business_canceled_checks_theme").attr('class', data.theme);
                $("#business_canceled_checks_body_text").html(data.body_text);
                $("#business_canceled_checks_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'business_canceled_checks');
                $("#business_canceled_checks_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
                
            }
            block_errors("business_canceled_checks", data);
        }
    );
}



function nps() {
    // Количество аннулированных чеков
    $.post("/store/" + full_sap + "/nps/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#nps_theme").attr('class', data.theme);
                $("#nps_body_text").html(data.body_text);
                $("#nps_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'nps');
                $("#nps_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
                
            }
            block_errors("nps", data);
        }
    );
}


function business_write_offs() {
    // Списания
    $.post("/store/" + full_sap + "/business_write_offs/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#business_write_offs_theme").attr('class', data.theme);
                $("#business_write_offs_body_text_m").html(data.body_text_1);
                $("#business_write_offs_body_text_w").html(data.body_text_2);
                $("#business_write_offs_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'business_write_offs');
                $("#business_write_offs_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("business_write_offs", data);
        }
    );
}

function business_sellers_perfom() {
    // Скорость сканирования кассиров
    $.post("/store/" + full_sap + "/business_sellers_perfom/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#business_sellers_perfom_theme").attr('class', data.theme);
                $("#business_sellers_perfom_body_text").html(data.body_text);
                $("#business_sellers_perfom_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'business_sellers_perfom');
                $("#business_sellers_perfom_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");                
            }
            block_errors("business_sellers_perfom", data);
        }
    );
}


function business_open_documents() {
    // Незакрытые документы приемки
    $.post("/store/" + full_sap + "/business_open_documents/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#business_open_documents_theme").attr('class', data.theme);
                $("#business_open_documents_body_text").html(data.body_text);
                $("#business_open_documents_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'business_open_documents');
                $("#business_open_documents_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body"); 
            }
            block_errors("business_open_documents", data);
        }
    );
}

function business_markdown() {
    // Незакрытые документы приемки АП
    $.post("/store/" + full_sap + "/business_markdown/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#business_markdown_theme").attr('class', data.theme);
                $("#business_markdown_body_text_0").html(data.body_text[0]);
                $("#business_markdown_body_text_1").html(data.body_text[1]);
                $("#business_markdown_body_text_2").html(data.body_text[2]);
                $("#business_markdown_body_text_3").html(data.body_text[3]);
                $("#business_markdown_footer_time").html(data.date);
                $("#business_markdown_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("business_markdown", data);
        }
    );
}

function business_checks_traffic() {
    // Количество аннулированных чеков
    $.post("/store/" + full_sap + "/business_checks_traffic/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                traffic = (data.body_text).split('|');
                $("#business_checks_traffic_theme").attr('class', data.theme);
                $("#business_checks_traffic_body_text").html(data.body_text);
                $('#today_traffic').html(traffic[0]);
                $('#lw_traffic').html(traffic[1]);
                $('#ly_traffic').html(traffic[2]);
                $("#business_checks_traffic_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'business_checks_traffic');
                $("#business_checks_traffic_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("business_checks_traffic", data);
        }
    );
}

function business_old_price() {
    // Количество аннулированных чеков
    $.post("/store/" + full_sap + "/business_old_price/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.theme) {
                $("#business_old_price_theme").attr('class', data.theme);
                $("#business_old_price_body_text").html(data.body_text);
                $("#business_old_price_footer_time").html(data.date);
                create_report_modal(data.tbody, data.thead, 'business_old_price');
                $("#business_old_price_body").attr('class', "card-body click_detect " + ((data.theme).split(' '))[1] + "-body");
            }
            block_errors("business_old_price", data);
        }
    );
}


