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
    return false;
  });
  $("#email").keyup(function() {
    $("usernameMsg").hide();
    var data = $("#signupForm").serialize();
    $.ajax({
      method: "POST",
      url: "/email",
      data: data
    }).done(function(res) {
      $("#emailMsg").html(res);
    });
    return false;
  });

  $("#liked_recipe").hide();
  $("#liked-tab").click(function() {
    console.log("clicked");
    $("#created-tab").removeClass("active");
    $("#liked-tab").addClass("active");
    $("#created_recipe").hide();
    $("#liked_recipe").show();
  });
  $("#created-tab").click(function() {
    console.log("clicked");
    $("#liked-tab").removeClass("active");
    $("#created-tab").addClass("active");
    $("#liked_recipe").hide();
    $("#created_recipe").show();
  });
  return false;
});
