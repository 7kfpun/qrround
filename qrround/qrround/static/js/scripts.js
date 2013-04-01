function popitup(url) {
  newwindow = window.open(url, 'name', 'height=500,width=500');
  if (window.focus) {newwindow.focus(); }
  return false;
}

$('.nav-tabs > li > a').hover(function() {
  $(this).tab('show');
});

///////////////////// QR code /////////////////////
// Send qrcode request
$('#getqrcode_input').keydown(function (e) {
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

        console.log(data['notice']);

        $('#qrcode').empty().append($(data['html']).hide().fadeIn('1000'));
        $('#getqrcode_button').button('complete');

        notify('#alerts', 'success', data['notice'] );

        // Append to gallery
        var new_qrcode_src = $('#qrcode img').attr('src');
        $('#gallery ul').prepend('<li class="span2"> \
           <a href="' + new_qrcode_src + '" title="' + data['text'] + '" class="thumbnail" data-gallery="gallery"> \
             <img src="' + new_qrcode_src + '" width="100" height="100"> \
           </a> \
         </li>');

        changeMeta(new_qrcode_src, new_qrcode_src);
      },
      error: function (request, status, error) {
        notify('#alerts', 'failure', request.responseText);
        $('#getqrcode_button').button('reset');
      },
    });
  }
}

function changeMeta(st_url, st_image) {
  $('span[class^="st_"]').html(''); // Empty span contents
  $('span[class^="st_"]').attr('st_processed', null); // Reset ST plugin
  
  $('span[class^="st_"]').attr('st_url', window.location.href + '/' + st_url);
  $('span[class^="st_"]').attr('st_image', window.location.href + '/' + st_url);
  stButtons.makeButtons(); 
}
// function changeMeta(new_qrcode_src) {
//     console.log('Changing meta tags');
//     $('meta[property="og:url"]').attr("content", new_qrcode_src);  // window.location.href + "?" + filename);
//     $('meta[property="og:image"]').attr("content", new_qrcode_src);
//     $('meta[property="og:description"]').attr("content", new_qrcode_src);  // filename);
// }

/////////////////// Gallery //////////////////////
setTimeout(function(){
  $.ajax({
    type: "GET",
    url: "/getgallery",
    success: function(gallery) {
      $('#gallery').empty().append($(gallery).hide().fadeIn(2000));
    }
  });
}, 5000);


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
//  setTimeout(function() {
//    alerts.fadeOut();
//  }, 5000);
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
var channels = ['facebook', 'google', 'kaixin001', 'linkedin', 'weibo']
setTimeout(function(){
  $.ajax({
    type: "GET",
    url: "/getauthurls",
    success: function(authurls) {
      $('#auth_url').empty().append(authurls);
      // setDetectCookies();
    }
  });
}, 600);


///////////////////// Initialize Tooltip and Model /////////////////////
console.log($.cookie('helptip2'));
if ( $.cookie('helptip2') != 'false' ) {
  $($('[data-toggle="popover"]')[2]).popover('show');

  $('.popover button,#id_accept').click(function() {
    $($('[data-toggle="popover"]')[2]).popover('destroy');
    $.cookie('helptip2', 'false');

    initialHelptip0();
  });
}

initialHelptip0();
function initialHelptip0() {
  console.log($.cookie('helptip0'));
  if ( $.cookie('helptip0') != 'false' && $.cookie('helptip2') == 'false' ) {
    $($('[data-toggle="popover"]')[0]).popover('show');

    $('.popover button,#import_button').click(function() {
      $($('[data-toggle="popover"]')[0]).popover('destroy');
      $.cookie('helptip0', 'false');

      initialHelptip1();
    });
  }
}

initialHelptip1();
function initialHelptip1() {
  console.log($.cookie('helptip1'));
  if ( $.cookie('helptip1') != 'false' && $.cookie('helptip0') == 'false' ) {
    $($('[data-toggle="popover"]')[1]).popover('show');
    $('.popover button,#getqrcode_button').click(function() {
      $($('[data-toggle="popover"]')[1]).popover('destroy');
      $.cookie('helptip1', 'false');
    });
  }
}

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
});


///////////////// Color picker ///////////////////
$('#colorpicker').colorpicker();
