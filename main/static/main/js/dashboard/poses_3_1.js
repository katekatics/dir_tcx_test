function pos() {
    // Кассы
    $.post("/store/" + full_sap + "/poses/", { csrfmiddlewaretoken: getCookie('tcx_token') },
        function (data) {
            if ("poses" in data) {
                var poses = '<div class="card-header bg-success text-white my-0" id="poses_theme" tabindex="0" data-toggle="collapse" data-target="#poses" aria-expanded="true" aria-controls="poses">';
                poses += '<div class="row"><div class="col-3"><h6 class=" mb-0"><i class="fas fa-cash-register pt-1"></i> Кассы (' + data.poses.length + ')</h6></div>';
                poses += '<div class="col-3"><small class="float-left" id="poses_footer_msg"></small></div>';
                poses += '<div class="col-6"><small class="float-right" id="poses_footer_time" data-toggle="tooltip"';
                poses += 'data-placement="right" data-original-title="Время последнего обновления блока"></small></div>';
                poses += '</div></div></div>';
                poses += '<div id="poses" class="collapse show" aria-labelledby="headingPoses">';
                poses += '<div class="card-body-p0 bg-light"><div class="row">';
                $.each(data.poses, function (index, i) {
                    poses += '<div class="col-xl-2 col-lg-3">';
                    if (i.theme != "card bg-dark text-white my-1") {
                        poses += '<div class="' + i.theme + '" tabindex="0" data-toggle="popover" data-placement="top" data-html="true"  data-content="">';
                    } else {
                        poses += '<div class="' + i.theme + '">';
                    }
                    poses += '<div class="card-body-p0">';
                    poses += '<p class="text-center mb-0">' + i.name + ' </p></div></div></div>';
                })
                poses += '</div></div></div>';
                $("#poses_card").html(poses);
                $("#poses_footer_time").html(data.date);
            }
            block_errors("poses", data)
            $(".popover").popover("hide");
            $('[data-toggle="popover"]').popover()
        }
    );
}