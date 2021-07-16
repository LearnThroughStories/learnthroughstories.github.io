function Page() {
  var config = {
    $bookBlock: $("#bb-bookblock"),
    $bookName: null, // will fix in init
    $isAudioAvailable: false,
  };

  var oldau = null;
  var aualerted = false;

  var playAudio = function (old, page, isLimit) {
    if (isLimit || !config.$isAudioAvailable) {
      return;
    }

    var url = page <= 9 ? "0" + page : "" + page;
    url = "assets/audio/" + config.$bookName + "/" + url + ".mp3";
    var au = new Audio(url);
    au.addEventListener("canplaythrough", (event) => {
      stopAudio();
      au.play()
        .then(function () {
          oldau = au;
        })
        .catch(function (err) {
          if (!aualerted) {
            // alert("Please enable automatic audio play");
            aualerted = true;
          }
        });
    });
  }; // playAudio

  var afterFlip = function (old, page, isLimit) {
    if (isLimit && page > 0) {
        $("#end-of-sample").css({visibility: "visible"});
    } else {
      $("#end-of-sample").css({visibility: "hidden"});
    }
    playAudio(old, page, isLimit);
  }


  var stopAudio = function () {
    if (oldau) {
      oldau.pause();
      oldau = null;
    }
  };

  var init = function (bookname, isAudioAvailable) {
      config.$bookName = bookname;
      config.$isAudioAvailable = isAudioAvailable;
      config.$bookBlock.bookblock({
        speed: 300,
        shadowSides: 0.8,
        shadowFlip: 0.7,
        onEndFlip: afterFlip,
      });
      initEvents();
      stopAudio();
      if (isAudioAvailable) {
        playAudio(0, 0, false); // Cover page
      }
    },
    initEvents = function () {
      var $slides = config.$bookBlock.children();
      $slides.each(function (i) {
        this.onclick = function (e) {
          if (e.offsetX > e.target.width / 2) {
            config.$bookBlock.bookblock("next");
          } else {
            config.$bookBlock.bookblock("prev");
          }
        };
      });

      // add keyboard events
      $(document).keydown(function (e) {
        var keyCode = e.keyCode || e.which,
          arrow = {
            left: 37,
            up: 38,
            right: 39,
            down: 40,
          };

        switch (keyCode) {
          case arrow.left:
            config.$bookBlock.bookblock("prev");
            break;
          case arrow.right:
            config.$bookBlock.bookblock("next");
            break;
        }
      });
    };

  var close = function () {
    stopAudio();
    config = null;
  };
  return { init: init, close: close };
}

window.Page = Page;

/* Support for book popup */

function getViewportWidth() {
    return Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
}
function getViewportHeight() {
    return Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);

}
const template = `
<div id='bb-bookblock' class='bb-bookblock'>
    <div id="book-close" onclick="closeBook()"> &times;<\/div>
    <div id="end-of-sample">end of sample</div>
    <div class="bb-item"> <img src="assets/img/books/BOOKNAME/00.png" \/><\/div>
    <div class="bb-item"> <img src="assets/img/books/BOOKNAME/01.jpg" \/><\/div>
    <div class="bb-item"> <img src="assets/img/books/BOOKNAME/02.jpg" \/><\/div>
    <div class="bb-item"> <img src="assets/img/books/BOOKNAME/03.jpg" \/><\/div>
    <div class="bb-item"> <img src="assets/img/books/BOOKNAME/04.jpg" \/><\/div>
<\/div>
`

function openBook(bookname, isAudioAvailable) {
    const book_open = $("#book-open");
    book_open.css("display", "block");
    const html = template.replaceAll("BOOKNAME", bookname);
    book_open.append(html);
    const bb_bookblock = book_open.find("#bb-bookblock");
    if (getViewportWidth() < getViewportHeight()) {
        bb_bookblock.addClass("bb-vw");
    } else {
        bb_bookblock.addClass("bb-vh");
    }
    const page = Page();
    page.init(bookname, isAudioAvailable);
    book_open.find("#book-close").click(() => { closeBook(page) });
}

function closeBook(page) {
    page.close();
    const book_open = $("#book-open");
    book_open.css("display", "none");
    $("#book-open").empty();
}
