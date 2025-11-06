const today = new Date();
today.setDate(today.getDate() + 15);
const minDate = today.toISOString().split("T")[0];
document.getElementById("pref_date").min = minDate;