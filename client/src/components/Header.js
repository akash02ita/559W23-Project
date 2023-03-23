import React from 'react'
import { Navbar,Nav, Form, FormControl, Button } from 'react-bootstrap'

function Header() {
  return (
    <Navbar bg="light" expand="lg">
      <Navbar.Brand href="#home">DFS-D</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Form inline>
          <FormControl type="text" placeholder="Search" className="mr-sm-2" />
          <Button  variant="outline-success" className="searchButton">Search</Button>
        </Form>
      </Navbar.Collapse>
    </Navbar>
  )
}

export default Header