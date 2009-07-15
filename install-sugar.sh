#!/bin/bash
# == Sugar installation script
# 
# This small script downloads the latest Sugar version and its dependencies
# into a new directory name 'Sugar' (created in the current directory).
#
# It will set everything up and create you a command that you'll be able
# to use to directly invoke Sugar.

mkdir Sugar ; cd Sugar ; export SUGAR_ROOT=`pwd`

git clone git://github.com/sebastien/lambdafactory.git lf-repo
git clone git://github.com/sebastien/sugar.git sg-repo

cd sg-repo/Dependencies ; ./make-dparser.sh ; cd ../..

echo '#!/bin/bash' > sugar
echo "export PYTHONPATH=${SUGAR_ROOT}/lf-repo/Distribution:${SUGAR_ROOT}/sg-repo/Sources:${SUGAR_ROOT}/sg-repo/Dependencies/dparser" >> sugar
echo "python2.5 ${SUGAR_ROOT}/sg-repo/Sources/sugar/main.py" >> sugar
chmod +x sugar

cd .. ;  echo "To run sugar: .${SUGAR_ROOT}/sugar"

# EOF
