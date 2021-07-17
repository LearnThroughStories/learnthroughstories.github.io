# Internals Documentation for the LeTS website

by Sriram Srinivasan (_firstname_@malhar.net)

## index.html

HTML/CSS is designed around a block model. In its simplest design, responsive design depends on blocks moving around, the way sentences adjust and words move to the next line when the window width is reduced. However, we wanted to avoid the blocky look-and-feel;  We wanted a more organic feel where the artwork is not seemingly restricted to one block. At the same time, the design had to be responsive.

The current design (at the time of release, July 15, 2021) is as follows. The artwork is a one large  composite image that is pegged to 100% width (and auto height, to preserve aspect ratio). The various text elements are positioned with "absolute" positioning and sizing (top%, left%) on this artwork, and given as much width and height as the space on the artwork would allow for the text to expand into, without the text bleeding into the next block.

The artwork is a foreground image (&lt;img&gt;), not a background-image property, because we need the image to force the size of the container. The background-image property makes the image passive, and attempts to make do with whatever space is available to it. For this reason, all other components must have an explicit `z-index` greater than 1.

This scheme is responsive because the dimensional dependencies are as follows (read the arrow as "dictates")

    Width of browser window  -> 
       width of artwork  -> 
         height of artwork (in accordance with aspect ratio) ->
           height of the container, since the container is sized to contain the image ->
              width and height of each text block, as they are expressed as percentages 
              of the container's corresponding dimensions. 

When the window shrinks in width, everything adjusts proportionally.

Each text block has the following form:

      <div id="intro-text-wrapper" class="text-wrapper">
         <div class="text-center">
            <div class="body-text">

The _xxx_-text-wrapper contains the position and size of that particular block. In general, the `text-wrapper` class contains all the generic properties of all such absolutely positioned units. The `text-center` class is meant to center the text vertically in the allotted height, and be a scroll container for the contained body-text.

## books.html

