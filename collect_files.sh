#!/bin/bash

# Проверка аргументов
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <input_dir> <output_dir> [--max_depth N]"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="$2"
MAX_DEPTH=""

# Обработка дополнительных аргументов
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

# Проверка существования директорий
if [ ! -d "$INPUT_DIR" ]; then
    echo "Input directory does not exist!"
    exit 1
fi

if [ ! -d "$OUTPUT_DIR" ]; then
    mkdir -p "$OUTPUT_DIR"
fi

# Поиск файлов
FIND_CMD=(find "$INPUT_DIR")
if [ -n "$MAX_DEPTH" ]; then
    FIND_CMD+=(-maxdepth "$MAX_DEPTH")
fi
FIND_CMD+=(-type f)

# Копирование файлов
for FILE_PATH in $("${FIND_CMD[@]}"); do
    FILE_NAME=$(basename "$FILE_PATH")
    DEST_FILE="$OUTPUT_DIR/$FILE_NAME"

    if [ ! -e "$DEST_FILE" ]; then
        cp "$FILE_PATH" "$DEST_FILE"
    else
        base="${FILE_NAME%.*}"
        ext="${FILE_NAME##*.}"
        if [ "$base" = "$ext" ]; then
            ext=""
        else
            ext=".$ext"
        fi

        i=1
        while [ -e "$OUTPUT_DIR/${base}${i}${ext}" ]; do
            ((i++))
        done
        cp "$FILE_PATH" "$OUTPUT_DIR/${base}${i}${ext}"
    fi
done
