# Commands

## Build with Docker

```
#OLD: docker rm -f jekyll; docker run --rm --name jekyll -v $(pwd):/src -w /src -it cannin/jekyll:github-pages-3.6.0 bash
docker run --rm --volume="$PWD:/srv/jekyll" -it jekyll/jekyll:3.6.0 jekyll build
```

### Build
From: https://jekyllrb.com/docs/quickstart/

#### Development
```
jekyll build --config _config_dev.yml
```

#### Production
```
jekyll build
```

## Run with Docker (in _site folder)
```
docker rm -f site; docker run --rm --name site -p 8080:8080 -v=$(pwd):/src -w /src -t cannin/nodejs-http-server:0.10.25
```

## Run Site
```
docker run --restart=always --name landingPageJekyll -p 8088:8080 -v /home/ubuntu/landingPageJekyll:/src -w /src -t cannin/nodejs-http-server:0.10.25
```

# GitHub Pages Dependencies
https://pages.github.com/versions/

# rsync
```
rsync -vrtzave "ssh -i FULLPATH" --exclude "_config.yml" FULLPATH/_site/* USER@HOST:PATH
```