import React from 'react';
import { Link } from 'react-router-dom';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import TypoGraphy from '@material-ui/core/Typography';


function NavBar(props) {

    return (
        <List component="nav">
            <ListItem component="div">
                <ListItemText inset>
                    <TypoGraphy color="inherit" variant="h6">
                        <Link style={{ color: 'inherit', textDecoration: 'inherit'}} to='/'>
                            Home
                        </Link>
                    </TypoGraphy>
                </ListItemText>


                <ListItemText inset>
                    <TypoGraphy color="inherit" variant="h6">
                        <Link style={{ color: 'inherit', textDecoration: 'inherit'}} to='/'> 
                            News
                        </Link>
                    </TypoGraphy>
                </ListItemText>


                <ListItemText inset>
                    <TypoGraphy color="inherit" variant="h6">
                        <Link style={{ color: 'inherit', textDecoration: 'inherit'}} to='/app/'> 
                            App 
                        </Link>
                    </TypoGraphy>
                </ListItemText>
            </ListItem >

        </List>
    )
}


export default NavBar;