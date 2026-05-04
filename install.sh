#!/usr/bin/env bash
set -e

BACKEND="cpu"
SERVER=false

for arg in "$@"; do
    case "$arg" in
        --server) SERVER=true ;;
        cpu|cu118|cu121|cu122|metal) BACKEND="$arg" ;;
    esac
done

INDEX_URL="https://abetlen.github.io/llama-cpp-python/whl/$BACKEND"
EXTRAS=""
if $SERVER; then
    EXTRAS="[server]"
fi

echo "Instalando gemma-talker con backend: $BACKEND${SERVER:+ (+ server)}"
pipx install -e ".$EXTRAS" --pip-args="--extra-index-url $INDEX_URL"
