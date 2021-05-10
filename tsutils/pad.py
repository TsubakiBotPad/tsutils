import pytz

# TZ used for PAD NA
# NA_TZ_OBJ = pytz.timezone('America/Los_Angeles')
NA_TZ_OBJ = pytz.timezone('US/Pacific')

# TZ used for PAD JP
JP_TZ_OBJ = pytz.timezone('Asia/Tokyo')

# This was overwritten by voltron. PDX opted to copy it +10,000 ids away
CROWS_1 = {x: x + 10000 for x in range(2601, 2635 + 1)}
# This isn't overwritten but PDX adjusted anyway
CROWS_2 = {x: x + 10000 for x in range(3460, 3481 + 1)}

PDX_JP_ADJUSTMENTS = {}
PDX_JP_ADJUSTMENTS.update(CROWS_1)
PDX_JP_ADJUSTMENTS.update(CROWS_2)


def get_pdx_id(m):
    pdx_id = m.monster_no_na
    if int(m.monster_id) == m.monster_no_jp:
        pdx_id = PDX_JP_ADJUSTMENTS.get(pdx_id, pdx_id)
    return pdx_id


def get_pdx_id_dadguide(m):
    pdx_id = m.monster_no_na
    if int(m.monster_id) == m.monster_no_jp:
        pdx_id = PDX_JP_ADJUSTMENTS.get(pdx_id, pdx_id)
    return pdx_id
