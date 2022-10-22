let file_name = location.pathname.substring(location.pathname.lastIndexOf("/") + 1);
let table_name = file_name.slice(0, -5);
console.log(table_name);

document.getElementById("nav").innerHTML = `
<div class="left_panel_top">
<a href="index.html"><span class="material-symbols-outlined nav_icons home_icon">home</span></a>               
</div>
<div class="left_panel_middle">
<a href="pescas.html"><span class="material-symbols-outlined nav_icons" id="pescas_nav">set_meal</span></a>
<a href="metodos.html"><span class="material-symbols-outlined nav_icons" id="metodos_nav">phishing</span></a>
<a href="cuencas.html"><span class="material-symbols-outlined nav_icons" id="cuencas_nav">water</span></a>
<span class="material-symbols-outlined nav_icons">info</span>
<span class="material-symbols-outlined nav_icons">help</span> 
</div>
<div class="left_panel_bottom">       
<span class="material-symbols-outlined nav_icons" onclick="alert('esto no funciona jeje')">logout</span>
</div>
`;

if (table_name === "pescas") {
    document.getElementById("pescas_nav").classList.toggle("selected");
}
else if (table_name === "metodos") {
    document.getElementById("metodos_nav").classList.toggle("selected");
}
else if (table_name === "cuencas") {
    document.getElementById("cuencas_nav").classList.toggle("selected");
}

function write_error (error_msg) {
    console.log("write_error() called");
    alert(error_msg);
    document.location.href = "index.html";
}
function write_msg (msg) {
    console.log("write_msg() called");
    alert(msg);
}
function clean_fields () {
    console.log("clean_fields() called");
    inputs = document.getElementsByClassName("crud_input");
    for (let i of inputs) { i.value=""; }
}
