document.getElementById('datetxnrange').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the link from navigating

    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');

    const accountId = this.getAttribute('data-account-id'); // Retrieve the account ID from the HTML

    let minDate;
    let maxDate;

    // Create a date picker for the minimum date
    const minDateStr = window.prompt('Filter - From(Enter Date In The Format YYYY-MM-DD):');
    minDate = new Date(minDateStr);
    const minDateRegex = /^\d{4}-\d{2}-\d{2}$/;

    if (!minDateStr) {
        // Do Nothing
        return
    }

    if (isNaN(minDate) || !minDateRegex.test(minDateStr)) {
        alert('Invalid Date Format. Make Sure The Date Is Exactly In The Format YYYY-MM-DD');
        return;
    }

    // Create a date picker for the minimum date
    const maxDateStr = window.prompt('Filter - To(Enter Date In The Format YYYY-MM-DD):');
    maxDate = new Date(maxDateStr);
    const maxdateRegex = /^\d{4}-\d{2}-\d{2}$/;

    if (!maxDateStr) {
        // Do Nothing
        return
    }

    if (isNaN(maxDate) || !maxdateRegex.test(maxDateStr)) {
        alert('Invalid Date Format. Make Sure The Date Is Exactly In The Format YYYY-MM-DD');
        return;
    }

    // Validate that maxDate is greater than minDate
    if (minDate && maxDate <= minDate) {
        alert('Invalid Date Range. Please Make Sure That The Maximum Date Is Greater Than The Minimum Date.');
        return
    }

    // Create a modal or use your preferred UI for displaying the date pickers

    // Handle the OK or submit button to send the selected date range and account ID to the backend
    // Construct the URL with parameters, including the account ID, min, and max dates
    if (accountId && minDate && maxDate) {
    
        // Create a confirmation message with account info
        const options = { year: 'numeric', month:'long', day:'numeric'}
        const confirmationMessage = `Filter Credit And Debit Demographics From ${minDate.toLocaleDateString(undefined, options)} To ${maxDate.toLocaleDateString(undefined, options)}?`;

        // Display a confirmation dialog
        const rangeConfirmation = confirm(confirmationMessage);

        if (rangeConfirmation) {
            const slugUrl = ''
            const rangeUrl = `/staff/user/account/demographics/txn/date/filter/${encodeURIComponent(minDateStr)}/${encodeURIComponent(maxDateStr)}/${encodeURIComponent(accountId)}/`;

            // Send data to the backend using fetch or your preferred method
            fetch(slugUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": csrfToken
                },
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
    }
});
