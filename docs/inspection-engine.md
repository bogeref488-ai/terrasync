# Inspection Engine

The inspection engine is the core logic of TerraSync.

## Workflow

```text
Work Order
↓
Assigned Report Type
↓
Load Inspection Template
↓
Complete Sections
↓
Capture Measurements, Photos, Remarks, Defects
↓
Generate One Report
↓
Sync
```

## Standard Inspection Item

Every inspection item follows the same structure:

```text
Inspection Item
├── Status
├── Measurement, if applicable
├── Capture Photo
├── Remarks / Description
└── Defect Details, if required
```

## Status Rules

| Status | Remarks Required | Photo Required |
|---|---|---|
| Good | Optional | Yes |
| Fair | Required | Yes |
| Poor | Required | Yes |
| Critical | Required | Yes |
| Not Accessible | Required | Optional |
| Not Applicable | Optional | No |

## Report Types

TerraSync supports configurable report templates. Telecom v1 includes:

1. Tower Inspection Report
2. Power Inspection Report
3. RMS Report
4. Preventive Maintenance Report
5. Corrective Maintenance Report
6. Transmission Inspection Report
7. Shelter Inspection Report
8. Site Acceptance Report

## One Template = One Report

Each task loads one template and produces one structured report.
