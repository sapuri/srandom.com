function getMedalCount(music_id) {
    $.ajax({
        url: SERVER_URL+'api/get_medal_count/'+music_id+'/',
        type: 'GET'
    })
    .then(
        function(response) {
            // 各メダルの枚数を描画
            for (let i = 1; i <= 11; i++) {
                $('td#medal-'+i).text(response.medal_count_list[i-1]);
            }
            $('td#medal-total').text(response.medal_count_total);
        },
        function(err) {
            console.log(err);
        }
    );
}
