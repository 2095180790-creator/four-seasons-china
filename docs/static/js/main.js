const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

requestAnimationFrame(() => {
  window.requestAnimationFrame(() => document.body.classList.add("is-ready"));
});

window.addEventListener("pageshow", () => {
  document.body.classList.remove("is-leaving");
});

for (const card of document.querySelectorAll("[data-season-card]")) {
  if (reduceMotion) {
    continue;
  }

  card.addEventListener("pointermove", (event) => {
    const bounds = card.getBoundingClientRect();
    card.style.setProperty("--mx", `${event.clientX - bounds.left}px`);
    card.style.setProperty("--my", `${event.clientY - bounds.top}px`);
  });
}

document.querySelectorAll("[data-page-transition]").forEach((link) => {
  link.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }
    document.body.classList.add("is-leaving");
  });
});

const activityList = document.querySelector("[data-activity-list]");

if (activityList) {
  const slug = activityList.dataset.slug;
  const storageKey = `four-seasons-activities-${slug}`;
  const customKey = `four-seasons-custom-activities-${slug}`;
  const deletedKey = `four-seasons-deleted-activities-${slug}`;
  const boxes = Array.from(activityList.querySelectorAll("[data-activity]"));
  const count = activityList.querySelector("[data-activity-count]");
  const total = activityList.querySelector("[data-activity-total]");

  const updateActivityCount = () => {
    const visibleBoxes = Array.from(
      activityList.querySelectorAll(".activity-row:not([hidden]) [data-activity]")
    );
    const done = visibleBoxes.filter((box) => box.checked).length;
    if (count) {
      count.textContent = String(done);
    }
    if (total) {
      total.textContent = String(visibleBoxes.length);
    }
  };

  const saveActivityState = () => {
    const state = boxes.map((box) => box.checked);
    try {
      localStorage.setItem(storageKey, JSON.stringify(state));
    } catch (error) {
      // Local storage can be unavailable in private browsing.
    }
  };

  let savedState = [];
  try {
    savedState = JSON.parse(localStorage.getItem(storageKey) || "[]");
  } catch (error) {
    savedState = [];
  }

  boxes.forEach((box, index) => {
    box.checked = Boolean(savedState[index]);
    box.closest(".activity-item")?.classList.toggle("is-done", box.checked);
    box.addEventListener("change", () => {
      box.closest(".activity-item")?.classList.toggle("is-done", box.checked);
      updateActivityCount();
      saveActivityState();
    });
  });

  updateActivityCount();

  const loadDeletedActivities = () => {
    try {
      const stored = JSON.parse(localStorage.getItem(deletedKey) || "[]");
      return Array.isArray(stored) ? stored : [];
    } catch (error) {
      return [];
    }
  };

  const saveDeletedActivities = (items) => {
    try {
      localStorage.setItem(deletedKey, JSON.stringify(items));
    } catch (error) {
      // Local storage can be unavailable in private browsing.
    }
  };

  const deletedIds = new Set(loadDeletedActivities());
  activityList.querySelectorAll(".activity-row").forEach((row) => {
    row.hidden = deletedIds.has(row.dataset.builtinId);
  });

  activityList.querySelectorAll("[data-delete-builtin]").forEach((button) => {
    button.addEventListener("click", () => {
      const row = button.closest(".activity-row");
      if (!row) {
        return;
      }
      const id = row.dataset.builtinId;
      const items = loadDeletedActivities();
      if (!items.includes(id)) {
        items.push(id);
      }
      saveDeletedActivities(items);
      row.hidden = true;
      updateActivityCount();
    });
  });

  const restoreButton = activityList.querySelector("[data-restore-activities]");
  restoreButton?.addEventListener("click", () => {
    try {
      localStorage.removeItem(deletedKey);
    } catch (error) {
      // Ignore storage errors when restoring.
    }
    window.location.reload();
  });

  const customSection = activityList.querySelector("[data-custom-activities]");
  if (customSection) {
    const customInput = customSection.querySelector(".custom-activity-input");
    const customAdd = customSection.querySelector(".custom-activity-add");
    const customList = customSection.querySelector("[data-custom-list]");

    const loadCustomActivities = () => {
      try {
        const stored = JSON.parse(localStorage.getItem(customKey) || "[]");
        return Array.isArray(stored) ? stored : [];
      } catch (error) {
        return [];
      }
    };

    const saveCustomActivities = (items) => {
      try {
        localStorage.setItem(customKey, JSON.stringify(items));
      } catch (error) {
        // Local storage can be unavailable in private browsing.
      }
    };

    const renderCustomActivities = () => {
      customList.replaceChildren();
      loadCustomActivities().forEach((item, index) => {
        const listItem = document.createElement("li");
        const text = document.createElement("span");
        text.className = "custom-activity-text";
        text.textContent = item;

        const deleteButton = document.createElement("button");
        deleteButton.className = "custom-activity-delete";
        deleteButton.type = "button";
        deleteButton.textContent = "Delete";
        deleteButton.dataset.index = String(index);

        listItem.append(text, deleteButton);
        customList.appendChild(listItem);
      });
    };

    customAdd.addEventListener("click", () => {
      const value = customInput.value.trim();
      if (!value) {
        return;
      }
      const items = loadCustomActivities();
      items.push(value);
      saveCustomActivities(items);
      customInput.value = "";
      renderCustomActivities();
    });

    customList.addEventListener("click", (event) => {
      const button = event.target.closest(".custom-activity-delete");
      if (!button) {
        return;
      }
      const items = loadCustomActivities();
      items.splice(Number(button.dataset.index), 1);
      saveCustomActivities(items);
      renderCustomActivities();
    });

    renderCustomActivities();
  }
}

