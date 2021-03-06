$(document).ready(function() {
  'use strict';

  var body = $("body"),
    menuOpenIcon = $(".nav__icon-menu"),
    menuCloseIcon = $(".nav__icon-close"),
    menuList = $(".menu-overlay"),
    searchOpenIcon = $(".search-button"),
    searchCloseIcon = $(".search__close"),
    searchInput = $(".search__text"),
    searchBox = $(".search");

  /* =======================
  // Open external links in a new tab
  ======================= */
  [].forEach.call(document.links, function(el) {
    if (el.hostname != window.location.hostname) {
      el.target = '_blank';
    } 
  });
    
  /* =======================
  // Menu and Search
  ======================= */
  menuOpenIcon.click(function () {
    menuOpen();
  })

  menuCloseIcon.click(function () {
    menuClose();
  })

  searchOpenIcon.click(function () {
    searchOpen();
  });

  searchCloseIcon.click(function () {
    searchClose();
  });

  function menuOpen() {
    menuList.addClass("is-open");
    body.addClass("overlay-active");
  }

  function menuClose() {
    menuList.removeClass("is-open");
    body.removeClass("overlay-active");
  }

  function searchOpen() {
    searchBox.addClass("is-visible");
    body.addClass("overlay-active");
    setTimeout(function () {
      searchInput.focus();
    }, 300);
  }

  function searchClose() {
    searchBox.removeClass("is-visible");
    body.removeClass("overlay-active");
  }

  $('.search, .search__box').on('click keyup', function (event) {
    if (event.target == this || event.keyCode == 27) {
      searchClose();
    }
  });


  /* =======================
  // Animation Load Page
  ======================= */
  setTimeout(function(){
    $('body').addClass('is-in');
  },150)


  // =====================
  // Simple Jekyll Search
  // =====================
  SimpleJekyllSearch({
    searchInput: document.getElementById("js-search-input"),
    resultsContainer: document.getElementById("js-results-container"),
    json: "/search.json",
    searchResultTemplate: '{article}',
    noResultsText: '<li class="no-results"><h3>No results found</h3></li>',
    debounceTime: 400
  });


  /* =======================
  // LazyLoad Images
  ======================= */
  var lazyLoadInstance = new LazyLoad({
    elements_selector: '.lazy'
  })


  // =====================
  // Ajax Load More
  // =====================
  var $load_posts_button = $('.load-more-posts');

  $load_posts_button.click(function(e) {
    e.preventDefault();
    var loadMore = $('.load-more-section');
    var request_next_link = pagination_next_url.split('/page')[0] + '/page/' + pagination_next_page_number + '/';

    $.ajax({
      url: request_next_link,
      beforeSend: function() {
        $load_posts_button.text('Loading...');
      }
    }).done(function(data) {
      var posts = $('.grid__post', data);
      $('.grid').append(posts);

      var lazyLoadInstance = new LazyLoad({
        elements_selector: '.lazy'
      })

      $load_posts_button.text('Load more');
      pagination_next_page_number++;

      if (pagination_next_page_number > pagination_available_pages_number) {
        loadMore.addClass('hide');
      }
    });
  });


  /* =======================
  // Responsive Videos
  ======================= */
  $(".post__content, .page__content").fitVids({
    customSelector: ['iframe[src*="ted.com"]', 'iframe[src*="player.twitch.tv"]', 'iframe[src*="facebook.com"]']
  });


  /* =======================
  // Zoom Image
  ======================= */
  $(".page img, .post img").attr("data-action", "zoom");
  $(".page a img, .post a img").removeAttr("data-action", "zoom");


  /* =======================
  // Scroll Top Button
  ======================= */
  $(".top").click(function() {
    $("html, body")
      .stop()
      .animate({ scrollTop: 0 }, "slow", "swing");
  });
  $(window).scroll(function() {
    if ($(this).scrollTop() > $(window).height()) {
      $(".top").addClass("is-active");
    } else {
      $(".top").removeClass("is-active");
    }
  });

});

/* =======================
// Mermaid Diagrams
//
// Note: The theme can be customised using something like:
//       themeVariables: { actorBorder: '#ff7b7b'},
//       themeCSS: ".actor { stroke: #ff7b7b; }",
//
// See:  https://mermaid-js.github.io/mermaid/#/theming
======================= */
var config = {

  startOnLoad: true,
  
  // Theme
  theme: 'dark',
  themeVariables: {    
    
    // Sequence diagram
    actorBorder: '#ff7b7b',
    labelBoxBorderColor: '#ff7b7b'
  },

  // Sequence diagram
  sequence:{

    // Actor
    actorFontFamily: 'Karla, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif',
    actorFontSize: 18,
    actorFontWeight: 700,
    
    // Note
    noteFontFamily: 'Karla, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif',
    noteFontSize: 14,
    
    // Message
    messageFontFamily: 'Karla, -apple-system, BlinkMacSystemFont, "Segoe UI", "Helvetica Neue", sans-serif',
    messageFontSize: 14
  }
};

mermaid.initialize(config);