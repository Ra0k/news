
export default class Article {
  title;
  url;
  description;
  siteShortName;

	constructor(initData) {
		Object.assign(this, initData);
	}

	static mapFromJSON(data) {
		if('node' in data){
			data = data.node;
		}
		return new Article({
			title: data.title,
      url: data.url,
      description: data.description,
      siteShortName: data.feed.site.shortName
		});
	}
}