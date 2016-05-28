/* 平均BAD数を取得 */
function getBadCountAvg(music_id) {
    var selector = 'tr#music-'+music_id+' .bad_count_avg';
    $.ajax({
        url: SERVER_URL+'api/get_bad_count_avg/'+music_id+'/',
        type: 'GET'
    })
    .then(
        function(response) {
            if (response.bad_count_avg == -1) response.bad_count_avg = '-';
            // 平均BAD数を描画
            $(selector).text(response.bad_count_avg);
        },
        function(err) {
            console.log(err);
        }
    );
}

/* 順位を取得 */
function getMyRank(music_id) {
    var selector = 'tr#music-'+music_id+' .rank';
    $.ajax({
        url: SERVER_URL+'api/get_myrank/'+music_id+'/',
        type: 'GET',
    })
    .then(
        function(response) {
            if (response.myrank == 0) response.myrank = '-';
            // 順位を描画
            $(selector).text(response.myrank+' / '+response.bad_count_num);
        },
        function(err) {
            console.log(err);
        }
    );
}
