
# Home Depot Retail Search Intelligence Platform

An independent, end-to-end retail search analytics project built with Terraform, Google Cloud Platform, Databricks, Delta Lake, BigQuery, and GitHub Actions.

> **Disclaimer:** This is an independent portfolio project using the historical public Home Depot Product Search Relevance competition dataset. It is not affiliated with, sponsored by, or connected to The Home Depot's production systems.

## Architecture

```text
Historical Home Depot Kaggle Dataset
                 |
                 v
         Google Cloud Storage
              Raw Bucket
                 |
       Manual import for demo
                 |
                 v
        Databricks Free Edition
                 |
        Bronze Delta Table
        74,067 original records
                 |
                 v
        Silver Delta Table
        Validation and enrichment
        74,067 valid records
                 |
                 v
        Gold Delta Table
        7,921 qualifying search terms
              /       \
             v         v
    Databricks AI/BI    CSV export
       Dashboard             |
                             v
                       GCS Curated
                             |
                             v
                         BigQuery

Infrastructure:
Terraform → GCP resources → GCS remote state

CI:
GitHub Actions → OIDC authentication
               → Terraform validation
               → Terraform plan
               → Drift detection
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Terraform | Infrastructure as Code |
| Google Cloud Storage | Raw, curated, and Terraform state storage |
| Google Cloud IAM | Service accounts and access control |
| Databricks | Apache Spark data processing |
| Delta Lake | Bronze, Silver, and Gold tables |
| Unity Catalog | Data governance and organization |
| BigQuery | SQL analytics |
| Databricks AI/BI | Interactive analytics dashboard |
| GitHub Actions | Infrastructure CI and drift detection |
| Workload Identity Federation | Keyless GitHub-to-GCP authentication |

## Dataset

Source: [Home Depot Product Search Relevance, Kaggle](https://www.kaggle.com/c/home-depot-product-search-relevance)

The dataset contains historical product-search relevance judgments, product descriptions, and product attributes.

Files used:

- `train.csv`
- `product_descriptions.csv`
- `attributes.csv`

The current Silver pipeline enriches training records using product descriptions. Product attributes are stored in the raw layer for potential future enrichment.

## Medallion Architecture

### Bronze

Preserves the original training records and adds ingestion metadata.

**Records:** 74,067

Table: `workspace.retail_intelligence.bronze_search`

### Silver

Standardizes text, validates identifiers and relevance scores, and joins product descriptions.

**Valid records:** 74,067  
**Rejected records:** 0

Tables:

- `workspace.retail_intelligence.silver_search`
- `workspace.retail_intelligence.rejected_search`

### Gold

Aggregates search relevance statistics for search terms with at least five labeled product matches.

**Qualifying search terms:** 7,921

Table: `workspace.retail_intelligence.gold_search_quality`

Metrics include:

- Product match count
- Average relevance score
- Percentage of low-relevance labeled pairs
- Missing product descriptions

## Analytics Results

The Databricks dashboard includes:

- 7,921 qualifying search terms
- Average per-search-term relevance: approximately 2.38 out of 3
- Search Quality Watchlist
- Distribution of average relevance scores

The 2.38 figure is an unweighted average across qualifying search terms.

### Search Quality Examples

For search terms with at least 10 labeled product matches:

| Search term | Matches | Average relevance | Low relevance % |
|---|---:|---:|---:|
| door boot gasket lg | 10 | 1.266 | 90.00 |
| slrd | 10 | 1.300 | 100.00 |
| bestine | 11 | 1.365 | 100.00 |

These are historical competition results, not measurements of current Home Depot website performance.

## Terraform Infrastructure

Terraform provisions:

- Raw GCS bucket
- Curated GCS bucket
- Data-processing service account
- Bucket-level IAM permissions
- BigQuery dataset

Reusable modules are located in `terraform/modules`.

Environment configuration is located in `terraform/environments/dev`.

### Remote State

Terraform state is stored in a dedicated, versioned GCS bucket:

`gs://hd-retail-intelligence-2026-tfstate`

The remote backend supports shared state management and state locking.

## GitHub Actions CI

The workflow performs:

1. Terraform formatting checks
2. Terraform initialization and validation
3. Google Cloud authentication using OIDC
4. Remote state initialization
5. Authenticated Terraform plan

GitHub Actions uses Workload Identity Federation and a dedicated Terraform CI service account. No long-lived Google Cloud service account keys are stored in GitHub.

The workflow does not automatically execute `terraform apply`.

### Verified CI Result

The authenticated Terraform plan completed successfully and reported:

`No changes. Your infrastructure matches the configuration.`

## Security

Implemented controls include:

- Private GCS buckets
- Uniform bucket-level access
- Public access prevention
- Dedicated service accounts
- Bucket-scoped data-processing permissions
- GitHub repository-restricted OIDC provider
- GCS remote Terraform state
- Git exclusions for state files, credentials, and datasets

The CI account has read-oriented project permissions and write access to Terraform state objects for backend operation.

## Current Limitations

This is a portfolio demonstration rather than a production deployment.

- Databricks Free Edition data ingestion uses a separate manual CSV upload.
- Gold results are manually exported to GCS before BigQuery loading.
- The data pipeline is not yet orchestrated end to end.
- Terraform CI runs plans but does not automatically apply changes.
- Data-quality validation has not yet been demonstrated using injected invalid records.
- No live product-search traffic, transactions, or conversion metrics are used.

## Potential Improvements

- Automated data movement between GCS and Databricks
- Scheduled Databricks jobs
- Automated BigQuery publishing
- Data-quality regression tests
- Environment-specific Terraform configurations
- CI policy checks and approval gates
- Monitoring and operational alerts

## Repository Structure

```text
.github/workflows/     GitHub Actions CI
terraform/bootstrap/   Bootstrap directory
terraform/environments/dev/  Development infrastructure
terraform/modules/     Reusable Terraform modules
databricks/            Databricks development artifacts
bigquery/              BigQuery development artifacts
dashboard/             Dashboard development artifacts
data/                  Local dataset files (Git ignored)
```

## Author

Independent AI engineering and data platform portfolio project.
