const minDate = new Date().toISOString().split("T")[0];
document.querySelector("#start_date").min = minDate;