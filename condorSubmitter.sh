#!/usr/bin/sh
source ${PWD}/prepareCondor.sh

geometry=Ring
scenarios=(darkPho)
mMed=(125 200 300 400 750 1000)
N=64
mDark=(1)
temp=(0.5 1 3 5)
HT=100
PT=(100 200 300 400 500 600 800 1000)

for sc in ${scenarios[@]}
do
for mass in ${mMed[@]}
do
for md in ${mDark[@]}
do
for t in ${temp[@]}
do
for pt in ${PT[@]}
do
#namestring=mMed${mass}_mDark${md}_temp${t}_${sc}_HT${HT}_iso${geometry}${N}
namestring=mMed${mass}_mDark${md}_temp${t}_${sc}_PT${pt}_iso${geometry}${N}
#namestring=mMed${mass}_mDark${md}_temp${t}_${sc}_iso${geometry}${N}
argument=${CMSSW_VERSION}\ ${mass}\ ${md}\ ${t}\ ${sc}\ ${HT}\ ${pt}\ ${geometry}\ ${N}\ \$\(Cluster\)\ \$\(Process\)

# Write jdl file
cat > jdl/condor_${namestring}.jdl << "EOF"
universe = vanilla
Executable = condor-exec.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = condor-exec.sh
Output = log/isotropy_$(Cluster)_$(Process).stdout
Error = log/isotropy_$(Cluster)_$(Process).stderr
Log = log/isotropy_$(Cluster)_$(Process).log
x509userproxy = $ENV(X509_USER_PROXY)
EOF
echo "Arguments = "${argument} >> jdl/condor_${namestring}.jdl
echo "Queue 1" >> jdl/condor_${namestring}.jdl

# Submit job
condor_submit jdl/condor_${namestring}.jdl
done
done
done
done
done
