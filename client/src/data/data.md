## Format
The json should be structured in the following format when getting list of files:
```
"filename/foldername": {
	type: "file/folder",
	size: 12341/12, // (bytes, count if file or folder)
	last_modified: "",
	last_modified_by: ""
}
```

## Examples:
```
"file1.txt": {
	type: "file",
	size: 1134321412,
	last_modified: "12 Jan 2022 8:59pm",
	last_modified_by: "Anonimous"
}, 
"songs": {
	type: "folder",
	size: 15,
	last_modified: "18th Feb 2023 7:08pm",
	last_modified_by: "Anonimous"
}, 
"data.pdf": {
	type: "file",
	size: 1100508,
	last_modified: "18th Aug 2019 12:45pm",
	last_modified_by: "Anonimous"
}
```