function popitup(url) {
	newwindow=window.open(url,'name','height=500,width=500');
	if (window.focus) {newwindow.focus()}
	return false;
}

// Send qrcode request
$('#getqrcode_input').keydown(function (e){
  if(e.keyCode == 13){
      getqrcode(this);
  }
});

$('#getqrcode_button').on("click", function() {
    getqrcode(this);
});

function getqrcode(el) {
  var form = $(el).parents('form');
  console.log("click", form.find('input.span5').val() === "");
  console.log(form.serialize());

  if (form.find('input.span5').val() === "") {

  } else {
    $('#getqrcode_button').button('loading');
    $.ajax({
      type: form.attr('method'),
      url: form.attr('action'),
      data: form.serialize(),
      success: function(data) {
        console.log(data);
        $('#qrcode').empty().append(
            data
        );
        $('#getqrcode_button').button('complete');
      },
      error: function (request, status, error) {
        alert(request.responseText);
        $('#getqrcode_button').button('reset');
      },
    });
  }
}


// Initialize Model
$("#policy_modal_link").on("click", function() {
    $('#policy_modal').modal('show');
});

$("#contact_modal_link").on("click", function() {
    $('#contact_modal').modal('show');
});

$("#about_modal_link").on("click", function() {
    $('#about_modal').modal('show');
});

$("#import_button").on("click", function() {
  $('#import_modal').modal('show');
});

$('#import').on("click", function() {
  $.post("/getfriends",
    {
      facebook_access_token: $.cookie('facebook_access_token'),
      google_access_token: $.cookie('google_access_token'),
      linkedin_access_token: $.cookie('linkedin_access_token'),
      twitter_access_token: $.cookie('twitter_access_token'),
      weibo_access_token: $.cookie('weibo_access_token'),
    },
    function(data) {
      console.log("Data Loaded: " + data);
      location.reload();
  });

  $('#import_modal').modal('hide');
});

$('#logout').on("click", function() {
  $.get("/logout",
    {
    },
    function(data) {
      console.log("Logout");
      // TODO: clear session and reload
  });
});

$('#google_client').on("click", function() {
  $('#signin_google_client button').click();
});


// Google plus http://garage.socialisten.at/2013/03/hacking-google-plus-the-sign-in-button/
function signinCallback(authResult) {
  if (authResult['access_token']) {
    // The user has authorized the app, so lets see who we've got here...
    // gAPI ('/people/me');
    gapi.client.request({path:'/plus/v1/people/me', method:'GET', callback: function(result) {
      console.log(result);
    }})

  } else if (authResult['error']) {
    // User has not authorized the G+ App!
  }
}

function sendCircle() {

  gapi.client.request({path:'/plus/v1/people/me', method:'GET', callback: function(me) {
    console.log(me);

    gapi.client.request({path:'/plus/v1/people/me/people/visible', method:'GET', callback: function(result) {
      console.log(result);

      var myJSONObject = {
        "meta": {
          "text": "this is text",
          "method": "text",
          "channel": "google",
        },
        "user": me,
        "friends": result["items"],
      };

      sendFriends(myJSONObject);
    }})
  }})
}


function sendFriends(object) {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: JSON.stringify(object),
    success: function(data) {
      console.log("Received: " + data);
    }
  });
}


// // Renren
// function renrenLogin(object) {
  // Renren.ui({
    // url : 'http://graph.renren.com/oauth/authorize',
    // display : 'popup',
    // params : {"response_type":"token", "client_id":"229108"},
    // onComplete : function(response) {
    // if(window.console){
      // if(response.access_token)
         // console.log("access token:"+ response.access_token);
      // if(response.error)
        // console.log("failure: " + response.error + ',' + response.error_description);
      // }
    // }
  // });
// }
// 
// function renrenUsersGetInfo(access_token) {
  // api_key = "d53f334760c949278f43344c39a8ce0e";
  // url = "https://api.renren.com/restserver.do?api_key=" + api_key
    // + "&access_token=" + access_token
    // + "&method=users.getInfo&format=json"
  // $.ajax({
    // type: "POST",
    // url: url,
    // dataType: "text/plain",
    // origin: "chrome-extension://hgmloofddffdnphfgcellkdfbfbjeloo",
    // success: function(data) {
                // console.log(data);
              // }
  // })
// }
// // Renren send feed
// function sendFeed(url,name,des,image) {
  // var uiOpts = {
      // url : "feed",
      // display : "popup",
      // method : "post",
      // params : {
        // "url":url,
        // "name":name,
        // "description":des,
        // "image":image,
        // "action_name": "过来一起玩",
        // "action_link":"http://apps.renren.com/xxxx"
      // },
      // onSuccess: function(r){/*alert("success!");*/},
      // onFailure: function(r){/*alert("fail");*/document.getElementById("ttt").value="111";}
  // };
  // Renren.ui(uiOpts);
// }


// Detect cookies change
var cookieRegistry = [];

function listenCookieChange(cookieName, callback) {
  setInterval(function() {
    if (cookieRegistry[cookieName]) {
      if ($.cookie(cookieName) != cookieRegistry[cookieName]) {
        // update registry so we dont get triggered again
        cookieRegistry[cookieName] = $.cookie(cookieName);
        return callback();
      }
    } else {
      cookieRegistry[cookieName] = $.cookie(cookieName);
    }
  }, 100);
}

// bind the listener
listenCookieChange('google_access_token', function() {
  alert('cookie google_access_token has changed!');
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: { google_import: $.cookie("google_access_token") },
    success: function(data) {
      console.log("Received: " + data);
    }
  });
});

// bind the listener
listenCookieChange('google_import', function() {
  alert('cookie google_import has changed!');
});

// bind the listener
listenCookieChange('linkedin_import', function() {
  alert('cookie linkedin_import has changed!');
});

// bind the listener
listenCookieChange('weibo_import', function() {
  alert('cookie weibo_import has changed!');
});
