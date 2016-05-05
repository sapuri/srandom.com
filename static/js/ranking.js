var SERVER_URL = 'http://127.0.0.1:8000/';

// ローディング画像を表示
function showLoadingImage(selector) {
    $(selector+' .loading').append('<img src="/static/img/ajax-loader.gif">');
}
// ローディング画像を消す
function hideLoadingImage(selector) {
    $(selector+' .loading').hide();
}

/* 平均BAD数取得 */
function getBadCountAvg(music_id) {
    var selector = 'tr#music-'+music_id+' .bad_count_avg';
    // ローディング画像を表示
    showLoadingImage(selector);
    $.ajax({
        url: SERVER_URL+'api/get_bad_count_avg/'+music_id+'/',
        type: 'GET',
        success: function(response){
            // ローディング画像を消す
            hideLoadingImage(selector);
            // 平均BAD数を描画
            if (response.bad_count_avg == -1) response.bad_count_avg = '-';
            $(selector).text(response.bad_count_avg);
        },
        error: function(err) {
            // ローディング画像を消す
            hideLoadingImage(selector);
            console.log(err);
        }
    })
}

/* 順位取得 */
function getMyRank(music_id) {
    var selector = 'tr#music-'+music_id+' .rank';
    // ローディング画像を表示
    showLoadingImage(selector);
    $.ajax({
        url: SERVER_URL+'api/get_myrank/'+music_id+'/',
        type: 'GET',
        success: function(response){
            // ローディング画像を消す
            hideLoadingImage(selector);
            // 順位を描画
            if (response.myrank == 0) response.myrank = '-';
            $(selector).text(response.myrank+' / '+response.bad_count_num);
        },
        error: function(err) {
            // ローディング画像を消す
            hideLoadingImage(selector);
            console.log(err);
        }
    })
}
