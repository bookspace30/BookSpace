// sizing
var width = window.innerWidth;
var height = window.innerHeight;

var largeHeader = document.getElementById('masthead');
var points = [];
var target = {x: width/2, y: height/2};
var animateHeader = true;

// canvas
var canvas = document.querySelector("canvas");
canvas.width = width;
canvas.height = height;

// context
var context = canvas.getContext("2d");

// start
var numStars = 600;
var stars = [];
var twinkleFactor = 0.3;
var maxStarRadius = 1;

var firework1;
var firework2;
var minStrength = 1.75; //lowest firework power
var maxStrength = 7; //highest firework power
var minTrails = 7; //min particles
var maxTrails = 30; //max particles
var particleRadius = 1;
var trailLength = 15; //particle trail length
var delay = 0.5; // number of lifetimes between explosions
var lifetime = 150; //life time of firework
var g = 5e-2; //strength of gravity
var D = 1e-3; //strength of drag (air resistance)

// Particle function
var Particle = function(x, y, vx, vy, ax, ay, colour) {
  this.x = x;
  this.y = y;
  this.vx = vx;
  this.vy = vy;
  this.ax = ax;
  this.ay = ay;
  this.lifetime = lifetime;
  this.path = [];
  this.colour = colour;
  this.r = particleRadius;

  this.update = function() {
    this.lifetime--;

    // add point to path but if full, remove a point first
    if (this.path.length >= trailLength) this.path.shift();
    this.path.push([this.x, this.y]);

    // update speed n position n stuff
    this.vy += this.ay;
    this.vx += this.ax;
    this.x += this.vx;
    this.y += this.vy;
  };

  this.draw = function() {
    var opacity = ~~((this.lifetime * 100) / lifetime) / 100;

    // tail
    context.fillStyle = "rgba(" + this.colour + opacity * 0.6 + ")";
    if (this.lifetime > lifetime * 0.95) context.fillStyle = "transparent";
    context.lineWidth = 1;
    context.beginPath();
    context.moveTo(this.x - this.r, this.y);
    var i = this.path.length - 1;
    context.lineTo(this.path[0][0], this.path[0][1]);
    context.lineTo(this.x + this.r, this.y);
    context.closePath();
    context.fill();

    // main dot
    context.fillStyle = "rgba(" + this.colour + opacity + ")";
    if (this.lifetime > lifetime * 0.95) context.fillStyle = "#fff";
    context.beginPath();
    context.arc(~~this.x, ~~this.y, this.r, 0, Math.PI * 2);
    context.fill();
    context.closePath();
  };
};

// Firework function
var Firework = function() {
  this.x = width * (Math.random() * 0.8 + 0.1); // from 0.1-0.9 widths
  this.y = height * (Math.random() * 0.8 + 0.1); // from 0.1-0.9 heights
  this.strength =
    Math.random() * (maxStrength - minStrength) + minStrength;
  this.colour =
    ~~(Math.random() * 255) +
    "," +
    ~~(Math.random() * 255) +
    "," +
    ~~(Math.random() * 255) +
    ",";
  this.lifetime = 0;
  this.particles = (function(x, y, strength, colour) {
    var p = [];

    var n = ~~(Math.random() * (maxTrails - minTrails)) + minTrails;
    var ay = g;
    for (var i = n; i--; ) {
      var ax = D;
      var angle = (i * Math.PI * 2) / n;
      if (angle < Math.PI) ax *= -1;
      var vx = strength * Math.sin(angle);
      var vy = strength * Math.cos(angle);
      p.push(new Particle(x, y, vx, vy, ax, ay, colour));
    }

    return p;
  })(this.x, this.y, this.strength, this.colour);

  this.update = function() {
    this.lifetime++;
    if (this.lifetime < 0) return; //allows  to be delayed
    for (var i = this.particles.length; i--; ) {
      this.particles[i].update();
      this.particles[i].draw();
      // could also make an extra draw function for firework function
    }
  };
};

