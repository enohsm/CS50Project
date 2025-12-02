// ENG: Set the preferred date to be at least 15 days later
// TR: Tercih edilen tarihi en erken 15 gün sonrası seçilebilecek şekilde ayarla

const today = new Date();
today.setDate(today.getDate() + 15);
const minDate = today.toISOString().split("T")[0];
document.getElementById("pref_date").min = minDate;