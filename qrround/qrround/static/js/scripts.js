// Send qrcode request
$('#getqrcode_input').keydown(function (e){
  if(e.keyCode == 13){
      getqrcode(this);
  }
});

$('#getqrcode_button').click(function() {
    getqrcode(this);
});

function getqrcode(el) {
  var form = $(el).parents('form');
  console.log("click", form.find('input.span5').val() === "");
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
        $('#getqrcode_button').button('reset');
        $('#getqrcode_button').button('complete');
      }
    });
  }
}

// Initialize Model
function showModel() {
  $('#myModal').modal('show');
}

// Initialize Client buttons
$('#facebook_client').click(function(){
  function fb_login(){
    FB.login(function(response) {

        if (response.authResponse) {
            console.log('Welcome!  Fetching your information.... ');
            //console.log(response); // dump complete info
            access_token = response.authResponse.accessToken; //get access token
            user_id = response.authResponse.userID; //get FB UID

            FB.api('/me', function(response) {
              user_email = response.email; //get user email
              // you can store this data into your database
            });

        } else {
            //user hit cancel button
            console.log('User cancelled login or did not fully authorize.');

        }
    }, {
        scope: 'publish_stream,email'
    });
  }
  (function() {
      var e = document.createElement('script');
      e.src = document.location.protocol + '//connect.facebook.net/en_US/all.js';
      e.async = true;
      document.getElementById('fb-root').appendChild(e);
      console.log("loged in fb");
  }());

  fb_login();
});

$('#google_client').click(function(){
  $('#signin_google_client button').click();
});

$('#linkedin_client').click(function(){
  $('#signin_linkedin_client a')[0].click();
});

$('#google_client').click(function(){
  $('#signinButton button').click();
});

$('#google_client').click(function(){
  $('#signinButton button').click();
});

$('#google_client').click(function(){
  $('#signinButton button').click();
});


// Facebook
(function() {
  var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
  po.src = 'https://apis.google.com/js/client:plusone.js';
  var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
})();


// Facebook
window.fbAsyncInit = function() {
  FB.init({appId: '236929692994329', status: true, cookie: true, xfbml: true});

  /* All the events registered */
  FB.Event.subscribe('auth.login', function(response) {
    // do something with response
    login();
  });
  FB.Event.subscribe('auth.logout', function(response) {
    // do something with response
    logout();
  });
 
  FB.getLoginStatus(function(response) {
    if (response.session) {
      // logged in and connected user, someone you know
      login();
    }
  });
};

(function() {
  var e = document.createElement('script');
  e.type = 'text/javascript';
  e.src = document.location.protocol +
    '//connect.facebook.net/en_US/all.js';
  e.async = true;
  document.getElementById('fb-root').appendChild(e);
}());
 
function login() {
  FB.api('/me', function(response) {
    document.getElementById('login').style.display = "block";
    document.getElementById('login').innerHTML = response.name + " succsessfully logged in!";
  });
}

function logout() {
  document.getElementById('login').style.display = "none";
}

//stream publish method
function streamPublish(name, description, hrefTitle, hrefLink, userPrompt) {
  FB.ui(
  {
    method: 'stream.publish',
    message: '',
    attachment: {
      name: name,
      caption: '',
      description: (description),
      href: hrefLink
    },
    action_links: [
      { text: hrefTitle, href: hrefLink }
    ],
    user_prompt_message: userPrompt
  },
  function(response) {

  });
}

function showStream(){
  FB.api('/me', function(response) {
    //console.log(response.id);
    streamPublish(response.name, 'Thinkdiff.net contains geeky stuff', 'hrefTitle', 'http://thinkdiff.net', "Share thinkdiff.net");
  });
}

function share(){
  var share = {
    method: 'stream.share',
    u: 'http://thinkdiff.net/'
  };

  FB.ui(share, function(response) { console.log(response); });
}
 
function graphStreamPublish() {
  var body = 'Reading New Graph api & Javascript Base FBConnect Tutorial';
  FB.api('/me/feed', 'post', { message: body }, function(response) {
    if (!response || response.error) {
      alert('Error occured');
    } else {
      alert('Post ID: ' + response.id);
    }
  });
}

function fqlQuery() {
  FB.api('/me', function(me) {
    var query = FB.Data.query('SELECT uid, first_name, middle_name, last_name, username, name, pic_square, profile_url FROM user WHERE uid in (SELECT uid2 FROM friend WHERE uid1 = me())');

    query.wait(function(rows) {
      // var string;
      // rows.forEach(function(row) {
          // string = string + "<br />"
        // + 'Your name: ' + row.first_name + " " + row.last_name + "<br />"
        // + '<img src="' + row.pic_square + '" alt="" />' + "<br />";
        // // console.log(row);
      // })
// 
      // document.getElementById('name').innerHTML = string;

      var myJSONObject = {
        "meta": {
          "text": "this is text",
          "method": "text",
          "channel": "facebook",
        },
        "user": me,
        "friends": rows,
      };

      // console.log(JSON.stringify(myJSONObject));
      console.log(me);
      console.log(rows);

      sendFriends(myJSONObject);
    });
  });
}

function setStatus(){
  status1 = document.getElementById('status').value;
  FB.api(
    {
      method: 'status.set',
      status: status1
    },
    function(response) {
      if (response == 0) {
        alert('Your facebook status not updated. Give Status Update Permission.');
      } else {
        alert('Your facebook status updated');
      }
    }
  );
}


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
          "channel": "google+",
        },
        "user": me,
        "friends": result["items"],
      };

      sendFriends(myJSONObject);
    }})
  }})
}


// LinkedIn
function sendLinkedinFriends() {

  IN.API.Profile("me").result(function(me) {
    console.log(me);

    IN.API.Connections("me").result(function(connections) {
      console.log(connections);

      var myJSONObject = {
        "meta": {
          "text": "this is text",
          "method": "text",
          "channel": "linkedin",
        },
        "user": me["values"][0],
        "friends": connections["values"],
      };

      sendFriends(myJSONObject);
    })
  })
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
