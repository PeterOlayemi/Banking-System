// Pay Loan
document.addEventListener('DOMContentLoaded', function() {
    const payButtons = document.querySelectorAll('.pay-loan');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    payButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const loanId = button.getAttribute('data-id');

            // Create a confirmation message with account info
            const confirmationMessage = `Are You Sure You Want To Pay This Loan For Customer?\n\nMake Sure This Action Conforms With PATRIDGE BANK STAFF REGULATION POLICY`;

            // Display a confirmation dialog
            const userConfirmation = confirm(confirmationMessage);

            if (userConfirmation) {
                // Construct the URL with parameters, including the date and account ID
                const slugUrl = ''
                const payUrl = `/staff/loan/management/pay/${encodeURIComponent(loanId)}/`;

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
                        window.location.href = payUrl
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
    });
});
