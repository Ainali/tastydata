## How to generate the pages

An automatic way is used to generate the json sources for the menus and the menues themselves. Two files are needed, demodata.tsv with the actual menus and demomatches.tsv that matches the words used in the demodata to Wikidata items. 

### Matching
demomatches.tsv is a simple two column file with the word of the courses or ingredients in the first column and the Wikidata id in the next. 

### Menu building
demodata.tsv is a bit more complex, but has each menu in the first column. Following the name of the menu is the background image and then the different colors in the color scheme for that menu that will go into the css file for the menu. On the next line and column comes the first course and in the column after that the price. On the next line and column comes the first ingredient. If the column to the right of an ingredient is used it will be showed in parentheses after the ingredient. Repeat with more ingredients and courses and menues. Looking at a file will probably make it easier to follow.

## Requirements
The menus must live in the same directory as `index.css`, `main.css`, `menu.js`, `code2langQ.json` and the `lib`
directory.

## Converting tsv to json
Convert the tsv files to json using something like
```python
Python
python
Import tsv2json
tsv2json.run(u'demodata.tsv', u'demomatches.tsv')
```

## Generate the menu
Then create the menu pages using 
Convert the tsv files to json using something like
```python
Python
python
Import tsv2json
generator.run(u'demodata.json', u'demomatches.json', u'../test')
```

### Result
The resulting files will be generated in the folder specified in the generator command (it does not have to be test). It will contain an index html file and css and one html and css file for each menu with name starting at 1 and increasing (example: 1.html and 1.css).

### Debugging
After running the menu generator, a file matchinfo.csv will be generated with all the courses and ingredients that could not be matched with anything in demomatches.tsv. 

## Note
The generator does not do matching on the index page. In this instance it was added manually after generating the files.
