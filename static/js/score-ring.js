document.addEventListener("DOMContentLoaded", () => {
    const rings = document.querySelectorAll(".score-ring");
    rings.forEach(ring => {
        const score = parseInt(ring.dataset.score || "0", 10);
        const clamped = Math.max(0, Math.min(100, score));
        const angle = (clamped / 100) * 360;

        ring.style.background = `
            conic-gradient(
                var(--accent-green) ${angle}deg,
                #374151 ${angle}deg
            )
        `;
        ring.textContent = `${clamped}%`;
    });
});
