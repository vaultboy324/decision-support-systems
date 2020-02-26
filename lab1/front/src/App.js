import React from 'react';
import {BrowserRouter, Route, Switch} from "react-router-dom";
import logo from './logo.svg';

import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css';

import './App.css';

import ShiftedIdeal from "./components/shifted_ideal/shifted_ideal";
import Permutations from "./components/permutations/permutations";

function App() {
  return (
    <div className="App">
        <BrowserRouter>
            <Switch>
                <Route exact path="/shifted_ideal" component={ShiftedIdeal}/>
                <Route exact path={"/permutations"} component={Permutations}/>
            </Switch>
        </BrowserRouter>
      {/*<header className="App-header">*/}
      {/*  <img src={logo} className="App-logo" alt="logo" />*/}
      {/*  <p>*/}
      {/*    Edit <code>src/App.js</code> and save to reload.*/}
      {/*  </p>*/}
      {/*  <a*/}
      {/*    className="App-link"*/}
      {/*    href="https://reactjs.org"*/}
      {/*    target="_blank"*/}
      {/*    rel="noopener noreferrer"*/}
      {/*  >*/}
      {/*    Learn React*/}
      {/*  </a>*/}
      {/*</header>*/}
    </div>
  );
}

export default App;
