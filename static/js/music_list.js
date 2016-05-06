/* 最新の更新日時を取得 */
function getLatestUpdatedAt(music_id) {
    var selector = 'tr#music-'+music_id+' .updated_at';
    showLoadingImage(selector);
    $.ajax({
        url: SERVER_URL+'api/get_latest_updated_at/'+music_id+'/',
        type: 'GET',
        success: function(response){
            hideLoadingImage(selector);
            var updated_at = '-';
            if (response.is_active) {
                // ゼロパディング
                response.day = ("0" + response.day).slice(-2);
                response.hour = ("0" + response.hour).slice(-2);
                response.minute = ("0" + response.minute).slice(-2);
                updated_at = response.year+'/'+response.month+'/'+response.day+' '+response.hour+':'+response.minute;
            }
            // 更新日時を描画
            $(selector).text(updated_at);
        },
        error: function(err) {
            hideLoadingImage(selector);
            console.log(err);
        }
    })
}
