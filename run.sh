template=$(
    cat <<-END
---
title: FAST Time Table (\today{})
geometry: margin=2cm
header-includes:
    - \usepackage{setspace}
    - \doublespacing
    - \usepackage{lineno}
---

END
)

path="course_files/md"

cwd=$(pwd)

# $(rm -rf $path/*.md $path/*.pdf)

python algorithms.py

mv file.md $path

cd $path

echo "$template" > timetable_mod.md

cat file.md >> timetable_mod.md

pandoc -s -o timetable.pdf timetable_mod.md -V papersize:a4

setsid xdg-open timetable.pdf
