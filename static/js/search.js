
function displayResults (results, store) {
  const searchResults = document.getElementById('results')
    console.log(searchResults)
  if (results.length) {
    let resultList = ''
    // Iterate and build result list elements
    for (const n in results) {
      const item = store[results[n].ref]
      //resultList += '<li class="list__item post"><p><a href="' + item.url + '">' + item.title + '</a></p>'
	//resultList += '<p>' + item.content.substring(0, 150) + '...</p></li>'
	//resultList += '<a href="' + item.url + '"><header class="main__header"> <h1 class="main__title">' + item.title + "</h1></header>";

	resultList += item.meta ;
    }
    searchResults.innerHTML = resultList
  } else {
    searchResults.innerHTML = 'No results found.'
  }
}

const params = new URLSearchParams(window.location.search)
const query = params.get('query')


if (query) {
  // Retain the search input in the form when displaying results
    console.log(query)
  document.getElementById('search-input').setAttribute('value', query)

  const idx = lunr(function () {
    this.ref('id')
    this.field('title', {
      boost: 15
    })
    this.field('tags')
    this.field('content', {
      boost: 10
    })

    for (const key in window.store) {
      this.add({
        id: key,
        title: window.store[key].title,
        tags: window.store[key].category,
        content: window.store[key].content
      })
    }
  })

  // Perform the search
  const results = idx.search(query)
  // Update the list with results
  displayResults(results, window.store)
}
