$(document).ready(function(){
    // Initial check
    checkService();

    // Function to check service and enable/disable phone number field
    function checkService() {
      var selectedService = $("#id_service option:selected").text();
      var phoneNumberField = $("#id_phone_number");

      // List of services that disable the phone number field
      var disabledPhoneServices = ["Eko Electricity Prepaid",
                                    "Abuja Electricity Prepaid",
                                    "Ibadan Electricity Prepaid"];

      // Check if the selected service is in the list of disabled services
      if (disabledPhoneServices.includes(selectedService)) {
        phoneNumberField.prop('disabled', true);
      } else {
        phoneNumberField.prop('disabled', false);
      }
    }

    // Bind the function to the change event of the service dropdown
    $("#id_service").change(function() {
      checkService();
    });
  });
