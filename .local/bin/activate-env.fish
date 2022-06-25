set dir $HOME/repo

if test (count $argv) -gt 1
  echo "activate-env takes at most one argument"
  exit 2
end

set repo $argv[1]
if test -z $repo
  for folder in (ls $dir)
    [ (string match --regex "^$dir/$folder\$" "$PWD") ] && set repo $folder && break
  end
end

set env_path
if test "$repo" != ""
  set env_path "$dir/$repo/$repo-env"
else
  set name (basename $PWD)
  set env_path "$PWD/$name-env"
end

set activate_path "$env_path/bin/activate.fish"
if test -f $activate_path
  [ -n "$_OLD_FISH_PROMPT_OVERRIDE" ] && functions -c fish_prompt _old_fish_prompt
  source $activate_path
end
