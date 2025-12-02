// ENG: User roles and permissions query script (written with AI assistance but all core logic is mine)
// TR: Kullanıcı ve yetkilerini sorgulama scripti (yapay zekadan destek alınarak yazıldı ama tüm temel bana ait)

// ENG: Store the input element in a variable
// TR: Input etiketini bir değişkene alıyorum
let input = document.querySelector('input');

// ENG: Function to change a user's role (asynchronous function)
// TR: Yetki değiştirme fonksiyonu (asenkron fonksiyon)
async function changeRole(user_id) {
    // ENG: Send a POST request to the set_roles route
    // TR: Set_roles rotasına post yöntemiyle istek gönder
    let response = await fetch(`/dashboard/admin/set_roles?id=${user_id}`, {method : 'POST'});

    // ENG: Return the result as JSON
    // TR: Sonucu JSON olarak döndür
    let result = await response.json();
    
    // ENG: If the result is valid, call the query function again
    // TR: Eğer sonucun içi doluysa sorgulama fonksiyonunu tekrar çağır
    if (result) {
        user_query();
    }
}

// ENG: Function for querying users
// TR: Kullanıcı sorgulama fonksiyonu
async function user_query() {
    
    // ENG: Perform the query when at least 3 characters are entered
    // TR: En az 3 karakter girildiğinde sorguyu gerçekleştir
    if (input.value.length >= 3) {
        
        // ENG: Send the request
        // TR: İstek gönder
        let response = await fetch('/dashboard/admin/get_roles?username=' + input.value);

        // ENG: Receive the response as JSON
        // TR: Yanıtı JSON olarak al
        let users = await response.json();

        // ENG: Create an HTML variable
        // TR: HTML değişkeni oluştur
        let html = '';

        // ENG: Fill the HTML variable for each user
        // TR: Her kullanıcı için html değişkenini doldur
        for (let user in users) {
            
            // ENG: Store the user's data in variables
            // TR: Kullanıcının verilerini değişkenlere al
            let username = users[user].username.replace('<', '&lt;').replace('&', '&amp;');
            let name = users[user].name.replace('<', '&lt;').replace('&', '&amp;');
            let surname = users[user].surname.replace('<', '&lt;').replace('&', '&amp;');
            let user_id = users[user].id;
            let str_role = '';
            let role = users[user].role;

            // ENG: Convert numeric role values into readable strings for the interface
            // TR: Rolleri arayüzde anlamlı şekilde görüntüleyebilmek için string haline getir
            if (role == 0) {
                str_role = 'User';
            }

            else if (role == 1) {
                str_role = 'Employee';
            }

            else if (role == 2) {
                str_role = 'Admin';
            }
            
            // ENG: If the role is 'user', display the role upgrade button
            // TR: Eğer rol 'user' ise yetki yükseltme butonu bulunacak
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

            // ENG: Otherwise, the upgrade button will be disabled
            // TR: Aksi takdirde yetki yükseltme butonu disabled olacak
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
        // ENG: Select the table body element
        // TR: Tablonun gövdesini seçiyoruz
        table = document.querySelector('tbody');
        
        // ENG: Fill the table body with the generated HTML
        // TR: Gövdeyi 'html' değişkeni ile dolduruyoruz
        table.innerHTML = html;
    }
}

// ENG: Run user_query when the input value changes
// TR: Inputa yapılan girişlerde user_query yapıyoruz
input.addEventListener('input', user_query);