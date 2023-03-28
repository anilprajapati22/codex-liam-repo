import './App.css';
import axios from 'axios';
import React, { useState, useEffect } from 'react';

function App() {

  const [data, setData] = useState([]); 
  const [case_id, setCase] = useState([]);

  const Upload_file = (e) =>{
    console.log(e);
    console.log(e.target.files);
    const files = e.target.files;
    const formData = new FormData();
    formData.append('file', files[0]);
    console.log("before");
    fetch("http://127.0.0.1:5000/file-upload",{
        method: "POST",
        body : formData    }).then((resp) => {
            resp.json().then((result) => {
                console.log("result",result)
            })
        })
    console.log("after");    
  }
  


  const handleFetch = async () => {
    const response = await fetch('https://5fp8wdighc.execute-api.ap-south-1.amazonaws.com/v1/hello');
    const data = await response.json();
    console.log(data);
    setData(data);
    };
  let Ptag;
  if ('sgnons' in data){
  Ptag = data['sgnons'].map( (d) => {
      return(
        <div>
        <button value={d} onClick={setCase({d})} > {d} </button> 
        
        
        </div>
        )});
  }
  return (
    <div className="App">
      <button onClick={handleFetch}>sgnons</button>
      <input type="file" onChange={ (e) => Upload_file(e)} name="img" /> 
        {Ptag}
    </div>
  );
}

export default App;
