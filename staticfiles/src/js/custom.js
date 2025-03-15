// document.getElementById("institute_logo").addEventListener("change", function(event) {
//     const file = event.target.files[0];
//     if (file) {
//         const img = new Image();
//         img.src = URL.createObjectURL(file);
//         img.onload = function() {
//             const width = img.width;
//             const height = img.height;
//             if (width !== height) {
//                 document.getElementById("error-message").classList.remove("d-none");
//                 event.target.value = ""; // Clear the file input
//             } else {
//                 document.getElementById("error-message").classList.add("d-none");
//             }
//         };
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const updateBtn = document.getElementById('updateBtn');
    const saveBtn = document.getElementById('saveBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const logoUploadBtn = document.getElementById('logoUploadBtn');
    const instituteUpdateForm = document.querySelector('#instituteUpdateForm');
    const instituteUpdateFields = instituteUpdateForm.querySelectorAll('input');

    // Make all inputs readonly or disabled
    instituteUpdateFields.forEach(field => {
        field.disabled = true;
    });

    // Hide Save and Cancel buttons initially
    saveBtn.classList.add('d-none');
    cancelBtn.classList.add('d-none');
    logoUploadBtn.classList.add('d-none');


    // When clicking update, enable all fields
    updateBtn.addEventListener('click', () => {
        instituteUpdateFields.forEach(field => {
            field.disabled = false;
        });

        // Show Save and Cancel buttons
        saveBtn.classList.remove('d-none');
        cancelBtn.classList.remove('d-none');
        logoUploadBtn.classList.remove('d-none');
        updateBtn.classList.add('d-none');
    });

    // Reload the page
    cancelBtn.addEventListener('click', () => {
        location.reload();
    });
});

