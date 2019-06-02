rm -f run1.py not.py run.py
outfile="not.py"
while read p; do
  #echo "$p"
  if [ "$p" == "# RUNBOOK ON" ] ; then
    outfile="run.py"
  fi
  if [ "$p" == "# RUNBOOK OFF" ] ; then
    outfile="not.py"
  fi
  if [[ $p =~ "import azurerm" ]] ; then
    f=`echo "$p" | cut -f2 -d" "`
    cat ../scripts/$f.py >> $outfile
    echo " " >> $outfile
  elif [[ $p =~ "# RUNBOOK INLINE1" ]] ; then
    cat ../scripts/runbook_auth.py >> $outfile
    echo " " >> $outfile
  elif [[ $p =~ "# RUNBOOK INLINE2" ]] ; then
    cat ../scripts/rbauth.py >> $outfile
    echo " " >> $outfile
  else 
    echo $p >> $outfile
  fi
done <../scripts/resources.py