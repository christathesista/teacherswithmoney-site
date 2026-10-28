/* Glitter cursor for the Summit pages: tiny brand-colored squares trail the pointer and burst on click.
   Mouse only (no trail on phones), off under reduced motion, nothing to click through. */
(function () {
  if (!window.matchMedia) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (!window.matchMedia("(pointer: fine)").matches) return;
  var c = document.createElement("canvas"); c.className = "sparkle"; c.setAttribute("aria-hidden", "true");
  document.body.appendChild(c);
  var ctx = c.getContext && c.getContext("2d"); if (!ctx) { c.remove(); return; }
  var dpr = Math.min(window.devicePixelRatio || 1, 2), W, H;
  function size() { W = window.innerWidth; H = window.innerHeight; c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
  size(); window.addEventListener("resize", size);
  var colors = ["#F9C000", "#E84263", "#FACC04", "#F97B06", "#EC321A", "#FAF3DE", "#6B1F3A"];
  var bits = [], last = 0, raf = null;
  function spawn(x, y, n, burst) {
    for (var i = 0; i < n; i++) {
      var a = Math.random() * Math.PI * 2, v = burst ? 2 + Math.random() * 4 : 0.2 + Math.random() * 0.8;
      bits.push({ x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - (burst ? 1.5 : 0.3), s: burst ? 5 + Math.random() * 5 : 3 + Math.random() * 4,
        r: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.3, life: 1, decay: burst ? 0.018 : 0.03, col: colors[Math.floor(Math.random() * colors.length)] });
    }
    if (bits.length > 220) bits.splice(0, bits.length - 220);
    if (!raf) raf = requestAnimationFrame(frame);
  }
  function frame() {
    ctx.clearRect(0, 0, W, H);
    for (var i = bits.length - 1; i >= 0; i--) {
      var b = bits[i];
      b.x += b.vx; b.y += b.vy; b.vy += 0.08; b.r += b.vr; b.life -= b.decay;
      if (b.life <= 0) { bits.splice(i, 1); continue; }
      ctx.save(); ctx.globalAlpha = Math.max(0, b.life); ctx.translate(b.x, b.y); ctx.rotate(b.r);
      ctx.fillStyle = b.col; ctx.fillRect(-b.s / 2, -b.s / 2, b.s, b.s); ctx.restore();
    }
    raf = bits.length ? requestAnimationFrame(frame) : null;
  }
  window.addEventListener("mousemove", function (e) {
    var now = performance.now(); if (now - last < 24) return; last = now;
    spawn(e.clientX, e.clientY, 2, false);
  }, { passive: true });
  window.addEventListener("click", function (e) {
    var t = e.target;
    if (t && t.closest && t.closest("input, textarea, select, iframe")) return;
    spawn(e.clientX, e.clientY, 14, true);
  });
})();
