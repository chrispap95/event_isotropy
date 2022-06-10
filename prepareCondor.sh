#!/bin/sh
USERBASE=`pwd`
#rm ${CMSSW_VERSION}.tgz
cd ${CMSSW_BASE}/..
echo "Creating tarball..."
tar --exclude="*.root"  --exclude-vcs -zcf ${CMSSW_VERSION}.tgz ${CMSSW_VERSION}
xrdcp -f ${CMSSW_VERSION}.tgz root://cmseos.fnal.gov//store/user/${USER}/CMSSW_TARBALLS/${CMSSW_VERSION}.tgz
if [ ! -f ${CMSSW_VERSION}.tgz ]; then
echo "Error: tarball doesn't exist!"
else
echo " Done!"
fi
rm ${CMSSW_VERSION}.tgz
cd $USERBASE
