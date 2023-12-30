document.addEventListener("DOMContentLoaded", function() {
  const serviceSelect = document.getElementById("id_service"); // Replace with the actual ID of the service field in your form
  const planSelect = document.getElementById("id_plan");       // Replace with the actual ID of the plan field in your form
  const planAmountSpan = document.getElementById("plan-amount");

  serviceSelect.addEventListener("change", function() {
    const selectedService = serviceSelect.value;
    planSelect.innerHTML = '<option value"" selected disabled>Choose A Plan</option>';
    fetch(`/customer/cable/get_plans_for_service/?service_id=${selectedService}`)
      .then(response => response.json())
      .then(data => {
        data.plans.forEach(plan => {
          const option = document.createElement("option");
          option.value = plan.id;
          option.text = plan.name;
          option.setAttribute("data-amount", plan.amount);
          planSelect.appendChild(option);
        });
      });
  });

  planSelect.addEventListener("change", function() {
    const selectedPlan = planSelect.value;
    const selectedPlanAmount = parseFloat(planSelect.options[planSelect.selectedIndex].getAttribute("data-amount"));
    planAmountSpan.textContent = "₦" + selectedPlanAmount.toFixed(2);
  });
});
