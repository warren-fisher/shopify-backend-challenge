import {useState} from 'react';

/**
 * Custom useState hook for storing user tokens in session storage
 */
export default function useToken() {

    const getToken = () => {
        const JSONToken = sessionStorage.getItem('token');

        if (JSONToken != "undefined") {
            const token = JSON.parse(JSONToken);
            return token?.token
        }

        return undefined;
    }

    const [token, setToken] = useState(getToken());

    const saveToken = (token) => {

        if (token === undefined) {
            token = '';
        }

        sessionStorage.setItem('token', JSON.stringify(token));
        setToken(token);
    }

    return [token, saveToken];
}