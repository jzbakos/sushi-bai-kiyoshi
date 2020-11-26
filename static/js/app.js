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
}