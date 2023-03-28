import React, { Component,useEffect } from 'react'
import {
	Navigate, redirect
} from 'react-router-dom';

export default class Login extends Component {
    
    login(){
        console.log("Sgnonsjkhjamjbm : ",this.state)
        if (this.state.email === 'liam' && this.state.password === 'GLiam'){
            localStorage.setItem('auth',true);
            console.log("sgnons login")
            window.location.replace("/")
                
        }
        else{
            localStorage.setItem('auth',false);   
        }
    }
  render() {
    var auth = localStorage.getItem('auth');
    console.log("login : ",auth)
    if (auth === 'true')
    {
        return(
            <Navigate to="/" />
        )
    }

    return (
        <>
            { localStorage.getItem('auth') === 'true' ? <Navigate to="/" /> : <>Login</> }
      <div>

        <input name='email' onChange={(e) => {this.setState({email:e.target.value})}} />

        <input name='password' onChange={(e) => {this.setState({password:e.target.value})}} />

        <button onClick={()=>this.login()}>Login</button>
      </div>
      </>
    )
  }
}
