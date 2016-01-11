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
                    console.info('success', data);
                    if (data.mime.match(/image\/.*/)) {
                        $(that).replaceWith('<img src="' + data.url + '"/>');
                    } else if (data.mime.match(/text\/.*/)) {
                        var txt = $("<pre />")
                        txt.insertAfter($(that));
                        txt.load(data.url);
                        $(that).remove();
                    } else {
                        $(that).replaceWith('<img src="/static/img/OSP_new-frog.png" />');
                    };
                },
                error: function (xhr, ajaxOptions, thrownError) {
                    console.log('error: ' + xhr.status + ' ' + xhr.statusText);
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


/* Inserts the meel address */

een = '.pso@maim||nehctik'
eentjes = een.split("||");
var reverse = function (s) {
  var ret ='';
  for (var i=s.length-1;i>=0;i--)
    ret+=s.charAt(i);
  return ret;
}

een = reverse(eentjes[0])+reverse(eentjes[1]);

$(function() {
    $('.envoyez').attr('href', 'mailto:' + een);
})
