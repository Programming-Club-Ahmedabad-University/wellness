document.addEventListener('DOMContentLoaded', ()=> {
    const togglePassword = document.querySelector('.eye-toggler');
    const password = document.querySelector('#password');
    
    togglePassword.onclick = ()=> {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        togglePassword.classList.toggle('fa-eye-slash');
    };
});