(function ($) {
    "use strict";
    
    var animationDelay = 2500,
            //loading bar effect
            barAnimationDelay = 3800,
            barWaiting = barAnimationDelay - 3000, //3000 is the duration of the transition on the loading bar - set in the scss/css file
            //letters effect
            lettersDelay = 50,
            //type effect
            typeLettersDelay = 150,
            selectionDuration = 500,
            typeAnimationDelay = selectionDuration + 800,
            //clip effect 
            revealDuration = 600,
            revealAnimationDelay = 1500;

    initHeadline();


    function initHeadline() {
        //insert <i> element for each letter of a changing word
        singleLetters($('.cd-headline.letters').find('b'));
        //initialise headline animation
        animateHeadline($('.cd-headline'));
    }

    function singleLetters($words) {
        $words.each(function () {
            var word = $(this),
                    letters = word.text().split(''),
                    selected = word.hasClass('is-visible');
            for (i in letters) {
                if (word.parents('.rotate-2').length > 0)
                    letters[i] = '<em>' + letters[i] + '</em>';
                letters[i] = (selected) ? '<i class="in">' + letters[i] + '</i>' : '<i>' + letters[i] + '</i>';
            }
            var newLetters = letters.join('');
            word.html(newLetters).css('opacity', 1);
        });
    }

    function animateHeadline($headlines) {
        var duration = animationDelay;
        $headlines.each(function () {
            var headline = $(this);

            if (headline.hasClass('loading-bar')) {
                duration = barAnimationDelay;
                setTimeout(function () {
                    headline.find('.cd-words-wrapper').addClass('is-loading')
                }, barWaiting);
            } else if (headline.hasClass('clip')) {
                var spanWrapper = headline.find('.cd-words-wrapper'),
                        newWidth = spanWrapper.width() + 10
                spanWrapper.css('width', newWidth);
            } else if (!headline.hasClass('type')) {
                //assign to .cd-words-wrapper the width of its longest word
                var words = headline.find('.cd-words-wrapper b'),
                        width = 0;
                words.each(function () {
                    var wordWidth = $(this).width();
                    if (wordWidth > width)
                        width = wordWidth;
                });
                headline.find('.cd-words-wrapper').css('width', width);
            }
            ;

            //trigger animation
            setTimeout(function () {
                hideWord(headline.find('.is-visible').eq(0))
            }, duration);
        });
    }

    function hideWord($word) {
        var nextWord = takeNext($word);

        if ($word.parents('.cd-headline').hasClass('type')) {
            var parentSpan = $word.parent('.cd-words-wrapper');
            parentSpan.addClass('selected').removeClass('waiting');
            setTimeout(function () {
                parentSpan.removeClass('selected');
                $word.removeClass('is-visible').addClass('is-hidden').children('i').removeClass('in').addClass('out');
            }, selectionDuration);
            setTimeout(function () {
                showWord(nextWord, typeLettersDelay)
            }, typeAnimationDelay);

        } else if ($word.parents('.cd-headline').hasClass('letters')) {
            var bool = ($word.children('i').length >= nextWord.children('i').length) ? true : false;
            hideLetter($word.find('i').eq(0), $word, bool, lettersDelay);
            showLetter(nextWord.find('i').eq(0), nextWord, bool, lettersDelay);

        } else if ($word.parents('.cd-headline').hasClass('clip')) {
            $word.parents('.cd-words-wrapper').animate({width: '2px'}, revealDuration, function () {
                switchWord($word, nextWord);
                showWord(nextWord);
            });

        } else if ($word.parents('.cd-headline').hasClass('loading-bar')) {
            $word.parents('.cd-words-wrapper').removeClass('is-loading');
            switchWord($word, nextWord);
            setTimeout(function () {
                hideWord(nextWord)
            }, barAnimationDelay);
            setTimeout(function () {
                $word.parents('.cd-words-wrapper').addClass('is-loading')
            }, barWaiting);

        } else {
            switchWord($word, nextWord);
            setTimeout(function () {
                hideWord(nextWord)
            }, animationDelay);
        }
    }

    function showWord($word, $duration) {
        if ($word.parents('.cd-headline').hasClass('type')) {
            showLetter($word.find('i').eq(0), $word, false, $duration);
            $word.addClass('is-visible').removeClass('is-hidden');

        } else if ($word.parents('.cd-headline').hasClass('clip')) {
            $word.parents('.cd-words-wrapper').animate({'width': $word.width() + 10}, revealDuration, function () {
                setTimeout(function () {
                    hideWord($word)
                }, revealAnimationDelay);
            });
        }
    }

    function hideLetter($letter, $word, $bool, $duration) {
        $letter.removeClass('in').addClass('out');

        if (!$letter.is(':last-child')) {
            setTimeout(function () {
                hideLetter($letter.next(), $word, $bool, $duration);
            }, $duration);
        } else if ($bool) {
            setTimeout(function () {
                hideWord(takeNext($word))
            }, animationDelay);
        }

        if ($letter.is(':last-child') && $('html').hasClass('no-csstransitions')) {
            var nextWord = takeNext($word);
            switchWord($word, nextWord);
        }
    }

    function showLetter($letter, $word, $bool, $duration) {
        $letter.addClass('in').removeClass('out');

        if (!$letter.is(':last-child')) {
            setTimeout(function () {
                showLetter($letter.next(), $word, $bool, $duration);
            }, $duration);
        } else {
            if ($word.parents('.cd-headline').hasClass('type')) {
                setTimeout(function () {
                    $word.parents('.cd-words-wrapper').addClass('waiting');
                }, 200);
            }
            if (!$bool) {
                setTimeout(function () {
                    hideWord($word)
                }, animationDelay)
            }
        }
    }

    function takeNext($word) {
        return (!$word.is(':last-child')) ? $word.next() : $word.parent().children().eq(0);
    }

    function takePrev($word) {
        return (!$word.is(':first-child')) ? $word.prev() : $word.parent().children().last();
    }

    function switchWord($oldWord, $newWord) {
        $oldWord.removeClass('is-visible').addClass('is-hidden');
        $newWord.removeClass('is-hidden').addClass('is-visible');
    }




    
    /*********Countdown 1**********/
    function getTimeRemaining(endtime) {
        var t = Date.parse(endtime) - Date.parse(new Date());
        var seconds = Math.floor((t / 1000) % 60);
        var minutes = Math.floor((t / 1000 / 60) % 60);
        var hours = Math.floor((t / (1000 * 60 * 60)) % 24);
        var days = Math.floor(t / (1000 * 60 * 60 * 24));
        return {
            'total': t,
            'days': days,
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds
        };
    }

    function initializeClock(id, endtime) {
        var clock = document.getElementById(id);
        var daysSpan = clock.querySelector('.days');
        var hoursSpan = clock.querySelector('.hours');
        var minutesSpan = clock.querySelector('.minutes');
        var secondsSpan = clock.querySelector('.seconds');

        function updateClock() {
            var t = getTimeRemaining(endtime);

            daysSpan.innerHTML = t.days;
            hoursSpan.innerHTML = ('0' + t.hours).slice(-2);
            minutesSpan.innerHTML = ('0' + t.minutes).slice(-2);
            secondsSpan.innerHTML = ('0' + t.seconds).slice(-2);

            if (t.total <= 0) {
                clearInterval(timeinterval);
            }
        }

        updateClock();
        var timeinterval = setInterval(updateClock, 1000);
    }

    var deadline = new Date(Date.parse(new Date()) + 28 * 11 * 28 * 60 * 1000);
    if ($('#clockdiv').length) {
        initializeClock('clockdiv', deadline);
    }

    /*********Countdown 2**********/
    var deadline = new Date(Date.parse(new Date()) + 28 * 11 * 28 * 60 * 1000);
    if ($('#clockdiv2').length) {
        initializeClock('clockdiv2', deadline);
    }

    /*********Countdown 3**********/
    var deadline = new Date(Date.parse(new Date()) + 28 * 11 * 28 * 60 * 1000);
    if ($('#clockdiv3').length) {
        initializeClock('clockdiv3', deadline);
    }

    /*********Countdown 3**********/
    var deadline = new Date(Date.parse(new Date()) + 28 * 11 * 28 * 60 * 1000);
    if ($('#clockdiv4').length) {
        initializeClock('clockdiv4', deadline);
    }

    /*===============Counter Js===================*/
    $('.counter_number1').counterUp({
        delay: 1,
        time: 1600
    });

    /*================Image Convert to Background Image Js======================*/


    $('.background-image-maker').each(function () {
        var imgURL = $(this).next('.holder-image').find('img').attr('src');
        $(this).css('background-image', 'url(' + imgURL + ')');
    });


    /*================Client Slider Js Style -1======================*/

    $(".carousal-client").owlCarousel({
        items: 6,
        itemsDesktop: [1199, 4],
        itemsDesktopSmall: [979, 3],
        itemsTablet: [768, 2],
        pagination: false,
        autoPlay: true
    });


    /*================Client Slider 2 Js Style -2======================*/

    $(".carousal-client2").owlCarousel({
        items: 4,
        itemsDesktop: [1199, 4],
        itemsDesktopSmall: [979, 4],
        itemsTablet: [768, 3],
        pagination: false,
        autoPlay: true
    });


    /*================Testimonial Slider Js Style -1======================*/


    $(".testimonial-slider").owlCarousel({
        items: 2,
        itemsDesktop: [1199, 2],
        itemsDesktopSmall: [979, 2],
        itemsTablet: [768, 1],
        pagination: true,
        autoPlay: true
    });


    /*================Testimonial Slider Js Style -2======================*/

    $(".testimonial-slider2").owlCarousel({
        items: 1,
        itemsDesktop: [1199, 1],
        itemsDesktopSmall: [979, 1],
        itemsTablet: [768, 1],
        pagination: true,
        navigation: false,
        autoPlay: false
    });

    /*================Carousal Slider Js======================*/

    $(".carousal-slide").owlCarousel({
        items: 1,
        pagination: false,
        navigation: true,
        autoPlay: false
    });


    /*================Testimonial Slider Js Style -2======================*/

    $("#owl-fullwidth").owlCarousel({
        items: 1,
        pagination: false,
        navigation: true,
        autoPlay: false
    });


    /*================Image Carousal Style -1======================*/


    $("#img-carousal").owlCarousel({
        items: 4,
        pagination: true,
        autoPlay: false
    });


    /*================Carousal Fullwidth Js======================*/

    $("#owl-fullwidth").owlCarousel({
        items: 1,
        pagination: false,
        navigation: true,
        autoPlay: false,
    });


    /*================Back To Top Button Js======================*/



    $('.scrollup').on('click', function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });

    $('.scrollup2').on('click', function () {
        $("html, body").animate({
            scrollTop: 0
        }, 600);
        return false;
    });


    /*================Animates======================*/
    new WOW().init();

    /*===============Progress Bar 1===================*/

    $('#jqmeter-horizontal').jQMeter({goal: '$10,000', raised: '8000', width: '100%', height: '26px', bgColor: '#e1e1e1', barColor: '#1e1e1e', animationSpeed: 1000, displayTotal: false});
    $('#jqmeter-horizonta2').jQMeter({goal: '$10,000', raised: '9000', width: '100%', height: '26px', bgColor: '#e1e1e1', barColor: '#1e1e1e', animationSpeed: 1000, displayTotal: false});
    $('#jqmeter-horizonta3').jQMeter({goal: '$10,000', raised: '6000', width: '100%', height: '26px', bgColor: '#e1e1e1', barColor: '#fc1e4e', animationSpeed: 1000, displayTotal: false});
    $('#jqmeter-horizonta4').jQMeter({goal: '$10,000', raised: '7000', width: '100%', height: '26px', bgColor: '#e1e1e1', barColor: '#494dff', animationSpeed: 1000, displayTotal: false});


    /*===============Progress Bar 2===================*/
    $('#demoprogressbar5').LineProgressbar({
        percentage: 80,
        fillBackgroundColor: '#1e1e1e',
        height: '4px'
    });
    $('#demoprogressbar6').LineProgressbar({
        percentage: 90,
        fillBackgroundColor: '#1e1e1e',
        height: '4px'
    });
    $('#demoprogressbar7').LineProgressbar({
        percentage: 60,
        fillBackgroundColor: '#fc1e4e',
        height: '4px'
    });
    $('#demoprogressbar8').LineProgressbar({
        percentage: 70,
        fillBackgroundColor: '#494dff',
        height: '4px'
    });

    /*===============Progress Bar 3===================*/

    $('#bar1').barfiller({barColor: '#1e1e1e'});
    $('#bar2').barfiller({barColor: '#1e1e1e'});
    $('#bar3').barfiller({barColor: '#fc1e4e'});
    $('#bar4').barfiller({barColor: '#494dff', duration: 3000});

    /*===============Same Color===================*/
    $('#bar9').barfiller({barColor: '#494dff'});
    $('#bar10').barfiller({barColor: '#494dff'});
    $('#bar11').barfiller({barColor: '#494dff'});
    $('#bar12').barfiller({barColor: '#494dff', duration: 3000});


    /*===============Progress Bar 4===================*/

    $('#bar5').barfiller({barColor: '#1e1e1e'});
    $('#bar6').barfiller({barColor: '#1e1e1e'});
    $('#bar7').barfiller({barColor: '#fc1e4e'});
    $('#bar8').barfiller({barColor: '#494dff', duration: 3000});
    $('#bar13').barfiller({barColor: '#ff6c00', duration: 3000});

    /*===============Gallery Portfolio 1===================*/

    /* initialize shuffle plugin */
    var $grid = $('#grid6');


    $grid.shuffle({
        itemSelector: '.item' // the selector for the items in the grid
    });
    /* reshuffle when user clicks a filter item */
    $('#filter6 a').on('click', function (e) {
        e.preventDefault();

        // set active class
        $('#filter6 a').removeClass('active');
        $(this).addClass('active');

        // get group name from clicked item
        var groupName = $(this).attr('data-group');

        // reshuffle grid
        $grid.shuffle('shuffle', groupName);
    });


    /*===============Gallery Portfolio 2===================*/

    /* initialize shuffle plugin */
    var $grid5 = $('#grid5');


    $grid5.shuffle({
        itemSelector: '.item' // the selector for the items in the grid
    });
    /* reshuffle when user clicks a filter item */
    $('#filter5 a').on('click', function (e) {
        e.preventDefault();

        // set active class
        $('#filter5 a').removeClass('active');
        $(this).addClass('active');

        // get group name from clicked item
        var groupName = $(this).attr('data-group');

        // reshuffle grid
        $grid5.shuffle('shuffle', groupName);
    });



    /*===============Gallery Portfolio 3===================*/

    /* initialize shuffle plugin */
    var $grid4 = $('#grid4');

    $grid4.shuffle({
        itemSelector: '.item' // the selector for the items in the grid
    });
    /* reshuffle when user clicks a filter item */
    $('#filter4 a').on('click', function (e) {
        e.preventDefault();

        // set active class
        $('#filter4 a').removeClass('active');
        $(this).addClass('active');

        // get group name from clicked item
        var groupName = $(this).attr('data-group');

        // reshuffle grid
        $grid4.shuffle('shuffle', groupName);
    });



    /*===============Gallery Portfolio 4===================*/

    /* initialize shuffle plugin */
    var $grid3 = $('#grid3');

    $grid3.shuffle({
        itemSelector: '.item' // the selector for the items in the grid
    });

    /* reshuffle when user clicks a filter item */
    $('#filter3 a').on('click', function (e) {
        e.preventDefault();

        // set active class
        $('#filter3 a').removeClass('active');
        $(this).addClass('active');

        // get group name from clicked item
        var groupName = $(this).attr('data-group');

        // reshuffle grid
        $grid3.shuffle('shuffle', groupName);
    });



    /*================Fanxy Box Gallery Js======================*/

    $('.fancybox').fancybox();


    /*================revolution Slider======================*/
    var tpj = jQuery;
    var revapi490;

    if (tpj("#rev_slider_490_1").revolution == undefined) {
        revslider_showDoubleJqueryError("#rev_slider_490_1");
    } else {
        revapi490 = tpj("#rev_slider_490_1").show().revolution({
            sliderType: "standard",
            sliderLayout: "fullwidth",
            dottedOverlay: "none",
            delay: 9000,
            navigation: {
                keyboardNavigation: "off",
                keyboard_direction: "horizontal",
                mouseScrollNavigation: "off",
                mouseScrollReverse: "default",
                onHoverStop: "off",
                touch: {
                    touchenabled: "on",
                    swipe_threshold: 75,
                    swipe_min_touches: 1,
                    swipe_direction: "horizontal",
                    drag_block_vertical: false
                }
                ,
                arrows: {
                    style: "zeus",
                    enable: true,
                    hide_onmobile: true,
                    hide_under: 600,
                    hide_onleave: true,
                    hide_delay: 200,
                    hide_delay_mobile: 1200,
                    tmp: '<div class="tp-title-wrap">  	<div class="tp-arr-imgholder"></div> </div>',
                    left: {
                        h_align: "left",
                        v_align: "center",
                        h_offset: 30,
                        v_offset: 0
                    },
                    right: {
                        h_align: "right",
                        v_align: "center",
                        h_offset: 30,
                        v_offset: 0
                    }
                }
            },
            responsiveLevels: [1240, 1024, 778, 480],
            visibilityLevels: [1240, 1024, 778, 480],
            gridwidth: [1240, 1024, 778, 480],
            gridheight: [880, 680, 580, 400],
            lazyType: "none",
            parallax: {
                type: "mouse",
                origo: "slidercenter",
                speed: 2000,
                levels: [2, 3, 4, 5, 6, 7, 12, 16, 10, 50, 46, 47, 48, 49, 50, 55],
                type: "mouse",
            },
            shadow: 0,
            spinner: "off",
            autoHeight: "off",
            disableProgressBar: "on",
            hideThumbsOnMobile: "off",
            hideSliderAtLimit: 0,
            hideCaptionAtLimit: 0,
            hideAllCaptionAtLilmit: 0,
            debugMode: false,
            fallbacks: {
                simplifyAll: "off",
                disableFocusListener: false,
            }
        });
    }


    /*================header Fixed Scroll======================*/
    $(window).on("scroll", function () {
        if ($(window).scrollTop() > 0) {
            $("#header-fix").addClass("active");
        } else {
            //remove the background property so it comes transparent again (defined in your css)
            $("#header-fix").removeClass("active");
        }
    });

    /*================Video Open Model======================*/
    $("#video2").on('click', function () {
        $('#my-modal2').modal('show');
    });
    $("#video3").on('click', function () {
        $('#my-modal3').modal('show');
    });
    /*================Asidebar======================*/

    var body = $("body");
    $(".menu-toggle").on("click", function () {
        body.toggleClass("menu-open");
        $(".menu-toggle").toggleClass("menu-toggle-left");
        return false;
    })


    /*================Click Open Search bar======================*/
    $(".search-bar").on('click', function () {
        $(".search-wrap").css("top", "0");
    });
    $(".close-btn").on('click', function () {
        $(".search-wrap").css("top", "-100%");
    });


    /*================revolution Slider 2======================*/
    var tpj = jQuery;
    var revapi1050;

    if (tpj("#rev_slider_1050_1").revolution == undefined) {
        revslider_showDoubleJqueryError("#rev_slider_1050_1");
    } else {
        revapi1050 = tpj("#rev_slider_1050_1").show().revolution({
            sliderType: "standard",
            jsFileLocation: "revolution/js/",
            sliderLayout: "fullscreen",
            dottedOverlay: "none",
            delay: 9000,
            navigation: {
                keyboardNavigation: "on",
                keyboard_direction: "vertical",
                mouseScrollNavigation: "on",
                mouseScrollReverse: "default",
                onHoverStop: "off",
                touch: {
                    touchenabled: "on",
                    swipe_threshold: 75,
                    swipe_min_touches: 50,
                    swipe_direction: "vertical",
                    drag_block_vertical: false
                }
                ,
                bullets: {
                    enable: true,
                    hide_onmobile: true,
                    hide_under: 1024,
                    style: "hephaistos",
                    hide_onleave: false,
                    direction: "vertical",
                    h_align: "right",
                    v_align: "center",
                    h_offset: 30,
                    v_offset: 0,
                    space: 5,
                    tmp: ''
                }
            },
            responsiveLevels: [1240, 1024, 778, 480],
            visibilityLevels: [1240, 1024, 778, 480],
            gridwidth: [1400, 1240, 778, 480],
            gridheight: [868, 768, 960, 720],
            lazyType: "none",
            shadow: 0,
            spinner: "spinner2",
            stopLoop: "on",
            stopAfterLoops: 0,
            stopAtSlide: 1,
            shuffle: "off",
            autoHeight: "off",
            fullScreenAutoWidth: "off",
            fullScreenAlignForce: "off",
            fullScreenOffsetContainer: "",
            fullScreenOffset: "",
            disableProgressBar: "on",
            hideThumbsOnMobile: "off",
            hideSliderAtLimit: 0,
            hideCaptionAtLimit: 0,
            hideAllCaptionAtLilmit: 0,
            debugMode: false,
            fallbacks: {
                simplifyAll: "off",
                nextSlideOnWindowFocus: "off",
                disableFocusListener: false,
            }
        });
    }





    //Screenshoot slider
    $("#owl-carousel").owlCarousel({
        responsive: {
            0: {
                items: 1
            },
            991: {
                items: 5
            }
        },
        loop: true,
        center: true,
        dots: true,
        nav: false,
        autoplay: false,
        pagination: false
    });

    /*------ MENU Fixed ------*/
    var $window = $(window);
    $window.on('scroll', function () {
        var $scroll = $window.scrollTop();
        var $navbar = $(".header-container");
        if ($scroll > 100) {
            $navbar.addClass("fixedmenu");
        } else {
            $navbar.removeClass("fixedmenu");
        }
        if ($(this).scrollTop() > 100) {
            $('.scrollup').fadeIn();
        } else {
            $('.scrollup').fadeOut();
        }
    });



    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').on('click', function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: (target.offset().top - 54)
                }, 1000, "easeInOutExpo");
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').on('click', function () {
        $('.navbar-collapse').collapse('hide');
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
        target: '#navbarNav',
        offset: 60
    });



})(jQuery);

