function getPercentageOfClear(user_id) {
    for (let i = 19; i >= 1; i--) {
        const selector = 'div#slv-'+i+' a span.bar';
        showLoadingImage(selector);
    }
    $.ajax({
        url: SERVER_URL+'users/api/get_percentage_of_clear/'+user_id+'/',
        type: 'GET'
    })
    .then(
        function(response) {
            for (let i = 19; i >= 1; i--) {
                const selector = 'div#slv-'+i+' a span.bar';
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
