(function () {
    'use strict'
    let forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                    PWeb.messageBox.showMessage(false, "Please check validation errors")
                }
                form.classList.add('was-validated')
            }, false)
        })
})()