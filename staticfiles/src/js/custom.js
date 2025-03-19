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

// loader

window.addEventListener("load", function() {
    const loaderSection = document.getElementById("loaderBody");
    loaderSection.classList.add('d-none')
});

document.addEventListener('DOMContentLoaded', () => {
    const updateBtn = document.getElementById('updateBtn');
    const saveBtn = document.getElementById('saveBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const logoUploadBtn = document.getElementById('logoUploadBtn');
    const departmentBtn = document.getElementById('departmentBtn');
    const sessionBtn = document.getElementById('sessionBtn');
    const shiftBtn = document.getElementById('shiftBtn');
    const instituteUpdateForm = document.querySelector('#instituteUpdateForm');
    const instituteUpdateFields = instituteUpdateForm.querySelectorAll('input');
    const usersBtn = document.getElementById('usersBtn');
    const semesterBtn = document.getElementById('semesterBtn');

    // Make all inputs readonly or disabled
    instituteUpdateFields.forEach(field => {
        field.disabled = true;
    });

    // Hide Save and Cancel buttons initially
    saveBtn.classList.add('d-none');
    cancelBtn.classList.add('d-none');
    logoUploadBtn.classList.add('d-none');
    departmentBtn.classList.remove('d-none');
    sessionBtn.classList.remove('d-none');
    shiftBtn.classList.remove('d-none');
    usersBtn.classList.remove('d-none');
    semesterBtn.classList.remove('d-none');
    


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
        departmentBtn.classList.add('d-none');
        sessionBtn.classList.add('d-none');
        shiftBtn.classList.add('d-none');
        usersBtn.classList.add('d-none');
        semesterBtn.classList.add('d-none');
    });

    // Reload the page
    cancelBtn.addEventListener('click', () => {
        location.reload();
    });

});

document.addEventListener('DOMContentLoaded', () => {
    const addDepBtn = document.getElementById('addDepBtn');
    const cancelFormButton = document.getElementById('cancelFormButton');
    const addDepForm = document.getElementById('addDepFrom');
    const inputFields = addDepForm.querySelectorAll('input, select'); // Select both input and select fields

    addDepBtn.addEventListener('click', () => {
        addDepForm.classList.add('show');
    });

    cancelFormButton.addEventListener('click', () => {
        addDepForm.classList.remove('show');
        
        // Reset all input and select fields
        inputFields.forEach(field => {
            if (field.tagName === "SELECT") {
                field.selectedIndex = 0; // Reset select dropdown
            } else {
                field.value = ""; // Clear text input fields
            }
        });

        console.log(inputFields); // Log all fields to verify
    });
});
