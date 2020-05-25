const wikiUrl = 'https://en.wikipedia.org'
const params = 'action=query&list=search&format=json&origin=*'

const breweryui_related_wikipedia_title_search = {
    "search": (input) => {
        const url = `${wikiUrl}/w/api.php?${
            params
        }&srsearch=${encodeURI(input)}`

        return new Promise(resolve => {
            if (input.length < 3) {
                return resolve([])
            }

            fetch(url)
                .then(response => response.json())
                .then(data => {
                    resolve(data.query.search)
                })
        })
    },
    "getResultValue": result => {
        return result.title;
    }
}
