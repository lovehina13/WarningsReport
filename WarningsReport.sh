SCRIPTS_DIR=$(readlink -f ${0} | xargs dirname)
SOURCES_DIR=${1}

rm -rf warnings-report
mkdir -p warnings-report
cd warnings-report
cmake -G "Unix Makefiles" \
    -DCMAKE_BUILD_TYPE=Debug \
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_C_COMPILER_WORKS=1 \
    -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_CXX_COMPILER_WORKS=1 \
    -DCMAKE_CXX_FLAGS="-fsyntax-only -Weverything -Wno-padded -Wno-c++98-compat -Wno-c++98-compat-pedantic" \
    -DCMAKE_CXX_CLANG_TIDY="clang-tidy;-header-filter=.*;-checks=*,-llvmlibc-*,-modernize-use-nodiscard,-modernize-use-trailing-return-type;--extra-arg=-I${CMAKE_CURRENT_SOURCE_DIR}" \
    ${SOURCES_DIR}
make -j8 -i 2>&1 | tee -a warnings-report.log
python ${SCRIPTS_DIR}/WarningsReport.py warnings-report.log warnings-report.html
# firefox warnings-report.html
