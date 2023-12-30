// Remove Beneficiary
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-button');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const beneficiaryName = button.getAttribute('data-name');
            const beneficiaryNumber = button.getAttribute('data-number');
            const beneficiaryId = button.getAttribute('data-id');
            const removeUrl = button.getAttribute('data-remove-url');
            const exitUrl = button.getAttribute('data-exit-url');
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Remove Beneficiary - ${beneficiaryName}/${beneficiaryNumber}?`);
       
            if (isConfirmed) {
                // Make an AJAX call to remove the beneficiary
                const xhr = new XMLHttpRequest();
                xhr.open('POST', removeUrl);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // Display a message indicating successful removal
                            alert('Beneficiary Removed Successfully.');
                        
                            // Redirect to all beneficiaries view after removal
                            window.location.href = exitUrl;
                        } else {
                            // Display an error message
                            alert('Failed To Remove Beneficiary.');
                        }
                    }
                };

                // Send the beneficiary information
                const data = `beneficiary_id=${beneficiaryId}`;
                xhr.send(data);
            } else {
                // Redirect to all beneficiaries view without removing
                window.location.href = exitUrl;
            }
        }); 
    });
});

// LogOut User
document.addEventListener('DOMContentLoaded', function() {
    const logoutStaff = document.querySelectorAll('.logout');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    logoutStaff.forEach(function(logoutStaff) {
        logoutStaff.addEventListener('click', function() {
            event.preventDefault();

            const logoutUrl = logoutStaff.getAttribute('data-logout-url');
            const successUrl = logoutStaff.getAttribute('data-success-url')
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Log Out?`);
       
            if (isConfirmed) {
                // Make an AJAX call to log out
                $.ajax({
                    type: "POST",
                    url: logoutUrl,
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    data: {},
                    success: function(response) {
                        window.location.href = successUrl;
                    },
                    error: function(error) {
                        console.error("Logout Error:", error)
                    }
                });
            }
        });
    });
});

// Freeze Account
document.addEventListener('DOMContentLoaded', function() {
    const freezeButtons = document.querySelectorAll('.freeze-button');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    freezeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const accountName = button.getAttribute('data-name');
            const accountNumber = button.getAttribute('data-number');
            const accountId = button.getAttribute('data-id');
            const freezeUrl = button.getAttribute('data-freeze-url');
            const doneUrl = button.getAttribute('data-done-url');
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Freeze This Customer's Account - ${accountName} / ${accountNumber}?\n\nMake Sure This Action Conforms With PATRIDGE BANK STAFF REGULATION POLICY`);
       
            if (isConfirmed) {
                // Make an AJAX call to remove the beneficiary
                const xhr = new XMLHttpRequest();
                xhr.open('POST', freezeUrl);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // Display a message indicating successful removal
                            alert("Customer's Account Has Been Frozen.");
                        
                            // Redirect to all beneficiaries view after removal
                            window.location.href = doneUrl;
                        } else {
                            // Display an error message
                            alert('Failed To Freeze Account.');
                        }
                    }
                };

                // Send the beneficiary information
                const data = `account_id=${accountId}`;
                xhr.send(data);
            }
        }); 
    });
});

// Unfreeze Account
document.addEventListener('DOMContentLoaded', function() {
    const unfreezeButtons = document.querySelectorAll('.unfreeze-button');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    unfreezeButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const accountName = button.getAttribute('data-name');
            const accountNumber = button.getAttribute('data-number');
            const accountId = button.getAttribute('data-id');
            const unfreezeUrl = button.getAttribute('data-unfreeze-url');
            const doneUrl = button.getAttribute('data-done-url');
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Unfreeze This Customer's Account - ${accountName} / ${accountNumber}?\n\nMake Sure This Action Conforms With PATRIDGE BANK STAFF REGULATION POLICY`);
       
            if (isConfirmed) {
                // Make an AJAX call to remove the beneficiary
                const xhr = new XMLHttpRequest();
                xhr.open('POST', unfreezeUrl);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // Display a message indicating successful removal
                            alert("Customer's Account Has Been Unfrozen.");
                        
                            // Redirect to all beneficiaries view after removal
                            window.location.href = doneUrl;
                        } else {
                            // Display an error message
                            alert('Failed To Unfreeze Account.');
                        }
                    }
                };

                // Send the beneficiary information
                const data = `account_id=${accountId}`;
                xhr.send(data);
            }
        }); 
    });
});

