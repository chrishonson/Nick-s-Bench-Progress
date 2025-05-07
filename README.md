# Nick's Bench Progress

## Progress: 7/34 tasks completed
<!-- Progress bar visual representation -->
![Progress](https://progress-bar.xyz/20/?scale=100&width=500&color=2EA043&suffix=%25)

## Progress: Udemy Ultimate AWS Certified Developer Associate 2025 DVA-C02
<!-- Progress bar visual representation -->
![Progress](https://progress-bar.xyz/10/?scale=100&width=500&color=2EA043&suffix=%25)


# AWS Developer–Associate Fast-Track Plan  
*(Workdays-only, starts May 2, preserves nights & weekends)*  

## Visual Calendar

| Week | Mon | Tue | Wed | Thu | Fri |
|------|-----|-----|-----|-----|-----|
| May<br>1-3 | | | | | • Read AWS Exam Guide<br>• Udemy kick-off<br>• Create Gap List |
| May<br>6-10 | *Vacation Day* | • Udemy Section 4 (IAM/CLI)<br>• Udemy Section 6 (EC2 Storage)<br>• Key takeaways | • Read Lambda Go docs<br>• Deploy "Hello Go" API<br>• Push to GitHub<br>• Udemy Section 10 (VPC) | • Watch DynamoDB video<br>• Implement Go CRUD<br>• Half-length quiz | • CodePipeline tutorial<br>• AWS SAM redeploy<br>• Commit templates |
| May<br>13-17 | • Whizlabs practice test<br>• Review sample questions<br>• Post score report | • EventBridge tutorial<br>• Add SQS/SNS fan-out | • Read AWS KMS sections<br>• IAM best practices<br>• Flash-card drill | • Tutorials Dojo Exam<br>• Score analysis | • Run system test<br>• Final review<br>• Prepare checklist |
| May<br>19-24 | **EXAM DAY**<br>• Sit AWS DVA-C02 exam<br>• Write reflection<br>• Plan next steps | | | | |

## Guiding Principles  
- **Pomodoro 25 / 5 cadence** → sustained concentration without fatigue.  
- **Visible progress** → log a short note or screenshot at day's end in this doc.  
- **Spaced repetition, not cramming** → review flash-cards after every module.  
- **Soft stop 4:30 p.m.** → evenings + weekends are family time.

---

## Fri May 2  
- [✅] 1. **Read the AWS Developer – Associate Exam Guide** — PDF download.  [oai_citation:0‡Amazon Web Services, Inc.](https://aws.amazon.com/certification/certified-developer-associate/?utm_source=chatgpt.com)  
- [✅] 2. **Udemy kick‑off 20 of 490 completed
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

## Wed May 7  
- [ ] 1. **Read the Lambda Go runtime docs** 15m [oai_citation:3‡AWS Documentation](https://docs.aws.amazon.com/lambda/latest/dg/lambda-golang.html?utm_source=chatgpt.com)  
- [ ] 2. Follow this Medium guide to **deploy a "Hello Go" API (API Gateway + Lambda) 50m **.  [oai_citation:4‡Medium](https://medium.com/%40hrshh17softdev/serverless-rest-apis-in-go-using-aws-api-gateway-lambda-dynamodb-cd04d938c421?utm_source=chatgpt.com)  
- [ ] 3. Push working code + endpoint URL to GitHub, link it in Confluence.
- [ ] 4. Udemy Section 10 – VPC Fundamentals 1 h 34 m 

---

## Thu May 8  
- [ ] 1. **Watch "Getting Started with Amazon DynamoDB"** 43m (YouTube workshop).  [oai_citation:5‡YouTube](https://www.youtube.com/watch?v=2k2GINpO308&utm_source=chatgpt.com)  
- [ ] 2. **Implement CRUD in Go** using AWS SDK v2 examples. 1h 20m  [oai_citation:6‡AWS Documentation](https://docs.aws.amazon.com/code-library/latest/ug/go_2_dynamodb_code_examples.html?utm_source=chatgpt.com)  
- [ ] 3. Take the 22-question half-length quiz; aim ≥ 70 %. Record your score. 15m

---

## Fri May 9  
- [ ] 1. Walk through the **CodePipeline blue-green deployment tutorial**.  [oai_citation:7‡AWS Documentation](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-ECSbluegreen.html?utm_source=chatgpt.com)  
- [ ] 2. Use the **AWS SAM "Getting Started" guide** to redeploy yesterday's Lambda.  [oai_citation:8‡AWS Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html?utm_source=chatgpt.com)  
- [ ] 3. Commit pipeline YAML and SAM template to GitHub.

---

## Mon May 12  
- [ ] 1. Sit the **Whizlabs free Developer-Associate practice test** in timed mode.  [oai_citation:9‡Whizlabs](https://www.whizlabs.com/aws-developer-associate/?utm_source=chatgpt.com)  
- [ ] 2. Review the **official AWS sample questions** PDF.  [oai_citation:10‡Amazon Web Services, Inc.](https://aws.amazon.com/certification/certified-developer-associate/?utm_source=chatgpt.com)  
- [ ] 3. Post your score report + remediation list.

---

## Tue May 13  
- [ ] 1. Complete the **Amazon EventBridge hands-on tutorial**; wire a rule to trigger your Lambda.  [oai_citation:11‡AWS Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-tutorial.html?utm_source=chatgpt.com)  
- [ ] 2. Add SQS or SNS to fan-out events; upload an architecture diagram.

---

## Wed May 14  
- [ ] 1. Read the key sections on **AWS KMS (CMKs vs. AWS-managed keys)**.  [oai_citation:12‡AWS Documentation](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html?utm_source=chatgpt.com)  
- [ ] 2. Re-read **IAM security best practices** and turn key points into flash-cards.  [oai_citation:13‡AWS Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html?utm_source=chatgpt.com)  
- [ ] 3. Drill flash-cards for 20 min (spaced repetition).

---

## Thu May 15  
- [ ] 1. Purchase (with stipend) and take **Tutorials Dojo Practice Exam Set #2** in exam mode.  [oai_citation:14‡Tutorials Dojo](https://tutorialsdojo.com/courses/aws-certified-developer-associate-practice-exams/?utm_source=chatgpt.com)  
- [ ] 2. Aim for ≥ 75 %. If < 65 %, flag for a reschedule decision.  
- [ ] 3. Record score + weak-domain analytics.

---

## Fri May 16  
- [ ] 1. Run the **Pearson VUE OnVUE system-test** to verify webcam, bandwidth, room setup.  [oai_citation:15‡Pearson VUE](https://www.pearsonvue.com/us/en/test-takers/onvue-online-proctoring.html?utm_source=chatgpt.com)  
- [ ] 2. Light review: skim notes, gap list, and flash-cards.  
- [ ] 3. Prepare the readiness checklist (ID, clean desk, allowed items).

---

## Mon May 19 — **EXAM DAY**  
- [ ] 1. **Sit the AWS DVA-C02 exam** (morning slot).  
- [ ] 2. Afternoon: write a reflection—what went well, what to improve—and post pass/fail summary.  
- [ ] 3. Close the sprint: plan next-week kickoff for the Go-migration spike.

## Contingency  
If any full practice score < 65 % by May 14, reschedule the exam to the week of May 20 (APN voucher reschedule is free).

## Burnout Safeguards  
- 5-min walk + hydration every two Pomodoros.  
- Box-breathing if anxiety spikes.  
- Friday Loom recap instead of late-night catch-up coding.

## After the Exam  
- Migrate first two IoT Cloud Functions from JavaScript to Go during the week of May 19.  
- Begin drafting the **"Kunai Serverless Starter Kit"** repo & Terraform scripts.

---
*Document last updated: May 5 2025*