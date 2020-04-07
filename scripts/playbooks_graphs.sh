#!/bin/bash
basepath=`echo $PWD`
for f in $basepath/playbooks/*; do
    if [ -d "$f" ]
    then
	echo ""
        for file2 in "$f/*"
		do
			
			if [ -d "$file2" ]
			then
				echo ""

			else
				for f2 in $file2
					do
						ext="${f2: -4}"
						if [[ ".xml" == $ext ]]
						then
              						ansible-playbook-grapher "$f2" -o "playbooks/svg/$f2"	
						fi
					done
			fi
		done

    else
	
	ext="${f: -4}"
	if [[ ".xml" == $ext ]]
	then
		echo $f       
		ansible-playbook-grapher "$f" -o "playbooks/svg/$f"	
	fi




	# $f is a directory
    fi
done

