/**
 * AeroResilience Master Keynote Presentation Deck Controller
 * Features:
 *  - 3D Atmospheric Aerosol Particle Engine & Vector Field (3d-web-experience)
 *  - 3D Card Parallax Tilt & Dynamic Specular Glint (better-ui)
 *  - Apple Keynote Fluid Gestures & Settle Springs (apple-design)
 *  - Keynote Light Table Slide Grid Modal (Mission Control)
 *  - Presenter Teleprompter Notes Drawer
 *  - Diurnal Atmospheric Inversion Simulator Widget (Slide 2)
 *  - Interactive Direct Impact Calculator Widget (Slide 12)
 *  - WCAG 2.1 AA Screen Reader Live Region Announcer
 */

document.addEventListener('DOMContentLoaded', () => {
  // -------------------------------------------------------------
  // 1. High-Performance 3D Atmospheric Particle Engine (3d-web-experience)
  // -------------------------------------------------------------
  const canvas = document.getElementById('atmosphere-canvas');
  const ctx = canvas ? canvas.getContext('2d') : null;
  let width = window.innerWidth;
  let height = window.innerHeight;
  let particles = [];
  const PARTICLE_COUNT = 90;
  let mouseX = width / 2;
  let mouseY = height / 2;
  let targetMouseX = width / 2;
  let targetMouseY = height / 2;
  let currentSlide = 1;
  let animationFrameId = null;

  function resizeCanvas() {
    if (!canvas) return;
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
  }
  window.addEventListener('resize', resizeCanvas);
  resizeCanvas();

  // Aerosol Particle Definition in 3D Space
  class Particle3D {
    constructor() {
      this.reset();
    }
    reset() {
      this.x = (Math.random() - 0.5) * width * 1.5;
      this.y = (Math.random() - 0.5) * height * 1.5;
      this.z = Math.random() * 800 + 200; // Depth coordinate
      this.vx = (Math.random() - 0.5) * 0.6;
      this.vy = (Math.random() - 0.5) * 0.4;
      this.vz = (Math.random() - 0.5) * 0.5;
      this.baseRadius = Math.random() * 2.2 + 1.0;
      // Color based on aerosol chemistry: Sky (clean), Amber (NO2), Rose (PM2.5 soot), Purple (VOCs)
      const colors = [
        'rgba(56, 189, 248, ',
        'rgba(244, 63, 94, ',
        'rgba(245, 158, 11, ',
        'rgba(168, 85, 247, '
      ];
      this.colorBase = colors[Math.floor(Math.random() * colors.length)];
      this.alpha = Math.random() * 0.45 + 0.2;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      this.z += this.vz;

      // Parallax deflection from mouse
      const dx = mouseX - width / 2;
      const dy = mouseY - height / 2;
      this.x += (dx * 0.0003) * (this.z * 0.002);
      this.y += (dy * 0.0003) * (this.z * 0.002);

      // Atmospheric Inversion Mode behavior on Slide 2 (Traps particulates downward)
      if (currentSlide === 2) {
        if (this.y < height * 0.05) this.vy += 0.04;
      } else if (currentSlide === 9 || currentSlide === 10) {
        // Midday solar lift: upward convection currents
        if (this.y > -height * 0.3) this.vy -= 0.03;
      }

      // Boundary wraps
      if (this.x < -width) this.x = width;
      if (this.x > width) this.x = -width;
      if (this.y < -height) this.y = height;
      if (this.y > height) this.y = -height;
      if (this.z < 100) this.z = 900;
      if (this.z > 1000) this.z = 150;
    }
    render() {
      if (!ctx) return;
      // 3D Perspective Projection
      const fov = 400;
      const scale = fov / (fov + this.z);
      const projX = (this.x * scale) + (width / 2);
      const projY = (this.y * scale) + (height / 2);
      const radius = Math.max(0.6, this.baseRadius * scale * 2.2);

      ctx.beginPath();
      ctx.arc(projX, projY, radius, 0, Math.PI * 2);
      ctx.fillStyle = `${this.colorBase}${this.alpha * scale})`;
      ctx.fill();
    }
  }

  // Initialize Particles
  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle3D());
  }

  function renderLoop() {
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);

    // Smooth mouse damping
    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;

    // Render connected aerosol links in 3D
    for (let i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].render();

      // Connect close neighbor particles
      for (let j = i + 1; j < Math.min(i + 4, particles.length); j++) {
        const p1 = particles[i];
        const p2 = particles[j];
        const dist = Math.hypot(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z);
        if (dist < 180) {
          const fov = 400;
          const s1 = fov / (fov + p1.z);
          const s2 = fov / (fov + p2.z);
          const x1 = (p1.x * s1) + (width / 2);
          const y1 = (p1.y * s1) + (height / 2);
          const x2 = (p2.x * s2) + (width / 2);
          const y2 = (p2.y * s2) + (height / 2);
          const linkAlpha = (1 - dist / 180) * 0.15 * Math.min(s1, s2);
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.lineTo(x2, y2);
          ctx.strokeStyle = `rgba(56, 189, 248, ${linkAlpha})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      }
    }

    animationFrameId = requestAnimationFrame(renderLoop);
  }

  // Only run 3D loop if reduced motion is not preferred
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    renderLoop();
  }

  window.addEventListener('pointermove', (e) => {
    targetMouseX = e.clientX;
    targetMouseY = e.clientY;
  });

  // -------------------------------------------------------------
  // 2. 3D Card Parallax Tilt & Specular Glint (better-ui)
  // -------------------------------------------------------------
  const cards = document.querySelectorAll('.slide-card');
  cards.forEach(card => {
    card.addEventListener('pointermove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;
      const rotX = ((y - centerY) / centerY) * -5;
      const rotY = ((x - centerX) / centerX) * 5;
      card.style.transform = `perspective(1000px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) translateY(-2px)`;
    });

    card.addEventListener('pointerleave', () => {
      card.style.transform = '';
    });
  });

  // -------------------------------------------------------------
  // 3. Apple Keynote Deck Controller Logic (apple-design)
  // -------------------------------------------------------------
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  let currentIndex = 0;
  let isAutoplaying = false;
  let autoplayTimer = null;

  const progressFill = document.getElementById('progress-fill');
  const counterCurrent = document.getElementById('counter-current');
  const counterTotal = document.getElementById('counter-total');
  const btnPrev = document.getElementById('btn-prev');
  const btnNext = document.getElementById('btn-next');
  const btnGrid = document.getElementById('btn-grid');
  const btnFooterGrid = document.getElementById('btn-footer-grid');
  const btnCloseGrid = document.getElementById('btn-close-grid');
  const gridModal = document.getElementById('grid-modal');
  const gridThumbnailsContainer = document.getElementById('grid-thumbnails-container');
  const btnNotes = document.getElementById('btn-notes');
  const btnCloseNotes = document.getElementById('btn-close-notes');
  const notesDrawer = document.getElementById('notes-drawer');
  const notesText = document.getElementById('notes-text');
  const btnAutoplay = document.getElementById('btn-autoplay');
  const labelAutoplay = document.getElementById('label-autoplay');
  const iconPlay = document.getElementById('icon-play');
  const btnShortcuts = document.getElementById('btn-shortcuts');
  const btnCloseShortcuts = document.getElementById('btn-close-shortcuts');
  const shortcutsDialog = document.getElementById('shortcuts-dialog');
  const announcer = document.getElementById('slide-announcer');

  if (counterTotal) counterTotal.textContent = String(totalSlides).padStart(2, '0');

  // Populate Slide Grid Thumbnails
  if (gridThumbnailsContainer) {
    gridThumbnailsContainer.innerHTML = '';
    slides.forEach((s, idx) => {
      const titleEl = s.querySelector('.slide-title');
      const title = titleEl ? titleEl.innerText.replace(/\s+/g, ' ') : `Slide ${idx + 1}`;
      const badgeEl = s.querySelector('.slide-badge');
      const badge = badgeEl ? badgeEl.innerText : `${idx + 1}`;

      const thumb = document.createElement('div');
      thumb.className = `thumb-card ${idx === 0 ? 'active-thumb' : ''}`;
      thumb.innerHTML = `
        <span class="thumb-num">${String(idx + 1).padStart(2, '0')} · ${badge}</span>
        <span class="thumb-title">${title}</span>
      `;
      thumb.addEventListener('click', () => {
        updateSlide(idx);
        closeGrid();
      });
      gridThumbnailsContainer.appendChild(thumb);
    });
  }

  function updateSlide(index) {
    if (index < 0 || index >= totalSlides) return;
    currentIndex = index;
    currentSlide = currentIndex + 1;

    slides.forEach((s, idx) => {
      s.classList.remove('active', 'exited-prev');
      if (idx === currentIndex) {
        s.classList.add('active');
        s.scrollTop = 0;
      } else if (idx < currentIndex) {
        s.classList.add('exited-prev');
      }
    });

    // Update Counter
    if (counterCurrent) counterCurrent.textContent = String(currentIndex + 1).padStart(2, '0');

    // Update Progress Bar
    if (progressFill) {
      const pct = ((currentIndex + 1) / totalSlides) * 100;
      progressFill.style.width = `${pct}%`;
    }

    // Update Button States
    if (btnPrev) btnPrev.disabled = currentIndex === 0;
    if (btnNext) {
      if (currentIndex === totalSlides - 1) {
        btnNext.innerHTML = '<span>Finish</span>';
      } else {
        btnNext.innerHTML = '<span>Next</span> <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>';
      }
    }

    // Update Grid Active Thumbnails
    const thumbs = document.querySelectorAll('.thumb-card');
    thumbs.forEach((t, i) => t.classList.toggle('active-thumb', i === currentIndex));

    // Update Presenter Notes
    if (notesText && slides[currentIndex]) {
      const notes = slides[currentIndex].getAttribute('data-notes') || 'No presenter notes provided for this slide.';
      notesText.innerHTML = notes;
    }

    // Live Announcer for Screen Readers
    if (announcer && slides[currentIndex]) {
      const currentTitle = slides[currentIndex].querySelector('.slide-title');
      announcer.textContent = `Slide ${currentIndex + 1} of ${totalSlides}: ${currentTitle ? currentTitle.textContent.trim() : 'Project Overview'}`;
    }
  }

  function nextSlide() {
    if (currentIndex < totalSlides - 1) {
      updateSlide(currentIndex + 1);
    } else if (isAutoplaying) {
      stopAutoplay();
    }
  }

  function prevSlide() {
    if (currentIndex > 0) {
      updateSlide(currentIndex - 1);
    }
  }

  if (btnNext) btnNext.addEventListener('click', nextSlide);
  if (btnPrev) btnPrev.addEventListener('click', prevSlide);

  // Slide Grid Modal Toggles
  function openGrid() {
    if (gridModal) gridModal.classList.add('open');
  }
  function closeGrid() {
    if (gridModal) gridModal.classList.remove('open');
  }
  if (btnGrid) btnGrid.addEventListener('click', openGrid);
  if (btnFooterGrid) btnFooterGrid.addEventListener('click', openGrid);
  if (btnCloseGrid) btnCloseGrid.addEventListener('click', closeGrid);

  // Presenter Notes Toggles
  function toggleNotes() {
    if (notesDrawer) {
      const isOpen = notesDrawer.classList.toggle('open');
      if (btnNotes) btnNotes.classList.toggle('active', isOpen);
    }
  }
  if (btnNotes) btnNotes.addEventListener('click', toggleNotes);
  if (btnCloseNotes) btnCloseNotes.addEventListener('click', toggleNotes);

  // Auto-Play Feature
  function startAutoplay() {
    isAutoplaying = true;
    if (btnAutoplay) btnAutoplay.classList.add('active');
    if (labelAutoplay) labelAutoplay.textContent = 'Pause';
    if (iconPlay) iconPlay.innerHTML = '<rect x="6" y="4" width="4" height="16"></rect><rect x="14" y="4" width="4" height="16"></rect>';
    autoplayTimer = setInterval(() => {
      nextSlide();
    }, 8000);
  }
  function stopAutoplay() {
    isAutoplaying = false;
    clearInterval(autoplayTimer);
    if (btnAutoplay) btnAutoplay.classList.remove('active');
    if (labelAutoplay) labelAutoplay.textContent = 'Auto-Play';
    if (iconPlay) iconPlay.innerHTML = '<polygon points="5 3 19 12 5 21 5 3"></polygon>';
  }
  function toggleAutoplay() {
    if (isAutoplaying) stopAutoplay();
    else startAutoplay();
  }
  if (btnAutoplay) btnAutoplay.addEventListener('click', toggleAutoplay);

  // Shortcuts Modal
  if (btnShortcuts) btnShortcuts.addEventListener('click', () => shortcutsDialog && shortcutsDialog.classList.add('open'));
  if (btnCloseShortcuts) btnCloseShortcuts.addEventListener('click', () => shortcutsDialog && shortcutsDialog.classList.remove('open'));

  // Keyboard Controller (apple-design standards)
  document.addEventListener('keydown', (e) => {
    // Ignore if active inside an input
    if (document.activeElement && ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) return;

    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
      e.preventDefault();
      nextSlide();
    } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
      e.preventDefault();
      prevSlide();
    } else if (e.key === 'Home') {
      e.preventDefault();
      updateSlide(0);
    } else if (e.key === 'End') {
      e.preventDefault();
      updateSlide(totalSlides - 1);
    } else if (e.key.toLowerCase() === 'g') {
      if (gridModal && gridModal.classList.contains('open')) closeGrid();
      else openGrid();
    } else if (e.key.toLowerCase() === 's') {
      toggleNotes();
    } else if (e.key.toLowerCase() === 'p') {
      toggleAutoplay();
    } else if (e.key === 'Escape') {
      closeGrid();
      if (shortcutsDialog) shortcutsDialog.classList.remove('open');
      if (notesDrawer && notesDrawer.classList.contains('open')) toggleNotes();
    } else if (e.key.toLowerCase() === 'f') {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else if (document.exitFullscreen) {
        document.exitFullscreen();
      }
    } else if (e.key >= '1' && e.key <= '9') {
      updateSlide(parseInt(e.key, 10) - 1);
    } else if (e.key === '?') {
      if (shortcutsDialog) shortcutsDialog.classList.toggle('open');
    }
  });

  // Pointer / Touch Swipe Tracking (apple-design direct manipulation)
  let touchStartX = 0;
  let touchStartY = 0;
  const stage = document.getElementById('deck-stage');

  if (stage) {
    stage.addEventListener('touchstart', (e) => {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
    }, { passive: true });

    stage.addEventListener('touchend', (e) => {
      const deltaX = e.changedTouches[0].clientX - touchStartX;
      const deltaY = e.changedTouches[0].clientY - touchStartY;
      if (Math.abs(deltaX) > 50 && Math.abs(deltaX) > Math.abs(deltaY) * 1.5) {
        if (deltaX < 0) nextSlide();
        else prevSlide();
      }
    }, { passive: true });
  }

  // -------------------------------------------------------------
  // 4. Slide 2 Interactive Diurnal Simulator Widget
  // -------------------------------------------------------------
  const simSlider = document.getElementById('sim-hour-slider');
  const simHourDisplay = document.getElementById('sim-hour-display');
  const simBlVal = document.getElementById('sim-bl-val');
  const simStatusVal = document.getElementById('sim-status-val');
  const simPmVal = document.getElementById('sim-pm-val');

  if (simSlider) {
    simSlider.addEventListener('input', (e) => {
      const hour = parseInt(e.target.value, 10);
      const hourFormatted = `${String(hour).padStart(2, '0')}:00 IST`;
      if (simHourDisplay) simHourDisplay.textContent = hourFormatted;

      if (hour >= 5 && hour <= 9) {
        // Peak Morning Inversion Trap
        if (simBlVal) simBlVal.textContent = '120 m (Trap)';
        if (simStatusVal) {
          simStatusVal.textContent = 'Peak Inversion Trap';
          simStatusVal.style.color = 'var(--color-accent-rose)';
        }
        if (simPmVal) simPmVal.textContent = '380 µg/m³';
      } else if (hour >= 12 && hour <= 15) {
        // Solar Convection Mixing Window
        if (simBlVal) simBlVal.textContent = '850 m (Solar Lift)';
        if (simStatusVal) {
          simStatusVal.textContent = 'Solar Convection Window';
          simStatusVal.style.color = 'var(--color-accent-emerald)';
        }
        if (simPmVal) simPmVal.textContent = '165 µg/m³';
      } else if (hour >= 18 && hour <= 22) {
        // Evening Re-inversion
        if (simBlVal) simBlVal.textContent = '220 m (Dropping)';
        if (simStatusVal) {
          simStatusVal.textContent = 'Evening Re-Inversion';
          simStatusVal.style.color = 'var(--color-accent-amber)';
        }
        if (simPmVal) simPmVal.textContent = '295 µg/m³';
      } else {
        // Overnight Stagnant Boundary
        if (simBlVal) simBlVal.textContent = '180 m (Stagnant)';
        if (simStatusVal) {
          simStatusVal.textContent = 'Nocturnal Stagnation';
          simStatusVal.style.color = 'var(--color-accent-purple)';
        }
        if (simPmVal) simPmVal.textContent = '260 µg/m³';
      }
    });
  }

  // -------------------------------------------------------------
  // 5. Slide 12 Interactive Impact Estimator Widget
  // -------------------------------------------------------------
  const calcPills = document.querySelectorAll('.calc-pill');
  const calcExpReduction = document.getElementById('calc-exp-reduction');
  const calcCo2Val = document.getElementById('calc-co2-val');

  if (calcPills.length > 0) {
    calcPills.forEach(pill => {
      pill.addEventListener('click', () => {
        pill.classList.toggle('active');
        let totalCo2 = 0;
        let totalExp = 0;

        calcPills.forEach(p => {
          if (p.classList.contains('active')) {
            const action = p.getAttribute('data-action');
            if (action === 'metro') { totalCo2 += 1.8; totalExp += 25; }
            if (action === 'wetmop') { totalExp += 35; }
            if (action === 'corsi') { totalExp += 40; }
            if (action === 'induction') { totalCo2 += 1.4; totalExp += 15; }
          }
        });

        if (calcCo2Val) calcCo2Val.textContent = totalCo2 > 0 ? `-${totalCo2.toFixed(1)} kg` : '0.0 kg';
        if (calcExpReduction) calcExpReduction.textContent = totalExp > 0 ? `-${Math.min(92, totalExp)}%` : '0%';
      });
    });
  }

  // Initialize Deck at Slide 0
  updateSlide(0);
});
