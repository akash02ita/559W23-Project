import React from 'react'
import { Navbar, FormControl, InputGroup } from 'react-bootstrap'

function Header() {
  return (
    <Navbar bg="navBarcolor" expand="lg">
      <Navbar.Brand href="#home">
        <h1>DFS-D</h1>
        <h4>Distributed File System - Drive</h4>
      </Navbar.Brand>
    </Navbar>
  )
}

export default Header