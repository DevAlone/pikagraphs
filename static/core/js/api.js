function getUsers(limit, offset, searchText, sortBy, reverseSort, responseHandler)
{
    var url = "/api/users/?limit=" + limit + "&offset=" + offset + "&search=" + searchText + "&sort_by=" + sortBy;
    url += "&reverse_sort=" + reverseSort;
    ajaxGet(url, function(result) {
        responseHandler(JSON.parse(result));
    }, function(status) {
        responseHandler({ error: status });
    });
}

function getUserInfo(username, responseHandler)
{
    ajaxGet("/api/user_info/" + username + "/", function(result) {
        responseHandler(JSON.parse(result));
    }, function(status) {
        responseHandler({ error: status });
    });
}

function getUserGraphs(username, responseHandler)
{
    ajaxGet("/api/user_graphs/" + username + "/", function(result) {
        responseHandler(JSON.parse(result));
    }, function(status) {
        responseHandler({ error: status });
    });
}

function getUserGraph(username, graphType, responseHandler)
{
    ajaxGet("/api/user_graph/" + username + "/" + graphType + "/", function(result) {
        responseHandler(JSON.parse(result));
    }, function(status) {
        responseHandler({ error: status });
    });
}

function getCommunityInfo(urlName, responseHandler)
{
    ajaxGet("/api/community_info/" + urlName + "/", function(result) {
        responseHandler(JSON.parse(result));
    }, function(status) {
        responseHandler({ error: status });
    });
}

function getCommunityGraphs(urlName, responseHandler)
{
    ajaxGet("/api/community_graphs/" + urlName + "/", function(result) {
        responseHandler(JSON.parse(result));
    }, function(status) {
        responseHandler({ error: status });
    });
}

function ajaxGet(url, successHandler, errorHandler)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                successHandler(this.responseText);
            } else {
                errorHandler(this.status);
            }
        }
    };
    xhttp.open("GET", url, true);
    xhttp.send();
}