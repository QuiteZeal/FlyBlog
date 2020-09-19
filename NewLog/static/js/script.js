let clipboard = new ClipboardJS('.btn');

clipboard.on('success', function (e) {
    console.log(e);
    $(".hidden-first").css("visibility", "visible");
});

clipboard.on('error', function (e) {
    console.log(e);
});


$(".close-clear").click(function () {
   $(".hidden-first").css("visibility", "hidden");
})

//media query at 375px
// const mqWidth = window.matchMedia( "(min-width: 375px)" );
//
// function hideShow(e) {
//     if (e.matches) {
//         $("#readMore").hide();
//     } else {
//        $("#readMore").show();
//     }
// }
//
// mqWidth.addListener(hideShow);

// show timestamp
$(function () {
    function render_time() {
        return moment($(this).data('timestamp')).format('lll')
    }
    $('[data-toggle="tooltip"]').tooltip(
        {
            title: render_time
        }
    );
});