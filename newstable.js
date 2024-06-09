const fetchNews = async () => {
    let NewsFile = await fetch("./news.json");
    let NewsJsonArray = await NewsFile.json();
    let rows = NewsJsonArray.filter(n => n.body).map((news) => {
      // Pick only the first classification for each row
      const classification = news.classifications && news.classifications.length > 0
        ? news.classifications[0] // Pick the first classification
        : "";
      return {
        title: news.title,
        publishDate: news.publishDate,
        classifications: classification,
        id: news.id,
        body: news.body,
      };
    });
    rows.sort((a, b) => a.title.localeCompare(b.title));
    setData(rows);
    setFilteredData(rows);
  };
  