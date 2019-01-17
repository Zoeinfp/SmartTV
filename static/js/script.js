var app = new Vue({
        el: '#app',
        data: {
            description: "Un outil à la disposition des acteurs du pôle innovation conçu pour faciliter l'échange et faire circuler les infos utiles."
        }
    })

$(document).on("click", ".messageModal", function () {
     $(".modal-body #message").val($(this).data('id'));
     $(".modal-body #sendmessage").val($(this).data('id'));
});
