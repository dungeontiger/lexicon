git config --global user.name "dungeontiger"
git config --global user.email "stephen.d.gibson@gmail.com"
git remote set-url --push origin https://dungeontiger:32e33b3ae57397172518d3bac967d21b2d799137@github.com/dungeontiger/lexicon.git
git checkout -b updates
git add .
git commit -m "lexicon updates"
git push --set-upstream origin updates
git checkout main
git branch -d updates