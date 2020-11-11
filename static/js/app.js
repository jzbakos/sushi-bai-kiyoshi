// Sends an alert message to the user
function alertMessage(type, message)
{
    let msgSuccess = document.getElementById("alertMessage");

    // Determine message type
    if (type == 'success')
    {
        msgSuccess.className = 'alert alert-success';
    }
    else if (type == 'error')
    {
        msgSuccess.className = 'alert alert-danger';
    }

    // Check if alert is visible
    if (msgSuccess.style.visibility == 'hidden')
    {
        msgSuccess.style.visibility = 'visible';
        msgSuccess.innerHTML = message;
        setTimeout(function() {msgSuccess.style.visibility = 'hidden'}, 3000);
    }
    else {
        msgSuccess.innerHTML = message;
    }
}

// Remove an item from the order
function removeOrderItem()
{
     
}


// Add an item to the order
function addOrderItem()
{

}