var Star = function() {
  this.x = Math.random() * width;
  this.y = Math.random() * height;
  this.r = Math.random() * maxStarRadius;
  this.b = ~~(Math.random() * 100) / 100;
};

Star.prototype.draw = function() {
  this.b += twinkleFactor * (Math.random() - 0.5);
  context.fillStyle = "rgba(255,255,255," + this.b + ")";
  context.beginPath();
  context.arc(~~this.x, ~~this.y, this.r, 0, Math.PI * 2);
  context.fill();
  context.closePath();
};

function createStars() {
  for (var i = numStars; i--; ) stars.push(new Star());
}

function main() {
  context.fillStyle = "transparent";
  context.fillRect(0, 0, width, height);

  for (var i = numStars; i--; ) stars[i].draw();

  firework1.update();
  firework2.update();

  if (firework1.lifetime == lifetime * delay) firework2 = new Firework();
  if (firework2.lifetime == lifetime * delay) firework1 = new Firework();

  window.requestAnimationFrame(main);
}

function initHeader() {

    largeHeader.style.height = height+'px';

    // create points
    for(var x = 0; x < width; x = x + width/20) {
        for(var y = 0; y < height; y = y + height/20) {
            var px = x + Math.random()*width/20;
            var py = y + Math.random()*height/20;
            var p = {x: px, originX: px, y: py, originY: py };
            points.push(p);
        }
    }

    // for each point find the 5 closest points
    for(var i = 0; i < points.length; i++) {
        var closest = [];
        var p1 = points[i];
        for(var j = 0; j < points.length; j++) {
            var p2 = points[j]
            if(!(p1 == p2)) {
                var placed = false;
                for(var k = 0; k < 5; k++) {
                    if(!placed) {
                        if(closest[k] == undefined) {
                            closest[k] = p2;
                            placed = true;
                        }
                    }
                }

                for(var k = 0; k < 5; k++) {
                    if(!placed) {
                        if(getDistance(p1, p2) < getDistance(p1, closest[k])) {
                            closest[k] = p2;
                            placed = true;
                        }
                    }
                }
            }
        }
        p1.closest = closest;
    }

    // assign a circle to each point
    for(var i in points) {
        var c = new Circle(points[i], 2+Math.random()*2, 'rgba(255,255,255,0.3)');
        points[i].circle = c;
    }
}

// Event handling
function addListeners() {
    if(!('ontouchstart' in window)) {
        window.addEventListener('mousemove', mouseMove);
    }
    window.addEventListener('scroll', scrollCheck);
    window.addEventListener('resize', resize);
}

function mouseMove(e) {
    var posx = posy = 0;
    if (e.pageX || e.pageY) {
        posx = e.pageX;
        posy = e.pageY;
    }
    else if (e.clientX || e.clientY)    {
        posx = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        posy = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }
    target.x = posx;
    target.y = posy;
}

function scrollCheck() {
    if(document.body.scrollTop > height) animateHeader = false;
    else animateHeader = true;
}

function resize() {
    width = window.innerWidth;
    height = window.innerHeight;
    largeHeader.style.height = height+'px';
    canvas.width = width;
    canvas.height = height;
}

// animation
function initAnimation() {
    animate();
    for(var i in points) {
        shiftPoint(points[i]);
    }
}

function animate() {
    if(animateHeader) {
        context.clearRect(0,0,width,height);
        for(var i in points) {
            // detect points in range
            if(Math.abs(getDistance(target, points[i])) < 4000) {
                points[i].active = 0.3;
                points[i].circle.active = 0.6;
            } else if(Math.abs(getDistance(target, points[i])) < 20000) {
                points[i].active = 0.1;
                points[i].circle.active = 0.3;
            } else if(Math.abs(getDistance(target, points[i])) < 40000) {
                points[i].active = 0.02;
                points[i].circle.active = 0.1;
            } else {
                points[i].active = 0;
                points[i].circle.active = 0;
            }

            drawLines(points[i]);
            points[i].circle.draw();
        }
    }
    requestAnimationFrame(animate);
}

