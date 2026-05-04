Untitled


---
date: <% tp.file.creation_date() %>
type: meeting
company: 
summary:
---
tags: [[🗣 Meetings MOC]]
Date: [[<% tp.date.now("YYYY-MM-DD-dddd") %>]]
<%*const moment = tp.date.now("YYYY/MM-MMMM");
const folder = `Meetings/${moment}`;
const fileName = tp.date.now("MM-DD-dddd") + " " + tp.file.title;

const filePath = `${folder}/${fileName}`;
await tp.file.move(filePath);
await tp.file.rename(fileName)%>

# [[<% tp.date.now("YYYY-MM-DD") + " " + tp.file.title %>]]

**Attendees**: 
- 

## Agenda/Questions
- 

## Notes
- 