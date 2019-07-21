$(document).ready(function() {
  $("#username").keyup(function() {
    var data = $("#signupForm").serialize();
    $.ajax({
      method: "POST",
      url: "/username",
      data: data
    }).done(function(res) {
      $("#usernameMsg").html(res);
    });
  });
  return false;
});
