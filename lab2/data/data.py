from data import fields

example = [
    {
        fields.NUMBER: 1,
        fields.PLAYER_DISTANCE: 100,
        fields.SHOP_DISTANCE: 1500,
        fields.PROMO_CODE: 30,
        fields.PORTAL_LEVEL: 4,
        fields.COUNT_OTHER_PLAYERS: 2
    },
    {
        fields.NUMBER: 2,
        fields.PLAYER_DISTANCE: 200,
        fields.SHOP_DISTANCE: 1200,
        fields.PROMO_CODE: 40,
        fields.PORTAL_LEVEL: 1,
        fields.COUNT_OTHER_PLAYERS: 5
    },
    {
        fields.NUMBER: 3,
        fields.PLAYER_DISTANCE: 400,
        fields.SHOP_DISTANCE: 900,
        fields.PROMO_CODE: 20,
        fields.PORTAL_LEVEL: 2,
        fields.COUNT_OTHER_PLAYERS: 12
    },
    {
        fields.NUMBER: 4,
        fields.PLAYER_DISTANCE: 100,
        fields.SHOP_DISTANCE: 1000,
        fields.PROMO_CODE: 30,
        fields.PORTAL_LEVEL: 3,
        fields.COUNT_OTHER_PLAYERS: 3
    }
]

example_prefers_table = {
    fields.PLAYER_DISTANCE: {
        fields.PLAYER_DISTANCE: 1,
        fields.SHOP_DISTANCE: 8,
        fields.PROMO_CODE: 2,
        fields.PORTAL_LEVEL: 4,
        fields.COUNT_OTHER_PLAYERS: 6
    },
    fields.SHOP_DISTANCE: {
        fields.PLAYER_DISTANCE: 1 / 8,
        fields.SHOP_DISTANCE: 1,
        fields.PROMO_CODE: 1 / 4,
        fields.PORTAL_LEVEL: 1 / 2,
        fields.COUNT_OTHER_PLAYERS: 1
    },
    fields.PROMO_CODE: {
        fields.PLAYER_DISTANCE: 1 / 2,
        fields.SHOP_DISTANCE: 4,
        fields.PROMO_CODE: 1,
        fields.PORTAL_LEVEL: 2,
        fields.COUNT_OTHER_PLAYERS: 3
    },
    fields.PORTAL_LEVEL: {
        fields.PLAYER_DISTANCE: 1 / 4,
        fields.SHOP_DISTANCE: 2,
        fields.PROMO_CODE: 1 / 2,
        fields.PORTAL_LEVEL: 1,
        fields.COUNT_OTHER_PLAYERS: 1
    },
    fields.COUNT_OTHER_PLAYERS: {
        fields.PLAYER_DISTANCE: 1 / 6,
        fields.SHOP_DISTANCE: 1,
        fields.PROMO_CODE: 1 / 3,
        fields.PORTAL_LEVEL: 1,
        fields.COUNT_OTHER_PLAYERS: 1
    }
}