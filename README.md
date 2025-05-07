# Nick's Bench Progress

## Progress: 9/47 tasks completed
<!-- Progress bar visual representation -->
![Progress](https://progress-bar.xyz/19/?scale=100&width=500&color=2EA043&suffix=%25)

## Progress: Udemy Ultimate AWS Certified Developer Associate 2025 DVA-C02
<!-- Progress bar visual representation -->
![Progress](https://progress-bar.xyz/15/?scale=100&width=500&color=2EA043&suffix=%25)

## Burndown Chart
![Burndown Chart](https://quickchart.io/chart?w=600&h=350&c={type:%27line%27,data:{labels:[%27Start%27,%27May%202%27,%27May%206%27,%27May%207%27,%27May%208%27,%27May%209%27,%27May%2012%27,%27May%2013%27,%27May%2014%27,%27May%2015%27,%27May%2016%27,%27May%2019%27,%27May%2020%27,%27May%2021%27,%27May%2022%27,%27May%2023%27],datasets:[{label:%27Ideal%27,data:[47,44,41,38,34,31,28,25,22,19,16,13,9,6,3,0],fill:false,borderColor:%27rgb(75,192,192)%27,tension:0.1,pointRadius:2},{label:%27Actual%27,data:[47,44,40,39,38,38,38,38,38,38,38,38,38,38,38,38],fill:false,borderColor:%27rgb(255,99,132)%27,tension:0.1,pointRadius:2}]},options:{title:{display:true,text:%27Task%20Burndown%20(47%20tasks,%2015%20Workdays%20to%20May%2023)%27},scales:{yAxes:[{ticks:{beginAtZero:true,suggestedMax:50},scaleLabel:{display:true,labelString:%27Tasks%20Remaining%27}}],xAxes:[{scaleLabel:{display:true,labelString:%27Date%20(Workdays)%27}}]}}})

# AWS Developer–Associate 90% Pass Probability Plan  
*(Workdays-only, starts May 2, preserves nights & weekends)*  

## Visual Calendar

| Week | Mon | Tue | Wed | Thu | Fri |
|------|-----|-----|-----|-----|-----|
| May<br>1-3 | | | | | • Read AWS Exam Guide<br>• Udemy kick-off<br>• Create Gap List |
| May<br>6-10 | *Vacation Day* | • Udemy Section 4 (IAM/CLI)<br>• Udemy Section 6 (EC2 Storage)<br>• Key takeaways | • Read Lambda Go docs<br>• Deploy "Hello Go" API<br>• Push to GitHub<br>• Udemy Section 10 (VPC) | • Watch DynamoDB video<br>• Implement Go CRUD<br>• Half-length quiz | • CodePipeline tutorial<br>• AWS SAM redeploy<br>• Commit templates |
| May<br>13-17 | • Whizlabs practice test<br>• Review sample questions<br>• Post score report | • EventBridge tutorial<br>• Add SQS/SNS fan-out | • Read AWS KMS sections<br>• IAM best practices<br>• Flash-card drill | • Tutorials Dojo Exam<br>• Score analysis | • Run system test<br>• Final review<br>• Prepare checklist |
| May<br>19‑23 | • Tutorials Dojo Practice Exam #1 (65 Q, 130 m)<br>• Review answers & update Gap List | • Whizlabs Full-length Exam #2 (65 Q, 130 m)<br>• Deep review & note-taking | • Re-watch weak-topic lectures<br>• Lab: CodeBuild + CodeDeploy mini-pipeline | • AWS Official Sample 20 Q — aim ≥ 90 %<br>• Quick labs on SQS/SNS/KMS | • 100-Q mixed quiz (TD)<br>• Final cheat-sheet consolidation<br>• Pearson Vue system test |
| May<br>26‑30 | **EXAM DAY**<br>• Sit AWS DVA-C02 exam<br>• Write reflection<br>• Plan next steps |  |  |  |  |

## Guiding Principles  
- **Pomodoro 25 / 5 cadence** → sustained concentration without fatigue.  
- **Visible progress** → log a short note or screenshot at day's end in this doc.  
- **Spaced repetition, not cramming** → review flash-cards after every module.  
- **Soft stop 4:30 p.m.** → evenings + weekends are family time.

---

## Fri May 2  
- [✅] 1. **Read the AWS Developer – Associate Exam Guide** — PDF download.  [oai_citation:0‡Amazon Web Services, Inc.](https://aws.amazon.com/certification/certified-developer-associate/?utm_source=chatgpt.com)  
- [✅] 2. **Udemy kick-off 20 of 490 completed
- [✅] 3. Create a **Gap List** page in this repo noting weak domains.

Notes: IAM-Identity and Access Management is a global service 

Gaps: Since I prevously was taking the course for practitioner, there is overlap, but not the 
depth required for my role. The developer content already feels much more apropriate. 

Projected course days remaining: 24 days. Expecting following days to pick up the pace
since I started the courses mid day. 

---

## Mon May 5  
*Vacation Day (Volunteered) *

---

## Tue May 6 
- [✅] 1. Udemy Section 4 – IAM & CLI 1 h 28 m 
- [✅] 2. Udemy Section 5 - EC2 Storage fundamentals. 2x speed review 
- [✅] 3. Udemy Section 6 – EC2 Storage 1 h 5 m
- [✅] 4. Complete the section quizzes and jot **key takeaways** for IAM and EC2 in your bench log. 

Key terms:

- Subnet: A contiguous range of IP addresses within a VPC
- VPC: Virtual Private Cloud - Isolated network environment in AWS
- Security groups: Virtual firewall that controls inbound and outbound traffic for AWS resources
- IAM: Identity and Access Management - AWS service for managing user access and permissions
- CLI: Command Line Interface - Tool for interacting with AWS services via command line
- EC2: Elastic Compute Cloud - Virtual servers in the cloud
- S3: Simple Storage Service - Object storage service for storing and retrieving data
- Classic ports to know: 22 SSH and secure FTP, 21 FTP, 80 HTTP, 443 HTTPS, 3389 RDP (Remote Desktop Protocol for Windows)
- IPAM: IP Address Manager - Helps to plan, track and manage IP addresses for workloads and on-prem networks
- Local EC2 Instance Store: High performance temporary block-level storage
- IOPS: Input/Output Operations Per Second - Measure of storage performance
- EBS: Elastic Block Storage - Persistent block storage volumes for EC2 instances
    - gp2 General Purpose SSD (older generation)
        - Baseline of 3 IOPS/GiB, up to 16,000 IOPS per volume
        - Volume size 1 GiB to 16 TiB
        - Burst up to 3,000 IOPS
        - Good for boot volumes, dev/test environments
    - gp3 General Purpose SSD (current generation)
        - Baseline 3,000 IOPS and 125 MiB/s throughput
        - Can increase up to 16,000 IOPS and 1,000 MiB/s throughput
        - Independent scaling of IOPS and throughput
        - 20% cheaper than gp2
    - io1/io2 Provisioned IOPS SSD
        - Highest performance SSD volume
        - Up to 64,000 IOPS per volume
        - io2 is more durable and more IOPS per GiB
    - st1 Throughput Optimized HDD
        - Low-cost HDD volume
        - Baseline throughput of 40 MB/s per TB
        - Burst up to 250 MB/s per TB
        - Good for big data, data warehouses, log processing
    - sc1 Cold HDD
        - Lowest cost HDD volume
        - Base 12 MB/s per TB
        - Burst up to 80 MB/s per TB
        - Good for infrequently accessed data
- EFS: Elastic File System - Scalable, fully managed NFS file system
---

## Wed May 7  —  ✳ Deep-study + Lab  
- [✅] 1. ✳ **Udemy Section 10 – VPC Fundamentals** (≈ 0.6 h)  
- [ ] 2. **Read Lambda Go runtime docs** (≈ 15 m) — [oai_citation:3‡AWS Documentation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-golang.html?utm_source=chatgpt.com)  
- [ ] 3. **Deploy "Hello Go" API (API Gateway + Lambda)** (≈ 50 m) — [oai_citation:4‡Medium](https://medium.com/%40hrshh17softdev/serverless-rest-apis-in-go-using-aws-api-gateway-lambda-dynamodb-cd04d938c421?utm_source=chatgpt.com)  
- [ ] 4. Push working code + endpoint URL to GitHub and link it in Confluence.

## Thu May 8  —  ✳ + ⏩  
- [ ] 1. ✳ **Udemy Section 11 – Amazon S3 Intro** (≈ 2.1 h)  
- [ ] 2. ⏩ **Udemy Section 8 – AWS Fundamentals: RDS + Aurora + ElastiCache** (≈ 0.8 h)  
- [✅] 3. ⏩ **Udemy Section 7 – ELB & Auto-Scaling** (≈ 1.2 h)  

## Fri May 9  —  ✳ + ⏩  
- [ ] 1. ✳ **Udemy Section 12 – DynamoDB & Databases** (≈ 2.6 h)  
- [ ] 2. ⏩ **Udemy Section 9 – ECS / Docker & ECR** (≈ 1.2 h)  
- [ ] 3. **Watch "Getting Started with Amazon DynamoDB"** (≈ 43 m) — [oai_citation:5‡YouTube](https://www.youtube.com/watch?v=2k2GINpO308&utm_source=chatgpt.com)  
- [ ] 4. **Implement CRUD in Go (AWS SDK v2)** (≈ 1 h 20 m) — [oai_citation:6‡AWS Documentation](https://docs.aws.amazon.com/code-library/latest/ug/go_2_dynamodb_code_examples.html?utm_source=chatgpt.com)  
- [ ] 5. **Take the 22-question DynamoDB quiz; aim ≥ 70 %** (≈ 15 m)

## Mon May 12  —  ✳ + ⏩  
- [ ] 1. ✳ **Udemy Section 13 – SQS / SNS Messaging** (≈ 2.0 h)  
- [ ] 2. ⏩ **Udemy Section 16 – Step Functions** (≈ 0.75 h)  
- [ ] 3. **Amazon EventBridge hands-on tutorial; trigger Lambda** (≈ 1 h) — [oai_citation:11‡AWS Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-tutorial.html?utm_source=chatgpt.com)

## Tue May 13  —  ✳ Focus Day  
- [ ] 1. ✳ **Udemy Section 14 – AWS Lambda Deep Dive** (≈ 3.1 h)  
- [ ] 2. **Re-deploy Lambda via AWS SAM** (≈ 0.5 h) — [oai_citation:8‡AWS Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html?utm_source=chatgpt.com)

## Wed May 14  —  ✳ + ⏩  
- [ ] 1. ✳ **Udemy Section 15 – API Gateway** (≈ 2.0 h)  
- [ ] 2. ⏩ **Udemy Section 19 – Monitoring & X-Ray** (≈ 0.8 h)  
- [ ] 3. **Review CloudWatch logs for Hello-Go API** (≈ 0.3 h)

## Thu May 15  —  ✳ Double Deployment  
- [ ] 1. ✳ **Udemy Section 17 – Developer Tools (CI/CD)** (≈ 2.3 h)  
- [ ] 2. ✳ **Udemy Section 18 – SAM & CloudFormation** (≈ 1.8 h)  
- [ ] 3. **Commit updated pipeline YAML & SAM templates** (≈ 0.3 h)

## Fri May 16  —  ✳ Security + Practice  
- [ ] 1. ✳ **Udemy Section 20 – KMS, Encryption & Secrets** (≈ 1.6 h)  
- [ ] 2. **Whizlabs 20-Q + AWS sample 15-Q** (≈ 1.0 h) — [oai_citation:9‡Whizlabs](https://www.whizlabs.com/aws-developer-associate/?utm_source=chatgpt.com)  
- [ ] 3. **Flash-card review of weak areas** (≈ 0.5 h)

## Mon May 19— Practice Exam  
- [ ] 1. Tutorials Dojo Practice Exam #1 (65 Q, 130 m)  
- [ ] 2. Deep review of each missed question  
- [ ] 3. Update Gap List & flash-card deck  

## Tue May 20— Practice Exam  
- [ ] 1. Whizlabs Full-length Exam #2 (65 Q, 130 m)  
- [ ] 2. Categorise errors by service domain  
- [ ] 3. Re-watch related Udemy lessons  

## Wed May 21— Weak-Topic Workshop  
- [ ] 1. Re-watch VPC, KMS, and Elastic Beanstalk deep dives  
- [ ] 2. Lab: build CI/CD demo with CodeBuild + CodeDeploy  
- [ ] 3. Retake failed quiz questions  

## Thu May 22— Confidence Builder  
- [ ] 1. AWS Official Sample Questions (20 Q) — target ≥ 90 %  
- [ ] 2. Quick labs: SQS queue fan-out, SNS filtering, KMS envelope encryption  
- [ ] 3. Flash-card speed-run  

## Fri May 23— Final Review  
- [ ] 1. 100-question mixed quiz (Tutorials Dojo) — target ≥ 85 %  
- [ ] 2. Consolidate last-minute cheat-sheet  
- [ ] 3. Pearson Vue system test & logistics check  

## Contingency  
*If any full-length practice score is below 70 % by **May 22**, reschedule the exam to the week of **June 2** (voucher reschedule is free).*  

## Burnout Safeguards  
- 5-min walk + hydration every two Pomodoros.  
- Box-breathing if anxiety spikes.  
- Friday Loom recap instead of late-night catch-up coding.

## After the Exam  
- Migrate first two IoT Cloud Functions from JavaScript to Go during the week of May 19.  
- Begin drafting the **"Kunai Serverless Starter Kit"** repo & Terraform scripts.

---