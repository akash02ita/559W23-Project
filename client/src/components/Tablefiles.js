import Table from 'react-bootstrap/Table'
import { BsFiletypeTxt, BsDownload, BsTrash } from 'react-icons/bs'
import { FiEye } from 'react-icons/fi'
import { BiCheckbox } from 'react-icons/bi'
import GetIcon from '../utils/GetIcon.js'

// nothing: when not hovering on row and row is not selected
// circle: when hovering on table
// checkcircle: when hovering on circle
// checkcirclefill: when row is selected
import { Circle, CheckCircle, CheckCircleFill } from 'react-bootstrap-icons'
import { useState } from 'react'

function downloadFn() {
  alert('Download Button was clicked');
}

function deleteFile() {
  alert('Delete Button was clicked');
}

function Tablefiles({ data }) {
  const jsondata = data;
  const lengthData = Object.keys(data).length;

  const [selectedRows, setSelectedRows] = useState([]);
  const [hovereredRows, setHovereredRows] = useState([]);

  const handleRowSelect = (index) => setSelectedRows((prev) => [...prev, index]);
  const handleRowUnSelect = (index) => setSelectedRows((prev) => prev.filter((i) => i !== index));
  const handleRowHover = (index) => !isRowHovered(index) ? setHovereredRows((prev) => [...prev, index]) : undefined;
  const handleRowUnHover = (index) => isRowHovered(index) ? setHovereredRows((prev) => prev.filter((i) => i !== index)) : undefined;
  const isRowSelected = (index) => selectedRows.includes(index);
  const isRowHovered = (index) => hovereredRows.includes(index);
  const handleRowClick = (index) => isRowSelected(index) ? handleRowUnSelect(index) : handleRowSelect(index);

  const renderData = () => {
    const rows = Object.entries(jsondata).map(([fname, fprops], index) => {
      console.log("data index is", index, "with fname", fname, "and fprops", fprops);
      const putCheckMark = (index) => {
        if (isRowSelected(index)) return <CheckCircleFill size={20} />;
        if (isRowHovered(index)) return <Circle size={20} />;
        return <></>; // do not put anything otherwise
      }
      return (
        <tr key={index}  
          onMouseEnter={() => handleRowHover(index)}
          onMouseLeave={() => handleRowUnHover(index)}
          onClick={() => handleRowClick(index)} 
        >
          <td> {putCheckMark(index)} </td>
          <td> <GetIcon fname={fname} size={30} type={fprops.type} /> </td>
          <td>{fname}</td>
          <td>{fprops.last_modified}</td>
          <td>{fprops.last_modified_by}</td>
          <td>{fprops.size} B</td>
          <td>
            <FiEye></FiEye>
            <BsDownload></BsDownload>
            <BsTrash></BsTrash>
          </td>
        </tr>
      );
    });

    return rows;
  }


  return (
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
          {renderData()}
        </tbody>
      </Table>
    </div>
  );
}

export default Tablefiles;