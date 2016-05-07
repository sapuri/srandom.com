/* 各メダルの枚数を取得 */
function getMedalCount(music_id) {
    $.ajax({
        url: SERVER_URL+'api/get_medal_count/'+music_id+'/',
        type: 'GET'
    })
    .then(
        function(response) {
            // 各メダルの枚数を描画
            for (var i = 1; i <= 11; i++) {
                $('td#medal-'+i).text(response.medal_count_list[i-1]);
            }
            $('td#medal-total').text(response.medal_count_total);
        },
        function(err) {
            console.log(err);
        }
    );
}

/* 平均BAD数を取得 */
function getBadCountAvg(music_id) {
    var selector = 'td#bad_count_avg';
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
