const textElement = document.getElementById('typewriter');
const wordsArray = ['Aspiring Data Scientist', 'AI/ML Engineer', 'Data Analyst & Power BI Developer', 'Full Stack Developer'];
let wordIdx = 0, charIdx = 0, isDeletingChar = false;

 function executeTypewriterLoop() {
    const activeString = wordsArray[wordIdx];
    let processingSpeed = isDeletingChar ? 40 : 80;
    
    if (isDeletingChar) {
        textElement.textContent = activeString.substring(0, charIdx - 1);
        charIdx--;
    } else {
        textElement.textContent = activeString.substring(0, charIdx + 1);
        charIdx++;
    }

    if (!isDeletingChar && charIdx === activeString.length) {
        isDeletingChar = true;
        processingSpeed = 1600; 
    } else if (isDeletingChar && charIdx === 0) {
        isDeletingChar = false;
        wordIdx = (wordIdx + 1) % wordsArray.length;
        processingSpeed = 2500; 
    }
    setTimeout(executeTypewriterLoop, processingSpeed);
}

const mainNavbarNode = document.getElementById('navbar');
const topScrollTriggerButton = document.getElementById('scroll-to-top');
const bootstrapNavCollapse = document.getElementById('navbarNav');

function processWindowScrollMetrics() {
    if (window.scrollY > 50) {
        mainNavbarNode.classList.add('scrolled');
    } else {
        mainNavbarNode.classList.remove('scrolled');
    }
    topScrollTriggerButton.style.display = window.scrollY > 300 ? 'block' : 'none';
}
window.addEventListener('scroll', processWindowScrollMetrics, { passive: true });

document.querySelectorAll('.nav-link').forEach(anchorNode => {
    anchorNode.addEventListener('click', () => {
        if (window.innerWidth < 992 && bootstrapNavCollapse.classList.contains('show')) {
            const collapseInstance = bootstrap.Collapse.getInstance(bootstrapNavCollapse);
            if (collapseInstance) collapseInstance.hide();
        }
    });
});

function playBarGrowthAnimation(elementId, targetLimit) {
    const graphicBarFill = document.getElementById(elementId);
    const labelStringPercent = document.getElementById(`${elementId}-percent`);
    if (!graphicBarFill || !labelStringPercent) return;
    
    graphicBarFill.style.width = '0%';
    labelStringPercent.textContent = '0%';

    setTimeout(() => {
        graphicBarFill.style.width = `${targetLimit}%`;
        let trackingValue = 0;
        const incrementalTimer = setInterval(() => {
            trackingValue += targetLimit / 40;
            if (trackingValue >= targetLimit) {
                trackingValue = targetLimit;
                clearInterval(incrementalTimer);
            }
            labelStringPercent.textContent = `${Math.floor(trackingValue)}%`;
        }, 25);
    }, 100); 
}

const portfolioSectionElements = document.querySelectorAll('section');
const crossLinksMenuCollection = document.querySelectorAll('.nav-link');

const modularViewObserver = new IntersectionObserver((observedEntries) => {
    observedEntries.forEach(viewItem => {
        const activeSectionId = viewItem.target.getAttribute('id');
        const associatedLinkNode = document.querySelector(`.nav-link[href="#${activeSectionId}"]`);

        if (viewItem.isIntersecting) {
            crossLinksMenuCollection.forEach(nodeItem => nodeItem.classList.remove('active'));
            if (associatedLinkNode) associatedLinkNode.classList.add('active');
            
            if (activeSectionId === 'skills') {
                playBarGrowthAnimation('progress-1', 95); 
                playBarGrowthAnimation('progress-2', 85); 
                playBarGrowthAnimation('progress-3', 90); 
                playBarGrowthAnimation('progress-4', 85); 
            }
        }
    });
}, { threshold: 0.15, rootMargin: "0px 0px -10% 0px" });

portfolioSectionElements.forEach(singleSec => modularViewObserver.observe(singleSec));

const overlayFrameModal = document.getElementById('lightboxModal');
const displayAssetImage = document.getElementById('lightboxImg');
const triggerCloseModal = document.getElementById('lightboxClose');
const clickTriggersList = document.querySelectorAll('.btn-lightbox-trigger');

clickTriggersList.forEach(actionBtn => {
    actionBtn.addEventListener('click', () => {
        const designatedAssetUrl = actionBtn.getAttribute('data-src');
        if (designatedAssetUrl) {
            displayAssetImage.src = designatedAssetUrl;
            overlayFrameModal.style.display = 'block';
        }
    });
});

triggerCloseModal.addEventListener('click', () => {
    overlayFrameModal.style.display = 'none';
});

overlayFrameModal.addEventListener('click', (clickEvent) => {
    if (clickEvent.target === overlayFrameModal) {
        overlayFrameModal.style.display = 'none';
    }
});

const masterCursorContainer = document.querySelector('.cursor-effects');
const analyticalCursorDot = document.querySelector('.cursor-dot');
const analyticalCursorRing = document.querySelector('.cursor-ring');
const hasFinePointerCapability = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

if (masterCursorContainer && analyticalCursorDot && analyticalCursorRing && hasFinePointerCapability) {
    document.body.classList.add('cursor-ready');

    const basicCoordinates = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
    const elasticCoordinates = { x: window.innerWidth / 2, y: window.innerHeight / 2 };

    window.addEventListener('pointermove', (pointerMoveEvt) => {
        basicCoordinates.x = pointerMoveEvt.clientX;
        basicCoordinates.y = pointerMoveEvt.clientY;
        masterCursorContainer.classList.add('is-visible');
    }, { passive: true });

    function pipelineFrameProcessingLoop() {
        elasticCoordinates.x += (basicCoordinates.x - elasticCoordinates.x) * 0.16;
        elasticCoordinates.y += (basicCoordinates.y - elasticCoordinates.y) * 0.16;

        analyticalCursorDot.style.left = `${basicCoordinates.x}px`;
        analyticalCursorDot.style.top = `${basicCoordinates.y}px`;

        analyticalCursorRing.style.left = `${elasticCoordinates.x}px`;
        analyticalCursorRing.style.top = `${elasticCoordinates.y}px`;

        requestAnimationFrame(pipelineFrameProcessingLoop);
    }
    requestAnimationFrame(pipelineFrameProcessingLoop);

    document.querySelectorAll('a, button, input, textarea, .btn-lightbox-trigger, .carousel-indicators button').forEach(clickableObject => {
        clickableObject.addEventListener('mouseenter', () => masterCursorContainer.classList.add('is-hovering'));
        clickableObject.addEventListener('mouseleave', () => masterCursorContainer.classList.add('is-hovering'));
    });
}

document.addEventListener('DOMContentLoaded', () => {
    executeTypewriterLoop();
    processWindowScrollMetrics();
    const milestoneCarousel = document.getElementById('milestoneCarousel');
    if (milestoneCarousel && window.bootstrap) {
        new bootstrap.Carousel(milestoneCarousel, { interval: 3000, ride: 'carousel', pause: 'hover', touch: true });
    }
});
