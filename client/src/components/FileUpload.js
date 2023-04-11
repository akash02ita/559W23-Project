import React, { useState } from 'react'
import { Modal, Button } from 'react-bootstrap';
import Tablefiles from './Tablefiles.js'
import { useDropzone } from 'react-dropzone';
import Dropzone from 'react-dropzone';
import { PlusSquareDotted } from 'react-bootstrap-icons';
import axios from 'axios';
import { useContext } from 'react';
import { FilesContext } from '../App.js';


{/* The flag and setFlag props are
passed from the AddMenu component */}
function FileUpload({ flag, setFlag }) {


  {/*const [files, setFiles] = useState([]);
    I got rid of the above line to prevent "prop drilling
  The useContext will allow any component to use the data as long 
 as it has the import statement and it's within the useContext wrapper in App.js -> return 

  In App.js, it's set to the state Hooks, hence it receives the two parameters*/} 

  const {files, setFiles} = useContext(FilesContext);
  {/* filesSelected is for table in Modal*/}
  const [filesSelected, setFilesSelected] = useState([]);
  
  const getFilesJson = () => {

      // I only need the files that user has currently selected.
      console.log("Files Selected by User are ", filesSelected);
      const data = {};
      
      Object.values(filesSelected).forEach((val) => {
        console.log("The val is ", val);
        const fname = val.name;
        const type = "file";
        const size = val.size;
        const last_modified = val.lastModifiedDate;
        const last_modified_by = "Anonimous";
        data[fname] = {
          "type": type,
          "size": size,
          "last_modified": last_modified,
          "last_modified_by": last_modified_by,
        };
      });
      
      return data;
  }

  function updateList(){
    setTimeout(async function() {
      try{
        axios.get("/fileslist")
        .then(res => {
          console.log("Received table data");
          console.log(res);
          console.log("res.data is");
          console.log(res.data);
          {/* The response here is an array with just the names of the file */}
          console.log("The list of files inside handleDone is: ");
          console.log(res.data);
          setFiles(res.data.files);
        })
      }
      catch(error){
        console.log(error);
      }
    }, 500 );
    
  }

  const handleDone = () => {
     
    console.log("upload files inside handleDone is", filesSelected);
    console.log("object entries uploadfiles", Object.entries(filesSelected));

    Object.entries(filesSelected).forEach(([index, upfile]) => {
      console.log("What is upfile INDEX", index, "upfile", upfile)
      const formData = new FormData();
      formData.append("uploaded_file", upfile);
      axios.post("/uploadfile", formData, {headers :{
        "Content-Type": "multipart/form-data",
      }})
      .then(res => {
        console.log("Server has replied. Files have been uploaded.")
        console.log("Receive response for index", index);
        console.log(res);
        console.log(res.data);
    })})  
    setFlag(false);
    {/* To get rid of files that would otherwise stay in the "Add" -> Modal */}
    setFiles([]);
    setFilesSelected([]);

    {/*Let's get the latest list of file from the server at this point */}
    {/*The upload post request could actually be slower and then this getlist
       request returns empty. So this is not a good approach. */}

    updateList();
  }

  const handleCancel = () => {
    setFlag(false);
    {/* To clear whatever was left in the Modal */}
    setFilesSelected([]);
  }
  {/* This section is all about the File Upload Modal */}
  return (
    <Modal show={flag} onHide={handleCancel} backdrop="static" size="xl" scrollable centered> 
      <Modal.Header closeButton>
        File upload
      </Modal.Header>

      <Modal.Body>
        {/* TODO: add a table builder with scroll. (use containers) */}
        {/* https://react-bootstrap.netlify.app/components/modal/#using-the-grid 
        data={""getFilesJson()""}
        */}
        <div>
          {/* The table here is for the files it display inside the Modal */}
          <Tablefiles data={getFilesJson()} mode="fileupload" />
        </div>
        <Dropzone onDrop={newfiles => setFilesSelected((prev) => prev.concat(newfiles))}>
          {({ getRootProps, getInputProps }) => (
            <section>
              <div {...getRootProps()}>
                <input {...getInputProps()} />
            
                <div className='text-secondary fs-4 text-center p-5'style={{ border: 'dotted' }}>
                    
                  <PlusSquareDotted size={50} />
                  <div>Click to browse or drag item(s) here</div>
                </div>
              </div>
            </section>
          )}
        </Dropzone>
      </Modal.Body>
      
      <Modal.Footer>
        <Button variant="primary" onClick={handleDone}>Done</Button>
        <Button variant="secondary" onClick={handleCancel}>Cancel</Button>
      </Modal.Footer>

    </Modal>
  )
}

export default FileUpload;