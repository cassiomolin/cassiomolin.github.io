This is the source code of my personal website, deployed on GitHub Pages.

## Developing locally

Install package:

```shell
$ npm --prefix themes/windy install themes/windy
```

In a terminal window, start the Tailwind CLI build process:

```shell
$ npm run --prefix themes/windy start:tailwindcss
```

In a _different_ terminal window, start the Hugo webserver:

```shell
$ hugo serve --bind=0.0.0.0 --buildDrafts --minify
```