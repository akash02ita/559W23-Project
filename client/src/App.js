import './App.css';
import styled from 'styled-components';
import { BsUpload } from 'react-icons/bs'
import Tablefiles from "./components/Tablefiles.js"
import Header from './components/Header';
import AddMenu from './components/AddMenu';



function uploadFn(){
  alert('Upload Button was clicked');
}

function App() {
  return (
    <>
      
      <Header/>

      <div style={{display: 'flex', justifyContent: 'center', marginTop: "1em"}}>
        <AddMenu />
      </div>

      <Tablefiles />

    </> 
  );
}

export default App;
