#!/bin/bash


CMD='tail -n7 ~peek/*.log;'
CMD="${CMD}"'echo;'
CMD="${CMD}"'echo;'

if which p_cat_queues.sh > /dev/null
then
    CMD="${CMD}$(which p_cat_queues.sh);"
fi

watch -n 5 "${CMD}"


