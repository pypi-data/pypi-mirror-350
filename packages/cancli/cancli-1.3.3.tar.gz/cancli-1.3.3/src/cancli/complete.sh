# source this file in ~/.bash_completion

__install_completions_from_help()
{
	local app flags
	app="$1"
	flags="$("$app" --help | sed -En 's/\s*(-([^-][^,]*),\s*)?(--[^ ]+).*/\3/p')"
	complete -W "$flags" "$app"
}

__install_completions_from_help cancli
