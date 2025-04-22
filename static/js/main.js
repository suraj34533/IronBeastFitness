// Main JavaScript functionality for IronBeast Gym Website

document.addEventListener('DOMContentLoaded', function() {
    // Mobile Menu Toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Add the golden text effect to all headings
    const headings = document.querySelectorAll('h1, h2, h3, h4, h5, h6');
    headings.forEach(heading => {
        if (!heading.classList.contains('golden-text') && !heading.classList.contains('shine-effect')) {
            heading.classList.add('golden-text');
        }
    });
    
    // Add shine effect to main headings
    const mainHeadings = document.querySelectorAll('h1, h2');
    mainHeadings.forEach(heading => {
        if (!heading.classList.contains('shine-effect')) {
            heading.classList.add('shine-effect');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Exercise Plan Tabs Functionality
    const exerciseTabs = document.querySelectorAll('.exercise-tab');
    const exerciseContents = document.querySelectorAll('.exercise-content');
    
    if (exerciseTabs.length > 0 && exerciseContents.length > 0) {
        exerciseTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs
                exerciseTabs.forEach(t => {
                    t.classList.remove('bg-yellow-800', 'text-white');
                    t.classList.add('bg-gray-800', 'text-gray-300');
                });
                
                // Add active class to current tab
                tab.classList.remove('bg-gray-800', 'text-gray-300');
                tab.classList.add('bg-yellow-800', 'text-white');
                
                // Hide all content
                exerciseContents.forEach(content => {
                    content.classList.add('hidden');
                });
                
                // Show selected content
                const target = tab.getAttribute('data-target');
                document.getElementById(target).classList.remove('hidden');
            });
        });
    }
    
    // Diet Plan Tabs Functionality
    const dietTabs = document.querySelectorAll('.diet-tab');
    const dietContents = document.querySelectorAll('.diet-content');
    
    if (dietTabs.length > 0 && dietContents.length > 0) {
        dietTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                // Remove active class from all tabs
                dietTabs.forEach(t => {
                    t.classList.remove('bg-yellow-800', 'text-white');
                    t.classList.add('bg-gray-800', 'text-gray-300');
                });
                
                // Add active class to current tab
                tab.classList.remove('bg-gray-800', 'text-gray-300');
                tab.classList.add('bg-yellow-800', 'text-white');
                
                // Hide all content
                dietContents.forEach(content => {
                    content.classList.add('hidden');
                });
                
                // Show selected content
                const target = tab.getAttribute('data-target');
                document.getElementById(target).classList.remove('hidden');
            });
        });
    }
    
    // FAQ accordion functionality
    const faqButtons = document.querySelectorAll('.faq-button');
    
    if (faqButtons.length > 0) {
        faqButtons.forEach(button => {
            button.addEventListener('click', () => {
                const content = button.nextElementSibling;
                const icon = button.querySelector('svg');
                
                // Toggle content visibility
                content.classList.toggle('hidden');
                
                // Rotate icon
                if (content.classList.contains('hidden')) {
                    icon.style.transform = 'rotate(0deg)';
                } else {
                    icon.style.transform = 'rotate(180deg)';
                }
            });
        });
    }
    
    // Add animations to cards on scroll
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    function checkScroll() {
        animatedElements.forEach(element => {
            const elementTop = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementTop < windowHeight - 100) {
                element.classList.add('animate-fade-in-up');
                element.classList.remove('opacity-0');
            }
        });
    }
    
    // Initial check and add scroll listener
    if (animatedElements.length > 0) {
        checkScroll();
        window.addEventListener('scroll', checkScroll);
    }
});

// Add a CSS animation class
document.head.insertAdjacentHTML('beforeend', `
<style>
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 30px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    .animate-fade-in-up {
        animation: fadeInUp 0.8s ease forwards;
    }
</style>
`);
