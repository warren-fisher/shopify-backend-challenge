import './App.css';

import Upload from './upload/upload.js';

import Gallery from './gallery/gallery.js';

import Album from './albums/album.js';

import Login from './login/login.js';

import React, {useState, useEffect} from 'react';

import {BrowserRouter, Route, Switch, Link} from 'react-router-dom';

import useToken from './useToken.js';

function App() {
    const [token, setToken] = useToken();
    const [loggedInUser, setLoggedInUser] = useState();

    return (
        <BrowserRouter>
            <header>
                <h2> Image hosting repository </h2>

                <h2><Link to={{pathname: "/",}}> Upload your images </Link> </h2>
                <h2><Link to={{pathname: "/albums",}}> Albums</Link></h2>
                <h2><Link to={{pathname: "/gallery",}}> Image Gallery</Link></h2>

                {/* Only display the login link if the user is not logged in*/}
                { token ?

                    <h2>Logged in as {loggedInUser}
                        <span onClick={()=> {setToken(undefined)}}>Logout</span>
                    </h2>
                    :
                    <h2><Link to={{ pathname: "/login", }}> Login</Link></h2>
                }


            </header>

            <div className="App">

                <Switch>

                    <Route exact path="/">
                        <Upload token={token}/>
                    </Route>

                    <Route path="/albums">
                        <Album token={token}/>

                    </Route>

                    <Route path="/gallery">
                        <Gallery token={token}/>
                    </Route>

                    <Route path="/login">
                        <Login setToken={setToken} setUser={setLoggedInUser}/>
                    </Route>

                </Switch>

            </div>


        </BrowserRouter>
    );
}

export default App;