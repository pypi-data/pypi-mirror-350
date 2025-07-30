#!/bin/bash

docker run \
       -it --rm \
       --memory=12g \
       --memory-swap=12g \
       --add-host=host.docker.internal:host-gateway \
       -v `pwd`:/codecraft \
       -v `pwd`/tmp.benchmarks/.:/benchmarks \
       -e OPENAI_API_KEY=$OPENAI_API_KEY \
       -e HISTFILE=/codecraft/.bash_history \
       -e PROMPT_COMMAND='history -a' \
       -e HISTCONTROL=ignoredups \
       -e HISTSIZE=10000 \
       -e HISTFILESIZE=20000 \
       -e CODECRAFT_DOCKER=1 \
       -e CODECRAFT_BENCHMARK_DIR=/benchmarks \
       codecraft-benchmark \
       bash
