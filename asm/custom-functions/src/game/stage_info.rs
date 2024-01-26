#![allow(non_upper_case_globals)]

#[derive(Default, Copy, Clone)]
pub struct StageInfo {
    pub name:   &'static str,
    pub layers: &'static [u8],
    pub rooms:  &'static [u8],
    // pub entrances: &'static [u8],
}

pub struct StageCategory {
    pub name:   &'static str,
    pub stages: &'static [StageInfo],
}

macro_rules! define_stages {
    ($(($name:expr, $layers:expr, $rooms:expr)),*)  => (
        [$(
            StageInfo {
                name: $name,
                layers: &$layers,
                rooms: &$rooms,
            },
        )*]
    )
}

pub const THE_SKY: StageCategory = StageCategory {
    name:   "The Sky",
    stages: &define_stages!(
        (
            "F000",
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 20, 28],
            [0]
        ),
        ("F001r", [0, 1, 2, 3, 4, 13, 14], [0, 1, 2, 3, 4, 5, 6]),
        ("F002r", [0, 1, 2], [0]),
        ("F004r", [0, 1, 3], [0]),
        ("F005r", [0, 1, 2], [0]),
        ("F006r", [0, 1, 2], [0]),
        ("F007r", [0, 1, 2], [0]),
        ("F008r", [0, 1], [0]),
        ("F009r", [0], [0]),
        ("F010r", [0, 1], [0]),
        ("F011r", [0, 1, 2, 12], [0]),
        ("F012r", [0, 1, 2, 4], [0]),
        ("F013r", [0, 1], [0]),
        ("F014r", [0, 2], [0]),
        ("F015r", [0, 1, 2], [0]),
        ("F016r", [0, 2], [0]),
        ("F017r", [0, 2], [0]),
        ("F018r", [0, 1, 2], [0]),
        ("F019r", [0, 2], [0]),
        ("F020", [0, 1, 2, 3, 4, 6], [0]),
        ("F021", [0], [1]),
        ("F023", [0, 1, 2, 13], [0])
    ),
};

pub const FARON: StageCategory = StageCategory {
    name:   "Faron",
    stages: &define_stages!(
        ("F100", [0, 1, 2, 3, 4, 5], [0]),
        ("F100_1", [0, 1, 2, 3], [0]),
        ("F101", [0, 1, 2, 3, 4, 5], [0]),
        ("F102", [0, 1, 2, 3], [0, 1, 2, 3, 4]),
        ("F102_1", [0, 1, 2, 3], [0]),
        ("F102_2", [0, 1, 3, 4], [0]),
        ("F103", [0, 1, 2], [0]),
        ("F103_1", [0, 1, 2], [0])
    ),
};
pub const ELDIN: StageCategory = StageCategory {
    name:   "Eldin",
    stages: &define_stages!(
        ("F200", [0, 1, 2, 3, 4], [0, 1, 2, 3, 4, 5, 6, 7, 8]),
        ("F201_1", [0, 2, 3, 4], [0]),
        ("F201_2", [0], [0]),
        ("F201_3", [0, 2, 3], [0]),
        ("F201_4", [0, 3], [0]),
        ("F202", [0, 1], [0, 1, 2, 3, 4, 5, 6]),
        ("F202_1", [0, 1], [0]),
        ("F202_2", [0], [0]),
        ("F202_3", [0], [0]),
        ("F202_4", [0], [0]),
        ("F210", [0, 1, 2, 3, 4], [0]),
        ("F211", [0, 1, 2, 3, 4], [0]),
        ("F221", [0, 2], [0])
    ),
};

pub const LANAYRU: StageCategory = StageCategory {
    name:   "Lanayru",
    stages: &define_stages!(
        ("F300", [0, 1, 2], [0]),
        ("F300_1", [0, 1, 2, 3, 4], [0, 1, 2]),
        ("F300_2", [0], [0]),
        ("F300_3", [0], [0]),
        ("F300_4", [0, 1, 2, 13], [0]),
        ("F300_5", [0], [0]),
        ("F301", [0], [0]),
        ("F301_1", [0, 1, 2, 3, 4, 5], [0]),
        ("F301_2", [0, 3, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ("F301_3", [0, 1, 2, 3], [0]),
        ("F301_4", [0, 1, 2, 3, 4, 5], [0]),
        ("F301_5", [0], [0]),
        ("F301_6", [0, 1, 2, 5], [0]),
        ("F301_7", [0, 1, 2], [0]),
        ("F302", [0, 1, 2, 13], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("F303", [0, 1, 2, 3, 4], [0])
    ),
};
pub const SEALED_GROUNDS: StageCategory = StageCategory {
    name:   "Sealed Grounds",
    stages: &define_stages!(
        ("F400", [0, 1, 2, 3, 4, 5, 6, 7, 8, 13], [0, 1]),
        ("F401", [0, 1, 2, 3, 4, 5, 6, 7], [1]),
        (
            "F402",
            [0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 15, 16, 17, 18, 19],
            [0, 2]
        ),
        ("F403", [0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 15], [1]),
        ("F404", [0, 1, 2, 3, 13, 14, 15], [0, 2]),
        ("F405", [0], [0]),
        ("F406", [0, 1, 2, 13], [1]),
        ("F407", [0, 13], [0])
    ),
};
pub const DUNGEONS: StageCategory = StageCategory {
    name:   "Dungeons",
    stages: &define_stages!(
        ("D000", [0, 1], [0]),
        ("D100", [0, 1], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
        ("D101", [0, 1, 2, 4, 5, 6], [0, 1, 2, 3, 4, 5, 7, 10]),
        ("D200", [0], [0, 1, 2, 3, 4]),
        ("D201", [0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
        ("D201_1", [0, 1], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]),
        ("D300", [0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        ("D300_1", [0], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]),
        (
            "D301",
            [0, 1, 2, 3, 4, 9, 10, 11, 12],
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        ),
        ("D301_1", [0, 2, 3], [0]),
        ("B100", [0, 1, 2, 3, 4, 5, 13], [0]),
        ("B100_1", [0, 1, 2, 3, 4, 13], [0]),
        ("B101", [0, 1, 2, 3, 6], [0]),
        ("B101_1", [0, 1], [0]),
        ("B200", [0, 1, 2, 3], [4, 10]),
        ("B201", [0, 1, 2, 3, 13], [0]),
        ("B201_1", [0], [0]),
        ("B300", [0, 1, 2, 3], [0]),
        ("B301", [0, 1, 2, 3, 13], [0]),
        ("B400", [0, 1], [0])
    ),
};
pub const SILENT_REALMS: StageCategory = StageCategory {
    name:   "Silent Realms",
    stages: &define_stages!(
        ("S000", [0, 2], [0]),
        ("S100", [0, 2], [0]),
        ("S200", [0, 2], [0]),
        ("S300", [0, 2], [0])
    ),
};
