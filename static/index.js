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
  // $("#liked").click(function() {
  //   var data = $("#likeForm").serialize();
  //   $.ajax({
  //     method: "POST",
  //     url: "/like",
  //     data: data
  //   }).done(function(res) {
  //     $("#likedMsg").html(res);
  //   });
  // });
  // $("#unliked").click(function() {
  //   var data = $("#unlikeForm").serialize();
  //   $ajax({
  //     method: "POST",
  //     url: "/unlike",
  //     data: data
  //   }).done(function(res) {
  //     $("#likedMsg").html(res);
  //   });
  // });
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
