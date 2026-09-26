from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.members.models import FamilyMember
from apps.analytics.models import HealthMetric
from .models import AIPrediction
from .ml_engine import ml_predictor

def get_risk_colors(risk):
    """Returns CSS color classes based on risk percentage."""
    if risk > 25:
        return {'text': 'text-red-600', 'bg': 'bg-red-500'}
    elif risk > 15:
        return {'text': 'text-amber-600', 'bg': 'bg-amber-500'}
    else:
        return {'text': 'text-emerald-600', 'bg': 'bg-emerald-500'}

def generate_pointwise_recommendations(member, sys_bp, dia_bp, sugar_level, weight, diabetes_risk, heart_risk, hypertension_risk):
    """
    Generates point-wise recommendations formatted as numbered lines 1), 2), 3)...
    """
    items = []
    age = member.age or 35
    is_child = age < 18
    is_senior = age >= 60

    if diabetes_risk > 20 or sugar_level >= 100:
        items.append("Monitor fasting blood sugar weekly and reduce refined carbohydrates.")
    
    if heart_risk > 20 or sys_bp >= 130:
        items.append("Schedule periodic ECG/cardiology checkups and maintain omega-3 fatty acid intake.")
    
    if hypertension_risk > 20 or sys_bp >= 130 or dia_bp >= 85:
        items.append("Limit sodium intake below 2g/day and track morning blood pressure.")

    if not items:
        items.append("Maintain routine annual health checkups and balanced nutrition with regular hydration.")

    if is_child:
        items.append("Target at least 60 minutes of daily active physical play and sports.")
    elif is_senior:
        items.append("Perform 30 minutes of low-impact walking or gentle yoga 5 days a week.")
    else:
        items.append("Target 150 minutes of moderate-intensity aerobic exercise per week.")

    if member.allergies and member.allergies.strip().lower() != 'none':
        items.append(f"Inform healthcare providers of known sensitivity to {member.allergies} before taking new prescriptions.")

    if member.chronic_conditions and member.chronic_conditions.strip().lower() != 'none':
        items.append(f"Ensure strict medication adherence for chronic condition: {member.chronic_conditions}.")

    # Number each point cleanly: 1) ..., 2) ..., 3) ...
    formatted_points = [f"{idx + 1}) {item}" for idx, item in enumerate(items)]
    return "\n".join(formatted_points)

def calculate_member_risks(member, user):
    """
    Predicts disease risks using trained ML models and generates point-wise recommendations.
    """
    latest_vitals = HealthMetric.objects.filter(user=user, member=member).order_by('-record_date').first()
    
    sys_bp = 120
    dia_bp = 80
    sugar_level = 95.0
    weight = 70.0

    if latest_vitals:
        if latest_vitals.sugar_level:
            sugar_level = float(latest_vitals.sugar_level)
        if latest_vitals.weight:
            weight = float(latest_vitals.weight)
        if latest_vitals.blood_pressure:
            parts = latest_vitals.blood_pressure.split('/')
            try:
                sys_bp = int(parts[0])
                if len(parts) > 1:
                    dia_bp = int(parts[1])
            except (ValueError, IndexError):
                pass

    # Call ML prediction engine
    ml_results = ml_predictor.predict_risk(
        age=member.age,
        gender_str=member.gender,
        sys_bp=sys_bp,
        dia_bp=dia_bp,
        sugar_level=sugar_level,
        weight=weight,
        chronic_conditions=member.chronic_conditions
    )

    diabetes_risk = ml_results['diabetes_risk']
    heart_risk = ml_results['heart_disease_risk']
    hypertension_risk = ml_results['hypertension_risk']

    recommendations_text = generate_pointwise_recommendations(
        member=member,
        sys_bp=sys_bp,
        dia_bp=dia_bp,
        sugar_level=sugar_level,
        weight=weight,
        diabetes_risk=diabetes_risk,
        heart_risk=heart_risk,
        hypertension_risk=hypertension_risk
    )

    return {
        'diabetes_risk': diabetes_risk,
        'heart_disease_risk': heart_risk,
        'hypertension_risk': hypertension_risk,
        'recommendations': recommendations_text
    }

@login_required
def ai_predictions_view(request):
    members = FamilyMember.objects.filter(user=request.user)
    
    # Handle explicit recalculate trigger
    if request.method == 'POST' and 'recalculate' in request.POST:
        for member in members:
            data = calculate_member_risks(member, request.user)
            AIPrediction.objects.update_or_create(
                user=request.user,
                member=member,
                defaults=data
            )
        messages.success(request, "AI Health Analysis recalculated successfully!")
        return redirect('ai_predictions')

    predictions = []
    for member in members:
        pred = AIPrediction.objects.filter(user=request.user, member=member).first()
        if not pred:
            data = calculate_member_risks(member, request.user)
            pred = AIPrediction.objects.create(
                user=request.user,
                member=member,
                **data
            )
        
        # Split recommendation lines into list for line-by-line <br> rendering
        rec_lines = [line.strip() for line in (pred.recommendations or '').split('\n') if line.strip()]

        predictions.append({
            'member': member,
            'prediction': pred,
            'recommendation_lines': rec_lines,
            'diabetes_color': get_risk_colors(pred.diabetes_risk),
            'heart_color': get_risk_colors(pred.heart_disease_risk),
            'hypertension_color': get_risk_colors(pred.hypertension_risk),
        })

    return render(request, 'ai_predictions.html', {'predictions': predictions})
