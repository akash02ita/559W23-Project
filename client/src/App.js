import './App.css';
import styled from 'styled-components';
import { BsUpload } from 'react-icons/bs'
import Tablefiles from "./components/Tablefiles.js"
import axios from 'axios';
import { useState } from 'react';



function App() {
  const [upfile, setUpfile] = useState(null);
  function uploadFn(){
    if (!upfile) return;

    console.log("What is upfile?", upfile)
    const formData = new FormData();
    formData.append("uploaded_file", upfile);
    axios.post("/uploadfile", formData, {headers :{
      "Content-Type": "multipart/form-data",
    }})
    .then(res => {
      console.log(res);
      console.log(res.data);
    })
    //alert('Upload Button was clicked');
  }
  return (
    <>
      <div className="App">
        <div>
          <h1 id='headerTxt'> DFS-D</h1>
            <footer id="footerInHeader"> Distributed File System - Drive</footer>
        </div>
          
        <div>
          <input type="text" className='SearchBar' placeholder='Search...' />
        </div>

      </div>

      <div className='ButtonRow'>
        <div>
          <main>
            <div onClick={ () => document.querySelector(".input-field").click()}>
              <input type="file" accept='image/*' className='input-field' hidden onChange={(e) => setUpfile(e.target.files[0])} onInput={uploadFn} multiple/>
              {/* <button onClick={uploadFn}>Upload</button> */}

              <BsUpload size={36} className='uploadButton'/>

            </div>

{/* <form action="/uploadfile/" encType="multipart/form-data" method="post">
<input name="uploaded_file" type="file" multiple />
<input type="submit" />
</form> */}
          
          </main>
        </div>
      </div>

      <Tablefiles />

    </> 
  );
}

export default App;
