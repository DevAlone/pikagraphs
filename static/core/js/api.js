// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function getUsers(limit, offset, searchText, sortBy, reverseSort, responseHandler)
{
    var url = "/api/users/?limit=" + limit + "&offset=" + offset + "&search=" + searchText + "&sort_by=" + sortBy;
    url += "&reverse_sort=" + reverseSort;
    ajaxGet(url, responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function editUserInfoField(username, info, responseHandler) {
    var url = "/api/edit_user_info_field/" + username + "/";
    ajaxPost(url, info, responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function getUserInfo(username, responseHandler)
{
    ajaxGet("/api/user_info/" + username + "/", responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function getUserGraphs(username, responseHandler)
{
    ajaxGet("/api/user_graphs/" + username + "/", responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function getUserGraph(username, graphType, responseHandler)
{
    ajaxGet("/api/user_graph/" + username + "/" + graphType + "/", responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function getCommunityInfo(urlName, responseHandler)
{
    ajaxGet("/api/community_info/" + urlName + "/", responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function getCommunityGraphs(urlName, responseHandler)
{
    ajaxGet("/api/community_graphs/" + urlName + "/", responseHandler, function(status) {
        responseHandler({ error: status });
    });
}

function ajaxGet(url, successHandler, errorHandler)
{
    $.get(url, successHandler).fail(errorHandler);
    /*var xhttp = new XMLHttpRequest();
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
    xhttp.send();*/
}

function ajaxPost(url, data, successHandler, errorHandler)
{
    $.post(url, data, successHandler).fail(errorHandler);
    /*var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                successHandler(this.responseText);
            } else {
                errorHandler(this.status);
            }
        }
    };
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('X-CSRFToken', )
    xhttp.send(data);*/
}