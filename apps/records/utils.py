import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from apps.members.models import FamilyMember
from apps.records.models import MedicalRecord
from apps.medicines.models import Medication
from apps.appointments.models import Appointment
from apps.analytics.models import HealthMetric
from apps.predictions.models import AIPrediction

def generate_health_summary_pdf(user, member_id=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f766e'),
        fontName='Helvetica-Bold',
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=15
    )
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1e293b'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )
    cell_style = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#334155')
    )
    header_cell_style = ParagraphStyle(
        'HeaderCellText',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.white,
        fontName='Helvetica-Bold'
    )

    # Filter data
    if member_id:
        members = FamilyMember.objects.filter(user=user, id=member_id)
    else:
        members = FamilyMember.objects.filter(user=user).order_by('-created_at')

    member_ids = list(members.values_list('id', flat=True))
    medicines = Medication.objects.filter(user=user, member_id__in=member_ids).select_related('member')
    appointments = Appointment.objects.filter(user=user, member_id__in=member_ids).select_related('member').order_by('date')
    metrics = HealthMetric.objects.filter(user=user, member_id__in=member_ids).select_related('member').order_by('-record_date')[:10]
    predictions = AIPrediction.objects.filter(user=user, member_id__in=member_ids).select_related('member')

    # Header Title
    story.append(Paragraph("FAMILY CARE — HEALTH PASSPORT REPORT", title_style))
    story.append(Paragraph(f"Generated for User: <b>{user.username}</b> &nbsp;|&nbsp; Date: {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0d9488'), spaceAfter=12))

    # Section 1: Household Family Members
    story.append(Paragraph("1. Family Members Profile", heading_style))
    member_data = [[
        Paragraph("Name", header_cell_style),
        Paragraph("Relation", header_cell_style),
        Paragraph("Age/Gender", header_cell_style),
        Paragraph("Blood", header_cell_style),
        Paragraph("Allergies", header_cell_style),
        Paragraph("Chronic Conditions", header_cell_style),
        Paragraph("Emergency Contact", header_cell_style),
    ]]
    for m in members:
        member_data.append([
            Paragraph(f"<b>{m.name}</b>", cell_style),
            Paragraph(m.relation or "Self", cell_style),
            Paragraph(f"{m.age or 'N/A'} yrs / {m.gender or 'N/A'}", cell_style),
            Paragraph(f"<b>{m.blood_group or '--'}</b>", cell_style),
            Paragraph(m.allergies or "None", cell_style),
            Paragraph(m.chronic_conditions or "None", cell_style),
            Paragraph(m.emergency_contact or "Unset", cell_style),
        ])
    
    t_members = Table(member_data, colWidths=[80, 50, 65, 40, 90, 110, 105])
    t_members.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f766e')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_members)
    story.append(Spacer(1, 12))

    # Section 2: Active Medications
    story.append(Paragraph("2. Active Medications & Dosage Schedule", heading_style))
    med_data = [[
        Paragraph("Patient Name", header_cell_style),
        Paragraph("Medication", header_cell_style),
        Paragraph("Dosage", header_cell_style),
        Paragraph("Frequency / Schedule", header_cell_style),
    ]]
    if medicines.exists():
        for med in medicines:
            med_data.append([
                Paragraph(f"<b>{med.member.name}</b>", cell_style),
                Paragraph(med.medicine_name, cell_style),
                Paragraph(med.dosage or "Unspecified", cell_style),
                Paragraph(med.time or "Daily", cell_style),
            ])
    else:
        med_data.append([Paragraph("No active medications recorded.", cell_style), Paragraph("", cell_style), Paragraph("", cell_style), Paragraph("", cell_style)])

    t_meds = Table(med_data, colWidths=[120, 140, 100, 180])
    t_meds.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_meds)
    story.append(Spacer(1, 12))

    # Section 3: Upcoming Appointments
    story.append(Paragraph("3. Scheduled Doctor Visits", heading_style))
    appnt_data = [[
        Paragraph("Patient", header_cell_style),
        Paragraph("Doctor Name", header_cell_style),
        Paragraph("Hospital / Clinic", header_cell_style),
        Paragraph("Date & Time", header_cell_style),
        Paragraph("Reason", header_cell_style),
    ]]
    if appointments.exists():
        for a in appointments:
            time_str = a.time.strftime('%I:%M %p') if a.time else ''
            appnt_data.append([
                Paragraph(a.member.name, cell_style),
                Paragraph(f"Dr. {a.doctor_name}", cell_style),
                Paragraph(a.hospital or "Clinic", cell_style),
                Paragraph(f"{a.date.strftime('%b %d, %Y')} {time_str}", cell_style),
                Paragraph(a.reason or "Routine checkup", cell_style),
            ])
    else:
        appnt_data.append([Paragraph("No upcoming appointments scheduled.", cell_style), Paragraph("", cell_style), Paragraph("", cell_style), Paragraph("", cell_style), Paragraph("", cell_style)])

    t_appnts = Table(appnt_data, colWidths=[90, 110, 120, 100, 120])
    t_appnts.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_appnts)
    story.append(Spacer(1, 12))

    # Section 4: Recent Vitals
    story.append(Paragraph("4. Recent Health Vitals Logs", heading_style))
    vitals_data = [[
        Paragraph("Patient", header_cell_style),
        Paragraph("Blood Pressure", header_cell_style),
        Paragraph("Blood Sugar (mg/dL)", header_cell_style),
        Paragraph("Weight (kg)", header_cell_style),
        Paragraph("Log Date", header_cell_style),
    ]]
    if metrics.exists():
        for vm in metrics:
            vitals_data.append([
                Paragraph(vm.member.name, cell_style),
                Paragraph(vm.blood_pressure or "--", cell_style),
                Paragraph(str(vm.sugar_level) if vm.sugar_level else "--", cell_style),
                Paragraph(str(vm.weight) if vm.weight else "--", cell_style),
                Paragraph(vm.record_date.strftime('%b %d, %Y'), cell_style),
            ])
    else:
        vitals_data.append([Paragraph("No vitals logged.", cell_style), Paragraph("", cell_style), Paragraph("", cell_style), Paragraph("", cell_style), Paragraph("", cell_style)])

    t_vitals = Table(vitals_data, colWidths=[110, 110, 110, 100, 110])
    t_vitals.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0f766e')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    story.append(t_vitals)

    # Build PDF
    doc.build(story)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
