export default function insertHtmlIntoTagId (tag, html){
  const node = document.getElementById(tag);
  if(!node){
    document.addEventListener("DOMContentLoaded", function () {
      // do things after the DOM loads partially
      insertHtml(tag, html)
    });
  } else {
    insertHtml(tag, html)
  }
 
} 

function insertHtml (tag, html) {
  const node = document.getElementById(tag);
  node.innerHTML = html;
}
