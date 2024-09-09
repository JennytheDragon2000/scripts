document.getElementById("captureBtn").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { action: "getTimeAndScreenshot" },
      (response) => {
        if (response && response.currentTime !== null) {
          const resultDiv = document.getElementById("result");
          resultDiv.innerHTML = `
          <p>Current Time: ${response.currentTime.toFixed(2)} seconds</p>
          <img src="${response.screenshot}" alt="Video Screenshot" style="max-width: 100%;">
        `;
        } else {
          alert(
            "Unable to capture time and screenshot. Make sure you are on a YouTube video page.",
          );
        }
      },
    );
  });
});
