from fastapi import APIRouter

router = APIRouter(prefix="/inspection-templates", tags=["inspection templates"])


@router.get("/")
def list_templates():
    return [
        "Tower Inspection Report",
        "Power Inspection Report",
        "RMS Report",
        "Preventive Maintenance Report",
        "Corrective Maintenance Report",
        "Transmission Inspection Report",
        "Shelter Inspection Report",
        "Site Acceptance Report",
    ]


@router.get("/tower-inspection")
def tower_inspection_template():
    return {
        "template_name": "Tower Inspection Report",
        "sections": [
            "Check-in",
            "Safety Readiness",
            "Ground / Base",
            "Foundation",
            "Tower Structure",
            "Verticality / Sway",
            "Grounding",
            "Cables & Feeders",
            "Equipment on Tower",
            "Top Platform",
            "Remarks & Defects",
            "Summary & Submit",
        ],
    }
