import {RiDeleteBin6Line} from 'react-icons/ri'


function downloadFn(){
    alert('Download Button was clicked');
}

function deleteFile(){
    alert('Delete Button was clicked');
}

function Tablefiles(props){
    const jsondata = props.data
    console.log("Tablefiles received json data", jsondata);

    const renderData = () => {
        const rows = Object.entries(jsondata).map(([fname, fprops], index) => {
            console.log("data index is", index, "with fname", fname, "and fprops", fprops);
            return (
                <tr key={index}>
                    <td></td>
                    <td>{fprops.type}</td>
                    <td>{fname}</td>
                    <td>{fprops.last_modified}</td>
                    <td>{fprops.last_modified_by}</td>
                    <td>{fprops.size} B</td>
                    <td>
                        <div className='actionItems'>
                            <button onClick={downloadFn} className="Download_Btn"> Download </button>
                            <RiDeleteBin6Line size={30} onClick={deleteFile} className='trashIcon' />
                        </div>
                    </td>

                </tr>
            );
        });

        return rows;
    }
    // TODO: apply get data functionality (renderData)
    // download link must be present in each download button
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
            {renderData()}
     


          </tbody>

        </table>
      </div>
    );
}

export default Tablefiles;