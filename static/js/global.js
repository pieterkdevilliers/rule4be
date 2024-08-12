
console.log('global.js loaded');

$(document).on('click', '[data-close-crud-modal]', function() {
    console.log('data-close-crud-modal clicked');
    // $('[data-modal-form-container]').hide();
});


// Handle button active state with event delegation
$(document).ready(function(){
    console.log('global.js loaded...');
    $(document).on('click', '[data-handle-active-button-state]', function(){
        $('[data-handle-active-button-state]').removeClass('active');
        $(this).addClass('active');
        // $(this).addClass('active').siblings().removeClass('active');
    });
    // $(document).on('click', '[data-handle-job-recording-intro]', function(){
    //     console.log('[data-handle-job-recording-intro] clicked...');
    //     $('[data-display-job-recording-intro-video]').click();
    // });
});


// Show/hide scroll overflow gradient
function attachScrollHandler() {
    $(".scroll-content").each(function() {
        // Check if content overflows
        if (this.scrollHeight > this.clientHeight) {
            // Content overflows, attach scroll handler
            $(this).off("scroll").on("scroll", function() {
                if(Math.round($(this).scrollTop() + $(this).innerHeight()) >= Math.round(this.scrollHeight)) {
                    $('.scroll-shadow').hide(); // Hide the scroll shadow when bottom is reached
                } else {
                    $('.scroll-shadow').show(); // Show the scroll shadow when not at bottom
                }
            });
            $('.scroll-shadow').show(); // Initially show the scroll shadow
        } else {
            // Content does not overflow, hide scroll shadow
            $('.scroll-shadow').hide();
        }
    });
}

// HTML structure for scroll overflow gradient:
// <div class="scroll-container">
//     <div class="scroll-content">
//         <!-- Content goes here -->
//     </div>
//     <div class="scroll-shadow"></div>
// </div>

$(document).ready(function() {
    attachScrollHandler();
    document.body.addEventListener('htmx:afterOnLoad', attachScrollHandler);
});

// Function to pause all playing videos
function pauseVideos() {
    $('video').each(function() {
        console.log('Videos paused...')
        this.pause();
    });
}


// Handle body classes 
function handleBodyClasses(bodyClass) {
    const body = document.querySelector('body');
    body.classList.forEach(className => {
        if (className.startsWith('body__')) {
            body.classList.remove(className);
        }
    });
    body.classList.add(bodyClass);
}


// Dev-only elements
$(document).ready(function() {
    // $('body').append('<div class="dev absolute left-1/2 transform -translate-x-1/2 mt-5 text-xs bg-white z-[100] p-3 hidden"></div>');
    let domain = window.location.hostname;
    if (domain === '192.168.68.105' || domain === 'localhost') {
    // if (domain === '192.168.68.105' ) {
        // $('.dev').removeClass('hidden').addClass('flex');
        $('body').append('<div class="dev absolute left-1/2 transform -translate-x-1/2 top-full mt-5 text-xs bg-white z-[100] p-1 flex justify-center"></div>');
        let deviceWidth = $(window).width();
        let deviceHeight = $(window).height();
        let orientation = (deviceWidth > deviceHeight) ? 'Landscape' : 'Portrait';
        $('.dev').append('<div id="showDeviceWidth"></div>');
        $('.dev').append('<div id="showDeviceHeight" class="ms-3"></div>');
        $('.dev').append('<div id="showOrientation" class="ms-3"></div>');
        $('.dev').append('<div id="showDomain" class="ms-3"></div>');
        $('#showDeviceWidth').html('Device width: ' + deviceWidth);
        $('#showDeviceHeight').html('Device height: ' + deviceHeight);
        $('#showOrientation').html('Device orientation: ' + orientation);
        $('#showDomain').html('Domain: ' + domain);
    }
});

$(document).ready(function() {
    const deviceWidth = $(window).width();
    const body = $('body');
    const sizeClasses = ['sm', 'md', 'lg', 'xl', '2xl'];
    const breakpoints = [375, 640, 768, 1024, 1280, 1536];
    
    body[0].classList.forEach(className => {
        if (className.startsWith('window-size--')) {
            body.removeClass(className);
        }
    });

    for (let i = 0; i < sizeClasses.length; i++) {
        if (deviceWidth > breakpoints[i] && deviceWidth <= breakpoints[i + 1]) {
            body.addClass(`window-size--${sizeClasses[i]}`);
            break;
        }
    }
});

$(window).on("resize", function() {
    const domain = window.location.hostname;
    const deviceWidth = $(window).width();
    const deviceHeight = $(window).height();
    const orientation = (deviceWidth > deviceHeight) ? 'landscape' : 'portrait';
    const body = $('body');

    body[0].classList.forEach(className => {
        if (className.startsWith('orientation--')) {
            body.removeClass(className);
        }
    });

    body.addClass(`orientation--${orientation}`);

    $('#showDeviceWidth').text(`Device width: ${deviceWidth}`);
    $('#showDeviceHeight').text(`Device height: ${deviceHeight}`);
    $('#showOrientation').text(`Device orientation: ${orientation}`);
    $('#showDomain').text(`Domain: ${domain}`);
});

