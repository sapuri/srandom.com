function getMyRank(music_id) {
    const selector = 'tr#music-'+music_id+' .rank';
    $.ajax({
        url: SERVER_URL+'api/get_myrank/'+music_id+'/',
        type: 'GET',
    })
    .then(
        function(response) {
            if (response.myrank === 0) response.myrank = '-';
            if (response.bad_count_num === 0) response.bad_count_num = '-';
            // 順位を描画
            $(selector).text(response.myrank+' / '+response.bad_count_num);
        },
        function(err) {
            console.log(err);
        }
    );
}
