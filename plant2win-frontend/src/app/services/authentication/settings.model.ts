interface Algorithms {
    chest: string[];
    mura: string[];
    ct_chest: string[];
    ct_head: string[];
}

export interface Disease {
    id: string;
    name: string;
    description: string;
}

export interface SettingsModel {
    Roles: string[];
    Algorithms: Algorithms;
    isPacs: string;
    pacsPlace: string;
    Disease: Disease[];
    allowed_report?: boolean;
}