function shiftPoint(p) {
    TweenLite.to(p, 1+1*Math.random(), {x:p.originX-50+Math.random()*100,
        y: p.originY-50+Math.random()*100, ease:Circ.easeInOut,
        onComplete: function() {
            shiftPoint(p);
        }});
}

// Canvas manipulation
function drawLines(p) {
    if(!p.active) return;
    for(var i in p.closest) {
        context.beginPath();
        context.moveTo(p.x, p.y);
        context.lineTo(p.closest[i].x, p.closest[i].y);
        context.strokeStyle = 'rgba(156,217,249,'+ p.active+')';
        context.stroke();
    }
}

function Circle(pos,rad,color) {
    var _this = this;

    // constructor
    (function() {
        _this.pos = pos || null;
        _this.radius = rad || null;
        _this.color = color || null;
    })();

    this.draw = function() {
        if(!_this.active) return;
        context.beginPath();
        context.arc(_this.pos.x, _this.pos.y, _this.radius, 0, 2 * Math.PI, false);
        context.fillStyle = 'rgba(156,217,249,'+ _this.active+')';
        context.fill();
    };
}

// Util
function getDistance(p1, p2) {
    return Math.pow(p1.x - p2.x, 2) + Math.pow(p1.y - p2.y, 2);
}

function init() {
  initHeader();
  initAnimation();
  addListeners();
  firework1 = new Firework();
  firework2 = new Firework();
  firework2.lifetime = -lifetime * delay;
  createStars();
  main();
}

init();
// Loading Overlay
window.onload = function() {
  document.body.className = "";
};
setTimeout(function() {
  $('html').removeClass('loading-overlay-showing');
}, 3000);

// Sidebar Navigation
$(".ui.main.sidebar").sidebar({
 dimPage: true,
 transition: 'overlay',
 exclusive: false,
 closable: true
 })
  .sidebar("attach events", ".ui.icon.item .bars.icon")
  .sidebar({
    onVisible: function() {
      $(".pusher").removeClass('pusher').addClass('dimmed pusher');
    },
    onHidden: function() {
      $(".pusher").removeClass('dimmed pusher').addClass('pusher');
    }
  })
;
// User Sidebar Menu
$(".ui.user.sidebar").sidebar({
 dimPage: true,
 transition: 'overlay',
 exclusive: false,
 closable: true
 })
  .sidebar("attach events", "a.item .cogs.icon")
  .sidebar({
    onVisible: function() {
      $(".pusher").removeClass('pusher').addClass('dimmed pusher');
    },
    onHidden: function() {
      $(".pusher").removeClass('dimmed pusher').addClass('pusher');
    }
  })
;

$(".ui.icon.item .bars").removeClass("disabled");
jQuery(".ui.sidebar .menu > .submenu").click(function(e) {
  jQuery(".ui.sidebar item menu").slideUp(), jQuery(this).next().is(":visible") || jQuery(this).next().slideDown(),
  e.stopPropagation()
})

// Fixed Menu Dropdown
$(".dropdown").dropdown({
 transition: "fade"
});

// Themantic Definition Tooltip
$(".tool-tip").popup({
 position: "top center",
 target: ".tool-tip",
 html: "<span class=\"ui medium text\"><strong>Themantic</strong></span> <span class=\"ui small grey text\">[ thee-man-tik ]</span><br><em><span class=\"ui medium text\">adjective</span></em><ol class=\"ui tiny list\"><li>of, or relating to the study of web development as it pertains to website theming.</li><li>the amalgamation of both the words <em>semantic</em> and <em>theme</em> to form the compound word <em>themantic</em>.</li></ol><em><span class=\"ui medium text\">noun</span></em><ol class=\"ui tiny list\"><li>the developer of Themantic's way of keeping Semantic's theme alive by means of word play.</li></ol>"
});

