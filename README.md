This is the source code of my personal website, deployed on GitHub Pages.

## Developing locally

In a terminal window, start the Tailwind CLI build process:

```shell
$ npm run --prefix themes/windy start:tailwindcss
```

In a _different terminal window_, start the Hugo webserver:

```shell
$ hugo serve --bind=0.0.0.0 --buildDrafts --minify
```