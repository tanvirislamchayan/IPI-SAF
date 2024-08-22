# SAF - Image Polytechnic Institute, Rangpur

This repository contains the source code for the SAF Scholarship application website, specifically designed for students of Image Polytechnic Institute. The platform streamlines the online application process for scholarships, ensuring a smooth and accessible experience.

## Features

- **Scholarship Application:** Students can easily fill out and submit their scholarship applications through the website.
- **Edit Scholarship Application:** Students can update their application details if changes are needed by searching with their SSC roll number and account number *(e.g., bKash, Nagad, Rocket, or Bank account number)*.
- **Scholarship Application Management:** Administrators have full control over the records, including creating, updating, reading, and deleting entries. Only administrators can delete applications.
- **Responsive Design:** The website is fully responsive, providing an optimal user experience across all devices.
- **Form Validation:** Robust client-side and server-side validations ensure that applications are correctly filled out before submission.

## Technologies Used

- **Frontend:**
  - HTML5
  - CSS3
  - JavaScript (with client-side form validation)
- **Backend:**
  - Django (Python web framework)
  - SQLite3 (Database)
- **Others:**
  - Git (Version Control)
  - Bootstrap (CSS Framework)

## Installation

1. **Create a Virtual Environment:**
   ```bash
   pip install virtualenv              # Install virtualenv
   virtualenv venv                     # Create a virtual environment named 'venv'
   source venv/bin/activate            # Activate the virtual environment
1. **Clone the Repository:**
    ```bash
    git clone https://github.com/tanvirislamchayan/IPI-SAF.git
    cd IPI-SAF/
    pip install -r requirements.txt     # Install required dependencies
1. **Clone the Repository:**
    ```bash
    ./manage.py runserver               # Or use `python3 manage.py runserver`