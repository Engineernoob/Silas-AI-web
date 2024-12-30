document.addEventListener("DOMContentLoaded", function () {
  console.log("Document ready");

  // Play startup audio by calling the backend API
  fetch("http://localhost:3000/api/startup-audio")
    .then((response) => response.json())
    .then((data) => {
      console.log(data.message); // Log success message
    })
    .catch((error) => {
      console.error("Error playing startup audio:", error);
    });

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

// Mic button click event with speech recognition and backend communication
$("#MicButton").click(function () {
  console.log("Mic button clicked");

  // Check if browser supports Web Speech API
  if (!("webkitSpeechRecognition" in window)) {
    alert("Speech Recognition is not supported in your browser. Please use Google Chrome.");
    return;
  }

  // Initialize SpeechRecognition
  const recognition = new webkitSpeechRecognition();
  recognition.continuous = false; // Stop after one result
  recognition.interimResults = false; // Don't show partial results
  recognition.lang = "en-US"; // Set recognition language

  // Start recognition
  recognition.start();

  // Handle recognition result
  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript; // Get the spoken words
    console.log("You said:", transcript);

    // Display the recognized text in the input box
    $("#chatbox").val(transcript);

    // Send the recognized text to the backend
    fetch("http://localhost:3000/api/message", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: transcript }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Backend response:", data.response);

        // Update Siri message with the backend response
        $(".siri-message").text(data.response);

        // Show Siri Wave animation
        $("#Oval").attr("hidden", true);
        $("#siriwave").attr("hidden", false);
      })
      .catch((error) => {
        console.error("Error sending message to backend:", error);
      });
  };

  // Handle recognition errors
  recognition.onerror = function (event) {
    console.error("Speech recognition error:", event.error);
  };

  // Handle recognition end
  recognition.onend = function () {
    console.log("Speech recognition ended");
  };
});

// Activate Siri Wave
siriWave.start();
siriWave.setAmplitude(2);
siriWave.setSpeed(0.2);
