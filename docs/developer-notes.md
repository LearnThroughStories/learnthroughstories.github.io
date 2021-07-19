# Internals Documentation for the LeTS website

by Sriram Srinivasan (_firstname_@malhar.net)

## index.html

HTML/CSS is designed around a block model. Responsive or fluid design is essentially a way for blocks to move around. Blocks (like images, or groups of elements) are like words in a sentence; they jostle for space on a line and move down vertically when the window is shrunk.

Unfortunately, it also lends a blocky look-and-feel to the site. We wanted a more organic feel where the artwork is not seemingly restricted to one block.  At the same time, the design had to be responsive.

The current design (at the time of release, July 15, 2021) is as follows. The artwork is a single large  composite image that is pegged to 100% width (and auto height, to preserve aspect ratio). On this canvas, the various text elements are positioned with "absolute" positioning and sizing (top%, left%) on this artwork, and given as much width and height as the space on the artwork would allow for the text to expand into, without the text bleeding into the next block.

The artwork is a foreground image `<img>`, not a `background-image` property on the containing div. Using background-image property makes the image passive; it makes do with whatever space is available to it. Instead, if the image is foregrounded, it enlarges the container to its own size.  The other components are layered on top (`z-index` greater than 1). 

The scheme is responsive because the dimensional dependencies are as follows (read the arrow as "dictates")

    Width of browser window  -> 
       width of artwork  -> 
         height of artwork (in accordance with aspect ratio) ->
           height of the container, since the container is sized to contain the image ->
              width and height of each text block, as they are expressed as percentages 
              of the container's corresponding dimensions. 

When the window shrinks in width, the artwork shrinks proportionally, and everything else atop does too.

Each text block has the following form:
      <div id="intro-text-wrapper" class="text-wrapper">
         <div class="text-center">
            <div class="body-text">

The _xxx_-text-wrapper contains the position and size of that particular block, and the `text-wrapper` class contains the properties common to all such absolutely positioned units. The `text-center` class is meant to center the text vertically in the allotted height, and be a scroll container for the contained body-text.

## books.html

The books' page flppping animation relies on BookBlock (https://tympanus.net/codrops/2012/09/03/bookblock-a-content-flip-plugin/), a somewhat fragile library.

The thumbnails of the books on the books page are placed in a standard css grid using grid-areas, in two configurations, small and large, as appropriate for the screen width.

The openBook() function in lets.js adds a bb-bookblock div as a popup only after the thumbnail has been clicked. This way the larger-sized images for a given book are loaded only on demand.

## gallery.html

