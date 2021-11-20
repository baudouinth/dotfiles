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
    printf (set_color yellow; fish_git_prompt)"$pipestring"
end

fish_add_path $HOME/bin/
set fish_greeting
set fish_color_command yellow
set fish_color_param "#55ffff"
set fish_prompt_pwd_dir_length 0

# function find -w find
#     /bin/find $argv -type d \( -name proc \) -prune
# end

export GOOGLE_APPLICATION_CREDENTIALS="/home/baudouin/.auth/google.json"
export AUTH_PATH="/home/baudouin/.auth"

alias dotfiles-git="/usr/bin/git --git-dir=$HOME/.dotfiles_git/ --work-tree=$HOME"
alias activate-env=". /home/baudouin/bin/activate-env.fish"
alias creactivate-env="create-env && activate-env"

activate-env
