/**
 * =============================================================
 * TEGQ // APP INTERACTION CONTROLLER
 * Matching the elegant editorial aesthetic of the reference
 * =============================================================
 */

window.TEGQ_PHONE = "573167755887";
window.TEGQ_EMAIL = "tomasestebangonzalezquintero@gmail.com";

document.addEventListener("DOMContentLoaded", () => {
  let soundActive = true;

  // Elements
  const contactModal = document.getElementById("contact-modal");
  const contactForm = document.getElementById("contact-form");
  const formStatus = document.getElementById("form-status");
  const btnCloseModal = document.getElementById("btn-close-modal");
  const btnOpenContact = document.getElementById("btn-open-contact");
  const navBtnContact = document.getElementById("nav-btn-contact");
  const btnWhatsappDirect = document.getElementById("btn-whatsapp-direct");
  const btnToggleSound = document.getElementById("btn-toggle-sound");
  const brandHome = document.getElementById("brand-home");

  const navLinks = document.querySelectorAll(".nav-link");
  const pillBars = document.querySelectorAll(".pill-bar");

  /* -----------------------------------------------------------
     1. INITIALIZE 3D BOOK ENGINE
  ----------------------------------------------------------- */
  let bookApp = null;

  if (typeof Book3DApp !== "undefined") {
    bookApp = new Book3DApp("book-viewport", {
      soundEnabled: soundActive,
      onLoadComplete: () => {
        // App ready
      },
      onPageChange: (currentSpread) => {
        updateUIState(currentSpread);
      },
      onInteractiveClick: (spread, side) => {
        if (spread === 4) {
          openContactModal();
        } else if (spread === 2) {
          window.open("https://github.com/TEstebanGQ", "_blank");
        } else if (spread === 3) {
          window.open("https://github.com/TEstebanGQ", "_blank");
        }
      }
    });
    window.bookApp = bookApp;
  }

  /* -----------------------------------------------------------
     2. UI STATE UPDATES (PILLS & NAV HIGHLIGHTS)
  ----------------------------------------------------------- */
  function updateUIState(spread) {
    // Update bottom pill indicators
    pillBars.forEach((pill) => {
      const pSpread = parseInt(pill.dataset.spread, 10);
      pill.classList.toggle("is-active", pSpread === spread);
    });

    // Update top nav links
    navLinks.forEach((link) => {
      const lSpread = parseInt(link.dataset.spread, 10);
      if (link.id === "nav-btn-contact") {
        link.classList.toggle("is-active", spread === 4);
      } else if (lSpread === spread || (lSpread === 2 && spread === 3)) {
        link.classList.add("is-active");
      } else {
        link.classList.remove("is-active");
      }
    });
  }

  // Nav link clicks
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      const targetSpread = parseInt(link.dataset.spread, 10);
      if (link.id === "nav-btn-contact") {
        if (bookApp) bookApp.jumpToSpread(4);
        setTimeout(() => openContactModal(), 400);
      } else if (bookApp) {
        bookApp.jumpToSpread(targetSpread);
      }
    });
  });

  // Bottom pill clicks
  pillBars.forEach((pill) => {
    pill.addEventListener("click", () => {
      const idx = parseInt(pill.dataset.spread, 10);
      if (bookApp) bookApp.jumpToSpread(idx);
    });
  });

  // Brand click -> Cover
  if (brandHome) {
    brandHome.addEventListener("click", () => {
      if (bookApp) bookApp.jumpToSpread(0);
    });
  }

  /* -----------------------------------------------------------
     3. SOUND CONTROLLER
  ----------------------------------------------------------- */
  if (btnToggleSound) {
    btnToggleSound.addEventListener("click", () => {
      soundActive = !soundActive;
      if (bookApp) bookApp.options.soundEnabled = soundActive;
      btnToggleSound.textContent = soundActive ? "🔊" : "🔇";
      btnToggleSound.title = soundActive ? "Silenciar" : "Activar sonido";
    });
  }

  /* -----------------------------------------------------------
     4. CONTACT MODAL & WHATSAPP
  ----------------------------------------------------------- */
  function openContactModal() {
    if (contactModal) contactModal.classList.add("is-open");
  }

  function closeContactModal() {
    if (contactModal) contactModal.classList.remove("is-open");
  }

  if (btnOpenContact) btnOpenContact.addEventListener("click", openContactModal);
  if (btnCloseModal) btnCloseModal.addEventListener("click", closeContactModal);

  if (contactModal) {
    contactModal.addEventListener("click", (e) => {
      if (e.target === contactModal) closeContactModal();
    });
  }

  function getFormData() {
    return {
      reason: document.getElementById("form-reason")?.value || "Consulta General",
      name: document.getElementById("form-name")?.value || "",
      phone: document.getElementById("form-phone")?.value || "",
      email: document.getElementById("form-email")?.value || "",
      message: document.getElementById("form-message")?.value || ""
    };
  }

  function constructWhatsAppUrl(data) {
    const text =
      `*Hola Tomás, te escribo desde tu portafolio web.*\n\n` +
      `📌 *Motivo:* ${data.reason}\n` +
      `👤 *Nombre:* ${data.name || "No especificado"}\n` +
      `📱 *Teléfono:* ${data.phone || "No especificado"}\n` +
      `📧 *Correo:* ${data.email || "No especificado"}\n\n` +
      `📝 *Mensaje:* \n${data.message || "Hola, me interesa conversar sobre una oportunidad de desarrollo."}`;

    return `https://wa.me/${window.TEGQ_PHONE}?text=${encodeURIComponent(text)}`;
  }

  if (btnWhatsappDirect) {
    btnWhatsappDirect.addEventListener("click", () => {
      const data = getFormData();
      const url = constructWhatsAppUrl(data);
      window.open(url, "_blank");
    });
  }

  if (contactForm) {
    contactForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const formData = new FormData(contactForm);
      const submitBtn = contactForm.querySelector(".form-btn-submit");
      const originalText = submitBtn.innerHTML;

      submitBtn.innerHTML = `⏳ ENVIANDO...`;
      submitBtn.disabled = true;

      fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams(formData).toString()
      })
        .then(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
          if (formStatus) {
            formStatus.className = "form-status is-success";
            formStatus.innerHTML = `✓ ¡Mensaje enviado con éxito a Tomás! También puedes contactarlo por WhatsApp.`;
          }
          contactForm.reset();
        })
        .catch(() => {
          submitBtn.innerHTML = originalText;
          submitBtn.disabled = false;
          if (formStatus) {
            formStatus.className = "form-status is-success";
            formStatus.innerHTML = `✓ Mensaje preparado. Pulsa abajo para enviarlo directo a WhatsApp.`;
          }
        });
    });
  }
});