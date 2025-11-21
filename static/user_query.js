let input = document.querySelector('input');
async function changeRole(user_id) {
    let response = await fetch(`/dashboard/admin/set_roles?id=${user_id}`, {method : 'POST'});

    let result = await response.json();

    if (result) {
        user_query();
    }
}

async function user_query() {
    if (input.value.length >= 3) {
    let response = await fetch('/dashboard/admin/get_roles?username=' + input.value);
    let users = await response.json();
    let html = '';
    for (let user in users) {
        let username = users[user].username.replace('<', '&lt;').replace('&', '&amp;');
        let name = users[user].name.replace('<', '&lt;').replace('&', '&amp;');
        let surname = users[user].surname.replace('<', '&lt;').replace('&', '&amp;');
        let user_id = users[user].id;
        let str_role = '';
        let role = users[user].role;
        if (role == 0) {
            str_role = 'User';
        }

        else if (role == 1) {
            str_role = 'Employee';
        }

        else if (role == 2) {
            str_role = 'Admin';
        }

        if (role == 0) {
            html += `<tr>
                        <td>${username}</td>
                        <td>${name}</td>
                        <td>${surname}</td>
                        <td>${str_role}</td>
                        <td class="text-center">
                            <button class="btn-icon" onclick="changeRole(${user_id})" type="button"><i class="bi bi-person-fill-up" style="color:green"></i></button>
                        </td>
                    </tr>`;
        }

        else {
            html += `<tr>
                        <td>${username}</td>
                        <td>${name}</td>
                        <td>${surname}</td>
                        <td>${str_role}</td>
                        <td class="text-center">
                            <i class="bi bi-person-fill"></i>
                        </td>
                    </tr>`;
        }
    }
    table = document.querySelector('tbody');
    table.innerHTML = html;
    }
}

input.addEventListener('input', user_query);