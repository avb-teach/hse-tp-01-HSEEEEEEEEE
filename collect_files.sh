#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <input_dir> <output_dir> [--max_depth N]"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
MAX_DEPTH=""

shift 2
while [[ $# -gt 0 ]]; do
    case $1 in
        --max_depth)
            MAX_DEPTH="$2"
            shift 2
            ;;
        *)
            echo "Unknown parameter: $1"
            exit 1
            ;;
    esac
done

if [ ! -d "$INPUT_DIR" ]; then
    echo "Input directory does not exist!"
    exit 1
fi

if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

FIND_CMD=(find "$INPUT_DIR")
if [ -n "$MAX_DEPTH" ]; then
    FIND_CMD+=(-mindepth 1)
fi
FIND_CMD+=(-type f)

while IFS= read -r FILE_PATH; do
    REL_PATH="${FILE_PATH#$INPUT_DIR/}"

    if [ -n "$MAX_DEPTH" ]; then
        # Считаем глубину файла
        DEPTH=$(echo "$REL_PATH" | grep -o "/" | wc -l)
        
        if [ "$DEPTH" -ge "$MAX_DEPTH" ]; then
            # Обрезаем путь до max_depth
            TRIMMED_PATH=$(echo "$REL_PATH" | awk -F'/' -v maxd="$MAX_DEPTH" '{out=$1; for (i=2;i<=maxd;i++) out=out"/"$i; print out}')
            REL_PATH="$TRIMMED_PATH"
        fi
    fi

    DEST_PATH="$OUTPUT_DIR/$REL_PATH"
    mkdir -p "$(dirname "$DEST_PATH")"

    if [ ! -e "$DEST_PATH" ]; then
        cp "$FILE_PATH" "$DEST_PATH"
    else
        base="${DEST_PATH%.*}"
        ext="${DEST_PATH##*.}"
        if [ "$base" = "$ext" ]; then
            ext=""
        else
            ext=".$ext"
        fi

        i=1
        while [ -e "${base}${i}${ext}" ]; do
            ((i++))
        done
        cp "$FILE_PATH" "${base}${i}${ext}"
    fi
done < <("${FIND_CMD[@]}")
