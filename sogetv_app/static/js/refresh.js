
function startRefresh() {
    $.get('', function(data) {
        $(document.body).html(data);
    });
}
$(function() {
    setTimeout(startRefresh,11000);
});


$(function() {
    $("#carousel").carousel();
});

$('#carousel').on('slid.bs.carousel', function () {
var currentSlide = $('#carousel div.active').index();
sessionStorage.setItem('lastSlide', currentSlide);
});
if(sessionStorage.lastSlide){
  $("#carousel").carousel(sessionStorage.lastSlide*1);
}