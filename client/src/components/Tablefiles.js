import {RiDeleteBin6Line} from 'react-icons/ri'


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
                        <button onClick={downloadFn} className="Download_Btn"> Download </button>
                        <RiDeleteBin6Line size={30} onClick={deleteFile} className='trashIcon'/>
                    </div>
                </td>

            </tr>

            <tr>
                <td></td>
                <td>PDF</td>
                <td>Stakeholder Relations.pdf</td>
                <td>20/02/2022</td>
                <td>Carlos Veintimilla</td>
                <td>150 MB</td>
                <td>
                    <div className='actionItems'>
                        <button onClick={downloadFn} className="Download_Btn"> Download </button>
                        <RiDeleteBin6Line size={30} onClick={deleteFile} className='trashIcon'/>
                    </div>
                </td>

            </tr>

            <tr>
                <td></td>
                <td>Word</td>
                <td>SiteA-WeeklyMeetings-Notes.docx</td>
                <td>15/03/2021</td>
                <td>Harsweet Singh</td>
                <td>32 MB</td>
                <td>
                    <div className='actionItems'>
                        <button onClick={downloadFn} className="Download_Btn"> Download </button>
                        <RiDeleteBin6Line size={30} onClick={deleteFile} className='trashIcon'/>
                    </div>
                </td>

            </tr>


          </tbody>

        </table>
      </div>
    );
}

export default Tablefiles;