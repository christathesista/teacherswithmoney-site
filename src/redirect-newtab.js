/* After someone signs up, beehiiv asks this page to go to the thank-you page (a "beehiiv:redirect" message).
   We try to open it in a new tab so this page stays open, and let beehiiv do its usual same-tab redirect
   only when the browser blocks the new tab (Safari often does). Registered before beehiiv's loader so it runs first. */
window.addEventListener("message", function (e) {
  var d = e.data;
  if (!d || d.type !== "beehiiv:redirect" || !d.url) return;
  if (e.origin !== "https://subscribe-forms.beehiiv.com") return;
  var w = null;
  try { w = window.open(d.url, "_blank"); } catch (err) { w = null; }
  if (w) {
    try { w.opener = null; } catch (err) {}
    e.stopImmediatePropagation();
  }
});
