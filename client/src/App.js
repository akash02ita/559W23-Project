import './App.css';
import styled from 'styled-components';
import { BsUpload } from 'react-icons/bs'

const Button = styled.button`
  background-color: #0072C6;
  color: white;
  padding: 5px 15px;
  border-radius: 10px;
  border-color: #FFFFFF;
  outline: 0;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 0px 2px 2px lightgray;
  transition: ease background-color 250ms;
  &:hover {
    background-color: #546e7a;
  }
`


function downloadFn(){
  alert('Download Button was clicked');
}

function uploadFn(){
  alert('Upload Button was clicked');
}

function App() {
  return (
    <>
      <div className="App">
        <h1 id='headerTxt'> DFS-D</h1>
        

          <label id="searchLabel"> Search </label>

        <div>
          <input type="text" className='SearchBar' />
        </div>

      </div>

      <div className='ButtonRow'>
        <div>
          <Button onClick={downloadFn} className="Download_Btn">
            Download
          </Button>
        </div>
        <div>
          <main>
            <form onClick={ () => document.querySelector(".input-field").click()}
            >
              <input type="file" accept='image/*' className='input-field' hidden />

              <BsUpload size={30}/>


            </form>
          
          </main>

            
            
        </div>
      </div>
      
      
    </> 
  );
}

export default App;
