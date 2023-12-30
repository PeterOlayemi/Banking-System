document.getElementById('amountrange').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the link from navigating

    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');

    const accountId = this.getAttribute('data-account-id'); // Retrieve the account ID from the attribute

    let minAmount;
    let maxAmount;

    // Keep prompting until a valid range is entered
    while (true) {
        minAmount = parseFloat(prompt('Enter Minimum Amount:'));

        if (isNaN(minAmount)) {
            return
        }

        maxAmount = parseFloat(prompt('Enter Maximum Amount:'));

        if (isNaN(maxAmount)) {
            return
        }

        if (!isNaN(minAmount) && !isNaN(maxAmount) && minAmount < maxAmount) {
            // Valid range, break out of the loop
            break;
        } else {
            // Invalid range, show an error message
            alert('Invalid Range. Please Make Sure The Maximum Amount Is Greater Than The Minimum Amount.');
        }
    }

    const confirmationMessage = `Filter Customer's Transactions From ₦${minAmount} To ₦${maxAmount}?`;

    // Display a confirmation dialog
    const rangeConfirmation = confirm(confirmationMessage);

    if (rangeConfirmation) {
        // Construct the URL with parameters, including the account ID
        const slugUrl = ''
        const rangeUrl = `/staff/transaction/history/filter/amount/${encodeURIComponent(minAmount)}/${encodeURIComponent(maxAmount)}/${encodeURIComponent(accountId)}/`;

        // Send data to the backend using fetch
        fetch(slugUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                "X-CSRFToken": csrfToken
            }
        })
        .then(response => {
            if (response.ok) {
                // Data sent successfully
                window.location.href = rangeUrl
            } else {
                // Handle errors here
                alert('Error Sending Data To Patridge Bank. Please Try Again Later.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error Sending Data To Patridge Bank. Please Try Again Later.');
        });
    };
});
