console.log('form-validation.js loaded...');

let validator = formValidator();

function formValidator() {
    console.log('formValidator() called...')
    return {
        email: '',
        emailError: '',
        phone: '',
        phoneError: '',
        init() {
            if (this.$refs.email) {
                this.email = this.$refs.email.dataset.initialValue;
            } else {
                this.email = '';
            }
            if (this.$refs.phone) {
            this.phone = this.$refs.phone.dataset.initialValue;
            } else {
                this.phone = '';
            }
        },
        url: '',
        urlError: '',
        imageFile: null,
        imageError: '',
        pdfFile: null,
        pdfError: '',
        videoFile: null,
        videoError: '',
        timeoutId: null,
        // Validate email
        validateEmail: function (event) {
            var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
            if (this.email && !emailRegex.test(this.email)) {
                this.emailError = 'Please enter a valid email address';
                event.target.form.querySelector('button[type="submit"]').disabled = true;
            } else {
                this.emailError = '';
                event.target.form.querySelector('button[type="submit"]').disabled = false;
            }
        },
        // Validate URL
        validateUrl: function (event) {
            var urlRegex = /^https:\/\/((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|((\d{1,3}\.){3}\d{1,3}))(:\d+)?(\/[-a-z\d%_.~+]*)*(\?[;&a-z\d%_.~+=-]*)?(\#[-a-z\d_]*)?$/i;
            if (this.url && !urlRegex.test(this.url)) {
                this.urlError = 'Please enter a valid URL';
                event.target.form.querySelector('button[type="submit"]').disabled = true;
            } else {
                this.urlError = '';
                event.target.form.querySelector('button[type="submit"]').disabled = false;
            }
        },
        // Validate image
        validateImage: function () {
            var allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
            if (this.imageFile) {
                if (!allowedExtensions.exec(this.imageFile.name)) {
                    this.imageError = 'Please choose a .jpg, .jpeg or .png image file';
                    return false;
                } else if (this.imageFile.size > 10 * 1024 * 1024) {
                    this.imageError = 'Please choose an image file smaller than 10MB';
                    return false;
                } else {
                    this.imageError = '';
                    return true;
                }
            }
        },
        // Validate PDF & other file types
        validatePdf: function () {
            // var allowedExtensions = /(\.pdf)$/i;
            var allowedExtensions = /(\.pdf|\.doc|\.docx|\.pptx|\.xls|\.xlsx)$/i;
            if (this.pdfFile) {
                if (!allowedExtensions.exec(this.pdfFile.name)) {
                    // this.pdfError = 'Please choose a .pdf file';
                    this.pdfError = 'Please choose a valid file (.pdf, .doc, .docx, .pptx, .xls, .xlsx)';
                    return false;
                } else if (this.pdfFile.size > 95 * 1024 * 1024) {
                    this.pdfError = 'Please choose a PDF file smaller than 95MB';
                    return false;
                } else {
                    this.pdfError = '';
                    return true;
                }
            }
        },
        // Validate video
        validateVideo: function () {
            var allowedExtensions = /(\.mov|\.mp4|\.avi|\.flv|\.wmv)$/i;
            if (this.videoFile) {
                if (!allowedExtensions.exec(this.videoFile.name)) {
                    this.videoError = 'Please choose a .mov, .mp4, .avi, .flv or .wmv video file';
                    return false;
                } else if (this.videoFile.size > 95 * 1024 * 1024) {
                    this.videoError = 'Please choose a video file smaller than 95MB';
                    return false;
                } else {
                    this.videoError = '';
                    return true;
                }
            }
        },
        // Validate phone number
        validatePhone: function (event) {
            // var phoneRegex = /^\+\d{2}\d{10}$/;
            var phoneRegex = /^\+\d{11,12}$/;
            if (this.phone && !phoneRegex.test(this.phone)) {
                this.phoneError = 'Please enter a valid phone number e.g. +12345678901';
                event.target.form.querySelector('button[type="submit"]').disabled = true;
            } else {
                this.phoneError = '';
                event.target.form.querySelector('button[type="submit"]').disabled = false;
            }
        },
        // Validate required field
        validateRequiredField: function (event) {
            let form = event.target.form;
            if (!event.target.value) {
                event.target.nextElementSibling.textContent = "This field is required.";
                form.querySelector('button[type="submit"]').disabled = true;
            } else {
                event.target.nextElementSibling.textContent = "";
                form.querySelector('button[type="submit"]').disabled = false;
            }
        },
        // Check if all required fields are filled in
        checkAllFieldsFilled: function (form) {
            let requiredInputs = form.querySelectorAll('input[required],textarea[required]');
            let allFilled = Array.from(requiredInputs).every(input => input.value !== '');
            form.querySelector('button[type="submit"]').disabled = !allFilled;
        },
        delayedValidateEmail: function (event) {
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => { this.validateEmail(event); }, 500);
        },
        delayedValidateUrl: function (event) {
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => { this.validateUrl(event); }, 500);
        },
        delayedValidateImage: function (event) {
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => { this.validateImage(event); }, 500);
        },
        delayedValidatePdf: function (event) {
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => { this.validatePdf(event); }, 500);
        },
        delayedValidatePhone: function (event) {
            clearTimeout(this.timeoutId);
            this.timeoutId = setTimeout(() => { this.validatePhone(event); }, 500);
        },
        // Remove 'None' from fields
        correctFields: function() {
            $("input").each(function() {
                if ($(this).val() === 'None') {
                    $(this).val('');
                }
            });
        },
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.body.addEventListener('htmx:afterSettle', function() {
        validator.correctFields();
    });
});


