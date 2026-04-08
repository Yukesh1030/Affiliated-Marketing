document.addEventListener('DOMContentLoaded', () => {
    // Navbar Scroll Effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile Menu Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navLinks = document.querySelector('.nav-links');

    mobileToggle.addEventListener('click', () => {
        mobileToggle.classList.toggle('active');
        navLinks.classList.toggle('mobile-active');
    });

    // Close mobile menu when clicking a link
    const links = document.querySelectorAll('.nav-links a');
    links.forEach(link => {
        link.addEventListener('click', () => {
            mobileToggle.classList.remove('active');
            navLinks.classList.remove('mobile-active');
        });
    });

    // Hero Search Animation Focus
    const heroSearch = document.getElementById('heroSearch');
    const searchContainer = document.querySelector('.search-container');
    
    heroSearch.addEventListener('focus', () => {
        searchContainer.style.transform = 'scale(1.02)';
        searchContainer.style.boxShadow = '0 15px 35px rgba(0,205,102,0.15)';
        searchContainer.style.borderColor = 'var(--primary)';
    });

    heroSearch.addEventListener('blur', () => {
        searchContainer.style.transform = 'scale(1)';
        searchContainer.style.boxShadow = '0 10px 25px rgba(0,0,0,0.05)';
        searchContainer.style.borderColor = 'rgba(0,0,0,0.05)';
    });

    // Typing Animation for Sub-heading
    const typeText = document.querySelector('.hero-left p');
    const text = typeText.innerText;
    typeText.innerText = '';
    
    let i = 0;
    function typeWriter() {
        if (i < text.length) {
            typeText.innerHTML += text.charAt(i);
            i++;
            setTimeout(typeWriter, 30);
        }
    }

    // Start typing after a short delay (once the reveal animation starts)
    setTimeout(typeWriter, 800);

    // Staggered reveal animations for hero text
    const reveals = document.querySelectorAll('.reveal');
    reveals.forEach((el, index) => {
        el.style.animationDelay = `${index * 0.15}s`;
    });
});
