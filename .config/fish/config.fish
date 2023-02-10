set __fish_git_prompt_show_informative_status
set __fish_git_prompt_showcolorhints

function fish_prompt
    set user_prompt (set_color -o)"$USER "(set_color normal)
    printf "$user_prompt"(set_color $fish_color_cwd; prompt_pwd)(set_color -o yellow)" \u0bb "(set_color normal)
end

function fish_right_prompt
    set last_pipestatus $pipestatus
    set pipestring (set_color red)" [$last_pipestatus]"
    if [ "$last_pipestatus" = 0 ]
        set pipestring ""
    end
    printf (fish_git_prompt)"$pipestring"
end

function fish_user_key_bindings
    bind \b backward-kill-word
    bind \e\[3\;5~ kill-word
end

fish_add_path $HOME/.local/bin/ $HOME/.sonar-scanner/bin/

set fish_greeting
set fish_color_command yellow
set fish_color_param "#55ffff"
set fish_prompt_pwd_dir_length 0

alias dotfiles-git="/usr/bin/git --git-dir=$HOME/.dotfiles_git/ --work-tree=$HOME"
alias activate-env=". $HOME/.local/bin/activate-env.fish"
alias creactivate-env="create-env && activate-env"
alias lord=". $HOME/.venv/lord/bin/activate.fish"
alias tf=terraform

activate-env

if status --is-login
    # bass source /etc/profile
    # bass source /etc/profile.d/*.sh

    set -gx XDG_CONFIG_HOME "$HOME/.config"
    set -gx XDG_CACHE_HOME "$HOME/.cache"
    set -gx XDG_DATA_HOME "$HOME/.local/share"
    set -gx XDG_STATE_HOME "$HOME/.local/state"

    set -gx XKB_DEFAULT_LAYOUT fr
    set -gx XKB_DEFAULT_VARIANT latin1

    set -gx MOZ_ENABLE_WAYLAND 1

    # set -gx LC_ALL en_US.UTF-8

    set -gx EDITOR nvim
    set -gx AUR_HELPER yay

    # set -gx MOUNT_CLOUD
    set -gx AUTH_PATH "$HOME/.auth"
    set -gx GOOGLE_APPLICATION_CREDENTIALS "$AUTH_PATH/google.json"
    set -gx GITLAB_API_TOKEN (cat "$AUTH_PATH/gitlab_api_token")
