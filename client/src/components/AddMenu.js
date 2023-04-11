import Dropdown from 'react-bootstrap/Dropdown';
import { Plus, FileEarmarkArrowUp } from 'react-bootstrap-icons';
import FileUpload from './FileUpload';
import { useState } from 'react';

function AddMenu() {
  const [fileUploadFlag, setFileUploadFlag] = useState(false);
  return (
    <>
      <Dropdown>
        <Dropdown.Toggle variant="success" id="dropdown-basic">
          <Plus size={30} />
          Add
        </Dropdown.Toggle>

        <Dropdown.Menu>
          <Dropdown.Item onClick={() => setFileUploadFlag(true)}><FileEarmarkArrowUp />File upload </Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      {/* The two props that will be passed to FileUpload are flag and setFlag */}
      <FileUpload flag={fileUploadFlag} setFlag={setFileUploadFlag}/>
    </>
  );
}

export default AddMenu;

