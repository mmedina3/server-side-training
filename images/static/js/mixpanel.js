
//This function executes when user requests corgi pic

function setProperties() {
    document.getElementById("id_distinct_id").value = mixpanel.get_distinct_id();
  }
  
function getCorgi() {
    mixpanel.track('Get Corgi');
}

function reset() {
    mixpanel.reset();
}