function requiredFieldIndicator() {
    console.log('requiredFieldIndicator() called...')
    $('input[required], textarea[required]').each(function(){
        if ($(this).val() == '') {
            $('button[type="submit"]').prop('disabled', true);
        }
        $(this).keyup(() => {
            if ($(this).val() == '') {
                $('button[type="submit"]').prop('disabled', true);
            } else {
                $('button[type="submit"]').prop('disabled', false);
            }
        });
        var form = this.form;
        var $label;
        if(this.tagName.toLowerCase() === 'textarea') {
            // $label = $(this).parent().prev('label');
            $label = $(this).siblings('label');
        } else if (this.type === 'file') {
            $label = $(this).closest('.form__label-field').children('label');
        } else {
            $label = $(this).siblings('label');
        }
        $label.append('<span class="required">required</span>');
        $(this).on('blur', function(event) {
            validator.validateRequiredField(event);
            validator.checkAllFieldsFilled(form);
        });
    });
    let invalidFeedback = document.querySelectorAll('[data-invalid-feedback]');
    invalidFeedback.forEach(function(feedback) {
        if (feedback.textContent != '') {
            console.log('submit should be disabled');
        }
    });
};


function customFileUpload() {
    // Image upload
    $('.image-upload-button').on('click', function() {
        $('.image-file-input').click();
    });

    $('.image-file-input').on('change', function(event) {
        var fileName = $(this).val().split('\\').pop();
        $('.image-file-name').text(fileName);
        validator.imageFile = event.target.files[0];
        var isImageValid = validator.validateImage();
        $('button[type="submit"]').prop('disabled', !isImageValid);
        $(this).closest('.file-upload__container').find('[data-invalid-feedback]').text(validator.imageError);
    });

    // PDF upload
    $('.pdf-upload-button').on('click', function() {
        $('.pdf-file-input').click();
    });

    $('.pdf-file-input').on('change', function(event) {
        var fileName = $(this).val().split('\\').pop();
        $('.pdf-file-name').text(fileName);
        validator.pdfFile = event.target.files[0];
        var isPdfValid = validator.validatePdf();
        $('button[type="submit"]').prop('disabled', !isPdfValid);
        $(this).closest('.file-upload__container').find('[data-invalid-feedback]').text(validator.pdfError);
    });

    // Video upload
    $('.video-upload-button').on('click', function() {
        $('.video-file-input').click();
    });

    $('.video-file-input').on('change', function(event) {
        var fileName = $(this).val().split('\\').pop();
        $('.video-file-name').text(fileName);
        validator.videoFile = event.target.files[0];
        var isVideoValid = validator.validateVideo();
        $('button[type="submit"]').prop('disabled', !isVideoValid);
        $(this).closest('.file-upload__container').find('[data-invalid-feedback]').text(validator.videoError);
    });
};



