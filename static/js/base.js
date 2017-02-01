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
                if (count > 0)
                    text = count;
                $('#count').html(text + " items");
            }
        })
    };

    var update_selection = function (id, json) {
        if (json.quantity <= 0) {
            $("span.quantity[data-id=" + id + "]").parents().eq(2).remove();
        } else {
            var text = "";
            if (json.quantity > 1) {
                text = json.quantity + " pieces";
            }

            $("span.quantity[data-id=" + id + "]").text(text);
            $("strong.subtotal[data-id=" + id + "]").text(json.subtotal + "$");
        }

        $.ajax({
            url: window.total_url,
            type: "get",
            success: function (json) {
                $("span.price").text(json.total + "$");
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
            success: update_count()
        });
    });

    $('.remove-item').click(function () {
        var id = $(this).attr("data-id");

        $.ajax({
            url: window.remove_url,
            type: "get",
            data: {
                id: id,
                q: $(this).attr("data-quantity")
            },
            success: function (json) {
                update_count();
                update_selection(id, json)
            }
        })
    });

    $("#empty").click(function() {
        $.ajax({
            url: window.empty_url,
            type: "get",
            success: function (){
                window.location.href = "/"
            }
        })
    });

    update_count();
    $("img").addClass('img-responsive');

});