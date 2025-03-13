document.addEventListener('DOMContentLoaded', function() {
    const agreeButton = document.getElementById('agreeButton');
    if (agreeButton) {
        agreeButton.addEventListener('click', function() {
            document.getElementById('id_agreed_to_terms').checked = true;
            const modal = bootstrap.Modal.getInstance(document.getElementById('termsModal'));
            modal.hide();
        });
    }
});

function togglePassword(id) {
    const passwordField = document.getElementById(id);
    const type = passwordField.getAttribute('type') === 'password' ? 'text' : 'password';
    passwordField.setAttribute('type', type);

    // Toggle the eye icon
    const eyeIcon = passwordField.nextElementSibling.querySelector('i');
    eyeIcon.classList.toggle('fa-eye');
    eyeIcon.classList.toggle('fa-eye-slash');
}
