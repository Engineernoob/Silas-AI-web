document.addEventListener("DOMContentLoaded", function () {
  console.log("Document ready");

  // Select the text element for animation
  const text = document.querySelector(".ask-anything");

  // Create a GSAP timeline for a more complex animation
  const tl = gsap.timeline({ repeat: -1, repeatDelay: 2 });

  // Add fade in and scaling animation
  tl.fromTo(
    text,
    { opacity: 0, scale: 0.8, y: 20 }, // Initial state: transparent, smaller, and moved down slightly
    { opacity: 1, scale: 1, y: 0, duration: 1.5, ease: "power3.out" } // End state: fully visible, normal size, original position
  );

  // Add a slight bounce for effect
  tl.to(text, {
    scale: 1.1,
    duration: 0.8,
    ease: "bounce.out",
  }).to(text, {
    scale: 1,
    duration: 0.4,
  });

  // Fade out before restarting
  tl.to(text, {
    opacity: 0,
    duration: 1,
    ease: "power3.in",
  });
});

// Siri Wave
var siriWave = new SiriWave({
  container: document.getElementById("siri-container"),
  width: 800,
  height: 200,
  style: "ios9",
  amplitude: 1,
  speed: 0.2,
  autostart: true,
});
// Siri Message animation
document.addEventListener("DOMContentLoaded", function () {
  console.log("Document ready");

  // Select the text element for animation
  const text = document.querySelector(".siri-message");

  // Create a GSAP timeline for a smooth animation
  const tl = gsap.timeline({ repeat: -1, repeatDelay: 1 });

  // Initial state
  tl.set(text, { opacity: 0, y: 20 });

  // Fade in and slide up animation
  tl.to(text, {
    opacity: 1,
    y: 0,
    duration: 2,
    ease: "power2.out",
  });

  // Hold the text visible
  tl.to(text, { duration: 3 });

  // Fade out and slide down animation
  tl.to(text, {
    opacity: 0,
    y: 20,
    duration: 2,
    ease: "power2.in",
  });
});

// mic button click event
$("#MicButton").click(function () {
  eel.playAssistantAudio();
  $("#Oval").attr("hidden", true);
  $("#siriwave").attr("hidden", false);
  eel.allCommands()();
});

// Activate Siri Wave
siriWave.start();

siriWave.setAmplitude(2);
siriWave.setSpeed(0.2);
