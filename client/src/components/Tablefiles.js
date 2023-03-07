import {RiDeleteBin6Line} from 'react-icons/ri'
import axios from 'axios';


function downloadFn(filePath){
  // must encode in url parameter format (? and =)
  axios.get(`/downloadfile/${filePath}`, { responseType: "blob"})
    .then(res => {
      console.log(`/downloadfile/${filePath} returned`, res);
      console.log(res.data);
      return res.data;
    })
    .then(blob => {
      // source : https://stackoverflow.com/questions/73410132/how-to-download-a-file-using-reactjs-with-axios-in-the-frontend-and-fastapi-in-t
      
      var url = window.URL.createObjectURL(blob);
      var a = document.createElement('a');
      a.href = url;

      const fname = filePath; // for now filepath is just same as filename
      a.download = fname;

      document.body.appendChild(a); // append the element to the dom
      a.click();
      a.remove(); // afterwards, remove the element  
    });
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
                            <button onClick={() => downloadFn(fname)} className="Download_Btn"> Download </button>
                            <RiDeleteBin6Line size={30} onClick={deleteFile} className='trashIcon' />
                        </div>
                    </td>

                </tr>
            );
        });

        return rows;
    }

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