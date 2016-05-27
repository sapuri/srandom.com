/* フォルダランプを取得 */
function getFolderLamp(level, is_srandom) {
    var selector = '#lv'+level+'.level-folder';
    $.ajax({
        url: SERVER_URL+'api/get_folder_lamp/'+level+'/',
        type: 'GET',
        data: {
            is_srandom: is_srandom
        }
    })
    .then(
        function(response) {
            $(selector).addClass(response.folder_lamp);
        },
        function(err) {
            console.log(err);
        }
    );
}
