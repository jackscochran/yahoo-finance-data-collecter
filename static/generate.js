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
        
        $.ajax({
            url: '/generate',
            type: 'POST',
            dataType: 'JSON',
            data: $(this).serializeArray(),
            success: function(data){
                $('#generate').hide()
                $('#processing').hide()
                $('#download').show()
                $('#download-page, #generate-page').prop('disabled', false)
                if(!data['success']){
                    alert(data['e']);
                }
            }
        })
    })

    setInterval(function(){
        $('#loading-bar').removeClass("loading")
        $('#loading-bar').addClass("loading")
    }, 2)

    $('#download-page').click(function(){
        $('#generate').hide()
        $('#processing').hide()
        $('#download').show()
    })

    $('#generate-page').click(function(){
        $('#generate').show()
        $('#processing').hide()
        $('#download').hide()
    })
})