import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import App from './components/App';
import PersonalPage from './components/PersonalPage';
import './App.css';

ReactDOM.render(
    <Router>
        <Switch>
            <Route exact path="/" component={App} />
            <Route path="/personal" component={PersonalPage} />
        </Switch>
    </Router>,
    document.getElementById('root')
);