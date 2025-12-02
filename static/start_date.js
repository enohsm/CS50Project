// ENG: Script to set the earliest insurance start date as today
// TR: Sigortanın en erken başlangıç tarihini bugün olarak ayarlama scripti

const minDate = new Date().toISOString().split("T")[0];
document.querySelector("#start_date").min = minDate;