if (window.location.href.endsWith("edit")) {
  // you could be all code in here so that if this JS runs on a
  // page without the editor - it will be ignored
}

// Initialize Quill editor 

var toolbarOptions = [
  ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
  ['blockquote', 'code-block'],

  [{ 'header': 1 }, { 'header': 2 }],               // custom button values
  [{ 'list': 'ordered'}, { 'list': 'bullet' }],
  [{ 'script': 'sub'}, { 'script': 'super' }],      // superscript/subscript
  [{ 'indent': '-1'}, { 'indent': '+1' }],          // outdent/indent
  [{ 'header': [1, 2, 3, 4, 5, 6, false] }],

  [{ 'color': [] }, { 'background': [] }], 
  [{ 'align': [] }],

  ['clean']                                         // remove formatting button
];

let quill = new Quill('#editor', {
  theme: 'snow',
  modules: {
    toolbar: toolbarOptions
  }
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