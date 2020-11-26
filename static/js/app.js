// Sends an alert message to the user
function alertMessage(type, message)
{
    let msgSuccess = document.getElementById("alertMessage");

    // Determine message type
    if (type == 'success')
    {
        msgSuccess.className = 'alert alert-success success';
    }
    else if (type == 'error')
    {
        msgSuccess.className = 'alert alert-danger error';
    }

    msgSuccess.innerHTML = message;
    setTimeout(function() {msgSuccess.innerHTML = ''; msgSuccess.className = '';}, 2000);
    

    // Check if alert is visible
    // if (msgSuccess.style.display == 'none')
    // {
    //     msgSuccess.style.display = 'block';
    //     msgSuccess.innerHTML = message;
    //     setTimeout(function() {msgSuccess.style.display = 'none'}, 3000);
    // }
    // else {
    //     msgSuccess.innerHTML = message;
    // }
}

// Remove an item from the order
function removeOrderItem()
{
     
}


// Add an item to the order
function addOrderItem()
{
    
}