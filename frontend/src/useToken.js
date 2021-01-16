import {useState} from 'react';

/**
 * Custom useState hook for storing user tokens in session storage
 */
export default function useToken() {

    const getToken = () => {
        const JSONToken = sessionStorage.getItem('token');
        const token = JSON.parse(JSONToken);
        return token?.token
    }

    const [token, setToken] = useState(getToken());

    const saveToken = (token) => {
        sessionStorage.setItem('token', JSON.stringify(token));
        setToken(token);
    }

    return [token, saveToken];
}