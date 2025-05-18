const videoElement = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const errorMessage = document.getElementById('errorMessage');
const startButton = document.getElementById('startButton');
const detectButton = document.getElementById('detectButton');
const popup = document.getElementById('popup');
const popupText = document.getElementById('popupText');
const detectedName = document.getElementById('detectedName');
const confirmButton = document.getElementById('confirmButton');
const cancelButton = document.getElementById('cancelButton');

let currentDetectedName = '';

async function startWebcam() {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = stream;
    startButton.style.display = 'none';
    detectButton.style.display = 'inline-block';
  } catch (err) {
    errorMessage.textContent = 'Webcam error: ' + err.message;
    errorMessage.style.display = 'block';
  }
}

function detectFace() {
  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  const ctx = canvas.getContext('2d');
  ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
  const base64Image = canvas.toDataURL('image/jpeg');

  fetch('/detect_face/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ image: base64Image })
  })
  .then(res => res.json())
  .then(data => {
    if (data.success) {
      currentDetectedName = data.name;
      detectedName.textContent = currentDetectedName;
      popup.style.display = 'block';
    } else {
      alert("Face not recognized.");
    }
  })
  .catch(err => {
    alert("Detection failed.");
    console.error(err);
  });
}

function confirmAttendance(){
 popup.style.display = 'none';
  fetch('/mark_attendance/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({ name: currentDetectedName })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
  })
  .catch(err => {
    console.error(err);
    alert("Failed to mark attendance.");
  });
}

// confirmButton.addEventListener('click', () => {
//   popup.style.display = 'none';
//   fetch('/confirm_attendance/', {
//     method: 'POST',
//     headers: {
//       'Content-Type': 'application/json',
//       'X-CSRFToken': getCookie('csrftoken')
//     },
//     body: JSON.stringify({ name: currentDetectedName })
//   })
//   .then(res => res.json())
//   .then(data => {
//     alert(data.message);
//   })
//   .catch(err => {
//     console.error(err);
//     alert("Failed to mark attendance.");
//   });
// });

cancelButton.addEventListener('click', () => {
  popup.style.display = 'none';
});


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

startButton.addEventListener('click', startWebcam);
detectButton.addEventListener('click', detectFace);
confirmButton.addEventListener('click', confirmAttendance)