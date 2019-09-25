import React from 'react';
import { Grid } from '@material-ui/core';

import { getApolloContext } from '@apollo/react-hooks';
import { gql } from 'apollo-boost';

import Article from '../../models/Article';
import NewsCard from '../elements/news-card/NewsCard';

import './newsGrid.css'

const FETCH_ARTICLES = gql`
{
allArticles(first: 100) {
  edges {
    node {
      title
      description
      url
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
    const news = data.allArticles.edges.map(Article.mapFromJSON);
    this.setState({
      news: news
    });
  }

  async fetchNews() {
    const result = await this.client.query({ query: FETCH_ARTICLES });
    this.onNewsFetched(result.data);
  }

  render() {
    return (
      <div className='news-container'>
        <Grid container spacing={5} justify='center'>
          {this.state.news.map((article, index) => (
            <NewsCard key={index} article={article} />
          ))}
        </Grid>
      </div>
    );
  }
}

export default NewsGrid;