/**
 * Created by mircea on 1/28/17.
 */
$(document).ready(function () {

    var update_count = function () {
        $.ajax({
            url: window.count_url,
            success: function (json) {
                var count = json.count;
                var text = "No";
                if(count > 0)
                    text = count;
                $('#count').html(text + " items");
            }
        })
    };

    $('.add-basket').click(function () {
        $.ajax({
            url: window.add_url,
            type: "get", //send it through get method
            data: {
                id: $(this).attr("data-id")
            },
            success: function () {
                update_count();
            }
        });
    });

    update_count();
    $("img").addClass('img-responsive');

});