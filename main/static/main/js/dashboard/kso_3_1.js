function kso() {
    // КСО
    $.post("/store/" + full_sap + "/kso/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if ("kso" in data){
                if (data.kso.length != 0) {
                    var kso = '<div class="' + data.theme + '" id="kso_theme" tabindex="0" data-toggle="collapse" data-target="#kso" aria-expanded="true" aria-controls="kso">';
                    kso += '<div class="row"><div class="col-2"><h6 class=" mb-0"><i class="fas fa-cash-register pt-1"></i> КСО (' + data.kso.length + ')</h6></div>';            
                    kso += '<div class="col-4"><small class="float-left" id="kso_footer_msg"></small></div>';
                    kso += '<div class="col-6"><small class="float-right" id="kso_footer_time" data-toggle="tooltip"';
                    kso += 'data-placement="right" data-original-title="Время последнего обновления блока"></small></div>';
                    kso += '</div></div></div>';
                    kso += '<div id="kso" class="collapse show" aria-labelledby="headingkso">';
                    kso += '<div class="card-body-p0 bg-light"><div class="row">';
                    $.each(data.kso, function (index, k) {
                        kso += '<div class="col-xl-2 col-lg-3">';
                        kso += '<div class="' + k.theme + '" tabindex="0" data-toggle="popover" data-placement="top" data-html="true" data-content="' + k.popover + '">';
                        kso += '<div class="card-body-p0" tabindex="0">';
                        kso += '<p class="text-center mb-0">' + k.name + ' </p></div></div></div>';
                    })
                    kso += '</div></div></div>';
                    $("#kso_card").html(kso);
                    $("#kso_footer_time").html(data.date);
                }
                else {
                    $("#kso_card").html('');
                    $("#kso_card").attr('class', 'card');
                }
            }
            else {
                $('#kso_card').remove();
            }
            block_errors("kso", data)
            $(".popover").popover("hide");
            $('[data-toggle="popover"]').popover()
        }
    );
}



