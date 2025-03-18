// message
document.addEventListener('DOMContentLoaded', () => {
    const body = document.querySelector('body');

    // Function to trigger the popup
    window.fadeIn = (type, msg = 'This is a default message') => {
        // create main div
        const mainDiv = document.createElement('div');
        mainDiv.classList.add('main_div');
        body.appendChild(mainDiv);

        // create row div
        const row = document.createElement('div');
        row.classList.add('row', 'h-100', 'd-flex', 'justify-content-center');
        mainDiv.appendChild(row);

        // create midle div
        const midleDiv = document.createElement('div');
        midleDiv.classList.add('midle_div', 'm-2', 'card', 'align-self-center', 'col-md-4', 'col-sm-6', 'col-xs-11');
        row.appendChild(midleDiv);

        // create msgDiv
        const msgDiv = document.createElement('div');
        msgDiv.classList.add('text-center');
        msgDiv.classList.add('msgDiv');
        midleDiv.appendChild(msgDiv);

        // create iconDiv with different icons based on type
        const iconDiv = document.createElement('div');
        iconDiv.classList.add('msg_icon', 'text-center', 'w-100');
        let iconHTML = '';
        if (type === 'success') {
            iconDiv.classList.add('success');
            iconHTML = '<i class="fa-solid fa-circle-check"></i>';
        } else if (type === 'error') {
            iconDiv.classList.add('error');
            iconHTML = '<i class="fa-solid fa-circle-xmark"></i>';
        } else if (type === 'info') {
            iconDiv.classList.add('info');
            iconHTML = '<i class="fa-solid fa-circle-info"></i>';
        } else if (type === 'warning') {
            iconDiv.classList.add('warning');
            iconHTML = '<i class="fa-solid fa-circle-exclamation"></i>';
        }
        iconDiv.innerHTML = iconHTML;
        msgDiv.appendChild(iconDiv);

        // create card-title
        const cardTitle = document.createElement('h4');
        cardTitle.classList.add('text-center', 'card-title');
        cardTitle.innerText = type.charAt(0).toUpperCase() + type.slice(1);
        if (type === 'success') {
            cardTitle.classList.add('text-success');
        } else if (type === 'error') {
            cardTitle.classList.add('text-danger');
        } else if (type === 'info') {
            cardTitle.classList.add('text-info');
        } else if (type === 'warning') {
            cardTitle.classList.add('text-warning');
        }
        msgDiv.appendChild(cardTitle);

        // create card-text
        const CardTxt = document.createElement('p');
        CardTxt.classList.add('card-text', 'mb-2');
        CardTxt.innerText = msg;
        msgDiv.appendChild(CardTxt);

        if (type === 'error' || type === 'warning'){
            // create buttonDiv
            const btnDiv = document.createElement('div');
            btnDiv.classList.add('msg-btn', 'd-flex', 'justify-content-end', 'mb-2');
            msgDiv.appendChild(btnDiv);

            // create button
            const btn = document.createElement('button');
            btn.classList.add('btn', 'btn-primary', 'btn-no-radious', 'button');
            btn.innerText = 'OK';
            btn.onclick = () => {
                handleClick(midleDiv, mainDiv);
            };
            btnDiv.appendChild(btn);
        } else if (type === 'success' || type === 'info') {
            const space = document.createElement('div');
            space.classList.add('my-2');
            midleDiv.appendChild(space)
            const progressBar = document.createElement('div');
            progressBar.classList.add('progressBar');
        
            // Add specific background class based on the type
            if (type === 'success') {
                progressBar.classList.add('bg-success');
            } else if (type === 'info') {
                progressBar.classList.add('bg-info');
            }
        
            // Append the progress bar to midleDiv
            midleDiv.appendChild(progressBar);

            setTimeout(() => {
                handleClick(midleDiv, mainDiv);
                console.log('Popup closed');
            }, 2400);
        }
        



        // Add event listener to close the popup when clicking outside midleDiv
        mainDiv.addEventListener('click', (e) => {
            if (!midleDiv.contains(e.target)) {
                handleClick(midleDiv, mainDiv);
            }
        });
    };

    // Function to handle button click and fade out popup
    const handleClick = (midleDiv, mainDiv) => {
        midleDiv.classList.add('fadout'); // Add fade-out class

        // Delay removal of mainDiv by 300ms
        setTimeout(() => {
            mainDiv.remove();
            console.log('Popup closed');
        }, 300);
    };
});