#! /usr/bin/env bash

function bluer_ai_refresh_branch_and_version() {
    export bluer_ai_version=$(python3 -c "import bluer_ai; print(bluer_ai.VERSION)")

    export bluer_ai_git_branch=$(bluer_ai_git bluer-ai get_branch)

    export abcli_fullname=bluer_ai-$bluer_ai_version.$bluer_ai_git_branch
}

# internal function for bluer_ai_seed.
function bluer_ai_seed_git() {
    # seed is NOT local
    local user_email=$(git config --global user.email)
    seed="${seed}git config --global user.email \"$user_email\"$delim"

    local user_name=$(git config --global user.name)
    seed="${seed}git config --global user.name \"$user_name\"$delim_section"

    pushd $abcli_path_git >/dev/null
    local repo_name
    for repo_name in $(ls -d */); do
        [[ ! -d "./$repo_name/.git" ]] && continue

        repo_name="${repo_name%/}"

        pushd $repo_name >/dev/null

        local branch_name=$(bluer_ai_git get_branch)
        seed="${seed}bluer_ai_git $repo_name checkout $branch_name$delim"

        popd >/dev/null
    done
    popd >/dev/null
}
