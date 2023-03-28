import './App.css';
import styled from 'styled-components';
import { BsUpload } from 'react-icons/bs'
import Tablefiles from "./components/Tablefiles.js"
import Header from './components/Header';
import axios from 'axios';
import { useEffect, useState } from 'react';


function App() {
  const [uploadFiles, setUpfiles] = useState([]);
  const [tableData, setTableData] = useState([]);

  function uploadFn(){
    if (!uploadFiles) return;
    console.log("upload files is", uploadFiles);
    console.log("object entries uploadfiles", Object.entries(uploadFiles));
    Object.entries(uploadFiles).forEach(([index, upfile]) => { // key=index, value=upfile
      console.log("What is upfile INDEX", index, "upfile", upfile)
      const formData = new FormData();
      formData.append("uploaded_file", upfile);
      axios.post("/uploadfile", formData, {headers :{
        "Content-Type": "multipart/form-data",
      }})
      .then(res => {
        console.log("Receive response for index", index);
        console.log(res);
        console.log(res.data);
        updateTableData();
      });
    })
    //alert('Upload Button was clicked');
  }

  const updateTableData = () => {
    axios.get("/fileslist/")
      .then(res => {
        console.log("Received table data");
        console.log(res);
        console.log("Res.data is");
        console.log(res.data);
        console.log("The files are ", res.data.files);

        // since backend does not return everything for now manually simulate json data
        const jsondata = {};
        res.data.files.forEach((fname, index) => {
          console.log(`\tLoop at filename ${fname} and index ${index}`);
          jsondata[fname] = {
            type: "file",
            size: 110011,
            last_modified: "18th January 2023 8:59pm",
            last_modified_by: "Anonimous"
          }
        });

        console.log("json data at the end is ", jsondata);
        setTableData(jsondata);
      });
  }

  useEffect(() => {
    updateTableData();
  }, [])
  return (
    <>
      <Header />
      <div className='ButtonRow'>
        <div>
          <main>
            <div>
              <div onClick={() => document.querySelector(".input-field").click()}>
                {/* <input type="file" accept='image/*' className='input-field' hidden onChange={(e) => setUpfiles(e.target.files)} onInput={uploadFn} multiple/> */}
                <input type="file" accept='image/*' className='input-field' hidden onChange={(e) => setUpfiles(e.target.files)} multiple />

                <BsUpload size={36} className='uploadButton' />
              </div>
              <button onClick={uploadFn}>Upload</button> {/* using button is better since onInput triggers before onChange (so empty files list is used instead)*/}
              </div>

          </main>
        </div>
      </div>

      <Tablefiles data={tableData}/>

    </> 
  );
}

export default App;
