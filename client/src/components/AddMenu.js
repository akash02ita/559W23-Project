import Dropdown from 'react-bootstrap/Dropdown';
import { Plus, FileEarmarkArrowUp, BoxArrowUp, FilePlus, FolderPlus } from 'react-bootstrap-icons';

function AddMenu() {
    return (
        <Dropdown>
          <Dropdown.Toggle variant="success" id="dropdown-basic">
            <Plus size={30}/>
            Add
          </Dropdown.Toggle>
    
          <Dropdown.Menu>
            <Dropdown.Item href="#/action-1"><FileEarmarkArrowUp />File upload </Dropdown.Item>
            <Dropdown.Item href="#/action-2"><BoxArrowUp />Folder upload</Dropdown.Item>
            <Dropdown.Item href="#/action-3"><FolderPlus />Create folder</Dropdown.Item>
            <Dropdown.Item href="#/action-3"><FilePlus />Create file</Dropdown.Item>
          </Dropdown.Menu>
        </Dropdown>
      );
}

export default AddMenu;

