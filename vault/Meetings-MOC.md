[[+Home]] %% tags:: #MOC %% 

# Meetings MOC
Meetings are timestamped events with other people, where information is exchanged and collected. Meeting notes are intrinsically ephemeral. They're stored in a separate Space than other Umami notes (`Timestamps/Meetings`) and rarely reviewed. If there's information in a meeting that needs to be accessed later, it should be moved into a more evergreen note in the Umami folder. 

**Template:** [[Template, Meeting]]


```meta-bind-button
label: NewMeeting3
icon: ""
style: default
class: ""
cssStyle: ""
backgroundImage: ""
tooltip: ""
id: ""
hidden: false
actions:
  - type: templaterCreateNote
    templateFile: 000 Templates/Template-Meeting-Note2.md
    folderPath: Meetings
    fileName: TKTK
    openNote: true
    openIfAlreadyExists: false

```


## Meeting Notes

```dataview
TABLE file.cday as Created, summary
FROM "Meetings" and -#MOC
SORT file.cday DESC
```