const STORAGE_KEY = "four-seasons-travel-memories";

requestAnimationFrame(() => {
  window.requestAnimationFrame(() => document.body.classList.add("is-ready"));
});

const form = document.getElementById("memory-form");
const imageInput = document.getElementById("memory-image");
const placeInput = document.getElementById("memory-place");
const activityInput = document.getElementById("memory-activity");
const status = document.getElementById("memory-status");
const grid = document.getElementById("memory-grid");

function loadMemories() {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    return Array.isArray(stored) ? stored : [];
  } catch (error) {
    return [];
  }
}

function saveMemories(memories) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(memories));
    return true;
  } catch (error) {
    status.textContent = "Storage is full. Delete an older memory and try again.";
    return false;
  }
}

function emptyState() {
  const paragraph = document.createElement("p");
  paragraph.className = "memory-empty";
  paragraph.textContent =
    "No memories yet. Add your first photograph above.";
  grid.appendChild(paragraph);
}

function createCard(memory) {
  const card = document.createElement("article");
  card.className = "memory-card";
  card.dataset.id = memory.id;

  const image = document.createElement("img");
  image.className = "memory-image";
  image.src = memory.image;
  image.alt = `${memory.place}: ${memory.activity}`;

  const body = document.createElement("div");
  body.className = "memory-card-body";

  const place = document.createElement("h2");
  place.className = "memory-place";
  place.textContent = memory.place;

  const activity = document.createElement("p");
  activity.className = "memory-activity";
  activity.textContent = memory.activity;

  const deleteButton = document.createElement("button");
  deleteButton.className = "memory-delete";
  deleteButton.type = "button";
  deleteButton.textContent = "Delete";

  body.append(place, activity, deleteButton);
  card.append(image, body);
  return card;
}

function renderMemories() {
  grid.replaceChildren();
  const memories = loadMemories();
  if (memories.length === 0) {
    emptyState();
    return;
  }
  memories.forEach((memory) => grid.appendChild(createCard(memory)));
}

function downscaleImage(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(new Error("Could not read the image."));
    reader.onload = () => {
      const image = new Image();
      image.onerror = () => reject(new Error("This file is not a valid image."));
      image.onload = () => {
        const maxWidth = 1000;
        const scale = Math.min(1, maxWidth / image.width);
        const canvas = document.createElement("canvas");
        canvas.width = Math.max(1, Math.round(image.width * scale));
        canvas.height = Math.max(1, Math.round(image.height * scale));
        const context = canvas.getContext("2d");
        context.drawImage(image, 0, 0, canvas.width, canvas.height);
        resolve(canvas.toDataURL("image/jpeg", 0.82));
      };
      image.src = reader.result;
    };
    reader.readAsDataURL(file);
  });
}

if (form && grid) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    status.textContent = "";

    if (!imageInput.files || imageInput.files.length === 0) {
      status.textContent = "Please choose a photograph.";
      return;
    }
    if (!placeInput.value.trim() || !activityInput.value.trim()) {
      status.textContent = "Please fill in both the place and the activity.";
      return;
    }

    const submitButton = form.querySelector(".memory-submit");
    submitButton.disabled = true;
    submitButton.textContent = "Saving...";

    try {
      const dataUrl = await downscaleImage(imageInput.files[0]);
      const memory = {
        id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
        image: dataUrl,
        place: placeInput.value.trim(),
        activity: activityInput.value.trim(),
      };
      const memories = loadMemories();
      memories.unshift(memory);
      if (saveMemories(memories)) {
        form.reset();
        status.textContent = "Memory saved on this device.";
        renderMemories();
      }
    } catch (error) {
      status.textContent = error.message || "Something went wrong.";
    } finally {
      submitButton.disabled = false;
      submitButton.textContent = "Add memory";
    }
  });

  grid.addEventListener("click", (event) => {
    const deleteButton = event.target.closest(".memory-delete");
    if (!deleteButton) {
      return;
    }
    const card = deleteButton.closest(".memory-card");
    if (!card) {
      return;
    }
    const memories = loadMemories().filter(
      (memory) => memory.id !== card.dataset.id
    );
    saveMemories(memories);
    renderMemories();
    status.textContent = "Memory deleted.";
  });

  renderMemories();
}