// Top Fixed Menu Search Input
$(".ui.right.search.item").search({
 apiSettings: {
  url: "//api.github.com/search/repositories?q={query}+user:daemondevin"
 },
 fields: {
  results: "items",
  title: "name",
  url: "html_url"
 },
 minCharacters: 3
});

// Fixed Menu Popup
$(".custom.link.item").popup({
 popup: $(".flowing.custom.popup"),
 on: "click",
 inline: false,
 hoverable: true,
 transition: "vertical flip",
 position: "bottom left",
 delay: {
  show: 300,
  hide: 800
 }
});

$(".guide.link.item").popup({
 popup: $(".guide.popup"),
 on: "click",
 inline: true,
 hoverable: true,
 position: "bottom center",
 delay: {
  show: 300,
  hide: 800
 }
});

// Landing Toast
$("#landing-toast").click(function() {
 $("body").toast({
  class: "success",
  title: "",
  showIcon: "egg",
  displayTime: 3000,
  message: "You found an easter egg already!",
  showProgress: "bottom",
  position: "bottom right"
 });
});

// Example Toasts
$("#toast").click(function() {
 $("body").toast({
  class: "success",
  title: "Awesome!",
  showIcon: "egg",
  displayTime: 3000,
  message: "You found an easter egg already!",
  showProgress: "bottom",
  position: "bottom right"
 });
});

$("#egg").dimmer({
 transition: "fade up",
 on: "hover"
});

// Subscribe Form
$(".ui.form").form({
 fields: {
  email: {
   identifier: "email",
   rules: [
    {
     type: "email",
     prompt: "Please enter a valid e-mail"
    }
   ]
  }
 },
 onFailure: function(formErrors, fields) {
  $("body").toast({
   class: "error",
   title: "Oops!",
   showIcon: "exclamation triangle",
   displayTime: 0,
   message: "Please enter a valid email!",
   closeIcon: true,
   position: "top right"
  });
  return false;
 }
});
$('.menu .item')
  .tab()
;

// Codeblock Examples
(function () {
  //filter IE8 and earlier which don't support the generated content
  if (typeof (window.getComputedStyle) == 'undefined') {
    return;
  }  //get the collection of PRE elements

  //add copy to clipboard feature
  var copy = document.getElementById('codeCopy');
  copy.setAttribute('onclick', 'codeToClipboard()');

  var pre = document.getElementsByTagName('pre');
  //now iterate through the collection
  for (var len = pre.length, i = 0; i < len; i++) {
    //get the CODE or SAMP element inside it,
    //or just in case there isn't one, continue to the next PRE
    var code = pre[i].getElementsByTagName('code').item(0);
    if (!code) {
      code = pre[i].getElementsByTagName('samp').item(0);
      if (!code) {
        continue;
      }
    }    //create a containing DIV column (but don't append it yet)

    //including aria-hidden so that ATs don't read the numbers
    var column = document.createElement('div');
    column.setAttribute('aria-hidden', 'true');
    column.setAttribute('class', 'numbers');
    //split the code by line-breaks to count the number of lines
    //then for each line, add an empty span inside the column
    for (var n = 0; n < code.innerHTML.split(/[\n\r]/g).length; n++) {
      column.appendChild(document.createElement('span'));
    }    //now append the populated column before the code element

    pre[i].insertBefore(column, code);
    //finally add an identifying class to the PRE to trigger the extra CSS
    pre[i].className = 'line-numbers';
  }
}) ();

// Code To Clipboard
function codeToClipboard() {
  var range = document.createRange();
  range.selectNode(document.getElementById("copyCode"));
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);
  document.execCommand("copy");
  window.getSelection().removeAllRanges();
}

// Copy Success Toast
$("copyCode").click(function() {
 $("body").toast({
  class: "success",
  title: "Copied Code!",
  showIcon: "code",
  displayTime: 3000,
  message: "This code blacks syntax was copied to the clipboard",
  showProgress: "bottom",
  position: "bottom left"
 });
});

