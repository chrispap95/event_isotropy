#!/bin/bash
echo "Starting job on " `date` #Date/time of start of job
echo "Running on: `uname -a`" #Condor job is running on this node
echo "System software: `cat /etc/redhat-release`" #Operating System on that node

# setting up the input variables
CMSSW=$1
mMed=$2
mDark=$3
temp=$4
scenario=$5
HT=$6
PT=$7
geometry=$8
N=$9
cluster=$10
process=$11

#inputDir=root://cmseos.fnal.gov//store/user/chpapage/SUEPTest/prod_v3
inputDir=root://cmseos.fnal.gov//store/user/chpapage/SUEP_svjprod
#nameIn=mMed${mMed}_mDark${mDark}_temp${temp}_gen14TeV_${scenario}_HT${HT}
nameIn=step_GEN_mMed${mMed}_mDark${mDark}_temp${temp}_gen13TeV_${scenario}
nameOut=${nameIn}_PT${PT}_iso${geometry}${N}

# bring in the tarball you created before with caches and large files excluded:
xrdcp -s root://cmseos.fnal.gov//store/user/chpapage/CMSSW_TARBALLS/${CMSSW}.tgz .
source /cvmfs/cms.cern.ch/cmsset_default.sh 
tar -xf ${CMSSW}.tgz
rm ${CMSSW}.tgz
cd ${CMSSW}/src/
scramv1 b ProjectRename # this handles linking the already compiled code - do NOT recompile
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
echo $CMSSW_BASE "is the CMSSW we have on the local worker node"

# run the desired code
cd event_isotropy
python3 isotropy${geometry}.py -N ${N} --ptcut ${PT} -f ${inputDir}/merged/${nameIn}.root -o ${nameOut}.root
xrdcp -f ${nameOut}.root ${inputDir}/results/${nameOut}.root
rm ${nameOut}.root
 
