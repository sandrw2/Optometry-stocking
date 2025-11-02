Enviroment Recreate:

conda env create -f environment.yml


If you want to update the environment for other people:

conda env export --from-history > dependencies/environment.yml

If you want to udpate th=e enviroment from other people:

conda env update -f environment.yml --prune


Git remove tracking:
git rm --cached {filename}

git commit -m ""


