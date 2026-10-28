/* The magic word. Type "party" anywhere on the page (not in a form field) and it rains confetti
   with a sticker. Nobody finds it unless Christa tells them. Confetti skips itself under reduced motion. */
(function () {
  var buf = "", last = 0;
  document.addEventListener("keydown", function (e) {
    var t = e.target, tag = t && t.tagName ? t.tagName.toLowerCase() : "";
    if (tag === "input" || tag === "textarea" || tag === "select" || (t && t.isContentEditable)) return;
    if (!e.key || e.key.length !== 1) return;
    buf = (buf + e.key.toLowerCase()).slice(-5);
    if (buf !== "party") return;
    buf = "";
    var now = Date.now();
    if (now - last < 6000) return;
    last = now;
    if (window.twmConfetti) twmConfetti();
    var old = document.querySelector(".magic-word");
    if (old) old.parentNode.removeChild(old);
    var wrap = document.createElement("div");
    wrap.className = "magic-word";
    wrap.setAttribute("role", "status");
    wrap.innerHTML = '<span class="sticker">you said the magic word!</span>'; /* DRAFT COPY: Christa to review */
    document.body.appendChild(wrap);
    setTimeout(function () { wrap.classList.add("out"); }, 3600);
    setTimeout(function () { if (wrap.parentNode) wrap.parentNode.removeChild(wrap); }, 4200);
  });
})();
