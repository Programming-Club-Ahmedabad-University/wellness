document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll('input').forEach( (input) => {
        if(input.type == 'checkbox') {
            input.className = "form-check-input edit-profile-fields";
        }
        else if(input.type == 'submit') {
            input.className = 'my-5 auth-button'
        }
        else {
            input.className = "mb-3 form-control edit-profile-fields";
        }
    });
    document.querySelectorAll('select').forEach( (select) => {
        select.className = "mb-3 form-control edit-profile-fields";
    });
});