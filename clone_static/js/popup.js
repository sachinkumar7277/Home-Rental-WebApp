var csrftoken = undefined;
function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie !== '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = cookies[i].trim();
             // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                   break;
            }
         }
     }
     return cookieValue;

}

document.addEventListener("DOMContentLoaded", function(event) {

      csrftoken = getCookie('csrftoken');
  });

//   get url link for api call

 url_link = window.location.href;
 url_link = url_link.slice(7)
 indx = url_link.indexOf("/")
 url_link = url_link.slice(0,indx)

check_url = "http://"+url_link+"/api/validatePhone"
console.log('popup js se aaya hu',check_url)




// For Verify Phone Pop up API CALL

var phoneVerifyform = document.getElementById('verifyPhoneform')
phoneVerifyform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on OTP Generate...')
    verifyPhone()
//    document.getElementById('form-button').classList.add("hidden");

})
    var verifyPhoneData = {

        'phone':null,

    }

function verifyPhone(){


        verifyPhoneData.phone = phoneVerifyform.phone.value



//    console.log('verifyphone data  :', verifyPhoneData)

    var url = "http://"+url_link+"/api/validatePhone"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(verifyPhoneData),

    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status){
           console.log("ye return aaya hai basckend se ",data)
           document.getElementById('verifyPhoneClose').click()
           $("#verifyOTPModal").modal()
        }
        else{
             alert(data.Detail)
             window.location.href = "/rent/home"

        }

    })
}



// For Verify OTP Pop up API CALL

var otpform = document.getElementById('verifyotpform')
otpform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on VerifyOTP...')
    verifyOTP()
//    document.getElementById('form-button').classList.add("hidden");

})


function verifyOTP(){

//    var userFormData = {
//        'name':null,
//        'email':null,
//        'total':total,
//    }

    var verifyOTPData = {

        'otp':null,
        'phone': verifyPhoneData.phone


    }


        verifyOTPData.otp = otpform.otp.value

    var url = "http://"+url_link+"/api/validateOTP"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(verifyOTPData),

    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status){
           console.log(data)
           document.getElementById('verifyOTPClose').click()
           $("#regModal").modal()
        }
        else{
          alert("OTP does not Matched try again")
          window.location.href = "/rent/home"
        }



    })
}



// register API call



var regform = document.getElementById('myform')
regform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on register ...')

     newpass = regform.password.value
     cnfPass = regform.confirm_password.value

     if (newpass == cnfPass ){

         Bool = CheckLength(newpass)
         if (Bool){
             register()
         }
         else{
         alert('Password should be of at least 8 character')
         }

     }
     else{
     alert("New Password not matched with confirm password Try again")
     }

//    document.getElementById('form-button').classList.add("hidden");

})


function register(){

    var userFormData = {
        'username':null,
        'email':null,
        'DOB':null,
        'password':null,
        'phone': verifyPhoneData.phone
    }


        userFormData.username = regform.full_name.value
        userFormData.email = regform.your_email.value
        userFormData.DOB = regform.dob.value
        userFormData.password = regform.password.value




    console.log('userFormData ka  data  :', userFormData)

    var url = "http://"+url_link+"/api/register"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(userFormData),

    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status){
           console.log(data)
           document.getElementById('CloseRegModal').click()
           alert("You have Successfully Registered")
        }
        else{
          console.log(data)
          alert("Registration failed ")

        }



    })
}

// Login API Call

var loginform = document.getElementById('loginform')

loginform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on login...')
    login()
//    document.getElementById('form-button').classList.add("hidden");

})
var loginformData = {
        'password':null,
        'phone': null
    }

var Auth_Token

function login(){

    loginformData.password = loginform.passwd.value
    loginformData.phone = loginform.phn.value

    var url = "http://"+url_link+"/api/login"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(loginformData),

    })
    .then((response) => response.json())
    .then((data) =>checkstatus(data))



     function checkstatus(data){

        if (data.status){
            Auth_Token = data.token
            localStorage.setItem('Auth_Token',Auth_Token)
            console.log(data)
            alert("You are logged in now")
            window.location.href = "/rent/home"

        }
        else{
          console.log(data)
          alert("Invalid Credentials")

        }

     }


}

