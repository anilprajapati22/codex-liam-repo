import React from "react";

function Upload_file(e){
    console.log(e);
    const files = e.target.files;
    const formData = new formData();
    formData.append('img', files[0]);
    fetch("http://127.0.0.1:5000/file-upload",{
        method: "POST",
        body : formData    }).then((resp) => {
            resp.json().then((result) => {
                console.log("result",result)
            })
        })
}

export default Upload_file;