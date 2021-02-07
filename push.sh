git config --global user.name "dungeontiger"
git config --global user.email "stephen.d.gibson@gmail.com"
git remote set-url --push origin https://dungeontiger:260ed35b886d96e788df35e5d74093aebd8eeab1@github.com/dungeontiger/lexicon.git
git checkout -b updates
git add .
git commit -m "lexicon updates"
git push --set-upstream origin updates
git checkout main
git branch -d updates