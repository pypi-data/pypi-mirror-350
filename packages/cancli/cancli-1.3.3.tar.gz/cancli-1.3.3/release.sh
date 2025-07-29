#!/usr/bin/env bash

# Copyright © 2022 erzo <erzo@posteo.de>
# This work is free. You can use, copy, modify, and/or distribute it
# under the terms of the BSD Zero Clause License, see LICENSE.


# ---------- strict mode ----------

set -euo pipefail
IFS="$(printf '\n\t')"


# ---------- set current working directory ----------
# to the directory where this script is located
# https://stackoverflow.com/questions/3349105/how-can-i-set-the-current-working-directory-to-the-directory-of-the-script-in-ba/17744637#17744637

cd -P -- "$(dirname -- "${BASH_SOURCE[0]}")"


# ---------- usage ----------

usage() {
echo "\
Usage: $0

Options:
  -h, --help        show this help and quit
  -v, --update-venv install/update all required packages in venv
  -t, --test        run the automated tests
  -w, --wheel       only build wheel file
  -m, --merge       set the version number to new release,
                    merge the current development branch into the master
                    and create a new tag for the new release
      --patch       this release contains only bugfixes
      --minor       this release contains new features
      --major       this release breaks backward compatibility
  -u, --upload      build and upload
  -b, --branch      prepare development branch to continue development
"
}


# ---------- command line arguments ----------

PARSED_ARGUMENTS=$(getopt -n "$0" -o hvtwdDmub --long help,update-venv,test,wheel,doc,doc-without-test,merge,patch,minor,major,upload,branch -- "$@")

increment=minor

update_venv=none
run_tests=none
build_doc=none
merge_and_tag=none
build_and_upload=none
new_branch=none
only_build_wheel=none

eval set -- "$PARSED_ARGUMENTS"
while true; do
	case "$1" in
		-h | --help)        usage; exit ;;
		-v | --update-venv) update_venv=true;        shift ;;
		-t | --test)        run_tests=true;          shift ;;
		-w | --wheel)       only_build_wheel=true;   shift ;;
		#-d | --doc)         build_doc=true;          shift ;;
		#-D | --doc-without-test) build_doc=true; run_tests=false; shift ;;
		-m | --merge)       merge_and_tag=true;      shift ;;
		     --patch)       increment=patch;         shift ;;
		     --minor)       increment=minor;         shift ;;
		     --major)       increment=major;         shift ;;
		-u | --upload)      build_and_upload=true;   shift ;;
		-b | --branch)      new_branch=true;         shift ;;
		--) shift; break ;;
		*) echo "Unexpected option: $1" ;;
	esac
done

if [ "$#" != 0 ]; then
	echo "Invalid positional arguments: $@"
	usage
	exit 1
fi

dont_publish=false
if [ "$run_tests" = "none" -a "$build_doc" = "none" -a "$merge_and_tag" = "none" -a "$build_and_upload" = "none" -a "$new_branch" = "none" ]; then
	run_tests=true
	#build_doc=true
	merge_and_tag=true
	build_and_upload=true
	new_branch=true
elif [ "$merge_and_tag" = "none" -a "$build_and_upload" = "none" -a "$new_branch" = "none" ]; then
	dont_publish=true
fi

if [ "$run_tests" = 'none' ]; then
	run_tests='true'
fi


# ---------- functions ----------

color_reset='[m'
color_cmd='[34m'
run() {
	# $ run echo "hello world"
	# works for commands with arguments
	# does not work for pipes, redirects and stuff
	echo "$color_cmd\$ $@$color_reset"
	"$@"
}

ask_yes_no() {
	local ans
	while true; do
		read -p "$1 [Y/n] " -r ans
		if [ "$ans" = "y" -o "$ans" = "Y" ]; then
			return 0
		elif [ "$ans" = "n" -o "$ans" = "N" ]; then
			return 1
		elif [ "$ans" = "q" -o "$ans" = "Q" ]; then
			exit
		elif [ "$ans" = "" ]; then
			return 0
		else
			echo "Invalid input '$ans'."
		fi
	done
}

increment_version() {
	local oldversion="$1"
	local inccmd
	if [ "$increment" = "patch" ]; then
		inccmd='@F[2]++'
	elif [ "$increment" = "minor" ]; then
		inccmd='@F[1]++; @F[2]=0'
	elif [ "$increment" = "major" ]; then
		inccmd='@F[0]++; @F[1]=0; @F[2]=0'
	else
		echo >&2 "Invalid value for increment: '$increment'. Should be one of patch, minor, major"
		exit 1
	fi
	if [ "$oldversion" = '' ]; then
		oldversion='v0.0.0'
	fi
	echo "$oldversion" | perl -na -F'\.' -e "$inccmd"'; print join ".", @F[0..$#F]'
}

