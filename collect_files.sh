#!/bin/bash

# Проверка аргументов
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

FIND_CMD=(find "$INPUT_DIR" -type f)

while IFS= read -r FILE_PATH; do
    REL_PATH="${FILE_PATH#$INPUT_DIR/}"

    if [ -n "$MAX_DEPTH" ]; then
        # Папочная часть + имя файла
        DIR_PATH=$(dirname "$REL_PATH")
        FILE_NAME=$(basename "$REL_PATH")

        # Разделить папки
        IFS='/' read -r -a DIR_PARTS <<< "$DIR_PATH"
        DIR_PARTS_LEN=${#DIR_PARTS[@]}

        if [ "$DIR_PARTS_LEN" -ge "$MAX_DEPTH" ]; then
            # Оставить только первые max_depth-1 уровней (каталоги) + положить туда файл
            TRIMMED_DIR=$(IFS='/'; echo "${DIR_PARTS[*]:0:MAX_DEPTH-1}")
            REL_PATH="$TRIMMED_DIR/$FILE_NAME"
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
