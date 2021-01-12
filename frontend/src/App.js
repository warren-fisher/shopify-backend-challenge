import './App.css';

import Upload from './upload/upload.js';

import Gallery from './gallery/gallery.js';

import Login from './login/login.js';

import React, {useState, useEffect} from 'react';

import {BrowserRouter, Route, Switch, Link} from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <header>
                <h2> Image hosting repository </h2>

                <h2><Link to={{pathname: "/",}}> Upload your images </Link> </h2>
                <h2><Link to={{pathname: "/albums",}}> Albums</Link></h2>
                <h2><Link to={{pathname: "/gallery",}}> Image Gallery</Link></h2>
                <h2><Link to={{pathname: "/login", }}> Login</Link></h2>

            </header>

            <div className="App">

                <Switch>

                    <Route exact path="/">
                        <Upload/>
                    </Route>

                    <Route path="/albums">

                    </Route>

                    <Route path="/gallery">
                        <Gallery/>
                    </Route>

                    <Route path="/login">
                        <Login/>
                    </Route>

                </Switch>

            </div>


        </BrowserRouter>
    );
}

export default App;