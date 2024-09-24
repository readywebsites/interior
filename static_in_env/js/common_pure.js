$(document).ready(function () {
  setupJQueryValidate();
  instagram();
  menu();
  checkboxLink();
  scrollTo();

  // Projects gallery
  gallerySlider();

  // Home page hero
  heroAnimation();

  // Projects grid animation
  projectsGridAnimation();

  // Single project carousel
  lightbox();

  // Photos carousel
  photos();
});

function setupJQueryValidate() {
  $.validator.setDefaults({
    ignore: [],
    errorElement: "div",
    errorClass: "invalid-feedback",
    errorPlacement: function (error, element) {
      if (element.prop("type") === "checkbox") {
        error.insertAfter(element.parent(".checkbox-field"));
      } else {
        error.insertAfter(element);
      }
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass("is-invalid");
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass("is-invalid");
    },
  });

  $.validator.addMethod("phone", function (value) {
    return /^$|(^[+]{0,1}[0-9]{8,}$)/.test(value);
  }, tbp_data_settings.jquery_validate.phone_validation);
}

function instagram() {
  var elem = $(".js-insta-btn");
  if (!elem.length) {
    return false;
  }

  var panel = $(".instagram-links");

  elem.click(function (e) {
    e.preventDefault();
    panel.toggleClass('active');
  });
}

function gallerySlider() {
  var swiper = new Swiper('.js-gallery-slider', {
    // Optional parameters
    autoplay: {
      delay: 5000,
    },
    speed: 500,
    direction: 'horizontal',
    loop: false,

    pagination: false,

    // Navigation arrows
    /*navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },*/
    navigation: false,

    // And if we need scrollbar
    scrollbar: {
      el: '.swiper-scrollbar',
    },
    draggable: true,
    freeMode: {
      enabled: true,
      sticky: true,
    },
    slidesPerView: 1,
    breakpoints: {
      770: {
        slidesPerView: 'auto',
      }
    }
  });
}

function heroAnimation() {
  var elem = $(".js-hero");
  if (!elem.length) {
    return false;
  }

  var updParallax = function (idx) {
    if (!$(".hero-parallax-mirror .parallax-mirror").length) {
      return false;
    }
    $(".hero-view-item").parallax("destroy");
    $(".hero-view-item").eq(idx).parallax();
  };

  updParallax(0);

  $(".js-hero-nav-link").mouseenter(function (e) {
    e.preventDefault();

    // change nav link class
    $(".js-hero-nav-link").removeClass("active");
    $(this).addClass("active");

    // change the view tab
    var viewID = $(this).data("id");

    $(".hero-view-item.active").css('z-index', '20').removeClass("active");
    $(".hero-view-item").filter("[data-id='" + viewID + "']").css('z-index', '30').addClass("active");

    updParallax(viewID);
  });
}

function menu() {
  var elem = $(".js-menu");
  if (!elem.length) {
    return false;
  }

  var menu = $(".menu");

  elem.click(function (e) {
    e.preventDefault();

    $("body").addClass('locked');
    //menu.fadeIn();
    menu.css('display', 'block');
  });

  $(".js-menu-close").click(function (e) {
    e.preventDefault();

    menu.css('display', 'none');
    $("body").removeClass('locked');
  });
}

function checkboxLink() {
  var elem = $(".js-agreement-text-link");
  if (!elem.length) {
    return false;
  }
  $(document).on("click", ".js-agreement-text-link", function (e) {
    e.stopPropagation();
  });
}

function scrollTo() {
  var $elem = $(".js-scroll-to");
  if (!$elem.length) {
    return false;
  }

  $elem.on("click", function (e) {
    var scrollElement = $(this).data("scroll-to");
    $("html, body").animate({
      scrollTop: $(scrollElement).offset().top
    }, 300);
  });
}

function projectsGridAnimation() {
  var elem = $(".portfolio-grid");
  if (!elem.length) {
    return false;
  }

  elem.on("mouseenter", ".projects-gallery-card", function () {
    var nearest_item = $(this).prev();
    if (!nearest_item.length) {
      nearest_item = $(this).next();
    }

    if (!nearest_item.length) {
      return false;
    }

    var current_offset = $(this).offset().top;
    var nearest_item_offset = nearest_item.offset().top;

    if (current_offset !== nearest_item_offset) {
      nearest_item = $(this).next();
      nearest_item_offset = nearest_item.offset().top;
    }

    // Start animation
    $(".projects-gallery-card").removeClass("wide").removeClass("narrow");
    $(this).addClass("wide");
    nearest_item.addClass("narrow");
  });

  elem.on("mouseleave", function () {
    $(".projects-gallery-card").removeClass("wide").removeClass("narrow");
  });
}

function photos() {
  var thumbsInstance;
  var photosInstance;

  if ($(".js-thumbs-carousel").length) {
    thumbsInstance = new Swiper('.js-thumbs-carousel', {
      // Optional parameters
      direction: 'horizontal',
      loop: false,

      slidesPerView: "auto",
      spaceBetween: 10,
      centeredSlides: false,

      // Navigation arrows
      navigation: {
        // nextEl: '.swiper-button-next',
        // prevEl: '.swiper-button-prev',
      },
      watchSlidesVisibility: true,
      watchSlidesProgress: true,
    });
  }

  if ($(".js-photos-carousel").length) {
    photosInstance = new Swiper('.js-photos-carousel', {
      slidesPerView: 1,
      pagination: {
        el: '.swiper-pagination',
        type: 'fraction',
      },
      thumbs: {
        swiper: thumbsInstance
      },
      navigation: {
        nextEl: $('.js-thumbs-carousel .swiper-button-next').get(0),
        prevEl: $('.js-thumbs-carousel .swiper-button-prev').get(0)
      },
    });
  }
}

function lightbox() {
  var $elem = $(".js-photos-carousel");
  if (!$elem.length) {
    return false;
  }
  if (!$elem.length) {
    return false;
  }

  $elem.magnificPopup({
    // Delay in milliseconds before popup is removed
    removalDelay: 300,

    // Class that is added to popup wrapper and background
    // make it unique to apply your CSS animations just to this exact popup
    mainClass: 'mfp-fade',

    delegate: '.photo-slide a', // the selector for gallery item
    type: 'image',
    gallery: {
      enabled: true
    }
  });
}
