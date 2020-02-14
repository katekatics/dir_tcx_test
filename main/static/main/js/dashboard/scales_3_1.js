function scale() {
    // Весы
    $.post("/store/" + full_sap + "/scales/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if (data.scales) {
                var scales = '<div class="' + data.theme + '" id="scales_theme" tabindex="0" data-toggle="collapse" data-target="#scales" aria-expanded="true" aria-controls="scales">';
                scales += '<div class="row"><div class="col-2"><h6 class=" mb-0"><i class="fas fa-balance-scale pt-1"></i> Весы (' + data.scales.length + ')</h6></div>';
                scales += '<div class="col-4"><small class="float-left" id="scales_footer_msg"></small></div>';
                scales += '<div class="col-6"><small class="float-right" id="scales_footer_time" data-toggle="tooltip"';
                scales += 'data-placement="right" data-original-title="Время последнего обновления блока"></small></div>';
                // scales += '<div class="col-1"><div class="spinner-border spinner-border-sm mb-0 float-right" role="status"></div>';
                scales += '</div></div></div>';
                scales += '<div id="scales" class="collapse show" aria-labelledby="headingscales">';
                scales += '<div class="card-body-p0 bg-light"><div class="row">';
                $.each(data.scales, function (index, scale) {
                    scales += '<div class="col-xl-3 col-lg-6 col-md-12">';
                    scales += '<div class="' + scale.theme + '" text-white my-1 ">';
                    if (scale.theme != "card bg-success text-white my-1") {
                        scales += '<div class="card-body-block" tabindex="0" data-toggle="tooltip" data-placement="top" data-html="true" ';
                        if (scale.theme == "card bg-dark text-white my-1") {
                            scales += 'title="Весы не в сети">';
                        } else if (scale.theme == "card bg-warning text-white my-1") {
                            scales += 'title="Прогрузка больше 6 часов назад">';
                        } else if (scale.theme == "card bg-danger text-white my-1") {
                            scales += 'title="Прогрузка больше 12 часов назад">';
                        }
                    } else {
                        scales += '<div class="card-body-block" tabindex="0">';
                    }
                    scales += '<p class="text-center mb-0">' + scale.name + '</p></div></div></div>';
                })
                scales += '</div></div></div>';
                $("#scales_card").html(scales);
                $("#scales_footer_time").html(data.date);
            }
            block_errors("scales", data)
            $(".tooltip").tooltip("hide");
            $('[data-toggle="tooltip"]').tooltip()
        }
    );
}