document.addEventListener("DOMContentLoaded", () => {
    const hero = document.querySelector(".landing-hero");
    if (!hero) return;

    let offset = 0;
    function animate() {
        offset += 0.3;
        hero.style.transform = `translateY(${Math.sin(offset / 20) * 4}px)`;
        requestAnimationFrame(animate);
    }
    animate();
});
