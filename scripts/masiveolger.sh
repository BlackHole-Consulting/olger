
baseàth="/"
for f in $basepath/data/$1/*; do
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
							python3 $basepath/bin/converter.py  "$f2" "$f2".json	
              						python $basepath/bin/maptograph.py "$f2".json "$1"
						fi
					done
			fi
		done

	# $f is a directory
    fi
done

