import React from 'react';
import {
  Typography,
  Grid,
  Card, 
  CardActionArea, 
  CardActions, 
  CardContent, 
  CardMedia,
  IconButton
} from '@material-ui/core';
import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';

import './NewsCard.css';

class NewsCard extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      title: props.article.title,
      url: props.article.url,
      description: props.article.description,
      siteShortName: props.article.siteShortName
    }
  }

  componentDidMount() {
    this.setState({
      title: this.props.article.title,
      url: this.props.article.url,
      description: this.props.article.description,
      siteShortName: this.props.article.siteShortName
    });
  }

  static getDerivedStateFromProps(props, state) {
    return {
      title: props.article.title,
      url: props.article.url,
      description: props.article.description,
      siteShortName: props.article.siteShortName
    };
  }

  shouldComponentUpdate(nextProps, nextState) {
    return true;
  }

  render() {
    return (
      <Grid item>
        <Card className='news-card'>
          <CardActionArea>
            <CardMedia
              component='img'
              alt='news'
              height='140'
              image='https://bit.ly/2WNi2Ml'
              title={this.state.title}
            />
            <CardContent>
              <Typography gutterBottom variant='h5' component='h2'>
                {this.state.title}
              </Typography>
              <Typography variant="body2" color="textSecondary" component="p">
                {this.state.description}
              </Typography>
            </CardContent>
          </CardActionArea>
          <CardActions className='news-card-actions'>
            <IconButton aria-label="add to favorites">
              <FavoriteIcon />
            </IconButton>
            <IconButton aria-label="share">
              <ShareIcon />
            </IconButton>
            <Typography className='news-card-site' gutterBottom variant='h5' component='h2'>
              {this.state.siteShortName}
            </Typography>
          </CardActions>
        </Card>
      </Grid>
    )
  }
}

export default NewsCard;