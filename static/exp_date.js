const today = new Date();
today.setDate(today.getDate() + 365);
const minDate = today.toISOString().split("T")[0];
document.getElementById("pass_exp").min = minDate;