branch_exists() {
	git branch | grep -q " $1$"
}

request_tag_description() {
	if [ ! -e "$fn_tag" ]; then
		cat >"$fn_tag" <<EOF
$newversion

# Please write a change log for the new release.
# This will be the description of the tag.
# You can take a break any time, after closing this
# file you will be asked whether you want to continue.
# Lines starting with a '#' are ignored.

New features:

Bugfixes:

Changes:

EOF
	else
		sed -i '1i # I have found this file. Please check if it is correct and complete' "$fn_tag"
	fi
	${EDITOR:-vim} "$fn_tag"
	sed -Ei '0,/^[^#]/{/^(#.*)?$/d}' "$fn_tag"
	check_tag_description
	sed -Ei '3,/^[^#]/{/^(#.*)?$/d}' "$fn_tag"
}

check_tag_description() {
	local title secondline
	title="$(head -n1 "$fn_tag")"
	if [ "$title" != "$newversion" ]; then
		if ask_yes_no "The title does not match the expected new version number $newversion. Do you want to fix that now?"; then
			vim "$fn_tag"
			check_tag_description
		elif ask_yes_no "Do you want to use '$title' as new version number instead?"; then
			newversion="$title"
		else
			exit 1
		fi
	fi

	secondline="$(head -n2 "$fn_tag" | tail -n1)"
	if [ "$secondline" ]; then
		if ask_yes_no "The second line is not empty. Do you want to fix that now?"; then
			vim "$fn_tag"
			check_tag_description
		else
			exit 1
		fi
	fi

	if grep -q TODO "$fn_tag"; then
		if ask_yes_no "The tag description contains TODO flags. Do you want to resolve them now?"; then
			vim "$fn_tag"
			check_tag_description
		elif ask_yes_no "Continue anyway?"; then
			:
		else
			exit 1
		fi
	fi
}

check_clean() {
	local status
	status="$(git status --porcelain=v1 | sed "/^?? $fn_tag\$/d")"
	if echo "$status" | grep -q '^[^?][^?]'; then
		echo "The repository is not clean."
		echo "Please commit or stash the changes before continuing."
		echo ""
		git status
		exit 1
	elif [ "$status" ]; then
		echo "There are untracked files:"
		echo "$status" | sed 's/^?? /- /'
		if ! ask_yes_no "Do you want to continue, anyway?"; then
			exit 1
		fi
	fi
}


strip_v_from_version() {
	echo "$1" | sed -E 's/^v(.*)/\1/'
}
commit_version() {
	local version
	version="$1"
	version="$(strip_v_from_version "$version")"
	sed -Ei "s/^(__version__ += +['\"])[^'\"]*(['\"])/\1$version\2/" "$fn_version"
	git add "$fn_version"
	git commit --message "set version to $version"
}


# ---------- venv ----------

install_requirements() {
	echo $color_cmd"installing requirements in venv"$color_reset
	python3 -m pip install --upgrade pip
	python3 -m pip install --upgrade -r requirements.txt
	python3 -m pip install --upgrade -r requirements-release.txt
	python3 -m pip install --upgrade -r requirements-test.txt
	python3 -m pip install -e .
}

if ! python3 -m flit --version >/dev/null; then
	if [ ! -d venv ]; then
		echo $color_cmd"creating new venv"$color_reset
		python3 -m venv venv
		. venv/bin/activate
		install_requirements
	else
		echo $color_cmd"activating venv"$color_reset
		. venv/bin/activate
		[ "$update_venv" = 'true' ] && install_requirements
	fi
else
	[ "$update_venv" = 'true' ] && install_requirements
fi

if [ "$update_venv" = 'true' ]; then
	exit
fi


# ---------- run tests ----------

COVERAGE_HTML_OUTPUT_PATH=htmlcov
if [ "$run_tests" = "true" ]; then
	tox_exit_code=0
	if [ -e "$COVERAGE_HTML_OUTPUT_PATH" ]; then
		rm -r "$COVERAGE_HTML_OUTPUT_PATH"
	fi
	tox || tox_exit_code=$?

	if [ "$tox_exit_code" != "0" ]; then
		exit $tox_exit_code
	fi

	#test_coverage="$(.tox/cov/bin/coverage report | sed -En 's/TOTAL.* ([0-9]+%)/\1/p')"
fi


# ---------- build wheel ----------

if [ "$only_build_wheel" = 'true' ]; then
	flit build
	exit
fi


# ---------- build documentation ----------

DOCS_BUILD_COVERAGE='docs/build/html/coverage'

fn_tag="tag"
fn_version="src/cancli/meta.py"

branchname="$(git branch | sed -En 's/^\* (.*)$/\1/p')"
lastversion="$(git tag --list 'v*' --sort=version:refname | tail -1)"
newversion="$(increment_version "$lastversion")"


