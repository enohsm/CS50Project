let passwords = document.querySelectorAll('.pass-input');
passwords.forEach(password => function() {
    password.addEventListener('input', async function() {
        pass = password.value;
    });
});