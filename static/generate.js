$(document).ready(function(){
    $('#generate').show()
    $('#processing').hide()
    $('#download').hide()

    $("#request-form").on('submit', function( event ){
        event.preventDefault();

        // display loading screen
        $('#generate').hide()
        $('#processing').show()
        $('#download').hide()

        //disable navigation bar
        $('#download-page, #generate-page').prop('disabled', true)
        
        $('#loadingText').text('Initiating Report...')
        $.ajax({
            url: '/generate',
            type: 'POST',
            dataType: 'JSON',
            data: $(this).serializeArray(),
            success: function(data){
                collect_data(data['tickers'], data['key'])
            }
        })
    })

    $('#download-page').click(function(){
        $('#generate').hide()
        $('#processing').hide()
        $('#download').show()
    })

    $('#generate-page').click(function(){
        $('#generate').show();
        $('#processing').hide();
        $('#download').hide();
    })
})

function collect_data(tickers, key) {
    tickerCount = 0;

    tickers.forEach(ticker => {
        
        tickerCount++;
        percent = updateProgress(tickerCount, tickers.length)

        $.ajax({
            url: '/save-ticker',
            type: 'POST',
            async: false,
            dataType: 'JSON',
            data: {'ticker': ticker, 'key': key},
            success: function(){

                if (percent == 100){ //when all tickers are completed
                    $('#generate').hide()
                    $('#processing').hide()
                    $('#download').show()

                    //disable navigation bar
                    $('#download-page, #generate-page').prop('disabled', false)
                }
            }
        })
        
    });
}

function updateProgress(current, total){
    percent = Math.round(current/total * 100);
    // $('#loadingText').text('Retreiving Ticker ' + current + '/' + total + '( ' + percent + ' )');
    // $('#loading-bar').css('width', percent + '%');

    $('#loadingText')[0].innerHTML = 'Retreiving ' + current + '/' + total + '( ' + percent + '% )';
    $('#loading-bar')[0].style.width = percent + '%';
    
    console.log(percent)
    return percent
}