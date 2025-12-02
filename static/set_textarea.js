// ENG: Script for filling the textarea
// TR: Textarea'yı doldurmak için script

let textarea = document.querySelector('textarea');

let text_value = document.getElementById('text_data').value;

textarea.value = text_value;