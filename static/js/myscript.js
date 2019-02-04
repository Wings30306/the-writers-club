if (window.location.href.endsWith("edit")) {
  // you could be all code in here so that if this JS runs on a
  // page without the editor - it will be ignored
}

// Initialize Quill editor 
let quill = new Quill('#editor', {
  theme: 'snow'
});


// Variables
const form = document.querySelector('#form');
const editor = document.querySelector('#editor');
const hiddenInput = document.querySelector('#hidden-input');
const qlEditor = document.querySelector(".ql-editor");


// Listen for submit and intersept
form.addEventListener('submit', (event) => {
  
  // prevent form from being submitted until we are ready
  event.preventDefault();
  
  // get innerHTML from editor and convert to JSON
  let data = JSON.stringify(qlEditor.innerHTML);

  // apply json data to hidden input value
  hiddenInput.value = data;
  console.log(data)

  // allow form to be submitted
  form.submit()
});