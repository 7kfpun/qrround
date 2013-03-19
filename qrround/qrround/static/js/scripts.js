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
  location.reload();
  // $('#import_modal').modal('hide');
});

$('#logout').on("click", function() {
  $.get("/logout",
    {
    },
    function(data) {
      console.log("Logout");
      location.reload();
  });
});


// TODO: useless, remove it
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

$.cookie('facebook', 0);
$.cookie('google', 0);
$.cookie('linkedin', 0);
$.cookie('kaixin001', 0);
$.cookie('twitter', 0);
// bind the listener
listenCookieChange('facebook', function() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: { import: 'facebook' },
    success: function(data) {
      console.log("Received: " + data);
    }
  });
});

// bind the listener
listenCookieChange('google', function() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: { import: 'google' },
    success: function(data) {
      console.log("Received: " + data);
    }
  });
});

// bind the listener
listenCookieChange('linkedin', function() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: { import: 'linkedin' },
    success: function(data) {
      console.log("Received: " + data);
    }
  });
});

// bind the listener
listenCookieChange('kaixin001', function() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: { import: 'kaixin001' },
    success: function(data) {
      console.log("Received: " + data);
    }
  });
});

// bind the listener
listenCookieChange('twitter', function() {
  $.ajax({
    type: "POST",
    url: "http://127.0.0.1:8001/getfriends",
    data: { import: 'twitter' },
    success: function(data) {
      console.log("Received: " + data);
    }
  });
});

// bind the listener
listenCookieChange('weibo', function() {
  alert('cookie weibo_import has changed!');
});
