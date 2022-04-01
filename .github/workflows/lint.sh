#!/bin/sh

# Shell script to format PyLint's messages to something that GitHub's
# Workflow runners can understand.

msg_template="::{category} file={path},line={line}\
,col={column},title={msg_id}::{msg}"

pylint --recursive=y . --msg-template="$msg_template" \
    | sed -re 's/convention|information|refactor/notice/i' \
    | sed -re 's/fatal/error/i'
