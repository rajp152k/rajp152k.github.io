---
title: Work Corpus
toc: false
sidebar: left
---

---

#### **RESUME.JSON**

For the programmatically enabled out there, here's a [js object](/resume/resume.json) for you to parse my work into tools of your choice.  

[jq](https://jqlang.github.io/jq/) is a decent start:  

```
curl -s https://thebitmage.com/resume/resume.json | jq -C
```

[Fabric](https://github.com/danielmiessler/fabric) is great if you have it handy:  

```
curl -s https://thebitmage.com/resume/resume.json | fabric -s --pattern  create_summary 
```

---

##### *As of 14th Oct 2024*

### Raj Patil | raj@thebitmage.com

## Experience

###  Principal Engineer: ESDS Software Solutions
###### *March 2024 - Present*

 - principally researching and developing applications of AI and ML targeted towards IT Operations - AIOps.
 - overseeing an interdisciplinary research lab that operates across domains: AI, IOT, Cyber-Security, and more.

### AI Engineer: ESDS Software Solutions
###### *Nov 2022 - March 2024*

 - developed a comprehensive sentiment analysis portal from the ground up, focusing on customer satisfaction within the ticketing portal.
   - now crucial within the organization, used to quantify customer satisfaction and identify areas of improvement with regards to customer experience.
 - headed AI integration across diverse departments, identifying and implementing multi-model pipelines (natural language processing, computer vision and traditional machine learning solutions)
 - served multiple client facing AI-related requests, most promiment of which resulted in the [School Education and Sports Department of Maharashtra](https://education.maharashtra.gov.in/sanch/users) winning a [Guinness World Record](https://thebitmage.com/post/guinness-dedup-anomaly/), for
   which ESDS was the technical facilitator. 
 - Mentored individuals across domains and began honing my managerial/leadership aptitude.

### Personal Sabbatical
###### *Aug 2022 - Nov 2022*

 - deliberate decision to take a hiatus to address health concerns
   - context: diagnosed with severe deficiencies in several micronutrients and minerals.
 - delved in several epistemological works to further my personal intellectual pursuits.

### Goldman Sachs: Analyst
###### *July 2022 - Aug 2022*

 - briefly worked as an Analyst at Goldman Sachs, gaining valuable exposure to the financial industry.
 - Although a shorter engagement, had the opportunity to gain insights into the organization and its operations.

### IIT Hyderabad | KLA Tencor: Research Assistant
###### *Aug 2021 - May 2022*

 - Collaborated with Prof. [Vineeth N.B.](https://people.iith.ac.in/vineethnb/index.html) on research to develop a generic transferability score for inter-domain transfer-learning tasks.
 - Focused on computer vision applications within chip technologies.
 - Leveraged knowledge in Domain Adaptation (Transfer Learning) to
   address relevant challenges.

### Goldman Sachs: Summer Analyst
###### *June 2021 - July 2021*

 - worked towards enhancing (unsupervised) clustering interpretability.
 - developed a versatile multidimensional hyperparameter grid search framework to automate model optimization and fine-tuning.

### CVPR 2021 Workshop paper | AUTONUE 2021 : Research Assistant
	
 - organized a [domain adaptation challenge](http://cvit.iiit.ac.in/autonue2021/challenge/) for semantic segmentation, contributing to a workshop paper.
 - Guided and mentored by [Prof. Vineeth N.B.](https://people.iith.ac.in/vineethnb/index.html) and [Prof. C.V. Jawahar](https://faculty.iiit.ac.in/~jawahar/)

---

## Projects

| **Project**                                                                                                                                                                                        | **Synopsis**                                                                                                                                                                                  | **Principal Domains**                         |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| [Guinness world Record : Deduplication, Anomaly Detection, Tampering Detection](https://thebitmage.com/post/guinness-dedup-anomaly/)                                                               | checkout blog link for more context                                                                                                                                                           | Computer Vision                               |
| Sentinment Analysis for Support Tickets                                                                                                                                                            | implemented a primal ETL, fine-tuned a Language Model (weakly-supervised) over a (psuedo-labelled) stratified subset, inference jobs formed integral part of business analysis crons                                          | Natural Language Processing, Data Engineering |
| [Quantum Error Correction Codes](https://github.com/rajp152k/coursework_IITH/blob/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_8/Quantum_Computing/Quantum_Project.ipynb)                          | created a framework to test efficacy of qubit allocation strategies for noise-resistant quantum computation                                                                                   | Quantum Computing                             |
| [Tic-Tac-Toe Reinforcement Learning](https://github.com/rajp152k/coursework_IITH/blob/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_7/AI3000/A2/RL%20A2%20Q5.ipynb)                                 | tested out RL algorithms with random and heuristics based agents                                                                                                                              | Reinforcement Learning                        |
| [Option Pricing via Monte Carlo Simulations](https://github.com/rajp152k/coursework_IITH/tree/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_7/MA4340/CS18BTECH11039_MA4340_PROJECT)                 | delved into monte carlo option pricers, while comparing results with conventional stochastic calculus models (Black Scholes)                                                                  | Stochastic Calculus                           |
| [Secure Multiparty Computation (for Deep Learning)](https://github.com/rajp152k/coursework_IITH/blob/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_7/CS6160/project/CS18BTECH11039_CS6160.pdf)      | Survey on how cryptographic techniques are used to maintain secrecy during multiparty computation (neural networks in this case)                                                              | Cryptography                                  |
| [WDGAF(We Do Give a Figure)](https://github.com/rajp152k/Compilers-II)                                                                                                                             | Created plotting DSL using principals of compilers and published it to pip                                                                                                                    | Compilers                                     |
| [Relational Databases and Data Hygeine](https://github.com/rajp152k/coursework_IITH/tree/master/SEM_6/DBMSII)                                                                                      | Executed complex relational database queries on the imdb movie database; implemented scraping scripts to fetch relevant data                                                                  | Relational Databases                          |
| [Optimizing scheduling algorithms](https://github.com/rajp152k/coursework_IITH/blob/master/SEM_7/CS5280/CS5280%20cs18btech11039%20cs21resch11011/project_report_cs18btech11039_cs21resch11011.pdf) | researched into tweaks to optimize the scheduling algorithms BOCC, BTO, MVTO                                                                                                                  | Distributed Computing                         |
| [Musical Chairs: inter-process coms](https://github.com/rajp152k/musical_chairs)                                                                                                                   | Simulating a game of musical chairs using modern concurrency constructs from C++11 onwards                                                                                                    | Concurrency                                   |
| [Chat Room App](https://github.com/rajp152k/coursework_IITH/tree/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_5/Computer-Networks-I/socket%20programming/Computer-Networks)                        | created a command line chat room app using principles of socket programming                                                                                                                   | Computer Networks                             |
| [Custom Deep Learning Framework](https://github.com/rajp152k/cust_dl_lib)                                                                                                                          | created a deep learning library from scratch (axioms being high school math )                                                                                                                 | Software Engineering                          |
| Calculator                                                                                                                                                                                         | wrote C to simulate the finite state machine on an ATmega16U2 (Arduino), designed and soldered the circuit (buttons, display, and the ATMega) on a veroboard, functional with add,mul,sub,div | Electronics                                   |
| 3D-printed pin ball machine                                                                                                                                                                        | designed the individual components from scratch in CAD and assembled the same (star wars themed - had a millenium falcon) into a functional pin ball setup                                    | Computer Aided Design                         |

---

## Extracurricular


### Teaching Assistance

  - [Prof. Vineeth
    N.B.](https://people.iith.ac.in/vineethnb/index.html) - CS5590 :
    Foundations of Machine Learning 
  - [Prof Srijith
    P.K.](https://sites.google.com/site/pksrijith/home) - AI1100 :
    Intro to Artificial Intelligence 

### [FitSoc](https://instagram.com/fitsoc_iith) 2021-2022

 - Established a fitness community dedicated to supporting college students in balancing their fitness and academic pursuits through a hybrid athleticism approach.
 - Organically bootstrapped and grew the community, currently comprising over 200 active members.

### Founding Core Member [Epoch](https://github.com/IITH-Epoch) (The ML club of IIT Hyderabad) - 2019

 - Conducted the [inaugural session](https://github.com/IITH-Epoch/Session-1-2019-10-03) of the club.
 - The session centered on exploratory data analysis utilizing key
   tools and libraries, including Pandas, NumPy, SciPy and matplotlib.

### National Service Scheme

 - participated in several cleanliness and plantation drives during my
   time at IIT-Hyderabad
 - created several social awareness posters regarding various societal
   issues

---

## Conferences Attended

This should serve as a quick index into my networking interests during phases of my career

| Conf                                                               | When               | Where         | My Focus and Incentives             |
|--------------------------------------------------------------------|--------------------|---------------|-------------------------------------|
| [NVIDIA AI Summit](https://www.nvidia.com/en-in/events/ai-summit/) | October 24-25 2024 | Mumbai, India | Successful LLMs in Prod, Networking |


## Education 

### B.Tech:  **Indian Institute of Technology Hyderabad** (2018-2022)

	All India Rank (JEE Advance 2018) - 658

	- Major (2018-2022) : Computer Science and Engineering  : 9.26/10
	- Minor (2020-2022) : Artificial Intelligence           : 9.50/10
 
---

### Further Musings

This is an index into my major deliverables that society might consider to be of relevance.
There are several non-incentivised musings and works that I keep myself occupied with: they have been indexed in the [ideation buffer](https://buffer.thebitmage.com)

As for my generic incentives, you'd find [this recursive-introspective terser composition](https://thebitmage.com/i-know-not/) to be a humble attempt towards expressing the same.

