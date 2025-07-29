#!/bin/bash

# exit when any command fails
set -e

if [ -z "$1" ]; then
  ARG=-r
else
  ARG=$1
fi

if [ "$ARG" != "--check" ]; then
  tail -1000 ~/.codecraft/analytics.jsonl > codecraft/website/assets/sample-analytics.jsonl
  cog -r codecraft/website/docs/faq.md
fi

# README.md before index.md, because index.md uses cog to include README.md
cog $ARG \
    README.md \
    codecraft/website/index.html \
    codecraft/website/HISTORY.md \
    codecraft/website/docs/usage/commands.md \
    codecraft/website/docs/languages.md \
    codecraft/website/docs/config/dotenv.md \
    codecraft/website/docs/config/options.md \
    codecraft/website/docs/config/codecraft_conf.md \
    codecraft/website/docs/config/adv-model-settings.md \
    codecraft/website/docs/config/model-aliases.md \
    codecraft/website/docs/leaderboards/index.md \
    codecraft/website/docs/leaderboards/edit.md \
    codecraft/website/docs/leaderboards/refactor.md \
    codecraft/website/docs/llms/other.md \
    codecraft/website/docs/more/infinite-output.md \
    codecraft/website/docs/legal/privacy.md
