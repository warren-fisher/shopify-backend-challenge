import { useEffect, useState } from "react";
import React from 'react';

export default function Login() {

    const [username, setUserName] = useState();
    const [password, setPassword] = useState();

    return (
        <div id="login-wrapper">
            <h3> Please login </h3>

            <form>

                <label>
                    <p>Username</p>
                    <input type="text" onChange={e => setUserName(e.target.value)}/>
                </label>

                <label>
                    <p>Password</p>
                    <input type="text" onChange={e => setPassword(e.target.value)} />
                </label>

                <div>
                    <button type="submit">Submit</button>
                </div>

            </form>


        </div>
    );
}