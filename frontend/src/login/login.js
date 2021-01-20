import { useEffect, useState } from "react";
import React from 'react';
import {useHistory} from "react-router-dom";

import './login.css'

import api_endpoint from '../config.js';

async function loginUser(username, hash) {

    const formData = new FormData();
    formData.append('user', username);
    formData.append('hash', hash);

    return fetch(`${api_endpoint}/post/login`, {
        method: 'POST',
        body: formData,
    }).then(response => response.json());
}

async function registerUser(username, hash) {

    const formData = new FormData();
    formData.append('user', username);
    formData.append('hash', hash);

    return fetch(`${api_endpoint}/post/register`, {
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
    return fetch(`${api_endpoint}/get/username/${username}`).then(response => response.json())
}

/**
 * React component to handle logging in to the application
 *
 * @param {func} props.setToken, function to set the token
 * @param {func} props.setUser, function to set the logged in user's name
 *                  Only purpose is for visual display, the token is used for identity verification
 */
export default function Login(props) {

    // State for username and password
    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    // State for checking if username & password are valid
    const [validUser, setValidUser] = useState(true);
    const [validPassword, setValidPassword] = useState(true);

    // History (for redirecting user upon login)
    const hist = useHistory();

    const handleSubmit = async e => {
        // We don't want the form to submit since we have our own custom methods of doing this
        e.preventDefault();

        let hash = await getHash(password);

        const token = await loginUser(username, hash);

        // User did not register succesfully
        if (typeof (token) != 'string') {
            setValidPassword(false);
            setValidUser(false);
            return;
        }

        // User logged in succesfully
        props.setToken(token);
        props.setUser(username);

        hist.push("/");
    }

    // TODO: updating of states is one step behind (everywhere??)
    const handleRegister = async e => {
        // We don't want the form to submit since we have our own custom methods of doing this
        e.preventDefault();

        let availableUser = await checkUser(username);
        let pswValid = passwordCheck();
        setValidPassword(pswValid);

        if (availableUser['available'] === true) {
            setValidUser(true);
        } else {
            setValidUser(false);
        }

        // Dont use state (validPassword, validUser) because it will be one update behind this
        // Instead use the values found
        if (pswValid && availableUser['available']) {
            let hash = await getHash(password);
            let token = await registerUser(username, hash);

            // User did not register succesfully
            if (typeof(token) != 'string') {
                alert("problem registering. Try again");
                return;
            }

            // Users succesfully registered
            props.setToken(token);
            props.setUser(username);
            hist.push("/");
        }
    }

    const passwordCheck = () => {

        if (password == undefined || password.length < 8) {
            return false;
        } else {
            return true;
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
                    <p>Enter a password atleast 8 characters long</p>
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