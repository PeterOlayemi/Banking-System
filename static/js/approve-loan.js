// Approve Loan
document.getElementById('approve-loan').addEventListener('click', function (event) {
    event.preventDefault(); // Prevent the link from navigating

    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');

    // Get the account ID and account information from the link's data attributes
    const loanId = this.getAttribute('data-id');
    const loanAccount = this.getAttribute('data-account');
    const loanAmount = this.getAttribute('data-amount');

    // Prompt for the date
    const selectedDateStr = prompt('Enter A Date Before Which The Loan Must be Paid in YYYY-MM-DD:');
    const selectedDate = new Date(selectedDateStr);

    if (!selectedDateStr) {
        // Do Nothing
        return
    }

    if (!selectedDate || isNaN(selectedDate)) {
        alert('Invalid Date. Please Enter A Valid Date In The Format YYYY-MM-DD');
        return;
    }

    const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
    if (!dateRegex.test(selectedDateStr)) {
        alert('Invalid Date Format. Make Sure The Date Is Exactly In The Format YYYY-MM-DD');
        return;
    }

    // Create a confirmation message with account info
    const options = { year: 'numeric', month:'long', day:'numeric'}
    const confirmationMessage = `Loan Details:\n\nAccount: ${loanAccount}\nAmount: ₦${loanAmount}\nTill: ${selectedDate.toLocaleDateString(undefined, options)}\n\nAre You Sure You Want To Approve This Loan Request?\n\nMake Sure This Action Conforms With PATRIDGE BANK STAFF REGULATION POLICY`;

    // Display a confirmation dialog
    const userConfirmation = confirm(confirmationMessage);

    if (userConfirmation) {
        // Construct the URL with parameters, including the date and account ID
        const slugUrl = ''
        const approveUrl = `/staff/loan/management/approve/${encodeURIComponent(selectedDateStr)}/${encodeURIComponent(loanId)}/`;

        // Send data to the backend using fetch or your preferred method
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
                window.location.href = approveUrl
            } else {
                // Handle errors here
                alert('Error Sending Data To Patridge Bank. Please Try Again Later.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error Sending Data To Patridge Bank. Please Try Again Later.');
        });
    }
});
