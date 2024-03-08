---
title: "Project : Guinness World Record - Plaque and Announcement"
date: 2024-03-08T15:21:07+05:30
categories: ["Project"]
tags: ["project","world-record","guinness","deduplication","anomaly-detection","tampering-detection"]
---

ESDS Software Solutions Ltd. (where I work currently) was lately the
technical facilitator for the School Education Department of the
Government of Maharashtra, towards conducting a state level slogan
competition, the winner of which was rewarded by a lunch with the
chief minister of Maharashtra.  


## Brief Context 

One of the records (total of 3) they were going for was the most number of
handwritten notes uploaded to a bespoke platform in 24 hours.  

The scale of photos we were talking about is 1.4e6. Post the pipelines
we applied:  
 - a meta-data based deduplication filter  
 - an unsupervised anomaly detection filter (need to really have a
   handwritten note)  
 - a tampering detection filter (no editing - used
   Error level analysis)  
 
The final reported qualified collection was around 1.1e6 handwritten
notes which were verified and the record plaque was presented on 5th
of March 2024.  

The previous record was for around 1e4 images.  

---

## The Plaque

![the plaque](https://ik.imagekit.io/rajp152k/rpdev/Guinness%20world%20record%20dedup/gwr.png?updatedAt=1709893092012)

## The Announcement

{{< youtube "1qJ0PNDdi3c" >}}  
