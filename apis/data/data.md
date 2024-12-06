# Data API 

## Curl Commands 

### File Upload 

```shell
curl -T <audio-file> "http://localhost:4242/entry/u42"
```

### Check User Entries 

```shell
curl -XPOST "http://localhost:4242/meta/entries/u42" -d '{ "from" : <from-time-in-ms> , "to" :  <to-time-in-ms> }'
```



## How it Works?

### Upload End Point 

File Gets stored in UTC time stamp with  `bucket:raw/yyyy/MM/dd/HH/mm/file-uid-(user_urn).bin` 
as the path to the actual file. 

### Batch Job 

Given this a batch job runs every minute to process all files which got accumulated
in the previous minute. This batch job would create a file :

1. `bucket:raw/yyyy/MM/dd/HH/mm/done` when completed the minute.
2. `bucket:raw/yyyy/MM/dd/HH/mm/part.txt` where it would maintain the file name it is currently working on.

These jobs would be multiple processes run using shell.
Once a particular file would be completed - the job would create a `json` file as follows:

```json
{
  "uurn" : "user_urn",
  "surn" : "file-uid",
  "src" : "bucket:raw/yyyy/MM/dd/HH/mm/file-uid-(user_urn).bin" ,
  "text" : "blabbering of the individual, voice converted to text",
  "entities" : [ "a" , "b" , "c" ], 
  "emotions" : {
    "audio" : [ "a", "b", "c" ],
    "text" : [ "a", "b", "e"]
  },
  "at" : "processing timestamp"
}
```
And would call the `/meta/:user_id` end point to upload the data.

### Meta Update End point

This can effectively run on a versioned storage.
This stores the information in here: `bucket:user_urn/meta/yyyy/MM/dd/file-uid.json` 
One can chose to overwrite it and edit as many time as one can, versions will be stored

### Entries Reading End Point

We simply read from : `bucket:user_urn/meta/yyyy/MM/dd/*` 
Our minimum reading granularity is one day. 
Given our use case at max we would not have more than 2/3 entries a day, 
A complete month worth read would yield only `~100` entries.

### Single Reading Voice Record
