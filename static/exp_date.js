// ENG: The passport expiration date must be at least one year later
// TR: Pasaportun geçerlilik tarihi en az bir yıl sonrası olmalı

const today = new Date();
today.setDate(today.getDate() + 365);
const minDate = today.toISOString().split("T")[0];
document.getElementById("pass_exp").min = minDate;