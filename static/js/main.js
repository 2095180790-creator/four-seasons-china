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

const seasonView = document.querySelector(".season-view");

if (seasonView) {
  const previousUrl = seasonView.dataset.previousUrl;
  const nextUrl = seasonView.dataset.nextUrl;

  document.addEventListener("keydown", (event) => {
    if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) {
      return;
    }

    if (event.key === "ArrowLeft" && previousUrl) {
      window.location.assign(previousUrl);
    }
    if (event.key === "ArrowRight" && nextUrl) {
      window.location.assign(nextUrl);
    }
    if (event.key === "Escape") {
      window.location.assign("/");
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
