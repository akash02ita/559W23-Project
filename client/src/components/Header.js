import React from 'react'
import { Navbar } from 'react-bootstrap'
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Logo from '../logo.png'

function Header() {
  return (
    <Navbar bg="navBarcolor" expand="lg" className='app-navbar'>
      <Navbar.Brand href="#home">
        <Container>
          <Row className="justify-content-md-center">
            <Col style={{alignSelf: "center"}}>
              <img
                alt="Logo"
                src={Logo}
                style={{width: '4rem'}}
              />
              </Col>
            <Col>
              <h1>DFS-D</h1>
              <h4>Distributed File System - Drive</h4>
            </Col>
          </Row>
        </Container>
      </Navbar.Brand>
    </Navbar>
  )
}

export default Header