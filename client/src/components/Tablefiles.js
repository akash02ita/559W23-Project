import Table from 'react-bootstrap/Table'
import { BsFiletypeTxt, BsDownload, BsTrash } from 'react-icons/bs'
import { FiEye } from 'react-icons/fi'
import { BiCheckbox } from 'react-icons/bi'


function downloadFn(){
    alert('Download Button was clicked');
}

function deleteFile(){
    alert('Delete Button was clicked');
}

function Tablefiles(){
    return(
        <div className='table-container'>
        <h1 className='myFilesHeader'> My Files</h1>            
        <Table striped bordered hover>
      <thead>
        <tr>
          <th>Select</th>
          <th>Type</th>
          <th>Name</th>
          <th>Last Modified</th>
          <th>Last Modified By</th>
          <th>Size</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td> <BiCheckbox></BiCheckbox></td>
          <td> <BsFiletypeTxt/> </td>
          <td>Some File</td>
          <td>2023-03-23 5:30 PM</td>
          <td>Steve Jobs</td>
          <td>3.7 MB</td>
          <td> <FiEye></FiEye> 
               <BsDownload></BsDownload>  
               <BsTrash></BsTrash> 
          </td>
        </tr>
        <tr>
        <td> <BiCheckbox></BiCheckbox></td>
          <td> <BsFiletypeTxt/> </td>
          <td>File Xbox</td>
          <td>2023-03-23 5:30 PM</td>
          <td>Bill Gates</td>
          <td>3.7 MB</td>
          <td> <FiEye></FiEye> 
               <BsDownload></BsDownload>  
               <BsTrash></BsTrash>
          </td> 
        </tr>
        <tr>
        <td> <BiCheckbox></BiCheckbox></td>
          <td> <BsFiletypeTxt/> </td>
          <td>File Azure</td>
          <td>2023-03-23 5:30 PM</td>
          <td>Satya Nadella</td>
          <td>3.7 MB</td>
          <td> <FiEye></FiEye> 
               <BsDownload></BsDownload>  
               <BsTrash></BsTrash>
          </td>  
        </tr>
      </tbody>
    </Table>
      </div>
    );
}

export default Tablefiles;