The books animation relies on BookBlock (https://tympanus.net/codrops/2012/09/03/bookblock-a-content-flip-plugin/), a somewhat fragile library.

The thumbnails of the books are placed in a standard css grid using areas, in two configurations, small and large, as appropriate for the screen width.

The openBook() function in lets.js adds a bb-bookblock div as a popup only after the thumbnail has been clicked. This way the larger-sized images for a given book are loaded only on demand.

## gallery.html

The gallery is a simple application of the nanogallery package (http://nanogallery2.nanostudio.org). To avoid typing/copying a whole lot of html boiler plate, I have used `scripts/items.py` to convert `assets/img/gallery/descriptions.txt` the html format required. That way gallery images and descriptions are kept simple and in sync.

Also, to experiment with different mosaic layout designs, the script `table2mosaic.py` helps one to convert the mosaic drawn on https://www.tablesgenerator.com/text_tables to the relevant mosaic format expected by nanogallery. 

## aboutus.html

For the animation on the top of the page, I couldn't find a single carousel or image slider library that worked the way I wanted. Some were not responsive, most page-oriented ones are unwilling to show a partial image and so on, so I wrote my own simple slider that explicitly scrolls the container, without showing the scrollbar. I hid the scrollbar by setting its width to 0.

# Lessons learnt

The first three are specific to the front page (index.html)
1. Text and art shrink congruently.

   This is a problem because text must be legible and in proportion to what the viewer expects out of that device. The artwork has no such restriction. We found that what is legible and appropriate on a desktop (16pt font, say) shrinks too much on the smaller mobiles, if it is to be kept congruent to the artwork. Experiments with a smooth but legible shrinkage (using calc) to compute font sizes were not successful, so I introduced media queries and stepped the font-size (of the html element) down in discrete units.

   Still, this asymmetry has caused a lot of problems. At smaller font-sizes, the available width cannot always be used, because longer words are moved to the next sentence (without hyphenation).This induces scrolling, with ugly scroll bars on small pieces of text (since the height is constrained). The final solution is to auto-hide the scrollbar, and introduce a "scroll indicator" -- a semi-transparent gray band at the bottom of each text box, whenever there is more content than is visible. This forces the viewer to subtly force the viewer to scroll up to uncover the text. Ideally, text should be unfettered in the vertical direction, but that is not an option in our scheme, because the artwork dictates the placement. This problem is only on small screens; given the amount of text currently on the front page, scroll indicators should not appear on larger screens or larger mobiles.

2. While the artwork has a fixed aspect ratio, what is designed for a desktop isn't appropriate for a slim mobile, esp. when text has to fit in the interstitial spaces. This makes the design fragile. For example, we find ourselves writing "kids" instead of "children" to  avoid scrollbars. In the future, artwork must be done separately for desktop and mobile layouts keeping the flow of text in mind. Preferably, do the mobile design first. 

3. The artwork jpg file is huge, which slows down the website. A light background image (like a paper texture) compresses better because it is not meant to stand out, and hence compresses 10x better. Regardless, the site is extraordinarily image heavy and relies on very good network accessibility. This may be ok for the primarily urban target audience.

4. Hosting on github.io has been very convenient. It is surprisingly fast, because it defers to fastly's servers and CMS. There are a few downsides though. github keeps the cache expiry time as 10min. Also, because it is a git site, I didn't feel like polluting the source with the distribution variant, to do standard performance-oriented things such as tree-shaking, code minifying and bundling commonly clustered pieces of code together. Also, since it is a static site, all common code gets duplicated (like header and footer). 

5. It is best to constrain `img` elements `div`s to constrain them. That way, images can be set to 100% the width of their wrapper and the height can either be constrained using object-fit:contain or height:auto to maintain their aspect ratio. This permits the the wrapper to be sized independently.

6. In some cases (the bio pics in about us), there is one way to ensure that the `div` surrounding the `img` has the exact aspect ratio as the underlying image. We want the div to be responsive to changes to its parent, but maintain the same aspect ratio as its contained image. We use the property that padding-top/bottom is a function of the *width*. So, we set the height of the div to 0, but the padding-top to be the appropriate fraction of the width. For example, `padding-top:50%` makes the element half as tall as the width. This div has not content of its own; its sole purpose is to act as a frame for a nested div. The latter is positioned in absolute terms, and is thus responsive as well. This trick is from https://css-tricks.com/aspect-ratio-boxes/

7. At the time of release, I hadn't paid particular attention to image resolution, and had resized all thumbnails as 200x200, which was a mistake. On retina displays, some images are blurry.

8. Having to position an image on top of a background-image is painful and expensive. Suppose the background image is a watercolour wash. On top of this we want to show an image of a person. But suppose the background of this image clashes with the underlying watercolour wash. We have no option but to eliminate the background. That is, we have to cut and extract the person out of the image on top, save it as a png file and overlay on the page background.  The png format is needed for its support of transparent pixels. Unfortunately, the png format is lossless, so the files are huge (10x). We can't merge the png file into the background because we want the top images to move fluidly with the text. I experimented with AVIF files (which supports lossy compression and transparent pixels), but the results were not very good and the format AVIF is not supported sufficiently by most mainstream browsers yet, so I deferred this decision with the aim of revisiting it soon. 


# Performance

These are the steps taken to ensure pages load fast, in spite of being such an image-heavy site.

1. **Split artwork**. On the landing page, the artwork was split into two images so that the top section can be shown as fast as possible, and the bottom section can be loaded a split second later, while the first-time viewer is digesting the top part. It didn't seem worth it to further slice the image.

2. **Image compression**. All jpg's were sent through http://squoosh.app with 65% quality, and all png's through tinypng.com. This results in up to 90% reduction in size.

3. **Multiple sizes/formats**.  `picture` elements were used instead of `<img>` with choices of 900px vs 1200px wide artwork, and `.webp` and `.jpg` formats for both sizes. `webp` saves about 20-30% and is well-supported.

4. **Font subsetting**. The Hepta Slab fonts work out to a total of 700k, but we only use the Latin subset of it, so why pay the price of loading other languages and glyphs? I used `pyftsubset` to extract only the glyphs I needed, compressing it by 8x. But alas, it introduced strange artifacts. So I used googlefonts to do some amount of subsetting for me. It is still a 6x compression, not as much as what I'd like, but good enough.

    a. The link that googlefonts gives to download fonts points to a css file. Download it. This file has many entries of the form: 

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

    b. Download the woff2 file from each of the URLs under the sections named Latin. There should be one for each font-weight. These are the lean fonts in the `fonts/` directory.

6. **Image dimensions in html**. Specifying the height and width of the image in the html allows the browser to decide the placement of the absolute-ly placed elements even before the artwork is done loading. However, to ensure that the image is responsively sized, there is a css rule that constrains the width to 100% and height to auto. (see the .bg-img rule in base.css). This way, we get to tell the browser the aspect ratio of the image.

7. **Lazy loading**: On the front page, all the youtube videos and the book animations are "below the fold" in newspaper-speak, in the bottom half. Therefore, the corresponding scripts are lazily loaded once the bottom section's image has been loaded (search for `loadLazy` in index.html). The actual youtube embedding and book animations are further deferred, until they are triggered by a click on a transparent div.

8.  **Style subsetting**: There is one css file per html page for rules that apply only to that page Common elements (such as font spec, menu and footer and media queries) are part of base.css. 

9.  **Social media icons as fonts**:  I used fontello.com to create a custom font with glyphs for the social media sites, and the play/pause button for animations on the about us page.

# Resources

These resources were particularly helpful:

1. Chrome dev tools. Great for Grid/flexbox options, absolute positioning interactively. Lighthouse is great for local performance testing.

2. W3 HTML validator (https://validator.w3.org). Often strange html behaviour is due to ill-formed html source.

3. Google pagespeed, for lighthouse perf testing by remote servers

4. Kevin Powell's free course on responsive design, and his other tutorials.

5. "Image optimization", book by Addy Osmani. 

6. css-tricks.com and smashing-magazine for innumerable css/html tips.

