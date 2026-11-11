function playFadeIn() {
    const body = document.body;
    body.style.animation = 'none'; // Kill any current animation
    void body.offsetWidth;         // Force the browser to "blink" (Reflow)
    body.style.animation = 'fadeIn 1.5s ease-out forwards'; /* Start fade-in animation */
}

// Handle initial load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', playFadeIn);
} else {
    playFadeIn();
}

// Handle the "Back" button (BFCache)
window.addEventListener('pageshow', function(event) {
    // event.persisted is true if the page was restored from cache (Back button)
    if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
        playFadeIn();
    }
});

// Handle the "Fade Out" when leaving
document.addEventListener('click', function(e) {
    const link = e.target.closest('a');
    if (link && link.href && !link.target) {
        const href = link.href;
        if (href.includes(window.location.origin) && href.endsWith('.html')) {
            e.preventDefault();
            document.body.style.animation = 'fadeOut 0.2s ease-in forwards'; /* Start fade-out animation */
            setTimeout(() => {
                window.location.href = href; /* Navigate after fade-out completes */
            }, 200); 
        }
    }
});
