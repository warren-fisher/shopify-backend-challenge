import { useEffect, useState } from "react";
import React from 'react';

import './login.css'

async function loginUser(username, hash) {

    const formData = new FormData();
    formData.append('user', username);
    formData.append('hash', hash);

    return fetch('https://apis.warrenfisher.net/post/login', {
        method: 'POST',
        body: formData,
    }).then(response => response.json());
}

async function registerUser(username, hash) {

    const formData = new FormData();
    formData.append('user', username);
    formData.append('hash', hash);

    return fetch('https://apis.warrenfisher.net/post/register', {
        method: 'POST',
        body: formData,
    }).then(response => response.json());
}

async function getHash(password) {
    let hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(password));
    hash = new Uint8Array(hash);

    let final_hash = '';
    for (let char of hash) {
        final_hash += btoa(String.fromCharCode(char)).slice(0,2);
    }
    return final_hash;
}

async function checkUser(username) {
    return fetch(`https://apis.warrenfisher.net/get/username/${username}`).then(response => response.json())
}

/**
 *
 *
 * @param {func} props.setToken, function to set the token
 */
export default function Login(props) {

    // State for username and password
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    // State for checking if username & password are valid
    const [validUser, setValidUser] = useState(true);
    const [validPassword, setValidPassword] = useState(true);

    const handleSubmit = async e => {
        // We don't want the form to submit since we have our own custom methods of doing this
        e.preventDefault();

        let hash = await getHash(password);

        const token = await loginUser(username, hash);
        console.log(token);
        props.setToken(token);
    }

    // TODO: updating of states is one step behind (everywhere??)
    const handleRegister = async e => {
        // We don't want the form to submit since we have our own custom methods of doing this
        e.preventDefault();

        let availableUser = await checkUser(username);
        passwordCheck();

        if (availableUser['available'] === true) {
            setValidUser(true);
        } else {
            setValidUser(false);
        }

        console.log(validPassword, validUser);
        if (validPassword == true && validUser == true) {
            let hash = await getHash(password);
            let token = await registerUser(username, hash);
            console.log(token);
        }
    }

    const passwordCheck = () => {
        console.log(password);

        if (password == undefined || password.length < 8) {
            setValidPassword(false);
        } else {
            setValidPassword(true);
        }
    }

    return (
        <div id="login-wrapper">
            <h3> Please login </h3>

            <form>

                <label>
                    <p>Username</p>
                    <input className={validUser == true ? "valid" : "invalid"} type="text" onChange={e => setUserName(e.target.value)}/>
                </label>

                <label>
                    <p>Password</p>
                    <input className={validPassword == true ? "valid" : "invalid"} type="text" onChange={e => setPassword(e.target.value)}/>
                </label>

                <div>
                    <button type="submit" onClick={handleSubmit}>Login</button>
                </div>
                <div>
                    <button type="submit" onClick={handleRegister}>Register</button>
                </div>

            </form>


        </div>
    );
}