// Remove Card
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-card-button');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const accountName = button.getAttribute('data-name');
            const accountNumber = button.getAttribute('data-number');
            const cardId = button.getAttribute('data-id');
            const removeUrl = button.getAttribute('data-remove-url');
            const doneUrl = button.getAttribute('data-done-url');
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Remove This Card Of ${accountName} / ${accountNumber}?`);
       
            if (isConfirmed) {
                // Make an AJAX call to remove the beneficiary
                const xhr = new XMLHttpRequest();
                xhr.open('POST', removeUrl);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // Display a message indicating successful removal
                            alert('Card Removed Successfully.');
                        
                            // Redirect to all beneficiaries view after removal
                            window.location.href = doneUrl;
                        } else {
                            // Display an error message
                            alert('Failed To Remove Card.');
                        }
                    }
                };

                // Send the beneficiary information
                const data = `card_id=${cardId}`;
                xhr.send(data);
            }
        }); 
    });
});

// Delete Account
document.addEventListener('DOMContentLoaded', function() {
    const deleteButtons = document.querySelectorAll('.delete-customer-button');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const accountName = button.getAttribute('data-name');
            const accountNumber = button.getAttribute('data-number');
            const accountId = button.getAttribute('data-id');
            const deleteUrl = button.getAttribute('data-delete-url');
            const doneUrl = button.getAttribute('data-done-url');
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Delete This Customer's Account - ${accountName} / ${accountNumber}?\n\nMake Sure This Action Conforms With PATRIDGE BANK STAFF REGULATION POLICY`);
       
            if (isConfirmed) {
                // Make an AJAX call to remove the beneficiary
                const xhr = new XMLHttpRequest();
                xhr.open('POST', deleteUrl);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // Display a message indicating successful removal
                            alert("Account Deleted Successfully.");
                        
                            // Redirect to all beneficiaries view after removal
                            window.location.href = doneUrl;
                        } else {
                            // Display an error message
                            alert('Failed To Delete Account.');
                        }
                    }
                };

                // Send the beneficiary information
                const data = `account_id=${accountId}`;
                xhr.send(data);
            }
        }); 
    });
});

// Disapprove Loan
document.addEventListener('DOMContentLoaded', function() {
    const disapproveButtons = document.querySelectorAll('.disapprove-button');
    const csrfToken = document.querySelector('[name=csrf-token]').getAttribute('content');
   
    disapproveButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const loanId = button.getAttribute('data-id');
            const disapproveUrl = button.getAttribute('data-disapprove-url');
            const doneUrl = button.getAttribute('data-done-url');
       
            // Show a confirmation dialog
            const isConfirmed = confirm(`Are You Sure You Want To Disapprove This Loan Request?\n\nMake Sure This Action Conforms With PATRIDGE BANK STAFF REGULATION POLICY`);
       
            if (isConfirmed) {
                // Make an AJAX call to remove the beneficiary
                const xhr = new XMLHttpRequest();
                xhr.open('POST', disapproveUrl);
                xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
                xhr.setRequestHeader('X-CSRFToken', csrfToken);
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        if (xhr.status === 200) {
                            // Display a message indicating successful removal
                            alert("Loan Has Been Disapproved.");
                        
                            // Redirect to all beneficiaries view after removal
                            window.location.href = doneUrl;
                        } else {
                            // Display an error message
                            alert('Failed To Disapprove Loan.');
                        }
                    }
                };

                // Send the beneficiary information
                const data = `loan_id=${loanId}`;
                xhr.send(data);
            };
        }); 
    });
});
