import styled from 'styled-components';
import {RiDeleteBin6Line} from 'react-icons/ri'

// Used for "Download Button"
const Button = styled.button`
  background-color: #0072C6;
  color: white;
  padding: 5px 5px ;
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

function deleteFile(){
    alert('Delete Button was clicked');
}

function Tablefiles(){
    return(
        <div className='table-container'>
        <table>
          <thead>
            <tr>
              <th>Select</th>  
              <th>Type</th>
              <th>Name</th>
              <th>Last Modified</th>
              <th>Last Modified by</th>
              <th>File Size</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
                <td></td>
                <td>Excel</td>
                <td>Q1 Balance Sheet.xlsx</td>
                <td>31/01/2023</td>
                <td>Akashdeep Singh</td>
                <td>4 MB</td>
                <td>
                    <div className='actionItems'>
                        <Button onClick={downloadFn} className="Download_Btn"> Download </Button>
                        <RiDeleteBin6Line size={30} onClick={deleteFile}/>
                    </div>
                </td>

            </tr>

            <tr>
                <td></td>
                <td>PDF</td>
                <td>Stakeholder Relations.pdf</td>
                <td>20/01/2022</td>
                <td>Carlos Veintimilla</td>
                <td>150 MB</td>
                <td>
                    <div className='actionItems'>
                        <Button onClick={downloadFn} className="Download_Btn"> Download </Button>
                        <RiDeleteBin6Line size={30} onClick={deleteFile}/>
                    </div>
                </td>

            </tr>
          </tbody>

        </table>
      </div>
    );
}

export default Tablefiles;