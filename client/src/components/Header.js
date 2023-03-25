import React from 'react'
import { Navbar, Nav, Form, FormControl, Button, InputGroup } from 'react-bootstrap'
import { Search, Funnel } from 'react-bootstrap-icons'
function Header() {
  return (
    <Navbar bg="navBarcolor" expand="lg">
      <Navbar.Brand href="#home">
        <h1>DFS-D</h1>
        <h4>Distributed File System - Drive</h4>
      </Navbar.Brand>
      
      <div className="w-50 p-3">
      <InputGroup>
      <InputGroup.Text><Search /></InputGroup.Text>
      <FormControl type="text" placeholder="Search"/>
      <InputGroup.Text><Funnel /></InputGroup.Text>
      </InputGroup>
      </div>
    </Navbar>
  )
}

export default Header