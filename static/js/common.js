// The Common module is designed as an auxiliary module
// to hold functions that are used in multiple other modules
/* eslint no-unused-vars: "off" */

var Common = (function() {
  // Publicly accessible methods defined
  return {
    buildDomElement: buildDomElementFromJson,
    fireEvent: fireEvent,
    listForEach: listForEach
  };

//LOADER/SPINNER
$(window).bind("load", function() {

    "use strict";
    
    $(".spn_hol").fadeOut(600);
});
  // Take in JSON object and build a DOM element out of it
  // (Limited in scope, cannot necessarily create arbitrary DOM elements)
  // JSON Example:
  //  {
  //    "tagName": "div",
  //    "text": "Hello World!",
  //    "className": ["aClass", "bClass"],
  //    "attributes": [{
  //      "name": "onclick",
  //      "value": "alert("Hi there!")"
  //    }],
  //    "children: [{other similarly structured JSON objects...}, {...}]
  //  }
  function buildDomElementFromJson(domJson) {
    // Create a DOM element with the given tag name
    var element = document.createElement(domJson.tagName);

    // Fill the "content" of the element
    if (domJson.text) {
      element.innerHTML = domJson.text;
    } else if (domJson.html) {
      element.insertAdjacentHTML('beforeend', domJson.html);
    }

    // Add classes to the element
    if (domJson.classNames) {
      for (var i = 0; i < domJson.classNames.length; i++) {
        element.classList.add(domJson.classNames[i]);
      }

      if (domJson.classNames == "img-bot") {
        console.log("Imagen bot");
        element.setAttribute("src", "/static/img/lucia.png");
      }
    }
    // Add attributes to the element
    if (domJson.attributes) {
      for (var j = 0; j < domJson.attributes.length; j++) {
        var currentAttribute = domJson.attributes[j];
        element.setAttribute(currentAttribute.name, currentAttribute.value);
      }
    }
    // Add children elements to the element
    if (domJson.children) {
      for (var k = 0; k < domJson.children.length; k++) {
        var currentChild = domJson.children[k];
        element.appendChild(buildDomElementFromJson(currentChild));
      }
    }
    return element;
  }

  // Trigger an event to fire
  function fireEvent(element, event) {
    var evt;
    if (document.createEventObject) {
      // dispatch for IE
      evt = document.createEventObject();
      return element.fireEvent('on' + event, evt);
    }
    // otherwise, dispatch for Firefox, Chrome + others
    evt = document.createEvent('HTMLEvents');
    evt.initEvent(event, true, true); // event type,bubbling,cancelable
    return !element.dispatchEvent(evt);
  }

  // A function that runs a for each loop on a List, running the callback function for each one
  function listForEach(list, callback) {
    for (var i = 0; i < list.length; i++) {
      callback.call(null, list[i]);
    }
  }
}());

$(document).ready(function() {

    "use strict";
    
    $(window).scroll(function() {

        "use strict";
        
        if ($(window).scrollTop() > 80) {
            $(".navbar").css({
                'margin-top': '0px',
                'opacity': '1'
            })
            $(".navbar-nav>li>a").css({
                'padding-top': '15px'
            });
            $(".navbar-brand img").css({
                'height': '45px'
            });
            $(".navbar-brand img").css({
                'padding-top': '0px'
            });
            $(".navbar-default").css({
                'background-color': 'rgba(25, 165, 211, 0.7)'
            });
        } else {
            $(".navbar").css({
                'margin-top': '-200px',
                'opacity': '0'
            })
            $(".navbar-nav>li>a").css({
                'padding-top': '45px'
            });
            $(".navbar-brand img").css({
                'height': '45px'
            });
            $(".navbar-brand img").css({
                'padding-top': '20px'
            });
            $(".navbar-default").css({
                'background-color': 'rgba(59, 59, 59, 0)'
            });
        }
    });
});

$(function() {
  
  "use strict";

  $('.url-none').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
});

// MENU SECTION ACTIVE
$(document).ready(function() {

    "use strict";
    
    $(".navbar-nav li a").click(function() {

        "use strict";
        
        $(".navbar-nav li a").parent().removeClass("active");
        $(this).parent().addClass("active");
    });
});



// Hilight MENU on SCROLl

$(document).ready(function() {

    "use strict";
    
    $(window).scroll(function() {

        "use strict";
        
        $(".page").each(function() {

            "use strict";
            
            var bb = $(this).attr("id");
            var hei = $(this).outerHeight();
            var grttop = $(this).offset().top - 70;
            if ($(window).scrollTop() > grttop - 1 && $(window).scrollTop() < grttop + hei - 1) {
                var uu = $(".navbar-nav li a[href='#" + bb + "']").parent().addClass("active");
            } else {
                var uu = $(".navbar-nav li a[href='#" + bb + "']").parent().removeClass("active");
            }
        });
    });
});

$(document).ready(function() {

    "use strict";
    
    setInterval(function() {

        "use strict";
        
        var widnowHeight = $(window).height();
        var containerHeight = $("#home-container").height();
        var padTop = widnowHeight - containerHeight;
        $("#home-container").css({
            'padding-top': '0px',
            'padding-bottom': '300px'
        });
    }, 10)
});

