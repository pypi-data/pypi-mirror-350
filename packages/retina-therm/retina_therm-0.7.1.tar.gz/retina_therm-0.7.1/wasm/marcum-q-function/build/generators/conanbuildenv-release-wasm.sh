script_folder="/home/cclark/Code/sync/projects/retina-therm/wasm/marcum-q-function/build/generators"
echo "echo Restoring environment" > "$script_folder/deactivate_conanbuildenv-release-wasm.sh"
for v in EMSDK EMSCRIPTEN EM_CONFIG EM_CACHE CC CXX AR NM RANLIB STRIP PATH
do
    is_defined="true"
    value=$(printenv $v) || is_defined="" || true
    if [ -n "$value" ] || [ -n "$is_defined" ]
    then
        echo export "$v='$value'" >> "$script_folder/deactivate_conanbuildenv-release-wasm.sh"
    else
        echo unset $v >> "$script_folder/deactivate_conanbuildenv-release-wasm.sh"
    fi
done


export EMSDK="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin"
export EMSCRIPTEN="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten"
export EM_CONFIG="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/.emscripten"
export EM_CACHE="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/.emscripten_cache"
export CC="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/emcc"
export CXX="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/em++"
export AR="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/emar"
export NM="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/emnm"
export RANLIB="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/emranlib"
export STRIP="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten/emstrip"
export PATH="/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin:/home/cclark/.conan2/p/b/emsdk629b3f8c78cdf/p/bin/upstream/emscripten:$PATH"