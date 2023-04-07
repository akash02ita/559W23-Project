import './App.css';
import styled from 'styled-components';
import { BsUpload } from 'react-icons/bs'
import Tablefiles from "./components/Tablefiles.js"
import Header from './components/Header';
import AddMenu from './components/AddMenu';
import axios from 'axios';
import { useEffect, useState } from 'react';
import sample_data from './data/data.json'
import React from 'react';

export const FilesContext = React.createContext();


function App() {
 
  const [files, setFiles] = useState([]);

  const pollForList = () => {
    axios.get("/fileslist")
    .then(res => {
      console.log("Received table data");
      console.log(res);
      console.log("res.data is");
      console.log(res.data);
      {/* The response here is an array with just the names of the file */}
      console.log("The list of files inside handleDone is: ");
      console.log(res.data);
      setFiles(res.data);
    })
  }

  return (
    <>
      <FilesContext.Provider value={{files, setFiles}}>
        <Header />

        <div style={{ display: 'flex', justifyContent: 'center', marginTop: "1em" }}>
          <AddMenu />
        </div>

        <div style={{ width: "80%" }}>
          {/*Passing an empty string for now so that it renders the headers of the table. Passing null will not allow anything to render */}
          <Tablefiles data={""} mode="home" />
        </div>
      </FilesContext.Provider>
    </> 
  );
}

export default App;