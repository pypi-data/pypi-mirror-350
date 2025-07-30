#! /usr/bin/env bash

function bluer_ai_wifi_copy_to_sd_card() {
    cp -v \
        $ABCLI_PATH_IGNORE/wpa_supplicant.conf \
        /Volumes/boot/
}
