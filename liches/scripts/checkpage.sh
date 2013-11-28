#/bin/bash
if [ -z "$1" ]; then
    echo usage: $0 url
    exit
fi
FN=$(hexdump -n 16 -v -e '/1 "%02X"' /dev/urandom)".csv"
bin/linkchecker --recursion-level=1 --file-output=csv/utf-8/$FN --pause=3 --no-warnings $1
# you can of course use the csv import of you db instead
bin/empty_link_table development.ini $1
bin/import_liches_csv development.ini $FN
rm $FN
