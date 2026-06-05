import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================
# TOP 10 LISTS  (PB numbers)
# ============================================================
TOP10 = {
    "Protocolo Básico": [1, 56, 121, 39, 246, 142, 195, 183, 36, 97, 209, 191, 192],
    "Top 10 Cardiológico": [69, 97, 75, 56, 177, 102, 61, 114, 47],
    "Top 10 Columna": [191, 192, 97, 154, 141, 90, 121, 73, 106, 107, 108, 109],
    "Top 10 Dermatológico": [24, 14, 16, 17, 125, 55, 114, 74, 56, 211],
    "Top 10 Disfuncional": [191, 192, 36, 209, 97, 193, 207, 195, 194, 192],
    "Top 10 Disnea": [30, 29, 75, 239, 69, 6, 66, 59, 102, 145, 97],
    "Top 10 Endocrinológico": [181, 182, 183, 184, 186, 159, 171, 187, 188, 288],
    "Top 10 Gastrointestinal": [39, 246, 81, 94, 34, 245, 259, 124, 129, 88],
    "Top 10 Gastritis": [245, 246, 252, 191, 238, 96, 193, 16, 72, 76, 88],
    "Top 10 Ginecológico": [100, 46, 44, 15, 71, 171, 187, 56, 135, 5],
    "Top 10 Hematológico": [121, 189, 84, 36, 206, 106, 108, 61, 97, 209],
    "Top 10 Hepatobiliar": [39, 36, 209, 132, 195, 246, 94, 93, 97, 56, 34, 38],
    "Top 10 Inmunológico (Enf. Autoinmunes)": [1, 35, 102, 74, 189, 56, 97, 61, 196],
    "Top 10 Inmunológico (Inmunodeficiencia)": [1, 56, 97, 162, 61, 189, 4, 196, 203],
    "Top 10 Intrahospitalario": [56, 51, 64, 104, 233, 96, 252, 97, 50, 113],
    "Top 10 Lesiones Deportivas": [164, 168, 117, 97, 164, 191, 141, 90, 121, 176],
    "Top 10 Neurológico": [142, 26, 27, 12, 67, 14, 49, 134, 16, 133],
    "Top 10 Nutricional": [191, 192, 97, 36, 209, 193, 192, 195, 158, 157],
    "Top 10 Oftalmológico": [56, 121, 26, 147, 57, 277, 285, 27, 10, 114],
    "Top 10 Oncológico": [114, 265, 264, 95, 56, 81, 46, 266, 35, 74],
    "Top 10 Osteomuscular": [97, 56, 1, 114, 7, 86, 97, 106, 108, 121, 207],
    "Top 10 Patogénico": [265, 264, 114, 17, 35, 81, 95, 258, 266, 142],
    "Top 10 Psicoemocional": [311, 307, 318, 316, 309, 310, 313, 308, 314, 315],
    "Top 10 Psiquiátrico": [302, 174, 321, 312, 317, 320, 322, 306, 298, 299, 284],
    "Top 10 Regularización intestinal": [191, 192, 157, 173, 193, 192, 195, 183, 158, 274],
    "Top 10 Reservorios": [164, 164, 100, 202, 294, 295, 289, 195, 201, 207],
    "Top 10 Respiratorio": [56, 121, 69, 99, 29, 30, 59, 75, 237, 68, 235],
    "Top 10 Tropical": [8, 267, 126, 45, 139, 223, 9, 227, 224, 258, 323, 324],
    "Top 10 Urológico": [97, 74, 1, 56, 81, 41, 201, 99, 222, 230],
    "Top 5 Conjuntivitis": [121, 57, 56, 10, 58],
    "Top 5 Desintoxicación": [209, 36, 97, 159, 316],
    "Top 5 Desparasitación": [124, 131, 169, 132, 129, 129, 270],
    "Top 5 IVU": [1, 56, 97, 74, 81],
    "Top 5 Odontológico": [1, 78, 164, 56, 106, 256],
    "Top 5 Pérdida de la Memoria": [11, 156, 166, 13, 117, 116],
    "Top 5 Postquirúrgico": [1, 97, 209, 36, 56],
    "PBs Diabetogénicos": [17, 14, 16, 1, 45, 94, 110, 111, 159, 192, 6, 38],
    "PBs Hiperglicémicos": [56, 97, 86, 121, 209, 81, 35, 36, 106, 74, 191, 192, 114, 158, 159, 191, 192],
    "PBs relacionados a Hepatitis": [34, 35, 36, 37, 38, 39],
    "PBs relacionados a Herpes": [21, 22, 23, 24, 25, 26, 213, 214],
    "PBs relacionados a Hígado": [34, 35, 36, 37, 38, 39, 84, 94, 95, 132, 209],
    "PBs relacionados a M. Tuberculosis": [56, 230, 291, 297],
    "PBs relacionados a M. Leprae": [114, 228, 229],
    "PBs relacionados a Proteus Mirabilis": [102, 103, 104, 105, 240],
    "PBs relacionados a Yersinia Pestis": [99, 100, 101],
}

