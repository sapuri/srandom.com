const SERVER_URL = location.protocol + '//' + location.host + '/';

/* メッセージボックス */
$(function () {
    $(document).ready(function() {
        $("#message-box").stop().fadeIn(1200).delay(1500).fadeOut("slow");
    });
});

/* トップに戻るボタン */
$(document).ready(function() {
    const pagetop = $('.pagetop');
    $(window).scroll(function () {
        if ($(this).scrollTop() > 1000) {
            pagetop.fadeIn();
        } else {
            pagetop.fadeOut();
        }
    });
    pagetop.click(function () {
        $('body, html').animate({ scrollTop: 0 }, 500);
        return false;
    });
});

/* ローディング画像を表示 */
function showLoadingImage(selector) {
    $(selector+' .loading').append(`<img src=${STATIC_URL}img/ajax-loader.gif alt="loading">`);
}

/* ローディング画像を消す */
function hideLoadingImage(selector) {
    $(selector+' .loading').hide();
}
