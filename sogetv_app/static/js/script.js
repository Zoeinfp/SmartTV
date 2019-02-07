var app = new Vue({
        el: '#app',
        data: {
            description: "Un outil à la disposition des acteurs du pôle innovation conçu pour faciliter l'échange et faire circuler les infos utiles."
        }
    })

//$(document).on("click", ".messageModal", function () {
//     $(".modal-body #message").val($(this).data('id'));
//     $(".modal-body #sendmessage").val($(this).data('id'));
//});


$(document).on("click", ".saved_message", function() { var element = $(event.target); manage_message(element);});
$(document).on("click", ".saved_message", function() { var element = $(event.target); manage_message(element);});
$(document).on("click", ".add-msg", function() { add_message(); });
$(document).on("click", ".update-msg", function() { update_message(); });
$(document).on("click", ".delete-msg", function() { delete_message(); });

function add_message()
{
    $( "#update-msg" ).hide();
    $("#add-msg").show();
}

function manage_message(element)
{
    $( "#update-msg" ).show();
    $("#add-msg").hide();
    var text = $(element).text();
    var correct_text = text.replace(/\(|\)/g, '');
    $('#store-msg').val(text);
    $('#inserted_message').val(text);
}

function update_message()
{
    var new_message = $("#inserted_message").val();
    var old_message = $("#store-msg").val();

    console.log(new_message);
    console.log(old_message);

    $.getJSON($SCRIPT_ROOT + '/update_message', {new_message:new_message, old_message:old_message},
            function (feedback)
            {
                if (feedback == 'Updated')
                {
                    console.log('Ok')
                }
                else
                {
                    console.log('KO');
                }
            });
    location.reload();
}

function delete_message()
{
    var old_message = $("#store-msg").val();
    console.log(''+old_message+'end');
    $.getJSON($SCRIPT_ROOT + '/delete_message', {old_message:old_message},
            function (feedback)
            {
                if (feedback == 'Delete')
                {
                    console.log('Ok')
                }
                else
                {
                    console.log('KO');
                }
            });
    location.reload();

}
