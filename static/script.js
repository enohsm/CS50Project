// 1️⃣ Sayfa tamamen yüklendikten sonra çalışacak fonksiyon
document.addEventListener("DOMContentLoaded", () => {

    // 2️⃣ Türkiye illerini çekeceğimiz API URL
    const PROVINCES_URL = "https://api.turkiyeapi.dev/v1/provinces";

    // 3️⃣ Fetch ile illeri çekme
    fetch(PROVINCES_URL)
        .then(response => response.json()) // JSON'a dönüştür
        .then(data => {
            const provinces = data.data || []; // data.data yoksa boş dizi kullan
            provinces.forEach(item => { // Her il için
                const opt = document.createElement("option"); // option oluştur
                opt.value = item.name; // value = il adı
                opt.textContent = item.name; // kullanıcıya görünen metin
                document.getElementById("province").appendChild(opt); // select'e ekle
            });
        })
        .catch(error => console.error("İl verisi yüklenirken hata:", error)); // hata yakalama

    // 4️⃣ Province select elementini seç
    const provinceSelect = document.getElementById("province");

    // 5️⃣ İl seçildiğinde çalışacak event listener
    provinceSelect.addEventListener("change", () => {

        // 6️⃣ Seçilen il adı
        const selectedProvince = provinceSelect.value;

        // 7️⃣ İl adına göre API URL oluştur
        const DISTRICTS_URL = `https://api.turkiyeapi.dev/v1/provinces?name=${selectedProvince}`;

        // 8️⃣ Fetch ile ilçeleri çek
        fetch(DISTRICTS_URL)
            .then(response => response.json())
            .then(data => {
                // 9️⃣ District select elementini seç ve temizle
                const districtSelect = document.getElementById("district");
                districtSelect.innerHTML = "<option selected disabled>Select District</option>";
                districtSelect.disabled = false;

                // 10️⃣ API’den gelen ilçeler
                const districts = data.data[0].districts || [];

                // 11️⃣ Her ilçe için option oluştur ve select’e ekle
                districts.forEach(district => {
                    const opt = document.createElement("option");
                    opt.value = district.name;
                    opt.textContent = district.name;
                    districtSelect.appendChild(opt);
                });
            })
            .catch(error => console.error("İlçe verisi yüklenirken hata:", error)); // fetch hatası yakalama
    });
});