const videoElement = document.getElementById('webcam');
const canvas = document.getElementById('canvas');
const errorMessage = document.getElementById('errorMessage');
const startButton = document.getElementById('startButton');
const captureButton = document.getElementById('captureButton');
const nameInput = document.getElementById('name');

async function startWebcam() {
  errorMessage.style.display = 'none';
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
    videoElement.srcObject = stream;
    startButton.style.display = 'none';
    captureButton.style.display = 'inline-block';
  } catch (err) {
    errorMessage.textContent = 'Error accessing webcam: ' + err.message;
    errorMessage.style.display = 'block';
  }
}

function captureAndSend() {
  const name = nameInput.value.trim();
  if (!name) {
    alert("Please enter your name before capturing.");
    return;
  }

  canvas.width = videoElement.videoWidth;
  canvas.height = videoElement.videoHeight;
  const context = canvas.getContext('2d');
  context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

  const base64Image = canvas.toDataURL('image/jpeg');

  fetch('register_face/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },  
    body: JSON.stringify({
      name: name,
      image: base64Image
    })
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message);
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Failed to send image.');
  });
}

// Helper: Get CSRF Token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

startButton.addEventListener('click', startWebcam);
captureButton.addEventListener('click', captureAndSend);
