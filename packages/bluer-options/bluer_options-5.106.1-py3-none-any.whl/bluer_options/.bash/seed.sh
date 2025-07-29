#! /usr/bin/env bash

function bluer_ai_seed() {
    local task=$1

    local list_of_seed_targets="arvancloud|cloudshell|docker|ec2|jetson|headless_rpi|mac|rpi|sagemaker-jupyterlab|studio-classic-sagemaker|studio-classic-sagemaker-system"

    if [ "$task" == "list" ]; then
        local list_of_targets=$(declare -F | awk '{print $NF}' | grep 'bluer_ai_seed_' | sed 's/bluer_ai_seed_//' | tr '\n' '|')
        list_of_targets="$list_of_targets|$list_of_seed_targets"
        bluer_ai_log_list "$list_of_targets" \
            --before "" \
            --delim \| \
            --after "target(s)"
        return
    fi

    local base64="base64"
    # https://superuser.com/a/1225139
    [[ "$abcli_is_ubuntu" == true ]] && base64="base64 -w 0"

    # internal function.
    if [ "$task" == "add_file" ]; then
        local source_filename=$2

        local destination_filename=$3

        local var_name=_bluer_ai_seed_$(echo $source_filename | tr / _ | tr . _ | tr - _ | tr \~ _ | tr \$ _)

        local seed="$var_name=\"$(cat $source_filename | $base64)\"$delim"
        seed="${seed}echo \$$var_name | base64 --decode > $var_name$delim"
        seed="$seed${sudo_prefix}mv -v $var_name $destination_filename"

        echo $seed
        return
    fi

    if [ "$task" == "eject" ]; then
        if [[ "$abcli_is_jetson" == true ]]; then
            sudo eject /media/bluer_ai/SEED
        else
            sudo diskutil umount /Volumes/seed
        fi
        return
    fi

    local seed=""

    local target=$(bluer_ai_clarify_input $1 ec2)

    local options=$2
    local do_log=$(bluer_ai_option_int "$options" log 1)
    local do_eval=$(bluer_ai_option_int "$options" eval 0)
    local include_aws=$(bluer_ai_option_int "$options" aws 0)
    local output=$(bluer_ai_option_choice "$options" clipboard,key,screen clipboard)
    [[ "$abcli_is_sagemaker" == true ]] &&
        output=screen

    local delim="\n"
    local delim_section="\n\n"
    if [ "$output" == "clipboard" ]; then
        delim="; "
        delim_section="; "
    fi

    local env_name=""
    [[ "$target" == "ec2" ]] &&
        env_name="worker"
    env_name=$(bluer_ai_option "$options" env $env_name)

    local sudo_prefix="sudo "
    [[ "$target" == *"sagemaker"* ]] &&
        sudo_prefix=""

    if [ "$output" == "key" ]; then
        local seed_path="/Volumes/seed"
        [[ "$abcli_is_jetson" == true ]] &&
            seed_path="/media/bluer_ai/SEED"

        if [ ! -d "$seed_path" ]; then
            bluer_ai_log_error "@seed: usb key not found."
            return 1
        fi

        mkdir -p $seed_path/bluer_ai/
    fi

    [[ "$do_log" == 1 ]] &&
        bluer_ai_log "$abcli_fullname seed 🌱 -$output-> $target"

    local seed="#! /bin/bash$delim"
    [[ "$output" == "clipboard" ]] && seed=""

    seed="${seed}echo \"$abcli_fullname seed for $target\"$delim_section"

    if [[ "|$list_of_seed_targets|" != *"|$target|"* ]]; then
        # expected to append to/update $seed
        local function_name="bluer_ai_seed_${target}"

        if [[ $(type -t $function_name) == "function" ]]; then
            $function_name "${@:2}"
        else
            bluer_ai_log_error "@seed: $target: target not found."
            return 1
        fi
    else
        if [ "$target" == docker ]; then
            seed="${seed}source /root/git/bluer-ai/bluer_ai/.abcli/bluer_ai.sh$delim"
        else
            if [[ "$target" != studio-classic-sagemaker ]]; then
                if [ -d "$HOME/.kaggle" ]; then
                    seed="${seed}mkdir -p \$HOME/.kaggle$delim"
                    seed="$seed$(bluer_ai_seed add_file $HOME/.kaggle/kaggle.json \$HOME/.kaggle/kaggle.json)$delim"
                    seed="${seed}chmod 600 \$HOME/.kaggle/kaggle.json$delim_section"
                else
                    bluer_ai_log_warning "@seed: kaggle.json not found."
                fi
            fi

            if [[ "$target" != studio-classic-sagemaker* ]] &&
                [[ "$target" != cloudshell ]] &&
                [[ "$include_aws" == 1 ]]; then
                seed="$seed${sudo_prefix}rm -rf ~/.aws$delim"
                seed="$seed${sudo_prefix}mkdir ~/.aws$delim_section"
                seed="$seed$(bluer_ai_seed add_file $HOME/.aws/config \$HOME/.aws/config)$delim"
                seed="$seed$(bluer_ai_seed add_file $HOME/.aws/credentials \$HOME/.aws/credentials)$delim_section"
            fi

            if [[ "|cloudshell|studio-classic-sagemaker|" != *"|$target|"* ]]; then
                seed="${seed}${sudo_prefix}mkdir -p ~/.ssh$delim_section"
                seed="$seed"'eval "$(ssh-agent -s)"'"$delim_section"
                seed="$seed$(bluer_ai_seed add_file $HOME/.ssh/$BLUER_AI_GIT_SSH_KEY_NAME \$HOME/.ssh/$BLUER_AI_GIT_SSH_KEY_NAME)$delim"
                seed="${seed}chmod 600 ~/.ssh/$BLUER_AI_GIT_SSH_KEY_NAME$delim"
                seed="${seed}ssh-add -k ~/.ssh/$BLUER_AI_GIT_SSH_KEY_NAME$delim_section"
            fi

            if [[ "$target" == "studio-classic-sagemaker-system" ]]; then
                # https://chat.openai.com/c/8bdce889-a9fa-41c2-839f-f75c14d48e52
                seed="${seed}conda install -y unzip$delim_section"

                seed="${seed}pip3 install opencv-python-headless$delim_section"
            fi

            if [[ "$target" == "studio-classic-sagemaker" ]]; then
                seed="${seed}apt-get update$delim"
                seed="${seed}apt install -y libgl1-mesa-glx rsync$delim"
                seed="${seed}conda install -c conda-forge nano --yes$delim_section"
            fi

            if [[ "$target" == *"rpi" ]]; then
                seed="${seed}ssh-keyscan github.com | sudo tee -a ~/.ssh/known_hosts$delim_section"
            fi

            if [[ "$target" != studio-classic-sagemaker ]] && [[ "$target" != cloudshell ]]; then
                seed="${seed}"'ssh -T git@github.com'"$delim_section"
            fi

            if [[ "$target" == *"rpi" ]]; then
                # https://serverfault.com/a/1093530
                # https://packages.ubuntu.com/bionic/all/ca-certificates/download
                certificate_name="ca-certificates_20211016ubuntu0.18.04.1_all"
                seed="${seed}wget --no-check-certificate http://security.ubuntu.com/ubuntu/pool/main/c/ca-certificates/$certificate_name.deb$delim"
                seed="$seed${sudo_prefix}sudo dpkg -i $certificate_name.deb$delim_section"

                seed="$seed${sudo_prefix}apt-get update --allow-releaseinfo-change$delim"
                seed="$seed${sudo_prefix}apt-get install -y ca-certificates libgnutls30$delim"
                seed="$seed${sudo_prefix}apt-get --yes --force-yes install git$delim_section"
            fi

            local repo_address="git@github.com:kamangir/bluer-ai.git"
            [[ "$target" == studio-classic-sagemaker-system ]] &&
                repo_address="https://github.com/kamangir/bluer-ai"

            if [[ "$target" == studio-classic-sagemaker ]]; then
                seed="${seed}pip install --upgrade pip --no-input$delim_section"
                seed="${seed}cd git/bluer-ai${delim}"
            else
                seed="${seed}cd; mkdir -p git; cd git$delim"
                seed="${seed}git clone $repo_address$delim"
                seed="${seed}cd bluer-ai${delim}"
                seed="${seed}git checkout $bluer_ai_git_branch; git pull$delim_section"
            fi

            if [ "$target" == "headless_rpi" ]; then
                seed="${seed}touch ~/storage/temp/ignore/headless$delim_section"
            fi

            if [ "$target" == "rpi" ]; then
                seed="${seed}python3 -m pip install --upgrade pip$delim"
                seed="${seed}pip3 install -e .$delim"
                seed="${seed}sudo python3 -m pip install --upgrade pip$delim"
                seed="${seed}sudo pip3 install -e .$delim_section"
            elif [ "$target" == "headless_rpi" ]; then
                seed="${seed}sudo apt-get --yes --force-yes install python3-pip$delim"
                seed="${seed}pip3 install -e .$delim"
                seed="${seed}sudo pip3 install -e .$delim_section"
            elif [ "$target" == "arvancloud" ]; then
                seed="${seed}sudo apt-get update$delim"
                seed="${seed}sudo apt install -y python3-pip$delim"
                seed="${seed}sudo apt install -y python3-venv$delim"
                seed="${seed}python3 -m venv \$HOME/venv/bluer_ai$delim"
                seed="${seed}source \$HOME/venv/bluer_ai/bin/activate$delim"
                seed="${seed}pip3 install setuptools$delim"
                seed="${seed}pip3 install -e .$delim"
                seed="${seed}pip3 install bluer_objects[opencv]$delim"
                seed="${seed}pip3 install --upgrade opencv-python-headless$delim"
                seed="${seed}sudo apt install -y libgl1$delim_section"
            else
                seed="${seed}pip3 install -e .$delim_section"
            fi

            seed="${seed}source ./bluer_ai/.abcli/bluer_ai.sh$delim_section"

            if [ "$target" == "ec2" ]; then
                seed="${seed}source ~/.bash_profile$delim_section"
            elif [ "$target" == "rpi" ]; then
                seed="${seed}source ~/.bashrc$delim_section"
            fi

            if [[ "$target" == sagemaker-jupyterlab ]]; then
                seed="${seed}pip3 install --upgrade opencv-python-headless$delim_section"
                seed="${seed}bluer_ai_plugins_install all$delim_section"
            fi

            if [ ! -z "$env_name" ]; then
                seed="${seed}bluer_ai_env dot copy $env_name$delim"
                seed="${seed}bluer_ai init$delim_section"
            fi

            if [[ "$target" == studio-classic-sagemaker ]]; then
                local plugin_name=$(bluer_ai_option "$options" plugin)

                [[ ! -z "$plugin_name" ]] &&
                    seed="${seed}bluer_ai_conda create name=$plugin_name,~recreate$delim"
            fi
        fi
    fi

    [[ "$do_eval" == 1 ]] &&
        seed="${seed}bluer_ai_eval ${@:3}$delim_section"

    [[ "$target" == studio-classic-sagemaker* ]] &&
        bluer_ai_log_warning "run \"bash\" before pasting the seed."

    if [ "$output" == "clipboard" ]; then
        if [ "$abcli_is_mac" == true ]; then
            echo $seed | pbcopy
        elif [ "$abcli_is_ubuntu" == true ]; then
            echo $seed | xclip -sel clip
        fi

        [[ "$do_log" == 1 ]] &&
            bluer_ai_log "📋 paste the seed 🌱 in the $target terminal."
    elif [ "$output" == "key" ] || [ "$output" == "filename" ]; then
        filename=$(bluer_ai_option "$options" filename $abcli_object_path/seed)
        [[ "$output" == "key" ]] &&
            filename="$seed_path/bluer_ai/$target"

        echo -en $seed >$filename.sh
        chmod +x $filename.sh

        echo "{\"version\":\"$bluer_ai_version\"}" >$filename.json

        [[ "$do_log" == 1 ]] &&
            bluer_ai_log "seed 🌱 -> $filename."
    elif [ "$output" == "screen" ]; then
        printf "$GREEN$seed$NC\n"
    else
        bluer_ai_log_error "this should not happen - output: $output".
        return 1
    fi
}
