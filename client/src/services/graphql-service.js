import ApolloClient from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { setContext } from 'apollo-link-context';
import { InMemoryCache } from 'apollo-cache-inmemory';



const httpLink = createHttpLink({
  uri: 'http://localhost:8001/graphql/',
  //fetch: customFetch
});


const customFetch = (uri, options) => {
  this.refreshingPromise = null;
  return fetch(uri, options);
}


const authLink = setContext((_, { headers }) => {
  const token = AuthService.getToken();
  return {
    headers: {
      ...headers,
      Authorization: token ? `JWT ${token}` : '',
    }
  }
});

export const client = new ApolloClient({
  link: authLink.concat(httpLink),
  cache: new InMemoryCache()
});