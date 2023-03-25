import './App.css';
import styled from 'styled-components';
import { BsUpload } from 'react-icons/bs'
import Tablefiles from "./components/Tablefiles.js"
import Header from './components/Header';
import AddMenu from './components/AddMenu';
import sample_data from './data/data.json'



function uploadFn() {
  alert('Upload Button was clicked');
}

function App() {
  return (
    <>

      <Header />

      <div style={{ display: 'flex', justifyContent: 'center', marginTop: "1em" }}>
        <AddMenu />
      </div>
      <div style={{ width: "80%" }}>
        <Tablefiles data={sample_data} mode="home" />
      </div>
      <div style={{ width: "50%" }}>
        <Tablefiles data={sample_data} mode="fileupload" />
      </div>

    </>
  );
}

export default App;
