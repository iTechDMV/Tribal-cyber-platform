function toggleGuide() {
    const panel = document.getElementById('guidePanel');
    if (!panel) return;
    panel.classList.toggle('d-none');
    if (!panel.classList.contains('d-none')) {
        const firstStep = panel.querySelector('.guide-step');
        if (firstStep) {
            firstStep.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } else {
        removeGuideHighlight();
    }
}

function initGuide() {
    const guideList = document.getElementById('guideList');
    if (!guideList) return;

    const steps = Array.from(guideList.querySelectorAll('.guide-step'));
    steps.forEach((step, index) => {
        const number = document.createElement('span');
        number.className = 'guide-step-index';
        number.textContent = index + 1;
        step.prepend(number);
        step.addEventListener('click', () => activateGuideStep(step));
    });

    const startButton = document.getElementById('guideStart');
    if (startButton && steps.length) {
        startButton.addEventListener('click', () => activateGuideStep(steps[0]));
    }
}

function activateGuideStep(step) {
    if (!step) return;
    document.querySelectorAll('.guide-step').forEach((item) => item.classList.remove('active'));
    step.classList.add('active');
    removeGuideHighlight();

    const targetSelector = step.dataset.stepTarget;
    if (!targetSelector) return;

    const target = document.querySelector(targetSelector);
    if (!target) return;

    target.classList.add('guide-highlight');
    target.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function removeGuideHighlight() {
    document.querySelectorAll('.guide-highlight').forEach((element) => {
        element.classList.remove('guide-highlight');
    });
}

window.addEventListener('DOMContentLoaded', initGuide);
