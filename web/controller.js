$(document).ready(function () {
  // Display Speak Message
  function DisplayMessage(message) {
    // Update the text of the <p> element with the class 'siri-message'
    $(".siri-message").text(message);

    // Apply an animation using Animate.css
    $(".siri-message").addClass("animate__animated animate__fadeIn");

    // Remove animation class after it's complete (to allow it to run again)
    $(".siri-message").one("animationend", function () {
      $(this).removeClass("animate__animated animate__fadeIn");
    });

    // Or use GSAP for more flexibility
    gsap.fromTo(".siri-message", { opacity: 0 }, { opacity: 1, duration: 1 });
  }

  // Example Usage: Simulating a message
  DisplayMessage("Hello! This is a frontend-only message.");

  // Display Hood
  function ShowHood() {
    // Show the Oval section by removing the hidden attribute
    $("#Oval").removeAttr("hidden");

    // Hide the Siriwave section by adding the hidden attribute
    $("#Siriwave").attr("hidden", true);
  }

  // Example Usage: Simulating hood display
  $("#MicButton").click(function () {
    ShowHood();
  });
});

