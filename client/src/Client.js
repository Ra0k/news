import ApolloClient from 'apollo-boost';
import { ApolloProvider } from '@apollo/react-hooks';


const client = new ApolloClient({
  uri: 'http://localhost:8001/graphql/'
});

/*
export {
  client
}*/