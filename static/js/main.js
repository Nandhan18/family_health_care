document.addEventListener('DOMContentLoaded', function () {
    // Initialize Lucide Icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Render Risk Progress Bars
    document.querySelectorAll('.risk-bar-progress').forEach(function (element) {
        var percent = element.getAttribute('data-risk-percent');
        if (percent) {
            element.style.width = percent + '%';
        }
    });
});

// Modal Helpers
function openModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
    }
}
