// Variables
const form = document.querySelector('#form');
const editor = document.querySelector('#editor');
const hiddenInput = document.querySelector('#hidden-input');
const qlEditor = document.querySelector(".ql-editor");
​
​
​
​
// Listen for submit and intersept
form.addEventListener('submit', (event) => {
​
  // get innerHTML from editor and convert to JSON
  let data = JSON.stringify(qlEditor.innerHTML);
​
  // apply json data to hidden input value
  hiddenInput.value = data;
  console.log(data)
​
  // return true to allow data to be posted to the backend
  return true;
})
​