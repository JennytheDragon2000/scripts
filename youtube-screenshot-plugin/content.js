function getCurrentTime() {
  const video = document.querySelector("video");
  return video ? video.currentTime : null;
}

function captureScreenshot() {
  const video = document.querySelector("video");
  if (!video) return null;

  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
  return canvas.toDataURL("image/png");
}

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getTimeAndScreenshot") {
    const currentTime = getCurrentTime();
    const screenshot = captureScreenshot();
    sendResponse({ currentTime, screenshot });
  }
});
