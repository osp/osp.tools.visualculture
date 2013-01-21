if (typeof (VC) === 'undefined') VC = {};


VC.annotations = (function ($) {
    // *-* utility methods *-*

    // *-* event methods *-*

    // *-* public methods *-*
    var init = function () {
        $('[rel=embed]').each(function() {
            var url = $(this).attr("href");
            var that = this;

            $.ajax(url, {
                dataType: 'json',
                beforeSend: function () {
                    console.info('beforeSend');
                    $(that).text('loading');
                },
                success: function (data) {
                    console.info('success');
                    if (data.mime === "image/png") {
                        $(that).replaceWith('<img src="' + data.url + '"/>');
                    } else {
                        $(that).replaceWith('<img src="/static/img/OSP_new-frog.png" />');
                    };
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.info('error');
                },
                complete: function () {
                    console.info('complete');
                }
            });

        });
    };

    // expose public methods
    return {
        init: init
    };
})(jQuery);
