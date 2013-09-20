function querySearchTerm()
{
    var searchAPI = 'api/search';
    var query = document.getElementById("query").value;
    var data = {"query": query, "first": first, "count": count};
    console.log("Handling Query: '" + query + "', first=" + first + ", count=" + count);
    document.getElementById("results").innerHTML = "<b>Searching...</b><br><img alt=\"Loading\" src=\"/static/ajax-loader.gif\">";
    $.getJSON(searchAPI, data).done(function(response) {
        document.getElementById("results").innerHTML = responseToHtml(response);
        document.getElementById("query").value = response["query"];
    });
}