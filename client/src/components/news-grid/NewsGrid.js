import React from 'react';
import {Grid, Typography} from '@material-ui/core';
import Card from '@material-ui/core/Card';
import CardActionArea from '@material-ui/core/CardActionArea';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import CardMedia from '@material-ui/core/CardMedia';
import IconButton from '@material-ui/core/IconButton';

import FavoriteIcon from '@material-ui/icons/Favorite';
import ShareIcon from '@material-ui/icons/Share';

import { getApolloContext } from '@apollo/react-hooks';
import { gql } from "apollo-boost";

import './newsGrid.css'

const FETCH_ARTICLES = gql`
{
allArticles(first: 100) {
    edges {
        node {
           title
           description
           feed {
               site {
                   shortName
               }
           }
        }
    }
}
}
`


class NewsGrid extends React.Component {
    static contextType = getApolloContext()

    constructor(props) {
        super(props)

        this.state = {
            news: []
        };

        this.fetchNews = this.fetchNews.bind(this);
        this.onNewsFetched = this.onNewsFetched.bind(this);
    }

    componentDidMount() {
        this.client = this.context.client
        this.fetchNews();
    }

    onNewsFetched(data) {
        const news = data.allArticles.edges.map( (edge) => edge.node)
        this.setState({
            news: news
        });
    }

    async fetchNews() {
        const result = await this.client.query({query: FETCH_ARTICLES});
        this.onNewsFetched(result.data);
    }
    
    render() {
        return (
            <div className='news-container'>
                <Grid container spacing={5} justify='center'>
                    {this.state.news.map(article => (
                        <Grid item key={article.title}>
                            <Card className='news-card'>
                                <CardActionArea>
                                    <CardMedia
                                     component='img'
                                     alt='news'
                                     height='140'
                                     image='https://bit.ly/2WNi2Ml'
                                     title={article.title}
                                    />
                                    <CardContent>
                                        <Typography gutterBottom variant='h5' component='h2'>
                                            {article.title}
                                        </Typography>
                                        <Typography variant="body2" color="textSecondary" component="p">
                                            {article.description}
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
                                            {article.feed.site.shortName}
                                    </Typography>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </div>
        );
    }
}

export default NewsGrid;