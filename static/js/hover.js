$(document).ready(function(){
    $(".hover").hover(function(){
        var description = $(this).data("desc");
        $(this).append('<div class="hover-description">' + description + '</div>');
        $(this).find(".hover-description").fadeIn(10);
    }, function(){
        $(this).find(".hover-description").fadeOut(10, function(){
            $(this).remove();
        });
    });
});
