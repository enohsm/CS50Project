function modify_post(id) {
    window.location.href = `/dashboard/admin/posts/modify?id=${id}`;
}

// ENG: Script for performing the delete operation using the POST method
// TR: Silme işlemini post yöntemiyle yapmak için script
async function delete_post(id) {
    const request_url = `/dashboard/admin/posts/delete?id=${id}`

    const response = await fetch(request_url, {method : 'POST'});

    let url = await response.text();

    window.location.href = url
}