import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';

import ApolloClient from 'apollo-boost';
import { ApolloProvider } from '@apollo/react-hooks';

import * as serviceWorker from './serviceWorker';
import './index.css';

import NewsGrid from './components/news-grid/NewsGrid';
import Header from './components/elements/header/Header';


const client = new ApolloClient({
  uri: 'http://localhost:8001/graphql/'
});

ReactDOM.render(
  (<ApolloProvider client={client}>
    <div>
      <Router>
        <Header />
        <Route path='/' exact component={NewsGrid} />
        <Route path='/app/' component={Header} />
      </Router>
    </div>
  </ApolloProvider>), 
  document.getElementById('root')
);


serviceWorker.unregister();
