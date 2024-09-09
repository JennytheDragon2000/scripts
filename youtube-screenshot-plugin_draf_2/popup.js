let currentCapture = null;

document.getElementById("captureBtn").addEventListener("click", () => {
  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    chrome.tabs.sendMessage(
      tabs[0].id,
      { action: "getTimeAndScreenshot" },
      (response) => {
        if (response && response.currentTime !== null) {
          currentCapture = response;
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

document.getElementById("saveNoteBtn").addEventListener("click", () => {
  if (!currentCapture) {
    alert("Please capture a screenshot first.");
    return;
  }

  const note = document.getElementById("noteInput").value;
  if (!note) {
    alert("Please enter a note.");
    return;
  }

  const savedNote = {
    time: currentCapture.currentTime,
    screenshot: currentCapture.screenshot,
    note: note,
  };

  chrome.storage.sync.get(["notes"], (result) => {
    const notes = result.notes || [];
    notes.push(savedNote);
    chrome.storage.sync.set({ notes: notes }, () => {
      console.log("Note saved:", savedNote);
      displaySavedNotes();
      document.getElementById("noteInput").value = "";
    });
  });
});

function displaySavedNotes() {
  chrome.storage.sync.get(["notes"], (result) => {
    const notes = result.notes || [];
    console.log("Retrieved notes:", notes);
    const savedNotesDiv = document.getElementById("savedNotes");
    savedNotesDiv.innerHTML = "<h2>Saved Notes:</h2>";
    if (notes.length === 0) {
      savedNotesDiv.innerHTML += "<p>No saved notes yet.</p>";
    } else {
      notes.forEach((note, index) => {
        savedNotesDiv.innerHTML += `
          <div class="saved-note">
            <p>Time: ${note.time.toFixed(2)} seconds</p>
            <p>Note: ${note.note}</p>
            <img src="${note.screenshot}" alt="Video Screenshot" style="max-width: 100%;">
            <button class="deleteNoteBtn" data-index="${index}">Delete</button>
          </div>
        `;
      });
    }

    // Add event listeners for delete buttons
    document.querySelectorAll(".deleteNoteBtn").forEach((button) => {
      button.addEventListener("click", (e) => {
        const index = parseInt(e.target.getAttribute("data-index"));
        deleteNote(index);
      });
    });
  });
}

function deleteNote(index) {
  chrome.storage.sync.get(["notes"], (result) => {
    const notes = result.notes || [];
    notes.splice(index, 1);
    chrome.storage.sync.set({ notes: notes }, () => {
      console.log("Note deleted, remaining notes:", notes);
      displaySavedNotes();
    });
  });
}

// Display saved notes when popup is opened
document.addEventListener("DOMContentLoaded", () => {
  displaySavedNotes();
});