// open login modal and close register modal

function openLogin_Modal(){
  document.getElementById('CloseRegModal').click()
  $("#loginModal").modal()

}



// open Reset Password through Email and close login modal

function openReset_Pass_Modal(){
  document.getElementById('loginModal').click()
  $("#reset_pass_modal").modal()

}






// Change Password API Call
function CheckLength(NewPassword){


 if (NewPassword.length  < 8){

     return false;
 }
 else{
     return true;
 }
}

function OnPassChange(){
  var changePwdForm = document.getElementById('changePwdForm')

  changePwdForm.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on ChngPassword...')

    newpass = changePwdForm.new_password.value
    cnfPass = changePwdForm.comfirm_password.value

    console.log(newpass,cnfPass,"Ye new or confirm password ha")

    if (newpass == cnfPass ){

         Bool = CheckLength(newpass)
         if (Bool){
             ChngPass()
         }
         else{
         alert('Password should be of at least 8 character')
         }

     }
     else{
     alert("New Password not matched with confirm password Try again")
     }
//    document.getElementById('confirm-change').classList.add("hidden");

  })

}


var ChngPassformData = {
        'new_password':null,
        'old_password': null
    }



function ChngPass(){

    ChngPassformData.new_password = changePwdForm.new_password.value
    ChngPassformData.old_password = changePwdForm.old_password.value
    var auth_token = localStorage.getItem('Auth_Token')
    var url = "http://"+url_link+"/api/change-password"
    fetch(url, {
        method:'PUT',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
            'Authorization': 'Token '+ auth_token


        },
        body:JSON.stringify(ChngPassformData),

    })
    .then((response) => response.json())
    .then((data) =>checkstatus(data))



     function checkstatus(data){
        console.log(data.status)
        if (data.status){
            console.log(data)
            window.location.href = "/rent/home"
        }
        else{
          alert("something went wrong ")
          window.location.href = "/rent/home"
        }

     }


}


//Reset password API call

var resetpassform = document.getElementById('reset_pass_form')
resetpassform.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on Reset Password...')
    resetPass()
//    document.getElementById('form-button').classList.add("hidden");

})


function resetPass(){

    var resetPassData = {

        "email":null

    }


        resetPassData.email = resetpassform.reset_email.value
        console.log(resetPassData.email)

    var url = "http://"+url_link+"/api/goToResetPass"
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({"email":resetPassData.email}),

    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status){
           console.log(data)
            window.location.href = "/rent/home"
           alert("Password Reset Email has been sent to your registered email."+"     "+ "please check your email")

        }
        else{

          alert("Failed to send email to reset password try again")
           window.location.href = "/rent/home"
        }



    })
}


//

// For ADDING PREMIUM

var premium = document.getElementById('premiumPlan')
premium.addEventListener('submit', function(e){
    e.preventDefault()
    console.log('Clicked on ADD Premium')
//    AddPremium()
//    document.getElementById('form-button').classList.add("hidden");

})


function AddPremium(){

    var premiumData = {

        'id':{{request.user.profile.id}},
        'planId'null:



    }


        premiumData.planId = document.querySelector( 'input[name="plan"]:checked');
        console.log(premiumData.planId)
        console.log(premiumData.planId)

    var url = "http://"+url_link+"/api/AddPremium"
    fetch(url, {
        method:'PUT',
        headers:{
            'Content-Type':'applicaiton/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify(premiumData),

    })
    .then((response) => response.json())
    .then((data) => {
        if (data.status){
           console.log(data)
           alert("Premium  Added Successfully !")


        }
        else{
          alert("Premium not Added try again")
//          window.location.href = "/rent/home"
        }



    })
}
