
console.log('global.js loaded');

$(document).on('click', '[data-close-crud-modal]', function() {
    console.log('data-close-crud-modal clicked');
    // $('[data-modal-form-container]').hide();
});