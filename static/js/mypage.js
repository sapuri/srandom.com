/* 各レベルのクリア率を取得 */
function getPercentageOfClear(user_id) {
    for (var i = 17; i >= 1; i--) {
        var selector = 'div#slv-'+i+' a span.bar';
        showLoadingImage(selector);
    }
    $.ajax({
        url: SERVER_URL+'users/api/get_percentage_of_clear/'+user_id+'/',
        type: 'GET'
    })
    .then(
        function(response) {
            for (var i = 17; i >= 1; i--) {
                var selector = 'div#slv-'+i+' a span.bar';
                $(selector).attr('style', 'width: '+response.percentage_of_clear[i-1]+'%');
                $(selector).text(response.percentage_of_clear[i-1]+'%');
            }
        },
        function(err) {
            hideLoadingImage(selector);
            console.log(err);
        }
    );
}

/* クリア状況を取得 */
function getClearStatus(music_id, user_id) {
    var selector = 'tr#music-'+music_id;
    $.ajax({
        url: SERVER_URL+'api/get_clear_status/'+music_id+'/',
        type: 'GET',
        data: {
            user_id: user_id
        }
    })
    .then(
        function(response) {
            $(selector).addClass(response.clear_status);
            $(selector+' script').remove();
        },
        function(err) {
            console.log(err);
        }
    );
}

/* BAD数を取得 */
function getBadCount(music_id, user_id) {
    var selector = 'tr#music-'+music_id+' .bad_count';
    $.ajax({
        url: SERVER_URL+'api/get_bad_count/'+music_id+'/',
        type: 'GET',
        data: {
            user_id: user_id
        }
    })
    .then(
        function(response) {
            var bad_count = '-';
            if (response.bad_count != null) {
                bad_count = response.bad_count;
            }
            // BAD数を描画
            $(selector).text(bad_count);
        },
        function(err) {
            console.log(err);
        }
    );
}

/* メダルを取得 */
function getMedal(music_id, user_id) {
    var selector = 'tr#music-'+music_id+' .medal';
    $.ajax({
        url: SERVER_URL+'api/get_medal/'+music_id+'/',
        type: 'GET',
        data: {
            user_id: user_id
        }
    })
    .then(
        function(response) {
            if (response.medal && response.medal != 12) {
                // 未プレイ以外ならメダルを描画
                var medal = response.medal;
                $(selector+' .loading').remove();
                $(selector+' img').attr('src', '/static/img/medal/'+medal+'.png');
                $(selector+' img').attr('width', '16');
                $(selector+' img').attr('height', '16');
                $(selector+' script').remove();
            } else {
                $(selector).text('-');
            }
        },
        function(err) {
            console.log(err);
        }
    );
}

/* 最新の更新日時を取得 */
function getLatestUpdatedAt(music_id, user_id) {
    var selector = 'tr#music-'+music_id+' .updated_at';
    $.ajax({
        url: SERVER_URL+'api/get_latest_updated_at/'+music_id+'/',
        type: 'GET',
        data: {
            user_id: user_id
        }
    })
    .then(
        function(response) {
            var updated_at = '-';
            if (response.is_active) {
                // ゼロパディング
                response.day = ("0" + response.day).slice(-2);
                response.minute = ("0" + response.minute).slice(-2);
                updated_at = response.year+'/'+response.month+'/'+response.day+' '+response.hour+':'+response.minute;
            }
            // 更新日時を描画
            $(selector).text(updated_at);
        },
        function(err) {
            console.log(err);
        }
    );
}
