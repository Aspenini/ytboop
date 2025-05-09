async function waitForYTBoop() {
  const status = document.getElementById("status");
  for (let i = 0; i < 10; i++) {
    try {
      const res = await fetch("http://localhost:5000/ping");
      if (res.ok) {
        status.textContent = "YTBoop is running!";
        return;
      }
    } catch (e) {}
    status.textContent = "Waiting for YTBoop to launch... (" + (10 - i) + "s)";
    await new Promise(r => setTimeout(r, 1000));
  }
  status.textContent = "YTBoop not detected. Please launch the app.";
}

waitForYTBoop();

function sendToYTBoop() {
  const url = document.getElementById("url").value;
  const type = document.getElementById("type").value;
  const format = document.getElementById("format").value;
  const status = document.getElementById("status");
  fetch("http://localhost:5000/download", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({ url, type, format })
  }).then(r => {
    if (r.ok) {
      status.textContent = "Download started! Check your Downloads folder.";
    } else {
      status.textContent = "Failed to download.";
    }
  }).catch(() => {
    status.textContent = "YTBoop is not running.";
  });
}
