#generator

Used to generate the menus and the json sources. Two files are needed, demodata.tsv with the actual menus and demomatches.tsv that matches the words used in the demodata to Wikidata items. 

The menus must live in the same directory
as `index.css`, `main.css`, `menu.js`, `code2langQ.json` and the `lib`
directory.

Convert the tsv files to json using something like `run(u'demodata.tsv', u'demomatches.tsv')`

Then create the menu pages using `run(u'demodata.json', u'demomatches.json', u'../test')
