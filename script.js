/* =============================================================
   TEGQ // PORTFOLIO  ·  GSAP-driven interactions
   ============================================================= */

document.addEventListener("DOMContentLoaded", () => {
  /* ----------------------------------------------------------
     0. UPDATE FOOTER DATE  (runs even if GSAP fails to load)
  ---------------------------------------------------------- */
  const updateEl = document.getElementById("lastUpdate");
  if (updateEl) {
    const now = new Date();
    const months = ["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"];
    updateEl.textContent = `${months[now.getMonth()]} ${now.getFullYear()}`;
  }

  /* ----------------------------------------------------------
     0.5  GSAP GUARD — graceful degradation if CDN fails
  ---------------------------------------------------------- */
  if (typeof gsap === "undefined") {
    console.warn("GSAP failed to load — page will render without animations.");
    document.documentElement.classList.add("no-gsap");
    // Still wire up the mobile nav toggle so navigation works
    const navEl = document.querySelector(".nav");
    const navToggleEl = document.querySelector(".nav__toggle");
    if (navToggleEl) {
      navToggleEl.addEventListener("click", () => navEl.classList.toggle("is-open"));
    }
    return;
  }

  // Register GSAP plugins
  gsap.registerPlugin(ScrollTrigger);

  /* ----------------------------------------------------------
     1. CUSTOM CURSOR  (desktop only)
  ---------------------------------------------------------- */
  const isFinePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
  if (isFinePointer) {
    const cursor = document.querySelector(".cursor");
    const ring = cursor.querySelector(".cursor__ring");
    let mx = window.innerWidth / 2, my = window.innerHeight / 2;
    let rx = mx, ry = my;

    window.addEventListener("mousemove", e => {
      mx = e.clientX;
      my = e.clientY;
      gsap.to(cursor, { x: mx, y: my, duration: 0.12, ease: "power2.out" });
    });

    // Smooth ring trailing
    gsap.ticker.add(() => {
      rx += (mx - rx) * 0.18;
      ry += (my - ry) * 0.18;
      gsap.set(ring, { x: rx - mx, y: ry - my });
    });

    // Hover state on links/buttons
    document.querySelectorAll("a, button, [data-magnetic], [data-link]").forEach(el => {
      el.addEventListener("mouseenter", () => cursor.classList.add("is-hovering"));
      el.addEventListener("mouseleave", () => cursor.classList.remove("is-hovering"));
    });

    /* ----------------------------------------------------------
       2. MAGNETIC ELEMENTS  (desktop only)
    ---------------------------------------------------------- */
    document.querySelectorAll("[data-magnetic]").forEach(el => {
      const strength = 0.35;
      el.addEventListener("mousemove", e => {
        const rect = el.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        gsap.to(el, { x: x * strength, y: y * strength, duration: 0.4, ease: "power3.out" });
      });
      el.addEventListener("mouseleave", () => {
        gsap.to(el, { x: 0, y: 0, duration: 0.6, ease: "elastic.out(1, 0.4)" });
      });
    });
  }

  /* ----------------------------------------------------------
     3. NAV TOGGLE (mobile)
  ---------------------------------------------------------- */
  const nav = document.querySelector(".nav");
  const navToggle = document.querySelector(".nav__toggle");
  if (navToggle) {
    navToggle.addEventListener("click", () => {
      nav.classList.toggle("is-open");
    });
    document.querySelectorAll(".nav__list a").forEach(a => {
      a.addEventListener("click", () => nav.classList.remove("is-open"));
    });
  }

  /* ----------------------------------------------------------
     4. HERO ENTRANCE TIMELINE
  ---------------------------------------------------------- */
  // Helper to split words into chars manually
  const splitChars = el => {
    const text = el.dataset.text || el.textContent;
    el.textContent = "";
    const chars = [];
    [...text].forEach(ch => {
      const span = document.createElement("span");
      span.className = "char";
      span.style.display = "inline-block";
      span.textContent = ch === " " ? "\u00A0" : ch;
      el.appendChild(span);
      chars.push(span);
    });
    return chars;
  };

  const titleWords = document.querySelectorAll(".hero__title .word");
  const allChars = [];
  titleWords.forEach(w => {
    splitChars(w).forEach(c => allChars.push(c));
  });

  // Initial state
  gsap.set(allChars, { yPercent: 110, opacity: 0 });
  gsap.set(".hero__meta .meta-line", { y: -20, opacity: 0 });
  gsap.set(".role-card", { scale: 0.6, opacity: 0, rotation: -10 });
  gsap.set(".hero__intro", { x: 30, opacity: 0 });
  gsap.set(".hero__cta .btn", { y: 20, opacity: 0 });
  gsap.set(".sticker", { scale: 0, opacity: 0 });
  gsap.set(".hero__scroll", { opacity: 0 });
  gsap.set(".hero__grid", { opacity: 0 });

  const tl = gsap.timeline({ defaults: { ease: "power3.out" } });

  tl.to(".hero__grid", { opacity: 1, duration: 1.2 }, 0)
    .to(".hero__meta .meta-line", { y: 0, opacity: 1, duration: 0.6, stagger: 0.08 }, 0.1)
    .to(allChars, {
      yPercent: 0,
      opacity: 1,
      duration: 0.9,
      ease: "power4.out",
      stagger: { amount: 0.6, from: "start" }
    }, 0.25)
    .to(".role-card", {
      scale: 1, opacity: 1, rotation: -2,
      duration: 0.7, ease: "back.out(2)"
    }, 0.85)
    .to(".hero__intro", { x: 0, opacity: 1, duration: 0.7 }, 0.95)
    .to(".hero__cta .btn", { y: 0, opacity: 1, duration: 0.5, stagger: 0.1 }, 1.05)
    .to(".sticker--1", { scale: 1, opacity: 1, rotation: 8, duration: 0.5, ease: "back.out(2)" }, 1.2)
    .to(".sticker--2", { scale: 1, opacity: 1, rotation: -6, duration: 0.5, ease: "back.out(2)" }, 1.3)
    .to(".hero__scroll", { opacity: 1, duration: 0.6 }, 1.4);

  /* ----------------------------------------------------------
     5. STICKER FLOAT (continuous)
  ---------------------------------------------------------- */
  gsap.to(".sticker--1", {
    y: 12, rotation: 12,
    duration: 2.4, ease: "sine.inOut",
    repeat: -1, yoyo: true
  });
  gsap.to(".sticker--2", {
    y: -10, rotation: -2,
    duration: 2.8, ease: "sine.inOut",
    repeat: -1, yoyo: true
  });

  /* ----------------------------------------------------------
     6. SECTION HEADERS — slide in
  ---------------------------------------------------------- */
  document.querySelectorAll(".section-head").forEach(head => {
    gsap.from(head.children, {
      scrollTrigger: {
        trigger: head,
        start: "top 85%",
      },
      y: 30,
      opacity: 0,
      duration: 0.7,
      stagger: 0.08,
      ease: "power3.out"
    });
  });

  /* ----------------------------------------------------------
     7. ABOUT — text reveal & info-blocks pop
  ---------------------------------------------------------- */
  document.querySelectorAll(".reveal-text").forEach(p => {
    gsap.from(p, {
      scrollTrigger: { trigger: p, start: "top 88%" },
      y: 30,
      opacity: 0,
      duration: 0.9,
      ease: "power3.out"
    });
  });

  gsap.from(".info-block", {
    scrollTrigger: { trigger: ".about__col--side", start: "top 80%" },
    scale: 0.7,
    opacity: 0,
    duration: 0.6,
    stagger: 0.1,
    ease: "back.out(1.6)"
  });

  /* ----------------------------------------------------------
     8. PROJECTS — staggered reveal + parallax-ish
  ---------------------------------------------------------- */
  document.querySelectorAll("[data-project]").forEach(proj => {
    const visual = proj.querySelector(".project__visual");
    const content = proj.querySelector(".project__content");
    const isRight = proj.classList.contains("project--right");

    gsap.from(visual, {
      scrollTrigger: { trigger: proj, start: "top 80%" },
      x: isRight ? 60 : -60,
      opacity: 0,
      duration: 0.9,
      ease: "power3.out"
    });

    gsap.from(content.children, {
      scrollTrigger: { trigger: proj, start: "top 80%" },
      y: 30,
      opacity: 0,
      duration: 0.6,
      stagger: 0.1,
      ease: "power3.out",
      delay: 0.15
    });

    // subtle parallax on the visual
    gsap.to(visual, {
      yPercent: -6,
      ease: "none",
      scrollTrigger: {
        trigger: proj,
        start: "top bottom",
        end: "bottom top",
        scrub: true
      }
    });
  });

  /* ----------------------------------------------------------
     9. STACK CARDS — flip in
  ---------------------------------------------------------- */
  gsap.from(".stack-card", {
    scrollTrigger: { trigger: ".stack__grid", start: "top 80%" },
    y: 50,
    opacity: 0,
    rotateX: -25,
    transformPerspective: 600,
    transformOrigin: "top center",
    duration: 0.7,
    stagger: 0.08,
    ease: "power3.out"
  });

  /* ----------------------------------------------------------
     10. CONTACT HERO — explosive reveal
  ---------------------------------------------------------- */
  const contactLines = document.querySelectorAll(".contact__line");
  contactLines.forEach((line, i) => {
    gsap.from(line, {
      scrollTrigger: { trigger: ".contact__hero", start: "top 75%" },
      y: 80,
      opacity: 0,
      skewY: i === 0 ? 5 : -5,
      duration: 0.9,
      delay: i * 0.12,
      ease: "power4.out"
    });
  });

  gsap.from(".contact-card", {
    scrollTrigger: { trigger: ".contact__grid", start: "top 80%" },
    y: 40,
    opacity: 0,
    duration: 0.6,
    stagger: 0.08,
    ease: "power3.out"
  });

  /* ----------------------------------------------------------
     11. FOOTER BIG TEXT — horizontal scroll-driven
  ---------------------------------------------------------- */
  const footerBig = document.querySelector(".footer__big span");
  if (footerBig) {
    gsap.fromTo(footerBig, { x: 80 }, {
      x: -80,
      ease: "none",
      scrollTrigger: {
        trigger: ".footer",
        start: "top bottom",
        end: "bottom top",
        scrub: true
      }
    });
  }

  /* ----------------------------------------------------------
     12. SCRAMBLE EFFECT on title chars (hover)  — desktop only
  ---------------------------------------------------------- */
  if (isFinePointer) {
    const scrambleChars = "!<>-_\\/[]{}—=+*^?#";
    titleWords.forEach(word => {
      word.addEventListener("mouseenter", () => {
        const chars = word.querySelectorAll(".char");
        chars.forEach((c, i) => {
          const original = c.textContent;
          let frame = 0;
          const interval = setInterval(() => {
            c.textContent = scrambleChars[Math.floor(Math.random() * scrambleChars.length)];
            frame++;
            if (frame > 4 + i % 4) {
              clearInterval(interval);
              c.textContent = original;
            }
          }, 35);
        });
      });
    });
  }

  /* ----------------------------------------------------------
     13. REFRESH ScrollTrigger after load
  ---------------------------------------------------------- */
  window.addEventListener("load", () => ScrollTrigger.refresh());
});