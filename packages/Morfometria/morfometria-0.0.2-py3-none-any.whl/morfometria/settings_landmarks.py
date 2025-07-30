landmark_names = [
    "SNOUT",
    "VENT",
    "LHead1",
    "LHead2",
    "LHead3",
    "RHead1",
    "RHead2",
    "RHead3",
    "LArmPit",
    "LElb",
    "LMCarp",
    "LFingerHand",
    "RArmPit",
    "RElb",
    "RMCarp",
    "RFingerHand",
    "LKnee",
    "LTar",
    "LToe",
    "RKnee",
    "RTar",
    "RToe",
]

landmarks_groups = {
    "SVL": {"landmarks": ["SNOUT", "VENT"], "angles": []},
    "HEAD": {
        "landmarks": [
            "SNOUT",
            "LHead1",
            "LHead2",
            "LHead3",
            "LArmPit",
            "RArmPit",
            "RHead3",
            "RHead2",
            "RHead1",
            "SNOUT",
        ],
        "angles": [],
    },
    "L_FORELIMB": {
        "landmarks": ["LArmPit", "LElb", "LMCarp", "LFingerHand"],
        "angles": [180, 90, 0, 0],
    },
    "R_FORELIMB": {
        "landmarks": ["RArmPit", "RElb", "RMCarp", "RFingerHand"],
        "angles": [0, -90, 0, 0],
    },
    "L_HINDLIMB": {
        "landmarks": ["VENT", "LKnee", "LTar", "LToe"],
        "angles": [180, -90, 90, 90],
    },
    "R_HINDLIMB": {
        "landmarks": ["VENT", "RKnee", "RTar", "RToe"],
        "angles": [0, 90, -90, -90],
    },
}

semilandmarks = {
    "MUSO_Sx": {
        "landmarks": ["LHead3", "SNOUT"],
        "nsemilandmarks": [8],
        "coordinates": [],
    },
    "MUSO_Dx": {
        "landmarks": ["RHead3", "SNOUT"],
        "nsemilandmarks": [8],
        "coordinates": [],
    },
}
