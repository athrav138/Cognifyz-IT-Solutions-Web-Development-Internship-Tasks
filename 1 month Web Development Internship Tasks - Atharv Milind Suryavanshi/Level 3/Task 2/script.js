document.addEventListener('DOMContentLoaded', () => {
    // Select DOM nodes for overlay UI handling
    const modalOverlay = document.getElementById('applyModal');
    const closeModalBtn = document.getElementById('closeModal');
    const openModalButtons = document.querySelectorAll('.open-modal');
    const applicationForm = document.getElementById('internshipForm');

    // Function to trigger presentation modal open state
    const openModal = () => {
        modalOverlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // Stop background viewport scroll
    };

    // Function to handle close modal routines
    const closeModal = () => {
        modalOverlay.classList.remove('active');
        document.body.style.overflow = ''; // Reinstate normal viewport scrolling
    };

    // Attach event listeners to all explicit landing CTA components
    openModalButtons.forEach(button => {
        button.addEventListener('click', openModal);
    });

    closeModalBtn.addEventListener('click', closeModal);

    // Close window event routing whenever user clicks outer gray bounds area
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) {
            closeModal();
        }
    });

    // Capture submit events inside popup view safely
    applicationForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        const candidateName = document.getElementById('fullName').value;
        
        // Simulating smooth registration receipt
        alert(`Thank you, ${candidateName}! Your application submission sample has been captured successfully.`);
        
        applicationForm.reset();
        closeModal();
    });
});