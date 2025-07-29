script_folder="/home/cclark/Code/sync/projects/retina-therm/wasm/marcum-q-function/build/generators"
echo "echo Restoring environment" > "$script_folder/deactivate_conanrunenv-release-wasm.sh"
for v in 
do
    is_defined="true"
    value=$(printenv $v) || is_defined="" || true
    if [ -n "$value" ] || [ -n "$is_defined" ]
    then
        echo export "$v='$value'" >> "$script_folder/deactivate_conanrunenv-release-wasm.sh"
    else
        echo unset $v >> "$script_folder/deactivate_conanrunenv-release-wasm.sh"
    fi
done

