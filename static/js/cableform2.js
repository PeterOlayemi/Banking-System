document.addEventListener('DOMContentLoaded', function () {
    var subscriptionType = document.getElementById('subscriptionType');
    var planField = document.getElementById('id_plan');
    var cardNumberField = document.getElementById('id_card_number');
    var amountParagraph = document.getElementById('amountParagraph');

    subscriptionType.addEventListener('change', function () {
        // Disable all form elements
        planField.disabled = true;
        cardNumberField.disabled = true;
        amountParagraph.style.display = 'none';

        // Show fields based on the selected subscription type
        if (subscriptionType.value === 'new') {
            planField.disabled = false;
            cardNumberField.disabled = false;
            amountParagraph.style.display = 'block';
        } else if (subscriptionType.value === 'renew') {
            planField.disabled = true;
            cardNumberField.disabled = false;
        }
    });

    // Trigger the change event to set initial disabled status on page load
    subscriptionType.dispatchEvent(new Event('change'));
});
