// Navigation and auth state management
document.addEventListener('DOMContentLoaded', function() {
    const loginBtn = document.getElementById('loginBtn');
    const profileIcon = document.getElementById('profileIcon');
    const profileImg = document.getElementById('profileImg');
    const profileInitials = document.getElementById('profileInitials');

    // Check if user is logged in
    fetch('/api/check-auth', {
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        if (data.authenticated) {
            loginBtn.style.display = 'none';
            profileIcon.style.display = 'flex';
            
            // If user has a profile image
            if (data.profile_image) {
                profileImg.src = data.profile_image;
                profileImg.style.display = 'block';
                profileInitials.style.display = 'none';
            } else {
                // Show initials if no profile image
                profileImg.style.display = 'none';
                profileInitials.style.display = 'block';
                profileInitials.textContent = data.name
                    .split(' ')
                    .map(n => n[0])
                    .join('')
                    .toUpperCase();
            }
        } else {
            loginBtn.style.display = 'block';
            profileIcon.style.display = 'none';
        }
    })
    .catch(error => {
        console.error('Error checking auth status:', error);
        loginBtn.style.display = 'block';
        profileIcon.style.display = 'none';
    });

    // Handle profile icon click
    profileIcon.addEventListener('click', function() {
        // Create dropdown menu
        const dropdown = document.createElement('div');
        dropdown.className = 'profile-dropdown';
        dropdown.innerHTML = `
            <a href="profile.html">Profile</a>
            <a href="#" id="logoutBtn">Logout</a>
        `;
        
        // Position dropdown
        const rect = profileIcon.getBoundingClientRect();
        dropdown.style.position = 'absolute';
        dropdown.style.top = rect.bottom + 'px';
        dropdown.style.right = (window.innerWidth - rect.right) + 'px';
        
        // Add to body
        document.body.appendChild(dropdown);
        
        // Handle click outside
        function handleClickOutside(e) {
            if (!dropdown.contains(e.target) && !profileIcon.contains(e.target)) {
                dropdown.remove();
                document.removeEventListener('click', handleClickOutside);
            }
        }
        
        // Add click outside listener
        setTimeout(() => {
            document.addEventListener('click', handleClickOutside);
        }, 0);
        
        // Handle logout
        document.getElementById('logoutBtn').addEventListener('click', function(e) {
            e.preventDefault();
            fetch('/api/logout', {
                method: 'POST',
                credentials: 'include'
            })
            .then(() => {
                window.location.reload();
            })
            .catch(error => {
                console.error('Error logging out:', error);
            });
        });
    });
});

// Form step navigation
document.addEventListener('DOMContentLoaded', function() {
    const steps = document.querySelectorAll('.step');
    let currentStep = 1;

    window.nextStep = function(step) {
        // Hide current step
        document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');
        
        // Show next step
        currentStep = step + 1;
        const nextStepElement = document.querySelector(`.step[data-step="${currentStep}"]`);
        if (nextStepElement) {
            nextStepElement.classList.add('active');
        }
    };

    window.prevStep = function(step) {
        // Hide current step
        document.querySelector(`.step[data-step="${currentStep}"]`).classList.remove('active');
        
        // Show previous step
        currentStep = step - 1;
        const prevStepElement = document.querySelector(`.step[data-step="${currentStep}"]`);
        if (prevStepElement) {
            prevStepElement.classList.add('active');
        }
    };
});

// Carousel functionality
document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.carousel-track');
    const cards = document.querySelectorAll('.precaution-card');
    const dotsContainer = document.querySelector('.carousel-dots');
    let currentIndex = 0;

    // Create dots
    cards.forEach((_, index) => {
        const dot = document.createElement('div');
        dot.classList.add('dot');
        if (index === 0) dot.classList.add('active');
        dot.addEventListener('click', () => goToSlide(index));
        dotsContainer.appendChild(dot);
    });

    // Update dots
    function updateDots() {
        const dots = document.querySelectorAll('.dot');
        dots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentIndex);
        });
    }

    // Go to specific slide
    function goToSlide(index) {
        currentIndex = index;
        track.style.transform = `translateX(-${currentIndex * 100}%)`;
        updateDots();
    }

    // Auto advance slides
    function autoAdvance() {
        currentIndex = (currentIndex + 1) % cards.length;
        goToSlide(currentIndex);
    }

    // Start auto-advance timer
    setInterval(autoAdvance, 3000); // Change slide every 3 seconds
});

