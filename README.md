# Running instructions

This README is a reference to the steps in this link [here](https://programminghistorian.org/en/lessons/building-static-sites-with-jekyll-github-pages#installing-dependencies-). 

You'll need to work with ruby and jekyll -

First, install `ruby` -
```bash
brew install ruby

```

You then need `rubygems`

```bash
gem install rubygems-update
```

At this point if you get an error, put the following lines in your `~/.zshrc`

```zsh
export GEM_HOME=$HOME/gems
export PATH=$HOME/gems/bin:$PATH
```
and remember to run `source ~/.zshrc`

You then need Node and Jekyll

```zsh
brew install node
gem install jekyll
```
Now you can start running your website locally.

## Changing code syntax highlighting
Following this link [here](https://dqdongg.com/blog/2018/12/22/Blog-rouge.html). 

1. In your `_config.yaml`, since you're using kramdown, make sure `syntax_highlighter: rouge`. 
2. Make sure you have the rouge gem installed.
3. Generate the css file using `rougify style monokai.sublime > assets/css/syntax.css`. To look at the available styles, look at the outupt of `rougify help style`, it will be

```bash
base16, 
base16.dark, 
base16.monokai, 
base16.monokai.light, 
base16.solarized, 
base16.solarized.dark, 
colorful, 
github, 
gruvbox, 
gruvbox.light, 
molokai, 
monokai, 
monokai.sublime, 
thankful_eyes
```
4. Create a css file like `rougify style monokai.sublime > assets/css/syntax.css`
5. In your `posts.html` under `_layouts`, make sure you add `<link rel="stylesheet" href="/assets/css/syntax.css" type="text/css" />` for the changes to take effect.
6. To enable line numbering, simple thing to do is to add it to your `_config.yml` like the following:

```bash
kramdown:
  input: GFM
  syntax_highlighter: rouge
  syntax_highlighter_opts:
    default_lang: html
    css_class   : 'syntax'
    block:
      line_numbers: true
      start_line: 1

```

## Running the website locally

When you get to this step `bundle exec jekyll serve --watch` to run Jekyll locally, you might get some errors about `bundler` versions, but they will tell you what to do. In the case on a new laptop, I had to run the following commands - 

```
sudo gem install bundler:1.17.3
```
and then 

```
bundle _1.17.3_ update
```
After running these, `bundle exec jekyll serve --watch` will work.
# Forty - Jekyll Theme

Will this  change show up? 

A Jekyll version of the "Forty" theme by [HTML5 UP](https://html5up.net/).  

![Forty Theme](assets/images/forty.jpg "Forty Theme")

# How to Use

For those unfamiliar with how Jekyll works, check out [jekyllrb.com](https://jekyllrb.com/) for all the details, 
or read up on just the basics of [front matter](https://jekyllrb.com/docs/frontmatter/), [writing posts](https://jekyllrb.com/docs/posts/), 
and [creating pages](https://jekyllrb.com/docs/pages/).

- **GitLab**: Simply fork this repository and start editing the `_config.yml` file!  
- **GitHub**: Fork this repository and create a branch named `gh-pages`, then start editing the `_config.yml` file.

# Added Features

* **[Formspree.io](https://formspree.io/) contact form integration** - just add your email to the `_config.yml` and it works!
* Use `_config.yml` to **set whether the homepage tiles should pull pages or posts**, as well as how many to display.
* Add your **social profiles** easily in `_config.yml`. Only social profiles buttons you enter in `config.yml` show up on the site footer!
* Set **featured images** in front matter.

# Issues

If you would like to report a bug, ask a question, request a feature, feel free to do so on [the GitLab repository](https://gitlab.com/andrewbanchich/forty-jekyll-theme) and I will be more than happy to help!

Alternatively, you can open an issue via email by emailing [incoming+andrewbanchich/forty-jekyll-theme@incoming.gitlab.com](mailto:incoming+andrewbanchich/forty-jekyll-theme@incoming.gitlab.com).

The GitHub repository is simply a mirror of the GitLab repository.

# Credits

Original README from HTML5 UP:

```
Forty by HTML5 UP
html5up.net | @ajlkn
Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)


This is Forty, my latest and greatest addition to HTML5 UP and, per its incredibly
creative name, my 40th (woohoo)! It's built around a grid of "image tiles" that are
set up to smoothly transition to secondary landing pages (for which a separate page
template is provided), and includes a number of neat effects (check out the menu!),
extra features, and all the usual stuff you'd expect. Hope you dig it!

Demo images* courtesy of Unsplash, a radtastic collection of CC0 (public domain) images
you can use for pretty much whatever.

(* = not included)

AJ
aj@lkn.io | @ajlkn


Credits:

	Demo Images:
		Unsplash (unsplash.com)

	Icons:
		Font Awesome (fortawesome.github.com/Font-Awesome)

	Other:
		jQuery (jquery.com)
		html5shiv.js (@afarkas @jdalton @jon_neal @rem)
		background-size polyfill (github.com/louisremi)
		Misc. Sass functions (@HugoGiraudel)
		Respond.js (j.mp/respondjs)
		Skel (skel.io)
```

Repository [Jekyll logo](https://github.com/jekyll/brand) icon licensed under a [Creative Commons Attribution 4.0 International License](http://choosealicense.com/licenses/cc-by-4.0/).
