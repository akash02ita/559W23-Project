import styled from 'styled-components';

// Used for "Download Button"
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

function Tablefiles(){
    return(
        <div className='table-container'>
        <table>
          <thead>
            <tr>
              <th>Type</th>
              <th>Name</th>
              <th>Last Modified</th>
              <th>File Size</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
                <td>Excel</td>
                <td>Q1 Balance Sheet.xlsx</td>
                <td>31/01/2023</td>
                <td>4 MB</td>
                <td><Button onClick={downloadFn} className="Download_Btn"> Download </Button></td>

            </tr>

            <tr>
                <td>PDF</td>
                <td>Stakeholder Relations.pdf</td>
                <td>20/01/2022</td>
                <td>150 MB</td>
                <td><Button onClick={downloadFn} className="Download_Btn"> Download </Button></td>

            </tr>
          </tbody>

        </table>
      </div>
    );
}

export default Tablefiles;