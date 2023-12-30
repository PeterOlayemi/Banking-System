document.getElementById('search-customer').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the link from navigating

    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');

    let accountNumber;

    while (true) {
        accountNumber = parseFloat(prompt("Enter Customer's Account Number:"));

        if (isNaN(accountNumber)) {
            return
        }

        if (/^\d{10}$/.test(accountNumber)) {
            break
        } else {
            alert('Enter A Valid 10-digit Account Number')
        }
    }

    // Construct the URL with parameters
    const slugUrl = ''
    const detailUrl = `/staff/customer/detail/%3Fq%3D${encodeURIComponent(accountNumber)}/`;

    // Send data to the backend using fetch
    fetch(slugUrl, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": csrfToken
        }
    })
    .then(response => {
        if (response.ok) {
            // Data sent successfully
            window.location.href = detailUrl
        } else {
            // Handle errors here
            alert('Error Sending Data To Patridge Bank. Please Try Again Later.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error Sending Data To Patridge Bank. Please Try Again Later.');
    });
});
