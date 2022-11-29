
btn_ = document.querySelector(".btn");
btn_.onclick = function() {
    let selected = document.getElementById("project_name").value;
    let upload = document.getElementById("files").value;
    if (selected!="" && upload!="") {
        this.classList.toggle('btn_load')
        this.innerHTML = "transcribing&nbsp;";

    }   
}
