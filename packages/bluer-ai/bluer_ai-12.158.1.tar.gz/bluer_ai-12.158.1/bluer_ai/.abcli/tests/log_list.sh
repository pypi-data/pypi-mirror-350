#! /usr/bin/env bash

function test_bluer_ai_log_list() {
    bluer_ai_log_list this+that \
        --before "list of" \
        --delim + \
        --after "important thing(s)"

    bluer_ai_log_list "this that" \
        --before "list of" \
        --delim space \
        --after "important thing(s)"

    bluer_ai_log_list "this,that" \
        --before "list of" \
        --delim , \
        --after "important thing(s)"

    bluer_ai_log_list this,that
}
