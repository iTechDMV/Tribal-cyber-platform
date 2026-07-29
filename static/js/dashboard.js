// Simple compliance score ring renderer
document.addEventListener("DOMContentLoaded", () => {
    const ring = document.querySelector(".score-ring");
    if (!ring) return;

    const score = parseInt(ring.dataset.score || "0", 10);
    const clamped = Math.max(0, Math.min(100, score));
    const angle = (clamped / 100) * 360;

    ring.style.background = `conic-gradient(#10B981 0deg, #10B981 ${angle}deg, #374151 ${angle}deg)`;
    ring.textContent = `${clamped}%`;
});