const lightbox = document.querySelector("[data-lightbox]");
const lightboxTrigger = document.querySelector("[data-lightbox-trigger]");

const openLightbox = () => {
  if (!lightbox || !lightboxTrigger) {
    return;
  }
  const sourceImage = lightboxTrigger.querySelector("img");
  const lightboxImage = lightbox.querySelector("[data-lightbox-image]");
  if (!sourceImage || !lightboxImage) {
    return;
  }
  lightboxImage.src = sourceImage.currentSrc || sourceImage.src;
  lightboxImage.alt = sourceImage.alt;
  lightbox.hidden = false;
  document.body.classList.add("lightbox-open");
  lightbox.querySelector(".lightbox-close")?.focus();
};

const closeLightbox = () => {
  if (!lightbox) {
    return;
  }
  lightbox.hidden = true;
  document.body.classList.remove("lightbox-open");
  lightboxTrigger?.focus();
};

if (lightboxTrigger && lightbox) {
  lightboxTrigger.addEventListener("click", openLightbox);
  lightboxTrigger.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openLightbox();
    }
  });

  lightbox.querySelector(".lightbox-close")?.addEventListener("click", closeLightbox);
  lightbox.addEventListener("click", (event) => {
    if (event.target === lightbox) {
      closeLightbox();
    }
  });
}

const seasonControls = document.querySelector("[data-season-controls]");
const seasonGrid = document.querySelector("[data-season-grid]");

if (seasonControls && seasonGrid) {
  const cards = Array.from(seasonGrid.querySelectorAll(".season-card"));
  let currentFilter = "all";
  let sortAscending = false;

  const filterButtons = Array.from(
    seasonControls.querySelectorAll("[data-filter]")
  );
  const sortButton = seasonControls.querySelector("[data-sort-toggle]");

  filterButtons.forEach((button) => {
    button.addEventListener("click", () => {
      currentFilter = button.dataset.filter;
      filterButtons.forEach((item) => {
        const active = item === button;
        item.classList.toggle("is-active", active);
        item.setAttribute("aria-pressed", String(active));
      });
      cards.forEach((card) => {
        const show =
          currentFilter === "all" || card.dataset.season === currentFilter;
        card.classList.toggle("is-hidden", !show);
      });
    });
  });

  sortButton?.addEventListener("click", () => {
    sortAscending = !sortAscending;
    sortButton.setAttribute("aria-pressed", String(sortAscending));
    sortButton.textContent = sortAscending ? "Sort Z–A" : "Sort A–Z";
    const sorted = [...cards].sort((first, second) => {
      const result = first.dataset.name.localeCompare(second.dataset.name);
      return sortAscending ? result : -result;
    });
    sorted.forEach((card) => seasonGrid.appendChild(card));
  });
}

const seasonView = document.querySelector(".season-view");

if (seasonView) {
  const previousUrl = seasonView.dataset.previousUrl;
  const nextUrl = seasonView.dataset.nextUrl;
  const homeUrl = seasonView.dataset.homeUrl || "/";

  document.addEventListener("keydown", (event) => {
    if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
      return;
    }

    if (event.key === "Escape" && lightbox && !lightbox.hidden) {
      closeLightbox();
      return;
    }

    if (event.key === "ArrowLeft" && previousUrl) {
      window.location.assign(previousUrl);
    }
    if (event.key === "ArrowRight" && nextUrl) {
      window.location.assign(nextUrl);
    }
    if (event.key === "Escape") {
      window.location.assign(homeUrl);
    }
  });

  let touchStartX = 0;
  let touchStartY = 0;

  seasonView.addEventListener(
    "touchstart",
    (event) => {
      const touch = event.changedTouches[0];
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
    },
    { passive: true }
  );

  seasonView.addEventListener(
    "touchend",
    (event) => {
      const touch = event.changedTouches[0];
      const deltaX = touch.clientX - touchStartX;
      const deltaY = touch.clientY - touchStartY;

      if (Math.abs(deltaX) < 65 || Math.abs(deltaX) < Math.abs(deltaY) * 1.25) {
        return;
      }

      window.location.assign(deltaX > 0 ? previousUrl : nextUrl);
    },
    { passive: true }
  );
} else {
  const seasonLinks = Array.from(document.querySelectorAll(".season-card"));

  document.addEventListener("keydown", (event) => {
    const index = Number(event.key) - 1;
    if (index >= 0 && index < seasonLinks.length) {
      seasonLinks[index].click();
    }
  });
}
