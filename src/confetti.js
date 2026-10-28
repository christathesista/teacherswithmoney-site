/* Teachers With Money confetti. Brand colors, square pieces, runs once, off under reduced motion.
   twmConfetti()            rain from the top of the viewport (thank-you page)
   twmConfetti({x, y})      burst from a point on screen (viewport pixels) */
window.twmConfetti = function (opts) {
  opts = opts || {};
  if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var c = document.createElement("canvas"); c.className = "confetti"; c.setAttribute("aria-hidden", "true");
  document.body.appendChild(c);
  var ctx = c.getContext && c.getContext("2d"); if (!ctx) { c.remove(); return; }
  var dpr = Math.min(window.devicePixelRatio || 1, 2), W = window.innerWidth, H = window.innerHeight;
  c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  var colors = ["#FAF3DE", "#F9C000", "#E84263", "#315647", "#FACC04", "#F97B06", "#EC321A", "#BB2D17", "#E84263", "#6B1F3A"];
  var burst = typeof opts.x === "number", n = opts.count || (burst ? 70 : Math.min(160, Math.round(W / 6)));
  var pieces = [], i;
  for (i = 0; i < n; i++) {
    var p = { s: 7 + Math.random() * 7, r: Math.random() * Math.PI, vr: (Math.random() - 0.5) * 0.25, col: colors[Math.floor(Math.random() * colors.length)] };
    if (burst) {
      var a = -Math.PI / 2 + (Math.random() - 0.5) * Math.PI * 0.95, v = 5 + Math.random() * 7;
      p.x = opts.x; p.y = opts.y; p.vx = Math.cos(a) * v; p.vy = Math.sin(a) * v;
    } else {
      p.x = Math.random() * W; p.y = -20 - Math.random() * H * 0.6; p.vx = (Math.random() - 0.5) * 2.2; p.vy = 2.5 + Math.random() * 3.5;
    }
    pieces.push(p);
  }
  var g = burst ? 0.18 : 0.05, start = null;
  function frame(ts) {
    if (!start) start = ts;
    ctx.clearRect(0, 0, W, H);
    var alive = 0;
    for (var k = 0; k < pieces.length; k++) {
      var q = pieces[k];
      q.x += q.vx; q.y += q.vy; q.vy += g; q.vx *= 0.99; q.r += q.vr;
      if (q.y < H + 20) alive++;
      ctx.save(); ctx.translate(q.x, q.y); ctx.rotate(q.r); ctx.fillStyle = q.col; ctx.fillRect(-q.s / 2, -q.s / 2, q.s, q.s); ctx.restore();
    }
    if (alive > 0 && ts - start < 4000) requestAnimationFrame(frame); else c.remove();
  }
  requestAnimationFrame(frame);
};
