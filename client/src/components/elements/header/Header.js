import React from 'react';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import TypoGraphy from '@material-ui/core/Typography';

import NavBar from '../navbar/NavBar';


class App extends React.Component {
  render() {
    return (
      <AppBar color="primary" position="static">
        <Toolbar>
          <TypoGraphy variant="h6" color="inherit">
            News Monitor
          </TypoGraphy>
          <NavBar />
        </Toolbar>
      </AppBar>
    )
  }
}


export default App;