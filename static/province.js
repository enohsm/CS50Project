// ENG: Script for setting province and district options (written with AI assistance)
// TR: İl ve ilçe seçeneklerini ayarlama scripti (yapay zekadan destek alınarak yazıldı)

document.addEventListener("DOMContentLoaded", () => {
    const PROVINCES_URL = "https://api.turkiyeapi.dev/v1/provinces";
    fetch(PROVINCES_URL)
        .then(response => response.json())
        .then(data => {
            const provinces = data.data || [];
            provinces.forEach(item => {
                const opt = document.createElement("option");
                opt.value = item.name;
                opt.textContent = item.name;
                document.getElementById("province").appendChild(opt);
            });
        })
        .catch(error => console.error("İl verisi yüklenirken hata:", error));
    const provinceSelect = document.getElementById("province");
    provinceSelect.addEventListener("change", () => {
        const selectedProvince = provinceSelect.value;
        const DISTRICTS_URL = `https://api.turkiyeapi.dev/v1/provinces?name=${selectedProvince}`;
        fetch(DISTRICTS_URL)
            .then(response => response.json())
            .then(data => {
                const districtSelect = document.getElementById("district");
                districtSelect.innerHTML = "<option selected disabled>District</option>";
                districtSelect.disabled = false;
                const districts = data.data[0].districts || [];
                districts.forEach(district => {
                    const opt = document.createElement("option");
                    opt.value = district.name;
                    opt.textContent = district.name;
                    districtSelect.appendChild(opt);
                });
            })
            .catch(error => console.error("Error:", error));
    });
});