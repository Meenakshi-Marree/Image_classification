$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make prediction by calling the /predict API
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Hide loader and show results
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').html(
                    `<strong>Disease:</strong> ${data.disease}<br>
                     <strong>Symptoms:</strong> ${data.symptoms}<br>
                     <strong>Remedies:</strong> ${data.remedies}`
                );
                console.log('Success!');
            },
            error: function (error) {
                $('.loader').hide();
                $('#result').fadeIn(600);
                $('#result').text('Error occurred. Please try again.');
                console.error('Error:', error);
            }
        });
    });
});