The gallery is a simple application of the nanogallery package (http://nanogallery2.nanostudio.org). To avoid typing or copying a whole lot of html boiler plate, I have used the script `scripts/items.py` to convert `assets/img/gallery/descriptions.txt` to the html format required by nanogallery. In other words, most of `gallery.html` is auto-generated from `descriptions.text`. That way gallery images and descriptions are kept simple and in sync.

Further, to experiment with different mosaic layout designs, I wrote `scripts/table2mosaic.py` to convert a visual representation of the mosaic to the format required by nanogallery. The visual representation is provided by https://www.tablesgenerator.com/text_tables. 

## aboutus.html

For the animation on the top of the page, I couldn't find a single carousel or image slider library that worked the way I wanted. Some were not responsive, most page-oriented ones are unwilling to show a partial image and so on, so I wrote my own simple slider that explicitly scrolls the container, without showing the scrollbar. I hid the scrollbar by setting its width to 0.

# Lessons learnt

The first three are specific to the front page (index.html)
1. Text and art shrink congruently.

   This is a problem because text must be legible and in proportion to what the viewer expects out of that device. The artwork has no such restriction. We found that what is legible and appropriate on a desktop (16pt font, say) shrinks too much on the smaller mobiles, if it is to be kept congruent to the artwork. Experiments with a smooth but legible shrinkage (using calc) to compute font sizes were not successful, so I introduced media queries and stepped the font-size (of the html element) down in discrete units.

   Still, this asymmetry has caused a lot of problems. At smaller font-sizes, the available width cannot always be used, because longer words are moved to the next sentence (without hyphenation).This induces scrolling, with ugly scroll bars on small pieces of text (since the height is constrained). The final solution is to auto-hide the scrollbar, and introduce a "scroll indicator" -- a semi-transparent gray band at the bottom of each text box, whenever there is more content than is visible. This forces the viewer to subtly force the viewer to scroll up to uncover the text. Ideally, text should be unfettered in the vertical direction, but that is not an option in our scheme, because the artwork dictates the placement. This problem is only on small screens; given the amount of text currently on the front page, scroll indicators should not appear on larger screens or larger mobiles.

2. While the artwork has a fixed aspect ratio, what is designed for a desktop isn't appropriate for a slim mobile, esp. when text has to fit in the interstitial spaces. This makes the design fragile. For example, we find ourselves writing "kids" instead of "children" to  avoid scrollbars. In the future, artwork must be done separately for desktop and mobile layouts keeping the flow of text in mind. Preferably, do the mobile design first. 

3. The artwork jpg file is huge, which slows down the website. A light background image (like a paper texture) compresses better because it is not meant to stand out, and hence compresses 10x better. Regardless, the site is extraordinarily image heavy and relies on very good network accessibility. This may be ok for the primarily urban target audience.

4. Hosting on github.io has been very convenient. It is surprisingly fast, because it defers to fastly's servers and CMS. There are a few downsides though. Github keeps the cache expiry time at a paltry 10 min, so heavy resources are constantly being reloaded. Also, because it is a git site, I didn't feel like polluting the source with the distribution variant, to do standard performance-oriented things such as tree-shaking, code minifying and bundling commonly clustered pieces of code together. Finally, since it is a static site, all common code gets duplicated (like header and footer). 

5. It is best to place `img` elements within `div`s so that the img style can worry about preserving its aspect ration (either width:100% height:auto, or object-fit:contain}, while the wrapper div can worry about creating sufficient room for the image, independent of aspect ratio. Also, the image can be replaced with a `picture` element in the future, without having to worry about positioning etc.

6. In some cases, the outer div has to worry about aspect ratio too, so that it can tightly wrap around the image. In the absence of popular support for the `aspect-ratio` property, I borrowed an ugly trick from https://css-tricks.com/aspect-ratio-boxes/. The problem is this. How does one constrain width given height, or vice-versa, to a specific aspect ratio, while still keeping the design fluid (that is, no hard-coding of widths/heights in absolute terms)? We cannot use percentage, because width% is a fraction of the container's width and height% is a fraction of the container's height, which means the element is at the mercy of the container's aspect ratio. The solution is to use 
the padding-top/bottom%, which although along the 'y' axis, is a function of the *width*!  This way we can dictate the x and y dimensions both as a function of width. But since padding only pushes the content down, we have the following nested div arrangement. Say we need a 2:1 aspect ratio (width 2x of height)

     frame (outer div).style=  width:100%; height:0; padding-top:50%; position:relative
        (inner div).style = "width: 100%; height: 100%; top=left=0; position:absolute"
             <img ...>

We create an outer frame, whose sole purpose is to provide an appropriately proportioned div. Note that its height comes from the padding property, not its height.  The inner div then latches on to the outer using absolute positioning. Shudder!

7. At the time of release, I hadn't paid particular attention to image resolution, and had resized all thumbnails as 200x200, which was a mistake. On retina displays, some images are blurry. This should be fixed soon.

8. Having to position an image on top of a background-image is painful and expensive. Suppose the background image is a watercolour wash. On top of this we want to show an image of a person. But suppose the background of this person image clashes with the underlying watercolour wash. We have no option but to eliminate the background. That is, we have to cut and extract the person out of the image on top, save it as a png file and overlay on the page background.  The png format is needed for its support of transparent pixels. Unfortunately, the png format is lossless, which makes the files huge (10x of what a jpg could be). We can't merge the png file into the background because we want the top images to move fluidly with the text. I experimented with AVIF files (which supports lossy compression and transparent pixels), but the results were not very good and the format is not supported sufficiently yet by most mainstream browsers, so I deferred this decision with the aim of revisiting it soon. 


# Performance

These are the steps taken to ensure pages load fast, in spite of the site being so image-heavy.

1. **Split artwork**. On the landing page, the artwork was split into two images so that the top section can be shown as fast as possible, and the bottom section can be loaded a split second later, while the first-time viewer is digesting the top part. It didn't seem worth it to further slice the image.

2. **Image compression**. All jpg's were sent through http://squoosh.app with 65% quality, and all png's through tinypng.com. This results in up to 90% reduction in size.

3. **Multiple sizes/formats**.  `picture` elements were used instead of `<img>` with choices of 900px vs 1200px wide artwork, and `.webp` and `.jpg` formats for both sizes. `webp` saves about 20-30% and is well-supported.

4. **Font subsetting**. The Hepta Slab fonts work out to a total of 700k, but we only use the Latin subset of it, so why pay the price of loading other languages and glyphs? I used `pyftsubset` to extract only the glyphs I needed, compressing it by 8x. But alas, it introduced strange artifacts. So I used googlefonts to do some amount of subsetting for me. It is still a 6x compression, not as much as what I'd like, but good enough.

    a. The link given by googlefonts (after selecting one or more styles) refers to a css file. Download it. This file has many entries of the form: 

    ```
    /* latin */
    @font-face {
        font-family: 'Hepta Slab';
        font-style: normal;
        font-weight: 400;
        src: url(https://fonts.gstatic.com/s/heptaslab/v9/ea8cadoyU_jkHdalebHv42llhHCXA3A.woff2) format('woff2');
       unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+2074, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD;
    }
    ```

    b. Download the woff2 file from each of the URLs under the sections named Latin. There should be one for each requested font-weight. Ignore the woff2 URLs for the other sections I have saved the latin subset as lean* fonts in the `fonts/` directory. 

6. **Image dimensions in html**. Specifying the height and width of the image in the html allows the browser to decide the placement of the absolute-ly placed elements even before the artwork is done loading. However, to ensure that the image is responsively sized, there is a css rule that constrains the width to 100% and height to auto. (see the `.bg-img` rule in `assets/css/base.css`). This way, we get to tell the browser the aspect ratio of the image.

7. **Lazy loading**: On the front page, all the youtube videos and the book animations are "below the fold" in newspaper-speak, in the bottom half, that is. Therefore, the corresponding scripts are lazily loaded once the bottom section's image has been loaded (search for `loadLazy` in index.html). The actual youtube embedding and book animations are further deferred, until they are triggered by a click on a transparent div.

8.  **Style subsetting**: There is one css file per html page for rules that apply only to that page Common elements (such as font spec, menu and footer and media queries) are part of base.css. 

9.  **Social media icons as fonts**:  I used fontello.com to create a custom font with glyphs for the social media sites, and the play/pause button for animations on the about us page.

10 **Local web server**.  In some cases, one cannot directly open an html file. For example, aboutus.html uses default-bg.jpg as a background image, specified in the style. This bg file cannot be loaded. So I use the following to load a simple web server that serves files to the browser. 

     python3 -m http.server

On the browser type :   `http://localhost:8000/index.html`. 

# Resources

These resources were particularly helpful:

1. Chrome dev tools. Great for Grid/flexbox options, and for interactive positioning and sizing. Lighthouse is great for local performance testing. 

2. W3 HTML validator (https://validator.w3.org). Often strange html behaviour is due to ill-formed html source.

3. Google pagespeed, for lighthouse perf testing by remote servers

4. Kevin Powell's free course on responsive design, and his other tutorials.

5. "Image optimization", book by Addy Osmani. 

6. css-tricks.com and smashing-magazine for innumerable css/html tips.