# ============================================================
# DISEASE PROTOCOLS
# Keys = normalized disease names; values = {tops, pbs, notes}
# pbs = specific PB numbers explicitly listed in protocol
# tops = Top 10/5 category names referenced
# ============================================================
DISEASES = {
    "Acné": {
        "tops": ["Top 10 Dermatológico", "Top 10 Endocrinológico", "Top 10 Reservorios", "Top 10 Psicoemocional"],
        "pbs": [77], "notes": ""
    },
    "Adenoma hipofisiario": {
        "tops": ["Top 10 Neurológico", "Top 10 Endocrinológico"],
        "pbs": [66, 182, 171, 155, 288], "notes": ""
    },
    "Aftas bucales": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 5 Odontológico", "Top 5 Desintoxicación"],
        "pbs": [30], "notes": ""
    },
    "Alergia": {
        "tops": ["Top 10 Dermatológico", "Top 10 Disfuncional", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [210, 54], "notes": ""
    },
    "Alopecia": {
        "tops": ["Top 10 Dermatológico", "Top 10 Endocrinológico", "Top 10 Disfuncional", "Top 10 Gastrointestinal", "Top 10 Gastritis", "Top 10 Regularización intestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Alzheimer": {
        "tops": ["Top 10 Neurológico", "Top 10 Disfuncional", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 5 Pérdida de la Memoria", "Top 5 Desintoxicación", "Top 5 Desparasitación"],
        "pbs": [116, 117], "notes": "PB Calcáneo-Calcáneo y Muñeca-Muñeca relacionados al Alzheimer"
    },
    "Amenorrea": {
        "tops": ["Top 10 Endocrinológico", "Top 10 Ginecológico", "Top 10 Neurológico", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Anemia": {
        "tops": ["Top 10 Hematológico", "Top 10 Gastrointestinal", "Top 10 Disfuncional", "Top 5 Desparasitación", "Top 5 Desintoxicación", "Top 5 Postquirúrgico"],
        "pbs": [], "notes": ""
    },
    "Anorexia": {
        "tops": ["Top 10 Neurológico", "Top 10 Disfuncional", "Top 10 Gastrointestinal", "Top 10 Gastritis", "Top 10 Regularización intestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 10 Psiquiátrico"],
        "pbs": [287], "notes": ""
    },
    "Ansiedad": {
        "tops": ["Top 10 Neurológico", "Top 10 Endocrinológico", "Top 10 Disfuncional", "Top 10 Gastrointestinal", "Top 10 Gastritis", "Top 10 Regularización intestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Arritmia": {
        "tops": ["Top 10 Cardiológico", "Top 10 Disfuncional", "Top 5 Desintoxicación"],
        "pbs": [177], "notes": ""
    },
    "Artritis Reumatoide": {
        "tops": ["Top 10 Osteomuscular", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 5 Desintoxicación"],
        "pbs": [207, 113, 106, 107], "notes": ""
    },
    "Artrosis": {
        "tops": ["Top 10 Osteomuscular", "Top 10 Endocrinológico", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 5 Desintoxicación"],
        "pbs": [207], "notes": ""
    },
    "Asma": {
        "tops": ["Top 10 Respiratorio", "Top 10 Disnea", "Top 10 Disfuncional", "Top 5 Desintoxicación"],
        "pbs": [208], "notes": ""
    },
    "Autismo": {
        "tops": ["Top 10 Neurológico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desparasitación", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Bocio": {
        "tops": ["Top 10 Endocrinológico", "Top 10 Inmunológico (Enf. Autoinmunes)"],
        "pbs": [183], "notes": ""
    },
    "Bronquitis": {
        "tops": ["Top 10 Respiratorio", "Top 10 Disnea", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Bulimia": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Gastritis", "Top 10 Psicoemocional", "Top 10 Psiquiátrico"],
        "pbs": [], "notes": ""
    },
    "Cáncer de Colon": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [81, 46, 85], "notes": "Zona de conflicto: Pliegue inguinal – Riñón"
    },
    "Cáncer de Estómago": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Hepatobiliar", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [85], "notes": "Zona de conflicto: Diafragma – Riñón"
    },
    "Cáncer de Hígado": {
        "tops": ["Top 10 Hepatobiliar", "Top 10 Gastrointestinal", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación", "PBs relacionados a Hepatitis"],
        "pbs": [85], "notes": "Zona de conflicto: Diafragma – Riñón"
    },
    "Cáncer de Mama": {
        "tops": ["Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [102], "notes": "Zona de conflicto: Mediastino – Riñón"
    },
    "Cáncer de Ovario": {
        "tops": ["Top 10 Endocrinológico", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [187], "notes": "Zona de conflicto: Pliegue inguinal – Riñón"
    },
    "Cáncer de Páncreas": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [282, 85], "notes": "Zona de conflicto: Diafragma – Riñón"
    },
    "Cáncer de Próstata": {
        "tops": ["Top 10 Urológico", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [222, 41, 42], "notes": "Zona de conflicto: Pliegue inguinal – Riñón"
    },
    "Cáncer de Pulmón": {
        "tops": ["Top 10 Respiratorio", "Top 10 Disnea", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [102], "notes": "Zona de conflicto: Mediastino – Riñón"
    },
    "Cáncer de Riñón": {
        "tops": ["Top 10 Urológico", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [97, 85], "notes": "Zona de conflicto: Diafragma – Riñón"
    },
    "Cáncer de Testículo": {
        "tops": ["Top 10 Urológico", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [99], "notes": "Zona de conflicto: Pliegue Inguinal – Riñón"
    },
    "Cáncer de Tiroides": {
        "tops": ["Top 10 Endocrinológico", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [183, 102], "notes": "Zona de conflicto: Mediastino – Riñón"
    },
    "Cáncer de Vejiga": {
        "tops": ["Top 10 Urológico", "Top 10 Oncológico", "Top 10 Patogénico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [74], "notes": "Zona de conflicto: Pliegue inguinal – Riñón"
    },
    "Candidiasis Vaginal": {
        "tops": ["Top 10 Ginecológico", "Top 5 Desintoxicación"],
        "pbs": [100, 5, 136], "notes": ""
    },
    "Ciática": {
        "tops": ["Top 10 Osteomuscular", "Top 10 Neurológico", "Top 10 Columna", "Top 5 Desintoxicación"],
        "pbs": [7], "notes": ""
    },
    "Cistitis": {
        "tops": ["Top 10 Urológico", "Top 5 Desintoxicación", "Top 5 IVU"],
        "pbs": [74], "notes": ""
    },
    "Cólico Nefrítico": {
        "tops": ["Top 10 Urológico", "Top 5 IVU", "Top 5 Desintoxicación"],
        "pbs": [164], "notes": ""
    },
    "Colitis Ulcerativa": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Regularización Intestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Conjuntivitis": {
        "tops": ["Top 10 Oftalmológico", "Top 5 Conjuntivitis"],
        "pbs": [], "notes": ""
    },
    "Déficit de Crecimiento": {
        "tops": ["Top 10 Neurológico", "Top 10 Endocrinológico"],
        "pbs": [155], "notes": ""
    },
    "Degeneración Macular": {
        "tops": ["Top 10 Oftalmológico", "Top 5 Conjuntivitis"],
        "pbs": [285], "notes": ""
    },
    "Demencia": {
        "tops": ["Top 10 Neurológico", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Depresión": {
        "tops": ["Top 10 Neurológico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico"],
        "pbs": [302], "notes": ""
    },
    "Dermatitis Atópica": {
        "tops": ["Top 10 Dermatológico", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [16], "notes": ""
    },
    "Diabetes Mellitus": {
        "tops": ["Top 10 Respiratorio", "Top 10 Gastrointestinal", "Top 10 Urológico", "Top 10 Neurológico", "Top 10 Cardiológico", "Top 10 Dermatológico", "Top 10 Psicoemocional", "Top 5 IVU", "Top 5 Desparasitación", "PBs Diabetogénicos", "PBs Hiperglicémicos", "PBs relacionados a Hepatitis"],
        "pbs": [204, 40], "notes": "PB 204: Riñón–Duodeno (Diabetes Mellitus). PB 40: Malar–Malar (Enterovirus, relacionado a DM)"
    },
    "Disfunción Eréctil": {
        "tops": ["Top 10 Urológico", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [52], "notes": ""
    },
    "Dislexia": {
        "tops": ["Top 10 Neurológico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico"],
        "pbs": [163], "notes": ""
    },
    "Dismenorrea": {
        "tops": ["Top 10 Ginecológico", "Top 10 Endocrinológico"],
        "pbs": [], "notes": ""
    },
    "Dispepsia": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Hepatobiliar", "Top 10 Gastritis"],
        "pbs": [], "notes": ""
    },
    "Diverticulitis": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Regularización intestinal", "Top 10 Nutricional"],
        "pbs": [], "notes": ""
    },
    "Edema Pulmonar": {
        "tops": ["Top 10 Respiratorio", "Top 10 Disnea"],
        "pbs": [], "notes": ""
    },
    "Endocarditis": {
        "tops": ["Top 10 Cardiológico"],
        "pbs": [], "notes": ""
    },
    "Endometriosis": {
        "tops": ["Top 10 Ginecológico", "Top 10 Endocrinológico"],
        "pbs": [86], "notes": "Útero–Sacro (Endometriosis)"
    },
    "Enfermedad Celiaca": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Disfuncional", "Top 10 Regularización Intestinal"],
        "pbs": [], "notes": ""
    },
    "Enfermedad de Crohn": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 10 Regularización intestinal", "Top 10 Nutricional", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Enfermedad de Huntington": {
        "tops": ["Top 10 Neurológico", "Top 5 Desintoxicación"],
        "pbs": [], "notes": ""
    },
    "Epilepsia": {
        "tops": ["Top 10 Neurológico", "Top 5 Desintoxicación", "Top 5 Desparasitación"],
        "pbs": [180, 124], "notes": ""
    },
    "Esclerosis Múltiple": {
        "tops": ["Top 10 Neurológico", "Top 10 Inmunológico (Enf. Autoinmunes)", "Top 10 Psicoemocional", "Top 5 Desintoxicación"],
        "pbs": [26, 142, 97], "notes": ""
    },
    "Espondilitis": {
        "tops": ["Top 10 Osteomuscular", "Top 10 Inmunológico (Enf. Autoinmunes)"],
        "pbs": [], "notes": ""
    },
    "Fibromialgia": {
        "tops": ["Top 10 Osteomuscular", "Top 10 Tropical", "Top 10 Inmunológico (Enf. Autoinmunes)"],
        "pbs": [126], "notes": ""
    },
    "Gastritis": {
        "tops": ["Top 10 Gastritis", "Top 10 Gastrointestinal", "Top 10 Regularización intestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 10 Psiquiátrico"],
        "pbs": [245, 246, 252, 96, 88, 72], "notes": ""
    },
    "Hepatitis A": {
        "tops": ["Top 10 Hepatobiliar", "Top 10 Gastrointestinal", "Top 5 Desintoxicación"],
        "pbs": [34], "notes": "PB 34: Colon Descendente – Hígado"
    },
    "Hepatitis B": {
        "tops": ["Top 10 Hepatobiliar", "Top 5 Desintoxicación", "PBs relacionados a Hepatitis"],
        "pbs": [35], "notes": "PB 35: Pleura – Hígado"
    },
    "Hepatitis C": {
        "tops": ["Top 10 Hepatobiliar", "Top 5 Desintoxicación", "PBs relacionados a Hepatitis"],
        "pbs": [36], "notes": "PB 36: Hígado – Hígado"
    },
    "Herpes Zóster": {
        "tops": ["Top 10 Dermatológico", "Top 10 Psicoemocional", "Top 10 Reservorios", "PBs relacionados a Herpes"],
        "pbs": [23], "notes": "PB 23: Cúbito–Cúbito (Herpes Zóster/VVZ)"
    },
    "Hipertensión Arterial": {
        "tops": ["Top 10 Cardiológico", "Top 5 Desintoxicación"],
        "pbs": [97, 175], "notes": "PB 175: Carótida–Carótida (Hipertensión Arterial)"
    },
    "Hipotiroidismo": {
        "tops": ["Top 10 Endocrinológico"],
        "pbs": [183], "notes": ""
    },
    "Hipertiroidismo": {
        "tops": ["Top 10 Endocrinológico"],
        "pbs": [183], "notes": ""
    },
    "Infertilidad": {
        "tops": ["Top 10 Endocrinológico", "Top 10 Ginecológico", "Top 10 Reservorios", "Top 10 Psicoemocional", "PBs relacionados a M. Tuberculosis", "PBs relacionados a M. Leprae"],
        "pbs": [44, 15, 52, 99, 100], "notes": ""
    },
    "Insuficiencia Renal": {
        "tops": ["Top 10 Urológico", "Top 5 Desintoxicación", "PBs Hiperglicémicos", "PBs relacionados a Hepatitis", "PBs relacionados a Hígado"],
        "pbs": [], "notes": ""
    },
    "Leucemia": {
        "tops": ["Top 10 Hematológico", "Top 5 Desintoxicación"],
        "pbs": [189, 84, 206, 61], "notes": "PB 206: Bazo–Duodeno (Leucemia)"
    },
    "Lupus Eritematoso": {
        "tops": ["Top 10 Inmunológico (Enf. Autoinmunes)", "PBs relacionados a Proteus Mirabilis"],
        "pbs": [], "notes": ""
    },
    "Meningitis": {
        "tops": ["Top 10 Neurológico", "Top 10 Intrahospitalario"],
        "pbs": [50, 113], "notes": "PB 50: Tiroides–Bulbo Raquídeo (Meningitis Viral). PB 113: Dorso–Lumbar (Neisseria Meningitidis)"
    },
    "Migraña": {
        "tops": ["Top 10 Neurológico", "Top 5 Desintoxicación"],
        "pbs": [11, 156], "notes": ""
    },
    "Obesidad": {
        "tops": ["Top 10 Endocrinológico", "Top 10 Neurológico", "Top 10 Disfuncional", "Top 10 Gastrointestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación"],
        "pbs": [183, 182, 279, 287], "notes": ""
    },
    "Osteoporosis": {
        "tops": ["Top 10 Osteomuscular", "Top 10 Endocrinológico"],
        "pbs": [], "notes": ""
    },
    "Parkinson": {
        "tops": ["Top 10 Neurológico"],
        "pbs": [280], "notes": "PB 280: Pospineal–Bulbo Raquídeo (Parkinson)"
    },
    "Prostatitis": {
        "tops": ["Top 10 Urológico", "Top 5 IVU"],
        "pbs": [], "notes": ""
    },
    "Psoriasis": {
        "tops": ["Top 10 Dermatológico", "Top 10 Inmunológico (Enf. Autoinmunes)"],
        "pbs": [69, 70, 74], "notes": ""
    },
    "Rinitis Alérgica": {
        "tops": ["Top 10 Respiratorio", "Top 10 Disnea"],
        "pbs": [210, 54, 53, 66], "notes": "PB 210: Nariz–Nariz (Rinitis Alérgica)"
    },
    "Síndrome de Colon Irritable": {
        "tops": ["Top 10 Gastrointestinal", "Top 10 Disfuncional", "Top 10 Neurológico", "Top 10 Regularización intestinal", "Top 10 Nutricional", "Top 10 Psicoemocional", "Top 5 Desparasitación"],
        "pbs": [], "notes": ""
    },
    "Toxoplasmosis": {
        "tops": ["Top 10 Patogénico", "Top 10 Reservorios"],
        "pbs": [134], "notes": "PB 134: Oído–Oído (Toxoplasma Gondii)"
    },
    "VIH/SIDA": {
        "tops": ["Top 10 Inmunológico (Inmunodeficiencia)", "Top 10 Oncológico", "Top 10 Respiratorio", "Top 10 Gastrointestinal", "Top 10 Urológico", "Top 10 Psicoemocional", "Top 10 Psiquiátrico", "Top 5 Desintoxicación", "Top 5 Desparasitación", "Top 5 IVU"],
        "pbs": [1, 35], "notes": "PB 1: Timo–Recto (VIH). PB 35: Pleura–Hígado (Hepatitis B, frecuente en VIH)"
    },
    "Várices": {
        "tops": ["Top 10 Hematológico"],
        "pbs": [71], "notes": ""
    },
}

# Write JavaScript output
output = f"""// Disease protocol data generated from PDFs (LINDE3 + Kronos BRI 2017)
const TOP10 = {json.dumps(TOP10, ensure_ascii=False, indent=2)};

const DISEASE_DATA = {json.dumps(DISEASES, ensure_ascii=False, indent=2)};
"""

with open(r'C:\Users\usuario\Desktop\biomagnetismo\disease_data.js', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Generated disease_data.js with {len(DISEASES)} diseases and {len(TOP10)} Top10 lists')
