# global history
function prompt_command {
  history 1 >> ~/.bash_history_global
}
export PROMPT_COMMAND=prompt_command

# search in global history
function hs {
  grep_cmd="egrep ."
  for i in "$@"; do
    grep_cmd="$grep_cmd | egrep $i"
  done
  cat ~/.bash_history_global | eval "$grep_cmd"
}