if [ "$build_doc" = 'true' ]; then
	echo "${color_cmd}running sphinx$color_reset"
	if [ "$dont_publish" = 'true' ]; then
		newversion="$lastversion-dev"
		if [ "${test_coverage:-}" = '' ]; then
			test_coverage='xxx%'
		fi
	else
		echo "Make sure none of the files is opened anymore (to make sure that there are no unsaved changes)"
		check_clean
	fi

	# update test coverage
	sed -Ei "s/Test coverage: .*%/Test coverage: $test_coverage/" 'docs/source/index.rst'
	sed -Ei "s/\(tested on [^)]*\)/(tested on `python3 --version`)/" 'docs/source/index.rst'

	# update version number
	echo "setting version in documentation to $newversion"
	sed -Ei "s/(release = ')[^']*(')/\\1$newversion\\2/" 'docs/source/conf.py'

	# update table of contents
	modules="$(find src/cancli/ -name '*.py' -type f | sed -E 's:src/cancli/(.*)\.py:cancli.\1:' | sed 's:/:.:g' | sed 's/cancli.__init__/cancli/' | sed 's/^/   /' | sort)"
	newline="$(printf '\n ')"  # the space is required to protect the newline. it does not seem to be inserted into the file.
	sed -i '/^Reference/,/^[A-Z]/ { /^\.\. toctree::/,/^===/ { /^ *cancli/d } }' 'docs/source/index.rst'
	sed -i "/^Reference/,/^[A-Z]/ { /^\.\. toctree::/,/^$/ { /^$/a \\${modules//$newline/\\$newline}$newline} }" 'docs/source/index.rst'

	# build documentation
	sphinx-apidoc --separate -o 'docs/source' 'src/cancli'
	sphinx-build -M html 'docs/source' 'docs/build'

	if [ "$dont_publish" != 'true' ]; then
		if [ -e "$DOCS_BUILD_COVERAGE" ]; then
			rm -r "$DOCS_BUILD_COVERAGE"
		fi
		cp -r "$COVERAGE_HTML_OUTPUT_PATH" "$DOCS_BUILD_COVERAGE"
		rm "$DOCS_BUILD_COVERAGE/.gitignore"
		git add docs
		if ! ask_yes_no 'Commit the new build of the html documentation?'; then
			exit 0
		fi
		git commit --allow-empty --message 'updated html docs'
	fi
fi


# ---------- main ----------

if [ "$dont_publish" = "true" ]; then
	exit
fi

echo "Make sure none of the files is opened anymore (to make sure that there are no unsaved changes)"

check_clean

#if grep -ERI -ho 'cancli v[0-9]+\.[0-9]+\.[0-9]+(-[^ ]*)?' docs/ | grep -v "cancli $version\$"; then
#	echo 'HTML documentation contains wrong version numbers'
#	exit 1
#fi

if [ "$merge_and_tag" = "true" ]; then
	request_tag_description
	check_clean

	commit_version "$newversion"

	if [ "$branchname" != "master" ]; then
		git checkout master
	else
		echo "Which branch do you want to merge?"
		git branch
		while true; do
			read -p "branch name: " branchname
			if branch_exists "$branchname"; then
				break
			else
				echo "No branch called $branchname"
			fi
		done
	fi

	git merge --no-ff "$branchname"
	git tag -a "$newversion" --file "$fn_tag"
	rm "$fn_tag"
else
	newversion="$lastversion"
fi

if [ "$build_and_upload" = "true" ]; then
	if [ -e dist ]; then
		rm -r dist
	fi
	if ask_yes_no "Do you have an internet connection to build and upload the new version?"; then
		run flit publish
		run git push
		run git push --tags
	fi
fi

if [ "$new_branch" = "true" ]; then
	if [ "$merge_and_tag" != "true" ]; then
		if [ "$branchname" = "master" ] && branch_exists "dev"; then
			branchname="dev"
		fi
	fi
	if [ "$branchname" = "dev" ]; then
		git checkout "$branchname"
		git merge --ff-only master
		commit_version "$newversion-dev"
	else
		if [ "$branchname" != "master" ] && ask_yes_no "Do you want to delete the old development branch ($branchname)?"; then
			git branch --unset-upstream "$branchname"
			git branch -d "$branchname"
		fi

		if ask_yes_no "Do you want to create a new development branch?"; then
			while true; do
				read -p "new branch name: " newbranchname
				if [ "$newbranchname" = "" ]; then
					echo "You need to enter a name for the new branch"
				elif branch_exists "$newbranchname"; then
					echo "Branch $newbranchname exists already"
				else
					git checkout -b "$newbranchname"
					commit_version "$newversion-dev"
					break
				fi
			done
		fi
	fi
fi
