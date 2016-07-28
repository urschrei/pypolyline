#!/bin/bash
set -e -x

PYBINS=(
  # "/opt/python/cp27-cp27m/bin"
  "/opt/python/cp27-cp27mu/bin"
  # "/opt/python/cp33-cp33m/bin"
  # "/opt/python/cp34-cp34m/bin"
  "/opt/python/cp35-cp35m/bin"
  )

mkdir -p /io/wheelhouse
# ls -la /io
# ls -la /io/pypolyline
echo $LD_LIBRARY_PATH
mkdir -p /usr/local/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
export DOCKER_BUILD=true
cp /io/pypolyline/libpolyline_ffi.so /usr/local/lib
cp /io/pypolyline/libpolyline_ffi.so /io/pypolyline/libpolyline_ffi.so_
# Compile wheels
for PYBIN in ${PYBINS[@]}; do
    ${PYBIN}/pip install -r /io/dev-requirements.txt
    ${PYBIN}/pip wheel /io/ -w wheelhouse/ --no-deps --build-option --plat-name=manylinux1_x86_64
done

# Bundle external shared libraries into the wheels
# for whl in wheelhouse/*.whl; do
    # auditwheel repair $whl -w /io/wheelhouse/
    # cp wheelhouse/*.whl /io/wheelhouse
# done

# Install packages and test
for PYBIN in ${PYBINS[@]}; do
    ${PYBIN}/pip install pypolyline --no-index -f /io/wheelhouse
    (cd $HOME; ${PYBIN}/nosetests pypolyline)
done
