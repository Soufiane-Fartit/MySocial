 function updateProfile(id) {
    $.ajaxSetup({async: false}); 
    var first_name = $("#first-name").val();
    var last_name = $("#last-name").val();
    var email = $("#email").val();
    var phone = $("#phone").val();
    var city = $("#city").val();
    var age = $("#age").val();
    var bio = $("#bio").val();
    var picture_path = $("#picture-path").val();
    console.log('updating profile ');
    $.post('/editprofile', 
            {'first_name':first_name,
            'last_name':last_name,
            'email':email,
            'phone':phone,
            'city':city,
            'age':age,
            'bio':bio,
            'picture_path':picture_path
        },
        function(data) {});
    location.reload();
}