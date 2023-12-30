// message form
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('messageForm');
    const subject = document.getElementById('subject');
    const body = document.getElementById('body');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const subjectInput = subject.value;
        const formattedsubjectInput = subjectInput.toUpperCase();
        const bodyInput = body.value;

        if (confirm(`Do You Want To Send The Message: "${formattedsubjectInput}: ${bodyInput}" To ${accountDetail}`)) {
            form.submit()
        }
    });
});

// loan form
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loanForm');
    const amount = document.getElementById('amount');
    const loanFor1 = document.getElementById('1week');
    const loanFor2 = document.getElementById('1month');
    const loanFor3 = document.getElementById('3months');
    const loanFor4 = document.getElementById('6months');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const amountInput = amount.value;
        const confirmloanFor1 = loanFor1.checked
        const confirmloanFor2 = loanFor2.checked
        const confirmloanFor3 = loanFor3.checked
        const confirmloanFor4 = loanFor4.checked

        let messageloanFor1 = "";
        let messageloanFor2 = "";
        let messageloanFor3 = "";
        let messageloanFor4 = "";

        if (confirmloanFor1) {
            messageloanFor1 = loanFor1.getAttribute('name')
        }
        if (confirmloanFor2) {
            messageloanFor2 = loanFor2.getAttribute('name')
        }
        if (confirmloanFor3) {
            messageloanFor3 = loanFor3.getAttribute('name')
        }
        if (confirmloanFor4) {
            messageloanFor4 = loanFor4.getAttribute('name')
        }

        let confirmationMessage = `Do You Want To Request This Loan:\n\nAccount: ${accountDetail};\nAmount: ₦${amountInput};`

        if (confirmloanFor1) {
            confirmationMessage += `\nFor: ${messageloanFor1}`
        }
        if (confirmloanFor2) {
            confirmationMessage += `\nFor: ${messageloanFor2}`
        }
        if (confirmloanFor3) {
            confirmationMessage += `\nFor: ${messageloanFor3}`
        }
        if (confirmloanFor4) {
            confirmationMessage += `\nFor: ${messageloanFor4}`
        }

        if (confirm(confirmationMessage)) {
            form.submit()
        }
    });
});

// statement form
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('statementForm');
    const doc = document.getElementById('doc');
    const email = document.getElementById('email');
    const start = document.getElementById('start');
    const stop = document.getElementById('stop');

    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const confirmdoc = doc.checked;
        const confirmemail = email.checked;
        const startDate = new Date(start.value);
        const stopDate = new Date(stop.value);

        let messagedoc = "";
        let messageemail = "";

        if (confirmdoc) {
            messagedoc = doc.getAttribute('name')
        }
        if (confirmemail) {
            messageemail = email.getAttribute('name')
        }

        const options = { year: 'numeric', month:'long', day:'numeric'}
        let confirmationMessage = `Do You Want To Request This Bank Statement:\n\nAccount: ${accountDetail};\nFrom: ${startDate.toLocaleDateString(undefined, options)};\nTo: ${stopDate.toLocaleDateString(undefined, options)};`

        if (confirmdoc) {
            confirmationMessage += `\nMethod: ${messagedoc}`
        }
        if (confirmemail) {
            confirmationMessage += `\nMethod: ${messageemail}`
        }

        if (confirm(confirmationMessage)) {
            form.submit()
        }
    });
});
