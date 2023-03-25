import Table from 'react-bootstrap/Table'
import GetIcon from '../utils/GetIcon.js'

// nothing: when not hovering on row and row is not selected
// circle: when hovering on table
// checkcircle: when hovering on circle
// checkcirclefill: when row is selected
import { Circle, CheckCircle, CheckCircleFill } from 'react-bootstrap-icons'
import { Eye, Download, Trash } from 'react-bootstrap-icons'
import { ButtonGroup, Button } from 'react-bootstrap'
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

  const handleRowSelect = (i) => setSelectedRows((prev) => [...prev, i]);
  const handleRowUnSelect = (i) => setSelectedRows((prev) => prev.filter((iprev) => iprev !== i));
  const handleRowHover = (i) => !isRowHovered(i) ? setHovereredRows((prev) => [...prev, i]) : undefined;
  const handleRowUnHover = (i) => isRowHovered(i) ? setHovereredRows((prev) => prev.filter((iprev) => iprev !== i)) : undefined;
  const isRowSelected = (i) => selectedRows.includes(i);
  const isRowHovered = (i) => hovereredRows.includes(i);
  const handleRowClick = (i) => isRowSelected(i) ? handleRowUnSelect(i) : handleRowSelect(i);

  const [hoveredTickMarks, setHovereredTickMarks] = useState([]);
  const handleHoverTickMark = (i) => !isTickMarkHovered(i) ? setHovereredTickMarks((prev) => [...prev, i]) : undefined;
  const handleUnHoverTickMark = (i) => isTickMarkHovered(i) ? setHovereredTickMarks((prev) => prev.filter((iprev) => iprev !== i)) : undefined;;
  const isTickMarkHovered = (i) => hoveredTickMarks.includes(i);

  const renderData = () => {
    const rows = Object.entries(jsondata).map(([fname, fprops], index) => {
      console.log("data index is", index, "with fname", fname, "and fprops", fprops);
      const putCheckMark = (index) => {
        if (isRowSelected(index)) return <CheckCircleFill size={20} />;
        if (isTickMarkHovered(index)) return <CheckCircle size={20} onMouseLeave={() => handleUnHoverTickMark(index)} />;
        if (isRowHovered(index)) return <Circle size={20} onMouseEnter={() => handleHoverTickMark(index)} />;
        return <></>; // do not put anything otherwise
      }
      const putActions = (index) => {
        // TODO: add 3 dot button on side
        if (isRowHovered(index) || isRowSelected(index)) return (
          <ButtonGroup>
          <Button variant="outline-primary"><Eye size={25} /></Button>
          <Button variant='outline-success'><Download size={25} /></Button>
          <Button variant="outline-danger"><Trash size={25} /></Button>
        </ButtonGroup>
        );
        // ensure that if no butotn group is selected the size still matches. Otherwise suddent growth in size is odd.
        // this is ensure using col-2 classname in td
        return <></>;
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
          <td className='col-2'>{putActions(index)}</td>
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