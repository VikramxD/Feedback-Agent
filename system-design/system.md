# Overall System 



## At A Glance 

Journaly is a mobile app, with data privacy as premium. The system comprise of a front end, that is a Flutter App, and back-end system which is essentially comprise of security,storage, and AI services. 



## Blocks 



### Mobile App 

For more see here.

<TODO ADD STUFF>

### Functional API Endpoints 

For more see here.

### Auth 

1. Create user 
2. Login 
3. Session Handling
4. Delete User  
5. De-Activate User



### User Profile

1. Base user dashboard data 

2. Metadata about user 

3. Personalization and configuration 

4. Speed Dial Configuration 

5. Create Custom Entity for emotional anchoring 

   

### Journaling 

1. Create journal entry 

2. Edit metadata of journal entry 

3. Get entries  

   1. Between time range 
   2. With emotions 
   3. With entities 

4. Free Text Meta Search 

### Analytics 

1.  Mood Circle Packing Diagram - over time
2.  Entity Mood Relation Diagram - over time 
3.  Numeric Stats - with badges 



### Event Driven Jobs 

Primarily, to process a voice jounral entry They run ML Tasks via `SQS`.

### ML Tasks  

For more see [here](../ml/ml-jobs.md).

1. Audio converter to `wav` 
2. Audio Emotion Analyzer 
3. Text Emotion Analyzer 
4. Text Named Entity Recognizer 
