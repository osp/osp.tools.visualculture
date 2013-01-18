if (typeof (VC) === 'undefined') VC = {};


VC.annotations = (function ($) {
    // *-* utility methods *-*

    // *-* event methods *-*

    // *-* public methods *-*
    var init = function () {
        $('[rel=embed]').each(function() {
            var url = $(this).attr("href"),
                that = this;

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
                    } else if (data.mime === "text/plain") {
                        console.log(data);
                        
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
