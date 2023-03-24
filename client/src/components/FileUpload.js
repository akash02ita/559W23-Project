
import React, { useState } from 'react'
import { Modal, Button } from 'react-bootstrap';

function FileUpload({flag, setFlag}) {
  const handleDone = () => {
    // TODO: fetch api call for file upload
    // on success: back
    // on failure: danger alert for failure
    setFlag(false);
  };
  const handleCancel = () => {
    setFlag(false);
  }

  return (
    <Modal show={flag} onHide={handleCancel} backdrop="static" keyboard={false}>
      <Modal.Header closeButton>
        File upload
      </Modal.Header>
      <Modal.Body>
        TODO: add a table builder with scroll. (use containers)
        {/* https://react-bootstrap.netlify.app/components/modal/#using-the-grid */}
        TODO: add a click and drag dotted area
      </Modal.Body>
      <Modal.Footer>
        <Button variant="primary" onClick={handleDone}>Done</Button>
        <Button variant="secondary" onClick={handleCancel}>Cancel</Button>
      </Modal.Footer>

    </Modal>
  )
}

export default FileUpload;