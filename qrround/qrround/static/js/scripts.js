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

function showModel() {
  $('#myModal').modal('show');
}


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
 
            function login(){
                FB.api('/me', function(response) {
        document.getElementById('login').style.display = "block";
        document.getElementById('login').innerHTML = response.name + " succsessfully logged in!";
    });


}
function logout(){
    document.getElementById('login').style.display = "none";
            }
 
            //stream publish method
function streamPublish(name, description, hrefTitle, hrefLink, userPrompt){
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
 
            function graphStreamPublish(){
                var body = 'Reading New Graph api & Javascript Base FBConnect Tutorial';
    FB.api('/me/feed', 'post', { message: body }, function(response) {
        if (!response || response.error) {
            alert('Error occured');
        } else {
            alert('Post ID: ' + response.id);
                    }
                });
            }
 
            function fqlQuery(){
                FB.api('/me', function(response) {
         var query = FB.Data.query('SELECT first_name, last_name, pic_square FROM user WHERE uid in (SELECT uid2 FROM friend WHERE uid1 = me())');

         query.wait(function(rows) {
            // console.log(rows);
            var string;
            rows.forEach(function(row) {
                string = string + "<br />"
                    + 'Your name: ' + row.first_name + " " + row.last_name + "<br />"
                    + '<img src="' + row.pic_square + '" alt="" />' + "<br />";
                // console.log(row);
            })

            document.getElementById('name').innerHTML = string;

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/getPic",
                data: JSON.stringify(rows),
                success: function(data) {
                   alert("Response: " + data);
                            }
                        });
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
        if (response == 0){
            alert('Your facebook status not updated. Give Status Update Permission.');
        }
        else{
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

    gapi.client.request({path:'/plus/v1/people/me/people/visible', method:'GET', callback: function(result) {
      console.log(result);

      $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/getPic",
            data: JSON.stringify(result),
            success: function(data) {
               alert("Response: " + data);
            }
        });
    }})
}


// // Weibo
// WB.core.load(['connect', 'client'], function() {
    // var cfg = {
        // key: '1349178671',
        // xdpath: 'http://127.0.0.1:8000/'
    // };
    // WB.connect.init(cfg);
    // WB.client.init(cfg);
// });
