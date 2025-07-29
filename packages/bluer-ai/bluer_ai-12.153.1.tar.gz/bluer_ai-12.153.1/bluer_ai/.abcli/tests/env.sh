#! /usr/bin/env bash

function test_bluer_ai_env() {
    bluer_ai env
    bluer_ai env path

    bluer_ai env dot cat config
    bluer_ai env dot cat
    bluer_ai env dot cat nurah

    bluer_ai env dot get TBD

    bluer_ai env dot list
}
