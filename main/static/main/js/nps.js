function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var settings = {
    "url": "https://app.te-ex.ru/Perekrestok/api/nps?last_modified=2020-02-10T10:00:00&last_modified_to=2020-02-16T11:00:00",
    "method": "GET",
    "timeout": 0,
    "headers": {
      "Authorization": "Basic cHJrbnBzMjpmZDNUZHM="
    },
  };
  
  $.ajax(settings).done(function (response) {
    console.log(response);
  });
  