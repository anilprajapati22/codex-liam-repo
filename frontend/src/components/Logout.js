import React, { Component } from 'react'
import { Navigate } from 'react-router-dom';

export default class Logout extends Component {
  render() {
    localStorage.setItem('auth',false);
    return (
      <Navigate to="/login" />
    )
  }
}
