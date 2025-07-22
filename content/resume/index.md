---
title: Work Corpus
toc: false
sidebar: left
---

##### *As of 1st June 2025*

### Raj Patil | raj@cognware.com

## Experience

###  Principal Engineer: ESDS Software Solutions
###### *March 2024 - Present*

 - Promoted into a more involved and expanded role geared towards optimizing their core product offering : [a Data Center Orchestrator](https://www.esds.co.in/enlight360)
 - Researching, designing, and developing cloud computing interfaces across the broader horizontal of Compute, Networking and Storage, along the full vertical of Data Center Orchestration (Hypervisors, DC Operations, Smart Racks, ... ) to Cloud Native operationalization (K8S, OKD, OpenShift ...)
 - Overseeing a growing interdisciplinary research lab that operates across domains : learning whatever the mission demands
    - further honing my collaboration acumen
 - Also invested in fostering a healthy engineering culture via:
   - self-hosting (volunteered for this to further deepen my understanding of the practicalities of DevOps) a somewhat distributed internal developer platform (stitching several open source projects), to make the lives of internal engineering teams (80 cumulative) easier.
   - hosting collaborative internal conferences and talks geared towards keeping the team up to date with SOTA
   - one of the technical proxies for inter-institutional (universities, research labs, industry) engineering collaboration
   - evangelizing [emacs](https://youtu.be/KsRCiL8ebmE) and [lisp](https://www.youtube.com/watch?v=guEbzVuYzPc)

### AI Engineer: ESDS Software Solutions
###### *Nov 2022 - March 2024*

 - Developed a comprehensive sentiment analysis portal from the ground up, focusing on customer satisfaction within the ticketing portal.
   - now crucial within the organization, used to quantify customer satisfaction and identify areas of improvement with regards to customer experience.
 - Headed AI integration across diverse departments, identifying and implementing multi-model pipelines (natural language processing, computer vision and traditional machine learning solutions)
 - Architected and engineered industry-scale AI solutions: the most prominent being School Education and Sports Department of Maharashtra, winning a [Guinness World Record](https://thebitmage.com/post/guinness-dedup-anomaly/), for
   which ESDS was the technical facilitator. 
 - Mentored individuals across domains, honing my managerial/leadership aptitude.

### Deliberate Hiatus
###### *Aug 2022 - Nov 2022*

 - Deliberate career break to realign my personal, career, health, and learning objectives
 - Overall health had taken a hit and needed to take a step back : later realized major underlying factor to be severe deficiencies in essential micronutrients

### Goldman Sachs: Analyst
###### *July 2022 - Aug 2022*

 - Briefly worked as a Strat in the Controllers Department, gaining valuable exposure to the financial industry.
 - Although a shorter engagement, gained insights into the organization and its operations.
 - Took a career break to address serious health concerns

### IIT Hyderabad | KLA Tencor: Research Assistant
###### *Aug 2021 - May 2022*

 - Collaborated with Prof. [Vineeth N.B.](https://people.iith.ac.in/vineethnb/index.html) on research to develop a generic transferability score for inter-domain transfer-learning tasks.
 - Focused on computer vision applications within chip technologies.
 - Leveraged knowledge in Domain Adaptation (Transfer Learning) to
   address relevant challenges.

### Goldman Sachs: Summer Analyst
###### *June 2021 - July 2021*

 - Worked towards enhancing (unsupervised) clustering interpretability.
 - Developed a versatile multidimensional hyperparameter grid search framework to automate model optimization and fine-tuning.
 - Was a remote engagement due to COVID-19 : valuable experience working with a distributed team

### CVPR 2021 Workshop paper | AUTONUE 2021 : Research Assistant
	
 - Part of the organizing team for a [domain adaptation challenge](http://cvit.iiit.ac.in/autonue2021/challenge/) for semantic segmentation, contributing to a workshop paper.
   - baselines available here : https://github.com/rajp152k/AUTONUE-III-Baselines
 - Guided and mentored by [Prof. Vineeth N.B.](https://people.iith.ac.in/vineethnb/index.html) and [Prof. C.V. Jawahar](https://faculty.iiit.ac.in/~jawahar/)
 - This is when I began using reverse chronological streams of work logs to serve as indices into progress

---

## Projects

| **Project**                                                                                                                                                                                        | **Synopsis**                                                                                                                                                                                                                                                                     | **Principal Domains**                         |
|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------|
| L1.epsilon | An agentic swarm geared toward assisting Level 1 support technicians  for swifter ticket resolution (integrating with self-hosted Data and Knowledge Bases via ReST, RAG, HITL, swarm orchestration) with ag2 (autogen fork) with end-to-end best-in-class swe practices : DDD + BDD + TDD with gherkin + pytest + pytest-bdd - levelling up my philosophical acumen for engineering with this one| Agentic-AI, Software Engineering |
| [Nth-Roam](https://github.com/rajp152k/nth-roam)                                                                                                                                                   | An [Emacs Package](https://youtu.be/EobRvrZpp1s?si=e7_LPfK-hZ4TvOkO) to efficiently manage multiple instances of emacs org-roam                                                                                                                                                  | Software Engineering                          |
| [fabric-gpt.el](https://github.com/rajp152k/fabric-gpt.el)                                                                                                                                         | An [Emacs Package](https://youtu.be/39OsH_OeWSA?si=xQLvotelXMECh9Lw) to employ crowd sourced prompts into an llm-client intuitively                                                                                                                                              | Software Engineering                          |
| Cloud Native LLM inference servers on heterogeneous compute infrastructure                                                                                                                         | Horizontally scaled self-hosted open source LLMs (OpenLLM, Kubernetes, nvidia-container-toolkit, VMWare ESXI) for serving LLMs (vLLMs) to the engineering and support teams on heterogeneous compute infrastructure (Nvidia (T4s & H100s), AMD (MI300Xs and MI300A), X86 and ARM) | (LLM:ML)Ops                                   |
| LLM Augmented Continuous Integration with self-hosted Gitlab                                                                                                                                       | Kubernetes to manage varied workers along with SOTA development and integration practices (Linting, Static and Dynamic Application Security Testing (SonarQube) along with LLM augmented security analysis (Ollama, Langchain, LlamaIndex))                                      | NLP, Dev(LLM:ML)Ops, CyberSecurity            |
| Cloud Native Web Application Firewall                                                                                                                                                              | Scalably productized(Kubernetes Horizontal Pod AutoScaler & Event Driven AutoScaler (KEDA : CNCF Grad)) and benchmarked(Apache bench) Coraza(an OWASP compliant Go WAF library)                                                                                                 | CyberSecurity                                 |
| [CLI timer](/post/cli-alarms)                                                                                                                                                                      | A bash function to save your soul                                                                                                                                                                                                                                                    | CLI-fu                                        |
| Storage Virtual Machine DR Replication Monitoring                                                                                                                                                   | Designed, developed and operationalized a golang microservice cluster to manage real time analytics streaming to be integrated into the existing observability stack (NetApp ONTAP, RabbitMQ, InfluxDB, Prometheus)                                                              | Real Time Observability                       |
| [Guinness world Record : Deduplication, Anomaly Detection, Tampering Detection](https://thebitmage.com/post/guinness-dedup-anomaly/)                                                               | context elaborated in blog link                                                                                                                                                                                                                                              | Computer Vision                               |
| Sentiment Analysis for Support Tickets                                                                                                                                                            | implemented a primal ETL, fine-tuned a Language Model (weakly-supervised) over a (pseudo-labelled) stratified subset, inference jobs formed integral part of business analysis crons                                                                                             | Natural Language Processing, Data Engineering |
| [Quantum Error Correction Codes](https://github.com/rajp152k/coursework_IITH/blob/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_8/Quantum_Computing/Quantum_Project.ipynb)                          | created a framework to test the efficacy of qubit allocation strategies for noise-resistant quantum computation                                                                                                                                                                      | Quantum Computing                             |
| [Tic-Tac-Toe Reinforcement Learning](https://github.com/rajp152k/coursework_IITH/blob/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_7/AI3000/A2/RL%20A2%20Q5.ipynb)                                 | tested out RL algorithms with random and heuristics-based agents                                                                                                                                                                                                                 | Reinforcement Learning                        |
| [Option Pricing via Monte Carlo Simulations](https://github.com/rajp152k/coursework_IITH/tree/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_7/MA4340/CS18BTECH11039_MA4340_PROJECT)                 | explored Monte Carlo option pricers, while comparing results with conventional stochastic calculus models (Black Scholes)                                                                                                                                                     | Stochastic Calculus                           |
| [Secure Multiparty Computation (for Deep Learning)](https://github.com/rajp152k/coursework_IITH/blob/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_7/CS6160/project/CS18BTECH11039_CS6160.pdf)      | Survey on how cryptographic techniques are used to maintain secrecy during multiparty computation (neural networks in this case)                                                                                                                                                 | Cryptography                                  |
| [WDGAF(We Do Give a Figure)](https://github.com/rajp152k/Compilers-II)                                                                                                                             | Created plotting DSL using principles of compilers and published it to pip                                                                                                                                                                                                       | Compilers                                     |
| [Relational Databases and Data Hygeine](https://github.com/rajp152k/coursework_IITH/tree/master/SEM_6/DBMSII)                                                                                      | Executed complex relational database queries on the IMDb movie database; implemented scraping scripts to fetch relevant data                                                                                                                                                     | Relational Databases                          |
| [Optimizing scheduling algorithms](https://github.com/rajp152k/coursework_IITH/blob/master/SEM_7/CS5280/CS5280%20cs18btech11039%20cs21resch11011/project_report_cs18btech11039_cs21resch11011.pdf) | researched tweaks to optimize the scheduling algorithms BOCC, BTO, MVTO                                                                                                                                                                                                     | Distributed Computing                         |
| [Musical Chairs: inter-process coms](https://github.com/rajp152k/musical_chairs)                                                                                                                   | Simulating a game of musical chairs using modern concurrency constructs from C++11 onwards                                                                                                                                                                                       | Concurrency                                   |
| [Chat Room App](https://github.com/rajp152k/coursework_IITH/tree/536c1a74dcb877ee25eeb7708652e6d8fcde8c02/SEM_5/Computer-Networks-I/socket%20programming/Computer-Networks)                        | created a command-line chat room app using principles of socket programming                                                                                                                                                                                                      | Computer Networks                             |
| [Custom Deep Learning Framework](https://github.com/rajp152k/cust_dl_lib)                                                                                                                          | created a deep learning library from scratch (axioms being high school math )                                                                                                                                                                                                    | Software Engineering                          |
| Calculator                                                                                                                                                                                         | wrote C to simulate the finite state machine on an ATmega16U2 (Arduino), designed and soldered the circuit (buttons, display, and the ATMega) on a veroboard, functional with add,mul,sub,div                                                                                    | Electronics                                   |
| 3D-printed pin ball machine                                                                                                                                                                        | first major project at IIT Hyderabad. designed the individual components from scratch in CAD and assembled the same (star wars themed - had a millenium falcon, a slide, a star trooper helmet and it came in black) into a functional pin ball setup                                                                                                                       | Computer Aided Design, Digital Fabrication                         |
| PLC HMI Design  | first explicit experience (in hindsight) with Finite State Machines when I was 14 as an Intern at [a local robotics firm](https://nashgroup.co.in/). analysed and reasoned about the states and corresponding control flows on programmable logic controllers.    | Digital System Design |


---

## Extracurricular


### Teaching Assistance

  - [Prof. Vineeth
    N.B.](https://people.iith.ac.in/vineethnb/index.html) - CS5590 :
    Foundations of Machine Learning 
  - [Prof Srijith
    P.K.](https://sites.google.com/site/pksrijith/home) - AI1100 :
    Introduction to Artificial Intelligence 

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


## Education 

### B.Tech:  **Indian Institute of Technology Hyderabad** (2018-2022)

	All India Rank (JEE Advance 2018) - 658

	- Major (2018-2022) : Computer Science and Engineering  : 9.26/10
	- Minor (2020-2022) : Artificial Intelligence           : 9.50/10

### *AutoDidacticism* (2000-Present)

 - reading, writing, thinking, conversations, teaching, disciplined curiosity and making mistakes play an essential role in how my learning trajectories unroll..
 - I'm not trying to build a career any more than I'm trying to explore the world epistemologically, in general
   - tbh, somewhat broken games are more fun than extremly structured ones ..
 - This was an index into major deliverables that might be societally gauge-able
 - As for my generic incentives, [this recursive-introspective terser composition](https://thebitmage.com/i-know-not/) is a summarization attempt