// Comments Reply
$('.type.example form')
  .form({
    on: 'blur',
    fields: {
      integer: {
        identifier  : 'integer',
        rules: [
          {
            type   : 'integer[1..100]',
            prompt : 'Please enter an integer value'
          }
        ]
      },
      decimal: {
        identifier  : 'decimal',
        rules: [
          {
            type   : 'decimal',
            prompt : 'Please enter a valid decimal'
          }
        ]
      },
      number: {
        identifier  : 'number',
        rules: [
          {
            type   : 'number',
            prompt : 'Please enter a valid number'
          }
        ]
      },
      email: {
        identifier  : 'email',
        rules: [
          {
            type   : 'email',
            prompt : 'Please enter a valid e-mail'
          }
        ]
      },
      url: {
        identifier  : 'url',
        rules: [
          {
            type   : 'url',
            prompt : 'Please enter a url'
          }
        ]
      }
    }
  })
;

//Table of Contents
var toc =
  "<h2 class=\"ui dividing header\"><i class=\"small list ol icon\"></i>Table Of Contents</h2>" +
	"<ol class=\"ui animated link list\">";
	//var count = 0;
	var newLine, el, title, link;
$(".header.anchor").each(function() {
  //count++
  el = $(this);
  title = el.text();
  link = $(location).attr('href') + "#" + el.attr("name");
  newLine = " <li><a class=\"header\" href=\"" + link + "\">" + title + "</a>" + "</li>";
    // count + ". <li><a class=\"header\" href=\"" + link + "\">" + title + "</a>" + "</li>";
  toc += newLine;
});
toc +=  "</ol>";
$(".anchors-away").prepend(toc);

// Reveal Header
var duration = 5;
var delay = 1.5;
var revealText = document.querySelector(".reveal");
var letters = revealText.textContent.split("");
revealText.textContent = "";
var middle = letters.filter(function (e) {return e !== " ";}).length / 2;
letters.forEach(function (letter, i) {
  var span = document.createElement("span");
  span.textContent = letter;
  span.style.animationDelay = delay + Math.abs(i - middle) * 0.1 + "s";
  revealText.append(span);
});

// Smooth Scrolling
$('a[href*="#"]')
  // Remove links that don't actually link to anything
  .not('[href="#"]')
  .not('[href="#0"]')
  .click(function(event) {
    // On-page links
    if (
      location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
      &&
      location.hostname == this.hostname
    ) {
      // Figure out element to scroll to
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      // Does a scroll target exist?
      if (target.length) {
        // Only prevent default if animation is actually gonna happen
        event.preventDefault();
        $('html, body').animate({
          scrollTop: target.offset().top - 63
        }, 1000, function() {
          // Callback after animation
          // Must change focus!
          var $target = $(target);
          $target.focus();
          if ($target.is(":focus")) { // Checking if the target was focused
            return false;
          } else {
            $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
            $target.focus(); // Set focus again
          };
        });
      }
    }
  });
$('.masthead')
  .visibility({
    once: false,
    onBottomPassed: function() {
      $('.fixed.menu').transition('fade in');
    },
    onBottomPassedReverse: function() {
      $('.fixed.menu').transition('fade out');
    }
  })
;
    $(".ui.small.modal")
      .modal({
        blurring: true,
      })
      .modal("setting", "transition", "vertical flip")
      .modal("setting", "closable", false)
      .modal("attach events", ".blue.button", "show")
    ;
    $(".ui.massive.violet.rating").rating({
      initialRating: 0,
      maxRating: 5,
      icon: "award",
      onRate: function(value) {
        $(this).rating("disable")
        $("body").toast({
          class: "success",
          title: value + " Award Ribbons!",
          showIcon: "thumbs up",
          displayTime: 3000,
          message: "Thanks for the " + value + " star rating!",
          position: "top right"
        });
      }
    });