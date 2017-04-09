$(document).ready(function () {
    $(".delete").click(function () {
        $.ajax({
            url: $(this).data('url'),
            type: 'DELETE',
            success: function (data) {
                $('#infobar').html("Successfully deleted").show()
            }
        });
    });
    $(".done").click(function () {
        $.ajax({
            url: $(this).data('url'),
            type: 'PATCH',
            data: {is_done: true},
            success: function (data) {
                $('#infobar').html("Successfully Mark as Done").show()
            }
        });
    });
});