// Function to display customer account details in a pop-up
function showAccountDetails(customerID, successUrl) {
    // Use AJAX to fetch account details from the backend
    $.ajax({
        url: '/staff/get_account_details/' + customerID + '/',
        type: 'GET',
        success: function(data) {
            // Create a pop-up or modal dialog to display account details
            const popupContainer = $('<div class="popup" align="center"></div>');
            const popupContent = $('<div class="popup-content"></div>');
           
            // Create the customer name by joining first name and last name
            const customerName = data.customer_name;
            const accountBalance  = data.account_balance;

            // Add account details to the pop-up
            popupContent.append('<p>Customer: ' + customerName + '</p>');
            popupContent.append('<p>Account Balance: ₦' + accountBalance + '</p>');

            const buttonContainer = $('<div class="button-container"></div>');

            // Add buttons for Credit, Debit, and Cancel
            const creditButton = $('<button class="creditbutton">Credit</button>');
            const debitButton = $('<button class="debitbutton">Debit</button>');
            const cancelButton = $('<button class="cancelbutton">Cancel</button>');

            // Attach event handlers to these buttons
            creditButton.click(function() {
                // Prompt user for credit amount
                const creditAmount = prompt('Enter The Amount To Credit:');
                if (creditAmount !== null) {
                    creditAccount(customerID, parseFloat(creditAmount), successUrl);
                }
            });

            debitButton.click(function() {
                // Prompt user for debit amount
                const debitAmount = prompt('Enter The Amount To Debit:');
                if (debitAmount !== null) {
                    debitAccount(customerID, parseFloat(debitAmount), successUrl);
                }
            });

            cancelButton.click(function() {
                // Close the pop-up
                popupContainer.remove();
            });

            buttonContainer.append(creditButton);
            buttonContainer.append(debitButton);
            buttonContainer.append(cancelButton);

            popupContainer.append(popupContent);
            popupContainer.append(buttonContainer);

            // Display the pop-up
            $('body').append(popupContainer);
        },
        error: function(error) {
            console.error('Error Fetching Account Details:', error);
        }
    });
}

// Function to handle credit operation
function creditAccount(customerID, amount, successUrl) {
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
    // Use AJAX to send a credit request to the backend
    $.ajax({
        url: '/staff/credit_account/' + customerID + '/' + amount + '/',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function(data) {
            // Handle success (e.g., show a success message)
            alert('Customer Credited Successfully!');
            window.location.href = successUrl
        },
        error: function(error) {
            console.error('Error Crediting Account:', error);
            alert('Error Crediting Account. Please Try Again Later.');
        }
    });
}

// Function to handle debit operation
function debitAccount(customerID, amount, successUrl) {
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
    // Use AJAX to send a debit request to the backend
    $.ajax({
        url: '/staff/debit_account/' + customerID + '/' + amount + '/',
        type: 'POST',
        headers: {
            "X-CSRFToken": csrfToken
        },
        success: function(data) {
            // Handle success (e.g., show a success message)
            alert('Customer Debited Successfully!');
            window.location.href = successUrl
        },
        error: function(error) {
            console.error('Error Debiting Account:', error);
            alert('Error Debiting Account. Please Try Again Later.');
        }
    });
}
