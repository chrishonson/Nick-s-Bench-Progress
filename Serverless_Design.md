

## Simple Example Lambda Arch
```mermaid
graph TD
    subgraph "AWS Account"
        Lambda[AWS Lambda Function]

        subgraph VPCNetwork["Your VPC Private Network"]
            direction LR
            subgraph PrivateSubnet["Private Subnet"]
                Lambda_ENI[Lambda ENI Private IP]
                DB[Database Private IP]
            end
            NAT[NAT Gateway Optional for Internet]
        end

        Internet([Internet External APIs])
    end

    Lambda -->|Uses| Lambda_ENI
    Lambda_ENI -->|Private Connection| DB
    Lambda_ENI -->|If needed| NAT
    NAT --> Internet

    style Lambda fill:#FF9900,stroke:#333,stroke-width:2px
    style Lambda_ENI fill:#FFD700,stroke:#333,stroke-width:2px
    style DB fill:#ADD8E6,stroke:#333,stroke-width:2px
    style NAT fill:#90EE90,stroke:#333,stroke-width:2px
    style VPCNetwork fill:#f0f8ff,stroke:#ccc,stroke-width:2px
    style PrivateSubnet fill:#e6e6fa,stroke:#ccc,stroke-width:1px

```

## More Complete Example Lambda Arch
```mermaid

graph TD
    subgraph AWS_Cloud ["AWS Cloud"]
        subgraph Lambda_Service_Env [Lambda Service Environment]
            Lambda["AWS Lambda Function (Execution Role)"]
            SG_Lambda[SG: Lambda ENIs]
        end

        subgraph VPC_Network ["User's VPC"]
            direction LR

            subgraph AZ_A ["Availability Zone A"]
                direction TB
                subgraph PVT_SUBNET_A ["Private Subnet A"]
                    ENI_A["Lambda ENI 1 (Private IP)"]
                    RDS_A["RDS Instance (Private IP)"]
                end
                SG_DB[SG: RDS]

                ENI_A -->|Access via Private IP| RDS_A
                RDS_A -.-> SG_DB
                ENI_A -.-> SG_Lambda
            end

            subgraph AZ_B ["Availability Zone B"]
                direction TB
                subgraph PVT_SUBNET_B ["Private Subnet B"]
                    ENI_B["Lambda ENI 2 (Private IP)"]
                    EC_B["ElastiCache Node (Private IP)"]
                end
                SG_CACHE[SG: ElastiCache]

                ENI_B -->|Access via Private IP| EC_B
                EC_B -.-> SG_CACHE
                ENI_B -.-> SG_Lambda
            end

            subgraph Public_Subnet_Zone ["Public Subnet(s)"]
                 direction TB
                 subgraph PUB_SUBNET_C ["Public Subnet C"]
                    NAT_GW["NAT Gateway (Elastic IP)"]
                 end
            end

            IGW[Internet Gateway]
            S3_VPCE[S3 VPC Gateway Endpoint]

            %% Routing
            PVT_SUBNET_A -->|Route to Internet via| NAT_GW
            PVT_SUBNET_B -->|Route to Internet via| NAT_GW
            PVT_SUBNET_A -->|Route to S3 via| S3_VPCE
            PVT_SUBNET_B -->|Route to S3 via| S3_VPCE
            NAT_GW --> IGW
            IGW --> Internet(["Internet/External APIs"])
            S3_VPCE --> S3[Amazon S3 Service]

        end

        Lambda -->|Configured for VPC| ENI_A
        Lambda -->|Configured for VPC| ENI_B
    end

    %% Styling
    style AWS_Cloud fill:#f9f9f9,stroke:#333,stroke-width:2px
    style Lambda_Service_Env fill:#fff0e6,stroke:#333,stroke-width:1px
    style VPC_Network fill:#e6f3ff,stroke:#333,stroke-width:1px
    style AZ_A fill:#d4e1f5,stroke:#333,stroke-width:1px
    style AZ_B fill:#d4e1f5,stroke:#333,stroke-width:1px
    style Public_Subnet_Zone fill:#fde2e2,stroke:#333,stroke-width:1px

    style PVT_SUBNET_A fill:#d9ead3,stroke:#333
    style PVT_SUBNET_B fill:#d9ead3,stroke:#333
    style PUB_SUBNET_C fill:#fce5cd,stroke:#333

    style Lambda fill:#ffcc99
    style ENI_A fill:#c9daf8
    style ENI_B fill:#c9daf8
    style RDS_A fill:#b4a7d6
    style EC_B fill:#b4a7d6
    style NAT_GW fill:#fff2cc
    style IGW fill:#e6b8af
    style Internet fill:#d9d9d9
    style S3_VPCE fill:#d0e0e3
    style S3 fill:#a2c4c9

    style SG_DB fill:#f4cccc
    style SG_CACHE fill:#f4cccc
    style SG_Lambda fill:#f4cccc
```

### 1. Route Table for Private Subnets (PVT_SUBNET_A and PVT_SUBNET_B)

These subnets house your Lambda ENIs (ENI_A, ENI_B), the RDS instance (RDS_A), and the ElastiCache node (EC_B). They need to:
Access other resources within the VPC.
Reach the internet via the NAT Gateway.
Access Amazon S3 via the S3 VPC Gateway Endpoint.
The route table associated with PVT_SUBNET_A and PVT_SUBNET_B would have the following entries:
| Destination | Target | Purpose |
| :----------------- | :------------------------------------- | :---------------------------------------------------------------------- |
| 10.0.0.0/16 | local | Enables communication with all resources within the VPC. |
| 0.0.0.0/0 | nat-xxxxxxxx (ID of your NAT Gateway NAT_GW) | Routes all other outbound traffic (to the internet) to the NAT Gateway. |
| pl-yyyyyyyy (S3 Prefix List) | vpce-zzzzzzzz (ID of your S3 VPC Endpoint S3_VPCE) | Routes traffic destined for Amazon S3 to the S3 VPC Gateway Endpoint. |
- pl-yyyyyyyy: This is an AWS-managed prefix list ID that represents the IP address ranges for Amazon S3 in that specific AWS Region.

### 2. Route Table for the Public Subnet (PUB_SUBNET_C)

This subnet is "public" because it has a direct route to the Internet Gateway (IGW). The NAT Gateway (NAT_GW) itself resides in this subnet and uses this route table to send traffic to the internet.
The route table associated with PUB_SUBNET_C would have:
| Destination | Target | Purpose |
| :-------------- | :----------------------------------- | :--------------------------------------------------------------------------- |
| 10.0.0.0/16 | local | Enables communication with all resources within the VPC. |
| 0.0.0.0/0 | igw-aaaaaaaa (ID of your Internet Gateway IGW) | Routes all other outbound traffic directly to the Internet Gateway. |