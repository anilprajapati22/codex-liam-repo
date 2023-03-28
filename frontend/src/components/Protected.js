import React, { Component } from 'react'
import {
	Navigate
} from 'react-router-dom';


export default function Protected(props) {
    var auth = localStorage.getItem('auth');
    console.log(auth, typeof auth)
    
    return auth === 'true' ? <props.cmp/> : <Navigate to="/login" />
    
}

