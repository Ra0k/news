import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from 'react-router-dom';

import { ApolloProvider } from '@apollo/react-hooks';
import { client } from './services/graphql-service';
import AuthService from './services/auth-service';

import * as serviceWorker from './serviceWorker';
import './index.css';

import Header from './components/elements/header/Header';
import Login from './components/login/Login';
import NewsGrid from './components/news-grid/NewsGrid';
import Copyright from './components/elements/copyright/Copyright';

auth = new AuthService();
auth.login("admin", "Dzer13d97sz");

ReactDOM.render(
  (<ApolloProvider client={client}>
    <div>
      <Router>
        <Header />
        <Route path='/' exact component={NewsGrid} />
        <Route path='/app/' component={Header} />
        <Route path='/login/' component={Login}/>
        <Copyright />
      </Router>
    </div>
  </ApolloProvider>), 
  document.getElementById('root')
);


serviceWorker.unregister();
