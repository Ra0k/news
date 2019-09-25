import { client } from './graphql-service';
import { gql } from 'apollo-boost';


const TOKEN_AUTH = gql`
mutation TokenAuth($username: String!, $password: String!) {
  tokenAuth(input: {username: $username, password: $password}) {
    token
    refreshToken
  }
}`;

const REFRESH_TOKEN =  gql`
mutation RefreshToken($refreshToken: String!) {
  refreshToken(token: $refreshToken) {
    token
    refreshToken
    payload
  }
}`;

const REVOKE_TOKEN = gql`
mutation RevokeToken($refreshToken: String!) {
  revokeToken(refreshToken: $refreshToken) {
    revoked
  }
}`;


class AuthService {
  constructor() {
    this.token = localStorage.getItem('token');
    this.refreshToken = localStorage.getItem('refreshToken');

    this.getToken = this.getToken.bind(this);
    this.getRefreshToken = this.getRefreshToken.bind(this);

    this.setToken = this.setToken.bind(this);
    this.setRefreshToken = this.setRefreshToken.bind(this);

    this.login = this.login.bind(this);
    this.logout = this.logout.bind(this);
    this.refreshTokens = this.refreshTokens.bind(this);
  }

  getToken() {
    return this.token;
  }

  getRefreshToken() {
    return this.refreshToken;
  }

  setToken(token) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  setRefreshToken(token) {
    this.refreshToken = token;
    localStorage.setItem('refreshToken', token);
  }

  async logout () {
    token = this.getToken();
    refreshToken = this.getRefreshToken();

    this.setToken(null);
    this.setRefreshToken(null);

    result = await client.mutate({
      mutation: REVOKE_TOKEN,
      variables: { refreshToken },
      context: {
        headers: {
          Authorization: token ? `JWT ${token}` : '',
        }
      }
    });
  }

  async login(username, password) {
    this.logout();

    result = await client.mutate({
      mutation: TOKEN_AUTH,
      variables: { username, password },
      context: {
        headers: {
          Authorization: null
        }
      }
    });
    
    this.setToken(result.data.tokenAuth.token);
    this.setRefreshToken(result.data.tokenAuth.refreshToken);
  }

  async refreshTokens() {
    token = this.getToken();
    refreshToken = this.getRefreshToken();

    result = await client.mutate({
      mutation: REFRESH_TOKEN,
      variables: { refreshToken },
      context: {
        headers: {
          Authorization: token ? `JWT ${token}` : '',
        }
      }
    });

    this.setToken(result.data.refreshToken.token);
    this.setRefreshToken(result.data.refreshToken.refreshToken);
  }
}

export default AuthService;