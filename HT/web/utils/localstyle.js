// web/utils/localStyle.js
export function applyUserStyle(cssString, id="user-style"){
  let tag = document.getElementById(id);
  if(tag) tag.remove();
  tag = document.createElement("style"); tag.id = id; tag.innerHTML = cssString; document.head.appendChild(tag);
}
