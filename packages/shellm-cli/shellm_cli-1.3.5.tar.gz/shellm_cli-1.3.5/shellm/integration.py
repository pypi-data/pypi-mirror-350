bash_integration = """
# Shell-GPT integration BASH v0.2
_shellm_bash() {
if [[ -n "$READLINE_LINE" ]]; then
    READLINE_LINE=$(shellm --shell <<< "$READLINE_LINE" --no-interaction)
    READLINE_POINT=${#READLINE_LINE}
fi
}
bind -x '"\\C-l": _shellm_bash'
# Shell-GPT integration BASH v0.2
"""

zsh_integration = """
# Shell-GPT integration ZSH v0.2
_shellm_zsh() {
if [[ -n "$BUFFER" ]]; then
    _shellm_prev_cmd=$BUFFER
    BUFFER+="⌛"
    zle -I && zle redisplay
    BUFFER=$(shellm --shell <<< "$_shellm_prev_cmd" --no-interaction)
    zle end-of-line
fi
}
zle -N _shellm_zsh
bindkey ^l _shellm_zsh
# Shell-GPT integration ZSH v0.2
"""
