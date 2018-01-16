# Fish completion definition for lulu.

complete -c lulu -s V -l version -d 'print version and exit'
complete -c lulu -s h -l help -d 'print help and exit'
complete -c lulu -s i -l info -d 'print extracted information'
complete -c lulu -s u -l url -d 'print extracted information'
complete -c lulu -l json -d 'print extracted URLs in JSON format'
complete -c lulu -s n -l no-merge -d 'do not merge video parts'
complete -c lulu -l no-caption -d 'do not download captions'
complete -c lulu -s f -l force -d 'force overwrite existing files'
complete -c lulu -s F -l format -x -d 'set video format to the specified stream id'
complete -c lulu -s O -l output-filename -d 'set output filename' \
         -x -a '(__fish_complete_path (commandline -ct) "output filename")'
complete -c lulu -s o -l output-dir  -d 'set output directory' \
         -x -a '(__fish_complete_directories (commandline -ct) "output directory")'
complete -c lulu -s p -l player -x -d 'stream extracted URL to the specified player'
complete -c lulu -s c -l cookies -d 'load cookies.txt or cookies.sqlite' \
         -x -a '(__fish_complete_path (commandline -ct) "cookies.txt or cookies.sqlite")'
complete -c lulu -s x -l http-proxy -x -d 'use the specified HTTP proxy for downloading'
complete -c lulu -s y -l extractor-proxy -x -d 'use the specified HTTP proxy for extraction only'
complete -c lulu -l no-proxy -d 'do not use a proxy'
complete -c lulu -s t -l timeout -x -d 'set socket timeout'
complete -c lulu -s d -l debug -d 'show traceback and other debug info'
