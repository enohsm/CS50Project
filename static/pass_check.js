let pass_input = document.getElementById('password');
let confirm_input = document.getElementById('confirmation');

let pass_message = document.getElementById('pass_message');
let confirm_message = document.getElementById('confirm_message');

const pattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.{8,}).*$/;

pass_input.addEventListener('input', function() {
    let pass = pass_input.value;
    

    if (pass.length < 1) {
        pass_message.innerHTML = ""
    }

    else if (pattern.test(pass)) {
        pass_message.innerHTML = '<i class="bi bi-check" style="color:green"></i>'
    }

    else if (!pattern.test(pass)) {
        pass_message.innerHTML = '<i class="bi bi-x" style="color:red"></i>'
    }
});

confirm_input.addEventListener('input', function() {
    let confirm = confirm_input.value;
    

    if (confirm.length < 1) {
        confirm_message.innerHTML = ""
    }

    else if (pattern.test(confirm)) {
        confirm_message.innerHTML = '<i class="bi bi-check" style="color:green"></i>'
    }

    else if (!pattern.test(confirm)) {
        confirm_message.innerHTML = '<i class="bi bi-x" style="color:red"></i>'
    }
});