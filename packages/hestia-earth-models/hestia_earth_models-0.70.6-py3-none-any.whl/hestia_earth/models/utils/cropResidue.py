PRODUCT_ID_TO_PRACTICES_ID = [
    {'product': 'aboveGroundCropResidueRemoved', 'practices': ['residueRemoved']},
    {'product': 'aboveGroundCropResidueIncorporated', 'practices': [
        'residueIncorporated',
        'residueIncorporatedLessThan30DaysBeforeCultivation',
        'residueIncorporatedMoreThan30DaysBeforeCultivation'
    ]},
    {'product': 'aboveGroundCropResidueBurnt', 'practices': ['residueBurnt']},
    {'product': 'aboveGroundCropResidueLeftOnField', 'practices': ['residueLeftOnField']}
]


def crop_residue_product_ids(): return [v.get('product') for v in PRODUCT_ID_TO_PRACTICES_ID]
