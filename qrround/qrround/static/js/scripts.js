function popitup(url) {
  newwindow=window.open(url,'name','height=500,width=500');
  if (window.focus) {newwindow.focus()}
  return false;
}


///////////////////// QR code /////////////////////
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
  console.log(form.serialize());

  if (form.find('input.span5').val() === "") {
    notify('#alerts', 'failure', 'Input some text first');
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
        var number = Math.floor(Math.random() * 6);
        var sentence;
        if(number === 0) { sentence = 'Try more one?' }
        else if(number === 1) { sentence = 'Step farther to make QR code more readable!' }
        else if(number === 2) { sentence = 'Look beautiful?' }
        else if(number === 3) { sentence = 'Love it?' }
        else if(number === 4) { sentence = 'Share it!!!' }
        else if(number === 5) { sentence = 'Where is your girlfriend?' }
        notify('#alerts', 'success', sentence );

        // Append to gallery

      },
      error: function (request, status, error) {
        // alert(request.responseText);
        notify('#alerts', 'failure', request.responseText);
        $('#getqrcode_button').button('reset');
      },
    });
  }
}


/////////////////// Gallery //////////////////////
setTimeout(function(){
  $.ajax({
    type: "GET",
    url: "/getgallery",
    success: function(gallery) {
      $('#gallery').empty().append(gallery);
    }
  });
}, 2000);


///////////////////// Alert /////////////////////
function notify(location, notify_type, msg) {
  var alerts = $(location);
  if (notify_type == 'success') {
    alerts.empty().append('<div class="alert alert-success fade in"> \
      <button type="button" class="close" data-dismiss="alert">×</button> \
      <strong>Yo!</strong> ' + msg + '</div>');
  }
  else if (notify_type == 'failure') {
    alerts.empty().append('<div class="alert alert-block fade in"> \
      <button type="button" class="close" data-dismiss="alert">×</button> \
      <strong>Alert!</strong> ' + msg + '</div>');
  }
  alerts.fadeIn('fast');
  setTimeout(function() {
    alerts.fadeOut();
  }, 5000);
}


/////////////////// Logout /////////////////////////////
$('#logout').on("click", function() {
  $.get("/logout",
    {},
    function(data) {
      console.log("Logout");
      location.reload();
  });
});


///////////// Remember accept checkbox state ///////////////////
$('#id_accept').attr('checked', $.cookie('id_accept') && $.cookie('id_accept') == "true");
$('#id_accept').change(function() {
    $.cookie('id_accept', $('#id_accept').is(':checked'));
    console.log($('#id_accept').is(':checked'));
});


///////////////// Get auth urls ///////////////////
var channels = []
setTimeout(function(){
  $.ajax({
    type: "GET",
    url: "/getauthurls",
    success: function(authurls) {
      $('#auth_url').empty().append(authurls);
      setDetectCookies();
    }
  });
}, 600);


///////////////////// Detect cookies change /////////////////////
function setDetectCookies() {
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
    }, 200);
  }


  $(channels).each(function(i, channel) {
    console.log(channel)
    $.cookie(channel, 0, { path: '/' });

    // bind the listener
    listenCookieChange(channel, function() {
      $.ajax({
        type: "POST",
        url: "/getfriends",
        data: { import: channel },
        success: function(data) {
          console.log("Received: " + data);
        }
      });
    });
  });
}


///////////////////// Initialize Model /////////////////////
$("#policy_modal_link").on("click", function() {
    $('#policy_modal').modal('show');
});

$("#contact_modal_link").on("click", function() {
    $('#contact_modal').modal('show');
});

$('#send_contact').on("click", function() {
  console.log("Send contact");

  $.ajax({
    type: "POST",
    url: "/sendcontact",
    data: $('#contact_modal form').serialize(),
    success: function(data) {
      console.log("Received: " + $('#contact_modal form').serialize());
      $('#contact_modal').modal('hide');
      $('#contact_modal form').find("input[type=text], textarea").val("");
      Recaptcha.reload();
    },
    error: function (request, status, error) {
      console.log("Received: " + request.responseText);
      notify('#contact_modal form .alerts', 'failure', request.responseText);
    },
  });
});

$("#about_modal_link").on("click", function() {
    $('#about_modal').modal('show');
});

$("#import_button").on("click", function() {
  $('#import_modal').modal('show');
});

$('#import').on("click", function() {
  location.reload();
  console.log("Import");
  $(channels).each(function(i, channel) {
    console.log(channel)

    $.ajax({
      type: "POST",
      url: "/getfriends",
      data: { import: channel },
      success: function(data) {
        console.log("Received: " + data);
      }
    });
  });
});


///////////////// Color picker ///////////////////
$('#colorpicker').colorpicker();
