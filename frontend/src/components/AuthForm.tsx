import '../assets/css/authform.css'
import { useRef, type RefObject } from 'react'
import { api } from '../Api'


export const AuthForm = () =>{
    let emailRef = useRef();
    let passwordRef = useRef();

    const loginUser = async()=>{
        const form = new URLSearchParams();
        form.append("username",emailRef.current.value);
        form.append("password",passwordRef.current.value);

        api.post('/auth/token',form)
        .then(function (response){
            console.log(response);
        })
        .catch(function (error){
            console.log(error)
        })
    }

    const handleSubmit = (event) =>{
        event.preventDefault();
        loginUser(); 
    }

    return (
    <>
    <div className="formWrapper">
    <form onSubmit={handleSubmit}>
        {/* <h2>Managr.</h2> */}
        <h4>Login</h4>
        <div className="formSection">
            <label htmlFor="email">Email</label>
            <input type="email" id="email" name="email" ref={emailRef} required/>
        </div>
        <div className="formSection">
            <label htmlFor="password">Password</label>
            <input type="password" id="password" name="password" ref={passwordRef} required />
        </div>
        <button type="submit">submit</button>
    </form>
    </div>
    </>
    )
}