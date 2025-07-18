# if you make changes to any of the python files or audio files make sure to run this script

rm docs/bounce.tar
tar cf docs/bounce.tar docs/training-python/*.py 
rm docs/trained.tar
tar cf docs/trained.tar docs/trained-python/*.py  docs/trained-python/*.pkl
rm docs/play.tar
tar cf docs/play.tar docs/playable-python/*.py