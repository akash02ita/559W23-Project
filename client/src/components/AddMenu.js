import Dropdown from 'react-bootstrap/Dropdown';
import { Plus, FileEarmarkArrowUp, BoxArrowUp, FilePlus, FolderPlus } from 'react-bootstrap-icons';
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
          <Dropdown.Item href="#/action-2"><BoxArrowUp />Folder upload</Dropdown.Item>
          <Dropdown.Item href="#/action-3"><FolderPlus />Create folder</Dropdown.Item>
          <Dropdown.Item href="#/action-3"><FilePlus />Create file</Dropdown.Item>
        </Dropdown.Menu>
      </Dropdown>
      <FileUpload flag={fileUploadFlag} setFlag={setFileUploadFlag}/>
    </>
  );
}

export default AddMenu;

